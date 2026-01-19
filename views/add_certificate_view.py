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
        self.certificates = []  # List to store [path, note] pairs
        
        # Create the main frame
        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(fill="both", expand=True)
        
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
            text="Certificate Images",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 10))
        
        # Image buttons
        image_btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        image_btn_frame.pack(pady=10)
        
        ctk.CTkButton(
            image_btn_frame,
            text="📁 Add Certificate Images",
            font=ctk.CTkFont(size=14),
            width=200,
            height=40,
            fg_color="#1E88E5",
            hover_color="#1976D2",
            command=self._choose_certificate
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            image_btn_frame,
            text="❌ Clear All",
            font=ctk.CTkFont(size=14),
            width=100,
            height=40,
            fg_color="#666666",
            hover_color="#888888",
            command=self._clear_certificate
        ).pack(side="left", padx=10)
        
        # Certificates display frame
        self.certificates_display_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.certificates_display_frame.pack(fill="both", expand=True, pady=10)
        
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
            text="💾 Save Certificates",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=45,
            fg_color="#43A047",
            hover_color="#388E3C",
            command=self._save_certificate
        ).pack(pady=20)
        
        # Load students and update display
        self._load_students()
        self._update_certificates_display()
    
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
        """Open file dialog to choose multiple certificate images"""
        file_paths = filedialog.askopenfilenames(
            title="Select Certificate Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.pdf")]
        )
        
        if file_paths:
            for file_path in file_paths:
                # Add certificate with empty note initially
                self.certificates.append([file_path, ""])
            
            # Refresh the certificates display
            self._update_certificates_display()
            self.message_label.configure(text=f"{len(file_paths)} certificate(s) added", text_color="green")
    
    def _clear_certificate(self):
        """Clear all selected certificates"""
        self.certificates = []
        self._update_certificates_display()
        
    
    def _update_certificates_display(self):
        """Update the certificates display area"""
        # Clear existing display
        for widget in self.certificates_display_frame.winfo_children():
            widget.destroy()
        
        if not self.certificates:
            ctk.CTkLabel(
                self.certificates_display_frame,
                text="No certificates added yet",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(pady=20)
            return
        
        # Display each certificate with preview and note field
        for idx, cert_data in enumerate(self.certificates):
            cert_path, cert_note = cert_data
            
            # Certificate card
            cert_card = ctk.CTkFrame(self.certificates_display_frame, fg_color="#2b2b2b", corner_radius=8)
            cert_card.pack(fill="x", padx=20, pady=5)
            
            # Left side - Preview and name
            left_frame = ctk.CTkFrame(cert_card, fg_color="transparent")
            left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            # Show preview thumbnail if image
            if cert_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                try:
                    img = Image.open(cert_path)
                    img.thumbnail((60, 60))
                    photo = ctk.CTkImage(light_image=img, dark_image=img, size=(60, 60))
                    img_label = ctk.CTkLabel(left_frame, image=photo, text="")
                    img_label.image = photo
                    img_label.pack(side="left", padx=5)
                except:
                    ctk.CTkLabel(left_frame, text="📄", font=ctk.CTkFont(size=30)).pack(side="left", padx=5)
            else:
                ctk.CTkLabel(left_frame, text="📄", font=ctk.CTkFont(size=30)).pack(side="left", padx=5)
            
            # Certificate name and note
            info_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(
                info_frame,
                text=os.path.basename(cert_path),
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor="w"
            ).pack(anchor="w")
            
            # Note entry
            note_label = ctk.CTkLabel(info_frame, text="Note:", font=ctk.CTkFont(size=10), anchor="w")
            note_label.pack(anchor="w", pady=(5, 0))
            
            note_entry = ctk.CTkEntry(info_frame, width=300, placeholder_text="Add a note (optional)")
            note_entry.insert(0, cert_note)
            note_entry.pack(anchor="w", fill="x")
            
            # Update note in list when changed
            def update_note(idx=idx, entry=note_entry):
                self.certificates[idx][1] = entry.get()
            
            note_entry.bind('<KeyRelease>', lambda e, idx=idx: update_note(idx, note_entry))
            
            # Right side - Remove button
            ctk.CTkButton(
                cert_card,
                text="✕",
                width=40,
                height=40,
                fg_color="#E53935",
                hover_color="#D32F2F",
                command=lambda idx=idx: self._remove_certificate(idx)
            ).pack(side="right", padx=10, pady=10)
    
    def _remove_certificate(self, idx):
        """Remove a certificate from the list"""
        if 0 <= idx < len(self.certificates):
            self.certificates.pop(idx)
            self._update_certificates_display()
            self.message_label.configure(text="Certificate removed", text_color="orange")
    
    def _save_certificate(self):
        """Save certificates to database"""
        # Validation
        if not self.students_dict or self.student_combo.get() == "No students found":
            self.message_label.configure(text="❌ Please select a student", text_color="red")
            return
        
        if not self.certificates:
            self.message_label.configure(text="❌ Please add at least one certificate", text_color="red")
            return
        
        try:
            # Get selected student ID
            selected_key = self.student_combo.get()
            student_id = self.students_dict[selected_key]
            
            # Create certificates directory if it doesn't exist
            certificates_dir = "student_certificates"
            if not os.path.exists(certificates_dir):
                os.makedirs(certificates_dir)
            
            # Save each certificate
            saved_count = 0
            failed_count = 0
            
            for cert_path, note in self.certificates:
                try:
                    # Copy certificate to the certificates directory
                    from datetime import datetime
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    filename = f"cert_{student_id}_{timestamp}_{saved_count}_{os.path.basename(cert_path)}"
                    dest_path = os.path.join(certificates_dir, filename)
                    shutil.copy2(cert_path, dest_path)
                    
                    # Save to database
                    success, message = self.db.add_certificate(student_id, dest_path, note)
                    
                    if success:
                        saved_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    failed_count += 1
            
            # Show result
            if saved_count > 0 and failed_count == 0:
                self.message_label.configure(
                    text=f"{saved_count} certificate(s) saved successfully!", 
                    text_color="green"
                )
                # Clear form
                self._clear_certificate()
                # Refresh students
                self._load_students()
            elif saved_count > 0 and failed_count > 0:
                self.message_label.configure(
                    text=f"⚠ {saved_count} saved, {failed_count} failed", 
                    text_color="orange"
                )
            else:
                self.message_label.configure(
                    text=f"❌ Failed to save certificates", 
                    text_color="red"
                )
                
        except Exception as e:
            self.message_label.configure(text=f"❌ Error: {str(e)}", text_color="red")
