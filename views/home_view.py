import customtkinter as ctk
from PIL import Image
import os


class HomeView:
    """Home dashboard view"""
    
    @staticmethod
    def create(parent, username: str, db):
        """Create and return the home view"""
        # Main container frame
        main_container = ctk.CTkFrame(parent, fg_color="#FFFBB8")
        main_container.pack(fill="both", expand=True)
        
        # Configure grid for centering
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=0)
        main_container.grid_rowconfigure(2, weight=0)
        main_container.grid_rowconfigure(3, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Top section: School name
        top_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="s", pady=(20, 10))
        
        school_name = ctk.CTkLabel(
            top_frame,
            text="Siri Seelananda Daham Pasala",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#000000"
        )
        school_name.pack()
        
        # Center section: Logo
        center_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        center_frame.grid(row=1, column=0)
        
        # Load and display logo
        try:
            if os.path.exists("logo.png"):
                img = Image.open("logo.png")
                # Resize logo to reasonable size for center display
                logo_size = (300, 300)
                img.thumbnail(logo_size, Image.Resampling.LANCZOS)
                
                photo = ctk.CTkImage(light_image=img, dark_image=img, 
                                    size=(img.width, img.height))
                logo_label = ctk.CTkLabel(center_frame, image=photo, text="")
                logo_label.pack(pady=20)
            else:
                # Fallback if logo not found
                logo_label = ctk.CTkLabel(
                    center_frame,
                    text="🏫",
                    font=ctk.CTkFont(size=120)
                )
                logo_label.pack(pady=20)
        except Exception as e:
            logo_label = ctk.CTkLabel(
                center_frame,
                text="🏫",
                font=ctk.CTkFont(size=120)
            )
            logo_label.pack(pady=20)
        
        # Bottom section: Student count
        bottom_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        bottom_frame.grid(row=2, column=0, sticky="n", pady=(10, 20))
        
        # Get student count
        students = db.get_all_students()
        
        student_count_label = ctk.CTkLabel(
            bottom_frame,
            text=f"Total Students: {len(students)}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#000000"
        )
        student_count_label.pack()
        
        # Empty row for bottom spacing
        spacer = ctk.CTkFrame(main_container, fg_color="transparent", height=1)
        spacer.grid(row=3, column=0, sticky="n")
        
        return main_container
