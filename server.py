from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Event, Booking
import jwt
import os
from datetime import datetime, timedelta, timezone
import ssl
from functools import wraps

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# JWT token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            is_admin=data.get('is_admin', False)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201
    
    except Exception as e:
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}'}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events"""
    try:
        events = Event.query.all()
        return jsonify([event.to_dict() for event in events]), 200
    except Exception as e:
        return jsonify({'message': f'Failed to fetch events: {str(e)}'}), 500

@app.route('/api/events', methods=['POST'])
@token_required
def create_event(current_user):
    """Create a new event (admin only)"""
    try:
        if not current_user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        
        data = request.get_json()
        
        if not data or not all(k in data for k in ['name', 'venue', 'event_date', 'total_tickets', 'price_per_ticket']):
            return jsonify({'message': 'Missing required fields'}), 400
        
        event = Event(
            name=data['name'],
            description=data.get('description', ''),
            venue=data['venue'],
            event_date=datetime.fromisoformat(data['event_date']),
            total_tickets=data['total_tickets'],
            available_tickets=data['total_tickets'],
            price_per_ticket=data['price_per_ticket'],
            created_by=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({'message': 'Event created successfully', 'event': event.to_dict()}), 201
    
    except Exception as e:
        return jsonify({'message': f'Failed to create event: {str(e)}'}), 500

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get specific event"""
    try:
        event = Event.query.get_or_404(event_id)
        return jsonify(event.to_dict()), 200
    except Exception as e:
        return jsonify({'message': f'Failed to fetch event: {str(e)}'}), 500

@app.route('/api/bookings', methods=['POST'])
@token_required
def create_booking(current_user):
    """Create a new booking"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['event_id', 'quantity']):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Convert quantity to integer and validate
        try:
            quantity = int(data['quantity'])
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid quantity format'}), 400
        
        if quantity <= 0:
            return jsonify({'message': 'Invalid quantity - must be greater than 0'}), 400
        
        event = Event.query.get(data['event_id'])
        if not event:
            return jsonify({'message': 'Event not found'}), 404
        
        if quantity > event.available_tickets:
            return jsonify({'message': f'Not enough tickets available. Available: {event.available_tickets}, Requested: {quantity}'}), 400
        
        total_amount = quantity * event.price_per_ticket
        
        booking = Booking(
            user_id=current_user.id,
            event_id=data['event_id'],
            quantity=quantity,
            total_amount=total_amount,
            status='confirmed'
        )
        
        db.session.add(booking)
        
        # Update event availability
        event.update_availability()
        
        db.session.commit()
        
        return jsonify({'message': 'Booking created successfully', 'booking': booking.to_dict()}), 201
    
    except Exception as e:
        return jsonify({'message': f'Failed to create booking: {str(e)}'}), 500

@app.route('/api/bookings', methods=['GET'])
@token_required
def get_user_bookings(current_user):
    """Get user's bookings"""
    try:
        bookings = Booking.query.filter_by(user_id=current_user.id).all()
        return jsonify([booking.to_dict() for booking in bookings]), 200
    except Exception as e:
        return jsonify({'message': f'Failed to fetch bookings: {str(e)}'}), 500

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
@token_required
def cancel_booking(current_user, booking_id):
    """Cancel a booking"""
    try:
        booking = Booking.query.get_or_404(booking_id)
        
        if booking.user_id != current_user.id:
            return jsonify({'message': 'Access denied'}), 403
        
        if booking.status == 'cancelled':
            return jsonify({'message': 'Booking already cancelled'}), 400
        
        booking.status = 'cancelled'
        
        # Update event availability
        booking.event.update_availability()
        
        db.session.commit()
        
        return jsonify({'message': 'Booking cancelled successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to cancel booking: {str(e)}'}), 500

@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    """Get system statistics (admin only)"""
    try:
        if not current_user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        
        total_users = User.query.count()
        total_events = Event.query.count()
        total_bookings = Booking.query.filter_by(status='confirmed').count()
        total_revenue = db.session.query(db.func.sum(Booking.total_amount)).filter(
            Booking.status == 'confirmed'
        ).scalar() or 0
        
        return jsonify({
            'total_users': total_users,
            'total_events': total_events,
            'total_bookings': total_bookings,
            'total_revenue': total_revenue
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to fetch stats: {str(e)}'}), 500

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Create admin user
        admin = User(username='admin', email='admin@tickets.com', is_admin=True)
        admin.set_password('admin123')
        
        # Check if admin already exists
        if not User.query.filter_by(username='admin').first():
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: username=admin, password=admin123")
        
        # Create sample events
        if Event.query.count() == 0:
            sample_events = [
                Event(
                    name='Concert Night',
                    description='Amazing live music performance',
                    venue='Grand Theater',
                    event_date=datetime.now() + timedelta(days=30),
                    total_tickets=100,
                    available_tickets=100,
                    price_per_ticket=50.0,
                    created_by=admin.id
                ),
                Event(
                    name='Tech Conference 2024',
                    description='Latest technology trends and innovations',
                    venue='Convention Center',
                    event_date=datetime.now() + timedelta(days=45),
                    total_tickets=200,
                    available_tickets=200,
                    price_per_ticket=75.0,
                    created_by=admin.id
                ),
                Event(
                    name='Sports Championship',
                    description='Championship finals',
                    venue='Stadium Arena',
                    event_date=datetime.now() + timedelta(days=60),
                    total_tickets=500,
                    available_tickets=500,
                    price_per_ticket=30.0,
                    created_by=admin.id
                )
            ]
            
            for event in sample_events:
                db.session.add(event)
            
            db.session.commit()
            print("Sample events created")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--init-db':
        init_db()
        print("Database initialized successfully!")
    else:
        # Initialize database
        init_db()
        
        # SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain('cert.pem', 'key.pem')
        
        print("Starting Ticket Reservation Server...")
        print("Server will be available at: https://localhost:8443")
        print("For LAN access, use: https://<server-ip>:8443")
        
        app.run(host='0.0.0.0', port=8443, ssl_context=ssl_context, debug=True)
