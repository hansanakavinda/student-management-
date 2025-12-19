import customtkinter as ctk
from database import Database

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.db = Database()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.container,
            text="Welcome Back",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=(40, 10), padx=40)
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.container,
            text="Sign in to your account",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Username entry
        self.username_entry = ctk.CTkEntry(
            self.container,
            placeholder_text="Username",
            width=300,
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.username_entry.grid(row=2, column=0, pady=10, padx=40)
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.container,
            placeholder_text="Password",
            show="•",
            width=300,
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.password_entry.grid(row=3, column=0, pady=10, padx=40)
        
        # Error label
        self.error_label = ctk.CTkLabel(
            self.container,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.error_label.grid(row=4, column=0, pady=5)
        
        # Login button
        self.login_button = ctk.CTkButton(
            self.container,
            text="Sign In",
            width=300,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            command=self.handle_login
        )
        self.login_button.grid(row=5, column=0, pady=(20, 10), padx=40)
        
        # Info label
        self.info_label = ctk.CTkLabel(
            self.container,
            text="Default credentials: admin / 1234",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.info_label.grid(row=6, column=0, pady=(20, 40))
        
        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda e: self.handle_login())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Clear previous error
        self.error_label.configure(text="")
        
        # Validate inputs
        if not username or not password:
            self.error_label.configure(text="Please enter both username and password")
            return
        
        # Authenticate
        if self.db.authenticate_user(username, password):
            self.on_login_success(username)
        else:
            self.error_label.configure(text="Invalid username or password")
            self.password_entry.delete(0, 'end')
