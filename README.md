# Ticket Reservation System

A secure client-server application for ticket reservation with SSL encryption and database storage.

## Features

- **Secure Communication**: SSL/TLS encrypted client-server communication
- **Database Storage**: SQLite database for persistent data storage
- **User Authentication**: Secure login and registration system
- **Ticket Management**: Create, view, book, and cancel tickets
- **Real-time Updates**: Live updates when tickets are booked/cancelled
- **Network Support**: Works over LAN with cable connection or individual mode

## Architecture

```
Client (GUI) <--SSL--> Server <--SQLite--> Database
```

## Components

- **Server**: Python Flask application with SSL support
- **Client**: Python Tkinter GUI application
- **Database**: SQLite with SQLAlchemy ORM
- **Security**: SSL certificates for encrypted communication

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Generate SSL certificates:
```bash
python generate_certificates.py
```

3. Initialize database:
```bash
python server.py --init-db
```

## Usage

### Server
```bash
python server.py
```

### Client
```bash
python client.py
```

## Network Configuration

- **LAN Mode**: Connect two devices with Ethernet cable
- **Individual Mode**: Run both client and server on same machine
- **Default Port**: 8443 (HTTPS)
- **Default Host**: 0.0.0.0 (accepts connections from any IP)

## Security Features

- SSL/TLS encryption for all communications
- Password hashing with bcrypt
- Session management with JWT tokens
- Input validation and sanitization
