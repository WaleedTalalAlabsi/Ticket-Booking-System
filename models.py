from flask_sqlalchemy import SQLAlchemy
from flask import request
from datetime import datetime, timezone
import bcrypt
import jwt
from functools import wraps

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    venue = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)
    price_per_ticket = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    bookings = db.relationship('Booking', backref='event', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'venue': self.venue,
            'event_date': self.event_date.isoformat(),
            'total_tickets': self.total_tickets,
            'available_tickets': self.available_tickets,
            'price_per_ticket': self.price_per_ticket,
            'created_at': self.created_at.isoformat(),
            'created_by': self.created_by
        }
    
    def update_availability(self):
        """Update available tickets count"""
        booked_tickets = db.session.query(db.func.sum(Booking.quantity)).filter(
            Booking.event_id == self.id,
            Booking.status == 'confirmed'
        ).scalar() or 0
        self.available_tickets = self.total_tickets - booked_tickets

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    booking_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'quantity': self.quantity,
            'total_amount': self.total_amount,
            'status': self.status,
            'booking_date': self.booking_date.isoformat(),
            'event': self.event.to_dict() if self.event else None,
            'user': self.user.to_dict() if self.user else None
        }

# JWT token decorator will be defined in server.py
