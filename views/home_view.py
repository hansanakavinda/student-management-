"""Home view for Student Management System"""
import customtkinter as ctk


class HomeView:
    """Home dashboard view"""
    
    @staticmethod
    def create(parent, username: str, db):
        """Create and return the home view"""
        welcome_frame = ctk.CTkFrame(parent)
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            welcome_frame,
            text="Student Management System",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(40, 20))
        
        subtitle = ctk.CTkLabel(
            welcome_frame,
            text=f"Welcome back, {username}!",
            font=ctk.CTkFont(size=18)
        )
        subtitle.pack(pady=10)
        
        # Get student count
        students = db.get_all_students()
        
        info_text = ctk.CTkLabel(
            welcome_frame,
            text=f"\n\nTotal Students: {len(students)}\n\n"
                 "Use the sidebar to:\n"
                 "• Add new students\n"
                 "• View student profiles\n"
                 "• Add exam results\n"
                 "• View exam results",
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        info_text.pack(pady=20)
        
        return welcome_frame
