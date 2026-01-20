"""Student detail view - shows complete information about a student"""
import customtkinter as ctk
from PIL import Image
import os


class StudentDetailView(ctk.CTkFrame):
    """View displaying complete student information"""
    
    def __init__(self, parent, student, db, on_back, on_edit_notes, on_view_results, on_view_certificates):
        super().__init__(parent)
        self.student = student
        self.db = db
        self.on_back = on_back
        self.on_edit_notes = on_edit_notes
        self.on_view_results = on_view_results
        self.on_view_certificates = on_view_certificates
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_content()
    
    def _create_content(self):
        """Create view content"""
        # Content - scrollable frame
        content = ctk.CTkScrollableFrame(self)
        content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content.grid_columnconfigure(0, weight=1)
        
        # Back button at the top
        ctk.CTkButton(
            content,
            text="← Back to Student Profiles",
            width=200,
            font=ctk.CTkFont(size=14),
            command=self.on_back
        ).pack(anchor="w", pady=(0, 20))
        
        # Create centered container within the scrollable content
        centered_container = ctk.CTkFrame(content, fg_color="transparent")
        centered_container.pack(expand=True, pady=20)
        
        # Title
        ctk.CTkLabel(
            centered_container,
            text="Student Profile",
            font=ctk.CTkFont(size=22, weight="bold"),
            width=400
        ).pack(pady=(10, 20))
        
        # Display image if available
        if self.student[8] and os.path.exists(self.student[8]):
            try:
                img = Image.open(self.student[8])
                img.thumbnail((150, 150))
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
                img_label = ctk.CTkLabel(centered_container, image=photo, text="")
                img_label.image = photo
                img_label.pack(pady=10)
            except:
                pass
        
        # Display fields
        fields = [
            ("Student ID:", self.student[0]),
            ("Name:", self.student[1]),
            ("Date of Birth:", self.student[2]),
            ("Grade Registered:", self.student[10] if len(self.student) > 10 else "N/A"),
            ("Gender:", self.student[3]),
            ("Address:", self.student[4]),
            ("Guardian Name:", self.student[5]),
            ("Guardian NIC:", self.student[6]),
            ("Guardian Contact:", self.student[7]),
            ("Registration Date:", self.student[9] if len(self.student) > 9 else "N/A"),
            ("Registered:", self.student[11] if len(self.student) > 11 else "N/A")
        ]
        
        for label, value in fields:
            frame = ctk.CTkFrame(centered_container, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                frame,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            ).pack(side="left", padx=10)
            
            ctk.CTkLabel(
                frame,
                text=str(value),
                font=ctk.CTkFont(size=14),
                anchor="w"
            ).pack(side="left", padx=10)
        
        # Notes section
        self._create_notes_section(centered_container)
        
        # Action buttons
        self._create_button_frame(centered_container)
    
    def _create_notes_section(self, content):
        """Create notes display section"""
        notes = self.db.get_student_notes(self.student[0])
        
        notes_frame = ctk.CTkFrame(content, fg_color="transparent")
        notes_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            notes_frame,
            text="Additional Notes:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.notes_display = ctk.CTkTextbox(
            notes_frame,
            height=80,
            font=ctk.CTkFont(size=12),
            wrap="word",
            state="disabled"
        )
        self.notes_display.pack(fill="x", padx=10, pady=5)
        
        if notes:
            self.notes_display.configure(state="normal")
            self.notes_display.insert("1.0", notes)
            self.notes_display.configure(state="disabled")
    
    def refresh_notes(self):
        """Refresh the notes display"""
        notes = self.db.get_student_notes(self.student[0])
        
        # Clear existing notes
        self.notes_display.configure(state="normal")
        self.notes_display.delete("1.0", "end")
        
        # Insert updated notes
        if notes:
            self.notes_display.insert("1.0", notes)
        
        self.notes_display.configure(state="disabled")
    
    def _create_button_frame(self, content):
        """Create action buttons"""
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # Edit Notes button
        ctk.CTkButton(
            button_frame,
            text="Edit Notes",
            font=ctk.CTkFont(size=14),
            width=140,
            height=40,
            fg_color="#2b7a0b",
            hover_color="#3a9b1a",
            command=lambda: self.on_edit_notes(self.student, self)
        ).pack(side="left", padx=10)
        
        # View Results button
        ctk.CTkButton(
            button_frame,
            text="View Exam Results",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180,
            height=40,
            command=lambda: self.on_view_results(self.student)
        ).pack(side="left", padx=10)
        
        # View Certificates button
        ctk.CTkButton(
            button_frame,
            text="View Certificates",
            font=ctk.CTkFont(size=14),
            width=160,
            height=40,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            command=lambda: self.on_view_certificates(self.student)
        ).pack(side="left", padx=10)
