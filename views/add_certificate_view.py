"""Add Certificate view for Student Management System"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import shutil
import os


class AddCertificateView:
    """Certificate addition form view"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.certificate_path = None
        
        # Create the main frame
        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI"""
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Title
        ctk.CTkLabel(
            self.main_frame,
            text="Add Student Certificate",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20, 10))
        
        # Filter section
        filter_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            filter_frame,
            text="Filter Students:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=5)
        
        self.student_filter = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Search by student name...",
            width=300,
            font=ctk.CTkFont(size=13)
        )
        self.student_filter.pack(side="left", padx=10)
        
        ctk.CTkButton(
            filter_frame,
            text="🔍 Filter",
            width=100,
            command=self._load_students
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Clear",
            width=80,
            fg_color="#666666",
            hover_color="#888888",
            command=self._clear_filter
        ).pack(side="left", padx=5)
        
        # Form section (scrollable)
        form_frame = ctk.CTkScrollableFrame(self.main_frame)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Student selection
        student_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        student_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            student_frame,
            text="Select Student:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        ).pack(side="left", padx=10)
        
        self.student_combo = ctk.CTkComboBox(
            student_frame,
            values=["No students available"],
            width=350,
            font=ctk.CTkFont(size=13),
            state="readonly"
        )
        self.student_combo.pack(side="left", padx=10)
        
        # Certificate image section
        ctk.CTkLabel(
            form_frame,
            text="Certificate Image",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 10))
        
        # Image preview
        self.preview_label = ctk.CTkLabel(
            form_frame,
            text="No certificate selected",
            font=ctk.CTkFont(size=12),
            width=400,
            height=300,
            fg_color="#2b2b2b",
            corner_radius=10
        )
        self.preview_label.pack(pady=10)
        
        # Image buttons
        image_btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        image_btn_frame.pack(pady=10)
        
        ctk.CTkButton(
            image_btn_frame,
            text="📁 Choose Certificate Image",
            font=ctk.CTkFont(size=14),
            width=200,
            height=40,
            command=self._choose_certificate
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            image_btn_frame,
            text="❌ Clear",
            font=ctk.CTkFont(size=14),
            width=100,
            height=40,
            fg_color="#666666",
            hover_color="#888888",
            command=self._clear_certificate
        ).pack(side="left", padx=10)
        
        # Note section
        note_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        note_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            note_frame,
            text="Note (Optional):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=5)
        
        self.note_entry = ctk.CTkTextbox(
            note_frame,
            height=80,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.note_entry.pack(fill="x", pady=5)
        
        # Status message
        self.message_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=13)
        )
        self.message_label.pack(pady=10)
        
        # Submit button
        ctk.CTkButton(
            form_frame,
            text="💾 Save Certificate",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=45,
            fg_color="#2b7a0b",
            hover_color="#3a9b1a",
            command=self._save_certificate
        ).pack(pady=20)
        
        # Load students
        self._load_students()
    
    def _load_students(self):
        """Load students from database with optional filter"""
        filter_text = self.student_filter.get().strip()
        students = self.db.search_students(filter_text) if filter_text else self.db.get_all_students()
        
        if students:
            self.students_dict = {f"{s[1]} (ID: {s[0]})": s[0] for s in students}
            self.student_combo.configure(values=list(self.students_dict.keys()))
            self.student_combo.set(list(self.students_dict.keys())[0])
        else:
            self.students_dict = {}
            self.student_combo.configure(values=["No students found"])
            self.student_combo.set("No students found")
    
    def _clear_filter(self):
        """Clear the student filter"""
        self.student_filter.delete(0, "end")
        self._load_students()
    
    def _choose_certificate(self):
        """Open file dialog to choose certificate image"""
        file_path = filedialog.askopenfilename(
            title="Select Certificate Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.pdf")]
        )
        
        if file_path:
            self.certificate_path = file_path
            
            # Show preview if it's an image
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                try:
                    img = Image.open(file_path)
                    img.thumbnail((400, 300))
                    photo = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 300))
                    self.preview_label.configure(image=photo, text="")
                    self.preview_label.image = photo
                except Exception as e:
                    self.preview_label.configure(text=f"Preview error: {str(e)}")
            else:
                # For PDF or other files
                filename = os.path.basename(file_path)
                self.preview_label.configure(text=f"Selected: {filename}", image="")
            
            self.message_label.configure(text="Certificate image selected", text_color="green")
    
    def _clear_certificate(self):
        """Clear the selected certificate"""
        self.certificate_path = None
        self.preview_label.configure(image="", text="No certificate selected")
        if hasattr(self.preview_label, 'image'):
            delattr(self.preview_label, 'image')
        self.message_label.configure(text="")
    
    def _save_certificate(self):
        """Save certificate to database"""
        # Validation
        if not self.students_dict or self.student_combo.get() == "No students found":
            self.message_label.configure(text="❌ Please select a student", text_color="red")
            return
        
        if not self.certificate_path:
            self.message_label.configure(text="❌ Please select a certificate image", text_color="red")
            return
        
        try:
            # Get selected student ID
            selected_key = self.student_combo.get()
            student_id = self.students_dict[selected_key]
            
            # Get note
            note = self.note_entry.get("1.0", "end-1c").strip()
            
            # Create certificates directory if it doesn't exist
            certificates_dir = "student_certificates"
            if not os.path.exists(certificates_dir):
                os.makedirs(certificates_dir)
            
            # Copy certificate to the certificates directory
            filename = f"cert_{student_id}_{os.path.basename(self.certificate_path)}"
            dest_path = os.path.join(certificates_dir, filename)
            shutil.copy2(self.certificate_path, dest_path)
            
            # Save to database
            success, message = self.db.add_certificate(student_id, dest_path, note)
            
            if success:
                self.message_label.configure(text="✓ Certificate saved successfully!", text_color="green")
                # Clear form
                self._clear_certificate()
                self.note_entry.delete("1.0", "end")
                # Refresh students
                self._load_students()
            else:
                self.message_label.configure(text=f"❌ Error: {message}", text_color="red")
                
        except Exception as e:
            self.message_label.configure(text=f"❌ Error: {str(e)}", text_color="red")
