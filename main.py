import customtkinter as ctk
from database import Database
from login_page import LoginPage
from main_menu import MainMenu

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Student Management System")
        self.geometry("1000x600")
        
        # Center window on screen
        self.center_window()
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize database
        db = Database()
        db.initialize_database()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Show login page
        self.current_user = None
        # Change to show_login() to start with login page
        self.show_login()
        # self.show_main_menu() 
        
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = 1000
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def show_login(self):
        """Display login page"""
        # Clear current content
        for widget in self.winfo_children():
            widget.destroy()
            
        # Create login page
        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.grid(row=0, column=0, sticky="nsew")
        
    def show_main_menu(self):
        """Display main menu"""
        # Clear current content
        for widget in self.winfo_children():
            widget.destroy()
            
        # Create main menu
        self.main_menu = MainMenu(self, self.current_user, self.on_logout)
        self.main_menu.grid(row=0, column=0, sticky="nsew")
        
    def on_login_success(self, username):
        """Handle successful login"""
        self.current_user = username
        self.show_main_menu()
        
    def on_logout(self):
        """Handle logout"""
        self.current_user = None
        self.show_login()

if __name__ == "__main__":
    app = App()
    app.mainloop()
