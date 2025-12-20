"""
Refactored Main Menu - Modular version using separate view modules
All views are now separated into individual files in the views/ directory
"""

import customtkinter as ctk
from database import Database
from views import (
    HomeView,
    AddStudentView,
    StudentProfilesView,
    AddExamResultsView,
    ViewExamResultsView,
    AddCertificateView
)


class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, username, on_logout):
        super().__init__(parent)
        self.username = username
        self.on_logout = on_logout
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Database instance
        self.db = Database()
        
        # Create sidebar
        self._create_sidebar()
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Show home by default
        self.show_content("Home")
    
    def _create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)
        
        # Logo/Title
        ctk.CTkLabel(
            self.sidebar,
            text="Student",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, pady=(10, 5), padx=20)
        
        ctk.CTkLabel(
            self.sidebar,
            text="Management",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, pady=(60, 10), padx=20)
        
        # Menu buttons
        menu_buttons = [
            ("🏠 Home", "Home", 1),
            ("➕ Add Student", "Add Student", 2),
            ("👥 Student Profiles", "Student Profiles", 3),
            ("📝 Add Exam Results", "Add Exam Results", 4),
            ("📊 View Exam Results", "View Exam Results", 5),
            ("🎓 Add Certificates", "Add Certificates", 6),
        ]
        
        for text, section, row in menu_buttons:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                font=ctk.CTkFont(size=14),
                height=40,
                corner_radius=8,
                command=lambda s=section: self.show_content(s)
            ).grid(row=row, column=0, pady=10, padx=20, sticky="ew")
        
        # User info
        user_frame = ctk.CTkFrame(self.sidebar)
        user_frame.grid(row=8, column=0, pady=20, padx=20, sticky="ew")
        
        ctk.CTkLabel(
            user_frame,
            text=f"👋 {self.username}",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, pady=10, padx=15)
        
        # Logout button
        ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            font=ctk.CTkFont(size=14),
            height=40,
            corner_radius=8,
            fg_color="transparent",
            border_width=2,
            command=self.on_logout
        ).grid(row=9, column=0, pady=(0, 20), padx=20, sticky="ew")
    
    def show_content(self, section):
        """Update main content area based on selected section"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if section == "Home":
            HomeView.create(self.content_frame, self.username, self.db)
        elif section == "Add Student":
            AddStudentView(self.content_frame, self.db)
        elif section == "Student Profiles":
            StudentProfilesView(self.content_frame, self.db)
        elif section == "Add Exam Results":
            AddExamResultsView(self.content_frame, self.db)
        elif section == "View Exam Results":
            ViewExamResultsView(self.content_frame, self.db)
        elif section == "Add Certificates":
            AddCertificateView(self.content_frame, self.db)
