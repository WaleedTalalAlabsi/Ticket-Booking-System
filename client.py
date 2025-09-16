import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import threading
from datetime import datetime
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TicketReservationClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticket Reservation System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # API configuration
        self.base_url = "https://localhost:8443/api"
        self.session = requests.Session()
        self.session.verify = False  # For self-signed certificates
        self.token = None
        self.current_user = None
        
        # Create GUI
        self.create_widgets()
        self.show_login_frame()
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Login frame
        self.login_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        
        # Login form
        login_title = tk.Label(self.login_frame, text="Ticket Reservation System", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        login_title.pack(pady=20)
        
        # Username
        tk.Label(self.login_frame, text="Username:", font=('Arial', 12), bg='#f0f0f0').pack()
        self.username_entry = tk.Entry(self.login_frame, font=('Arial', 12), width=30)
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(self.login_frame, text="Password:", font=('Arial', 12), bg='#f0f0f0').pack()
        self.password_entry = tk.Entry(self.login_frame, font=('Arial', 12), width=30, show='*')
        self.password_entry.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.login_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Login", command=self.login, 
                 font=('Arial', 12), bg='#3498db', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="Register", command=self.show_register, 
                 font=('Arial', 12), bg='#95a5a6', fg='white', width=10).pack(side='left', padx=5)
        
        # Main application frame
        self.app_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        
        # Header
        header_frame = tk.Frame(self.app_frame, bg='#34495e', height=60)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        self.welcome_label = tk.Label(header_frame, text="", font=('Arial', 14, 'bold'), 
                                     bg='#34495e', fg='white')
        self.welcome_label.pack(side='left', padx=20, pady=15)
        
        tk.Button(header_frame, text="Logout", command=self.logout, 
                 font=('Arial', 10), bg='#e74c3c', fg='white').pack(side='right', padx=20, pady=15)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.app_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Events tab
        self.events_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.events_frame, text="Events")
        
        # Events list
        events_title = tk.Label(self.events_frame, text="Available Events", 
                               font=('Arial', 16, 'bold'), bg='#f0f0f0')
        events_title.pack(pady=10)
        
        # Events treeview
        columns = ('Name', 'Venue', 'Date', 'Available', 'Price')
        self.events_tree = ttk.Treeview(self.events_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.events_tree.heading(col, text=col)
            self.events_tree.column(col, width=150)
        
        self.events_tree.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbar for events
        events_scrollbar = ttk.Scrollbar(self.events_frame, orient='vertical', command=self.events_tree.yview)
        self.events_tree.configure(yscrollcommand=events_scrollbar.set)
        
        # Booking frame
        booking_frame = tk.Frame(self.events_frame, bg='#f0f0f0')
        booking_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(booking_frame, text="Quantity:", font=('Arial', 12), bg='#f0f0f0').pack(side='left')
        self.quantity_var = tk.StringVar(value="1")
        quantity_spinbox = tk.Spinbox(booking_frame, from_=1, to=10, textvariable=self.quantity_var, 
                                     font=('Arial', 12), width=5)
        quantity_spinbox.pack(side='left', padx=5)
        
        tk.Button(booking_frame, text="Book Tickets", command=self.book_tickets, 
                 font=('Arial', 12), bg='#27ae60', fg='white').pack(side='left', padx=10)
        
        tk.Button(booking_frame, text="Refresh Events", command=self.load_events, 
                 font=('Arial', 12), bg='#3498db', fg='white').pack(side='right')
        
        # My Bookings tab
        self.bookings_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.bookings_frame, text="My Bookings")
        
        bookings_title = tk.Label(self.bookings_frame, text="My Bookings", 
                                 font=('Arial', 16, 'bold'), bg='#f0f0f0')
        bookings_title.pack(pady=10)
        
        # Bookings treeview
        booking_columns = ('Event', 'Venue', 'Date', 'Quantity', 'Amount', 'Status', 'Booking Date')
        self.bookings_tree = ttk.Treeview(self.bookings_frame, columns=booking_columns, show='headings', height=10)
        
        for col in booking_columns:
            self.bookings_tree.heading(col, text=col)
            self.bookings_tree.column(col, width=120)
        
        self.bookings_tree.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Booking actions
        booking_actions = tk.Frame(self.bookings_frame, bg='#f0f0f0')
        booking_actions.pack(fill='x', padx=10, pady=10)
        
        tk.Button(booking_actions, text="Cancel Booking", command=self.cancel_booking, 
                 font=('Arial', 12), bg='#e74c3c', fg='white').pack(side='left')
        
        tk.Button(booking_actions, text="Refresh Bookings", command=self.load_bookings, 
                 font=('Arial', 12), bg='#3498db', fg='white').pack(side='right')
        
        # Admin tab (only for admin users)
        self.admin_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.admin_frame, text="Admin")
        
        admin_title = tk.Label(self.admin_frame, text="Administration Panel", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        admin_title.pack(pady=10)
        
        # Create event form
        create_event_frame = tk.LabelFrame(self.admin_frame, text="Create New Event", 
                                          font=('Arial', 12, 'bold'), bg='#f0f0f0')
        create_event_frame.pack(fill='x', padx=10, pady=10)
        
        # Event form fields
        fields = ['Name', 'Description', 'Venue', 'Event Date (YYYY-MM-DD HH:MM)', 'Total Tickets', 'Price per Ticket']
        self.event_entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(create_event_frame, text=f"{field}:", font=('Arial', 10), bg='#f0f0f0').grid(row=i, column=0, sticky='w', padx=5, pady=2)
            entry = tk.Entry(create_event_frame, font=('Arial', 10), width=40)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.event_entries[field.lower().replace(' ', '_')] = entry
        
        tk.Button(create_event_frame, text="Create Event", command=self.create_event, 
                 font=('Arial', 12), bg='#27ae60', fg='white').grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        # Statistics
        stats_frame = tk.LabelFrame(self.admin_frame, text="System Statistics", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        stats_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=10, font=('Arial', 10))
        self.stats_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Button(stats_frame, text="Refresh Statistics", command=self.load_stats, 
                 font=('Arial', 12), bg='#3498db', fg='white').pack(pady=5)
    
    def show_login_frame(self):
        """Show login frame and hide app frame"""
        self.login_frame.pack(fill='both', expand=True)
        self.app_frame.pack_forget()
    
    def show_register(self):
        """Show registration dialog"""
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        register_window.geometry("400x300")
        register_window.configure(bg='#f0f0f0')
        register_window.grab_set()
        
        # Center the window
        register_window.transient(self.root)
        register_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        tk.Label(register_window, text="Register New User", font=('Arial', 16, 'bold'), 
                bg='#f0f0f0').pack(pady=20)
        
        # Registration form
        fields = ['Username', 'Email', 'Password']
        entries = {}
        
        for field in fields:
            tk.Label(register_window, text=f"{field}:", font=('Arial', 12), bg='#f0f0f0').pack()
            entry = tk.Entry(register_window, font=('Arial', 12), width=30)
            if field == 'Password':
                entry.config(show='*')
            entry.pack(pady=5)
            entries[field.lower()] = entry
        
        def register_user():
            username = entries['username'].get()
            email = entries['email'].get()
            password = entries['password'].get()
            
            if not all([username, email, password]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                response = self.session.post(f"{self.base_url}/register", 
                                           json={'username': username, 'email': email, 'password': password})
                
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Registration successful! Please login.")
                    register_window.destroy()
                else:
                    error_msg = response.json().get('message', 'Registration failed')
                    messagebox.showerror("Error", error_msg)
            except Exception as e:
                messagebox.showerror("Error", f"Connection failed: {str(e)}")
        
        tk.Button(register_window, text="Register", command=register_user, 
                 font=('Arial', 12), bg='#27ae60', fg='white').pack(pady=20)
    
    def login(self):
        """Handle user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        try:
            response = self.session.post(f"{self.base_url}/login", 
                                       json={'username': username, 'password': password})
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['token']
                self.current_user = data['user']
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
                
                self.welcome_label.config(text=f"Welcome, {self.current_user['username']}!")
                
                # Show app frame and hide login frame
                self.login_frame.pack_forget()
                self.app_frame.pack(fill='both', expand=True)
                
                # Load data
                self.load_events()
                self.load_bookings()
                
                # Show admin tab only for admin users
                if self.current_user['is_admin']:
                    self.notebook.add(self.admin_frame, text="Admin")
                    self.load_stats()
                else:
                    # Hide admin tab if not admin
                    for tab_id in self.notebook.tabs():
                        if self.notebook.tab(tab_id, "text") == "Admin":
                            self.notebook.forget(tab_id)
                            break
                
                messagebox.showinfo("Success", "Login successful!")
            else:
                error_msg = response.json().get('message', 'Login failed')
                messagebox.showerror("Error", error_msg)
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
    
    def logout(self):
        """Handle user logout"""
        self.token = None
        self.current_user = None
        self.session.headers.pop('Authorization', None)
        self.show_login_frame()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def load_events(self):
        """Load events from server"""
        try:
            response = self.session.get(f"{self.base_url}/events")
            
            if response.status_code == 200:
                events = response.json()
                
                # Clear existing items
                for item in self.events_tree.get_children():
                    self.events_tree.delete(item)
                
                # Add events to tree
                for event in events:
                    event_date = datetime.fromisoformat(event['event_date']).strftime('%Y-%m-%d %H:%M')
                    self.events_tree.insert('', 'end', values=(
                        event['name'],
                        event['venue'],
                        event_date,
                        event['available_tickets'],
                        f"${event['price_per_ticket']:.2f}"
                    ), tags=(event['id'],))
            else:
                messagebox.showerror("Error", "Failed to load events")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
    
    def book_tickets(self):
        """Book selected tickets"""
        selection = self.events_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select an event")
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Invalid quantity - must be greater than 0")
                return
            
            # Get event ID from selection
            event_id = self.events_tree.item(selection[0])['tags'][0]
            
            print(f"Debug: Booking {quantity} tickets for event {event_id}")  # Debug info
            
            response = self.session.post(f"{self.base_url}/bookings", 
                                       json={'event_id': int(event_id), 'quantity': quantity})
            
            print(f"Debug: Server response status: {response.status_code}")  # Debug info
            print(f"Debug: Server response: {response.text}")  # Debug info
            
            if response.status_code == 201:
                messagebox.showinfo("Success", "Tickets booked successfully!")
                self.load_events()
                self.load_bookings()
            else:
                error_msg = response.json().get('message', 'Booking failed')
                messagebox.showerror("Error", error_msg)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity - please enter a number")
        except Exception as e:
            messagebox.showerror("Error", f"Booking failed: {str(e)}")
    
    def load_bookings(self):
        """Load user bookings"""
        try:
            response = self.session.get(f"{self.base_url}/bookings")
            
            if response.status_code == 200:
                bookings = response.json()
                
                # Clear existing items
                for item in self.bookings_tree.get_children():
                    self.bookings_tree.delete(item)
                
                # Add bookings to tree
                for booking in bookings:
                    event = booking['event']
                    event_date = datetime.fromisoformat(event['event_date']).strftime('%Y-%m-%d %H:%M')
                    booking_date = datetime.fromisoformat(booking['booking_date']).strftime('%Y-%m-%d %H:%M')
                    
                    self.bookings_tree.insert('', 'end', values=(
                        event['name'],
                        event['venue'],
                        event_date,
                        booking['quantity'],
                        f"${booking['total_amount']:.2f}",
                        booking['status'].title(),
                        booking_date
                    ), tags=(booking['id'],))
            else:
                messagebox.showerror("Error", "Failed to load bookings")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
    
    def cancel_booking(self):
        """Cancel selected booking"""
        selection = self.bookings_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a booking")
            return
        
        booking_id = self.bookings_tree.item(selection[0])['tags'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this booking?"):
            try:
                response = self.session.delete(f"{self.base_url}/bookings/{booking_id}")
                
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Booking cancelled successfully!")
                    self.load_bookings()
                    self.load_events()
                else:
                    error_msg = response.json().get('message', 'Cancellation failed')
                    messagebox.showerror("Error", error_msg)
            except Exception as e:
                messagebox.showerror("Error", f"Cancellation failed: {str(e)}")
    
    def create_event(self):
        """Create new event (admin only)"""
        try:
            # Get form data
            event_data = {}
            for field, entry in self.event_entries.items():
                value = entry.get().strip()
                if not value:
                    messagebox.showerror("Error", f"All fields are required")
                    return
                
                if field == 'total_tickets' or field == 'price_per_ticket':
                    try:
                        event_data[field] = float(value)
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid {field}")
                        return
                elif field == 'event_date':
                    try:
                        # Parse date string
                        event_data[field] = datetime.strptime(value, '%Y-%m-%d %H:%M').isoformat()
                    except ValueError:
                        messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD HH:MM")
                        return
                else:
                    event_data[field] = value
            
            response = self.session.post(f"{self.base_url}/events", json=event_data)
            
            if response.status_code == 201:
                messagebox.showinfo("Success", "Event created successfully!")
                # Clear form
                for entry in self.event_entries.values():
                    entry.delete(0, tk.END)
                self.load_events()
            else:
                error_msg = response.json().get('message', 'Event creation failed')
                messagebox.showerror("Error", error_msg)
        except Exception as e:
            messagebox.showerror("Error", f"Event creation failed: {str(e)}")
    
    def load_stats(self):
        """Load system statistics (admin only)"""
        try:
            response = self.session.get(f"{self.base_url}/stats")
            
            if response.status_code == 200:
                stats = response.json()
                
                stats_text = f"""
System Statistics
================

Total Users: {stats['total_users']}
Total Events: {stats['total_events']}
Total Bookings: {stats['total_bookings']}
Total Revenue: ${stats['total_revenue']:.2f}

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                
                self.stats_text.delete(1.0, tk.END)
                self.stats_text.insert(1.0, stats_text)
            else:
                messagebox.showerror("Error", "Failed to load statistics")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")

def main():
    root = tk.Tk()
    app = TicketReservationClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
