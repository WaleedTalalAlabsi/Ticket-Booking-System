# Network Setup Guide

This guide explains how to set up the Ticket Reservation System for both individual and LAN (two-device) operation.

## Individual Mode (Single Device)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Server**
   ```bash
   python run_server.py
   ```

3. **Start Client** (in another terminal)
   ```bash
   python run_client.py
   ```

## LAN Mode (Two Devices with Cable)

### Prerequisites
- Two computers with Ethernet ports
- Ethernet cable (crossover or straight-through)
- Python installed on both devices

### Setup Steps

#### On Server Device:

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Network**
   - Connect Ethernet cable to both devices
   - Set static IP address (e.g., 192.168.1.100)
   - Subnet mask: 255.255.255.0
   - Gateway: 192.168.1.1 (optional)

3. **Update Configuration**
   Edit `config.py`:
   ```python
   CLIENT_SERVER_URL = 'https://192.168.1.100:8443'  # Server's IP
   ```

4. **Start Server**
   ```bash
   python run_server.py
   ```

#### On Client Device:

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Network**
   - Set static IP address (e.g., 192.168.1.101)
   - Subnet mask: 255.255.255.0
   - Gateway: 192.168.1.1 (optional)

3. **Update Configuration**
   Edit `config.py`:
   ```python
   CLIENT_SERVER_URL = 'https://192.168.1.100:8443'  # Server's IP
   ```

4. **Start Client**
   ```bash
   python run_client.py
   ```

## Network Configuration Commands

### Windows (Command Prompt as Administrator)

```cmd
# Set static IP
netsh interface ip set address "Ethernet" static 192.168.1.100 255.255.255.0

# Check IP configuration
ipconfig

# Test connectivity
ping 192.168.1.101
```

### Linux/macOS

```bash
# Set static IP (Ubuntu/Debian)
sudo ip addr add 192.168.1.100/24 dev eth0
sudo ip link set eth0 up

# Check IP configuration
ip addr show

# Test connectivity
ping 192.168.1.101
```

## Troubleshooting

### Connection Issues

1. **Check IP Configuration**
   - Ensure both devices are on the same subnet
   - Verify IP addresses are correct

2. **Test Network Connectivity**
   ```bash
   ping <server-ip>
   ```

3. **Check Firewall Settings**
   - Allow port 8443 through firewall
   - Windows: Add inbound rule for port 8443
   - Linux: `sudo ufw allow 8443`

4. **Verify SSL Certificates**
   - Ensure `cert.pem` and `key.pem` exist
   - Regenerate if needed: `python generate_certificates.py`

### Common Issues

1. **"Connection Refused"**
   - Server not running
   - Wrong IP address
   - Firewall blocking connection

2. **"SSL Certificate Error"**
   - Self-signed certificate warning (normal for development)
   - Click "Advanced" and "Proceed" in browser
   - Or disable SSL verification in client code

3. **"Port Already in Use"**
   - Another process using port 8443
   - Change port in `config.py`
   - Kill process: `netstat -ano | findstr :8443`

## Security Notes

- This setup uses self-signed SSL certificates for development
- In production, use proper SSL certificates from a trusted CA
- Change the SECRET_KEY in production
- Enable SSL verification in production

## Testing the Setup

1. **Server Test**
   ```bash
   curl -k https://localhost:8443/api/events
   ```

2. **Client Test**
   - Open client application
   - Try to register a new user
   - Try to login and book tickets

## Default Credentials

- **Admin User**: username=admin, password=admin123
- **Regular User**: Register through the client application
