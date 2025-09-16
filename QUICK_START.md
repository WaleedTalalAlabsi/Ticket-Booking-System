# 🎫 Ticket Reservation System - Quick Start Guide

## ✅ Installation Complete!

Your Ticket Reservation System is now fully installed and ready to use.

## 🚀 How to Start

### Option 1: Using Python Scripts
```bash
# Terminal 1 - Start Server
python run_server.py

# Terminal 2 - Start Client  
python run_client.py
```

### Option 2: Using Batch Files (Windows)
```bash
# Double-click these files:
start_server.bat
start_client.bat
```

## 🔑 Login Credentials

### Admin Account (Pre-configured)
- **Username:** `admin`
- **Password:** `admin123`

### Regular Users
- Register through the client application

## 🌐 Network Modes

### Individual Mode (Default)
- Server runs on `localhost:8443`
- Client connects to `localhost:8443`
- Perfect for single-device development

### LAN Mode (Two Devices)
1. Connect devices with Ethernet cable
2. Set static IP addresses (e.g., 192.168.1.100, 192.168.1.101)
3. Update `config.py`:
   ```python
   CLIENT_SERVER_URL = 'https://192.168.1.100:8443'  # Server's IP
   ```

## 🎯 Features Available

### For All Users:
- ✅ View available events
- ✅ Book tickets
- ✅ View booking history
- ✅ Cancel bookings
- ✅ User registration/login

### For Admin Users:
- ✅ Create new events
- ✅ View system statistics
- ✅ Monitor all bookings
- ✅ Manage users

## 🔧 Troubleshooting

### If Server Won't Start:
```bash
# Check if port 8443 is free
netstat -ano | findstr :8443

# Regenerate SSL certificates
python generate_certificates.py

# Reinitialize database
python server.py --init-db
```

### If Client Can't Connect:
1. Make sure server is running
2. Check firewall settings (allow port 8443)
3. For LAN mode, verify IP addresses

### Test System:
```bash
python test_system.py
```

## 📁 Project Files

- `server.py` - Flask server with SSL
- `client.py` - Tkinter GUI client
- `models.py` - Database models
- `config.py` - Configuration settings
- `cert.pem` / `key.pem` - SSL certificates
- `instance/ticket_system.db` - SQLite database

## 🛡️ Security Features

- ✅ SSL/TLS encryption
- ✅ Password hashing (bcrypt)
- ✅ JWT token authentication
- ✅ Input validation
- ✅ Session management

## 📞 Support

If you encounter any issues:
1. Run `python verify_installation.py` to check system status
2. Check `NETWORK_SETUP.md` for detailed network configuration
3. Review error messages in the terminal

---

**🎉 Enjoy your Ticket Reservation System!**
