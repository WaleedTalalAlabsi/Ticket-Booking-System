# Configuration file for Ticket Reservation System

# Server Configuration
SERVER_HOST = '0.0.0.0'  # Accept connections from any IP
SERVER_PORT = 8443
SERVER_DEBUG = True

# Database Configuration
DATABASE_URI = 'sqlite:///ticket_system.db'

# Security Configuration
SECRET_KEY = 'your-secret-key-change-in-production'  # Change this in production!
JWT_EXPIRATION_HOURS = 24

# SSL Configuration
SSL_CERT_FILE = 'cert.pem'
SSL_KEY_FILE = 'key.pem'

# Client Configuration
CLIENT_SERVER_URL = 'https://localhost:8443'  # Change to server IP for LAN access
CLIENT_VERIFY_SSL = False  # Set to True for production with valid certificates

# Network Configuration
# For LAN connection, update CLIENT_SERVER_URL to use the server's IP address
# Example: CLIENT_SERVER_URL = 'https://192.168.1.100:8443'
