"""Add Student view for Student Management System"""
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog
from PIL import Image
import shutil
import os
from widgets import WatermarkWidget
from student_folder_utils import (save_student_profile_image, save_student_certificate,
                                   ensure_student_folder_exists)
from validators import Validators
from formatters import Formatters


class AddStudentView:
    """Student registration form view"""
    
    def __init__(self, parent, db, form_message_callback=None):
        self.parent = parent
        self.db = db
        self.image_path = None
        self.certificates = []  # List to store (path, note) tuples
        self.form_message_callback = form_message_callback
        self.error_labels = {}  # Store error label widgets
        
        # Create the form
        self.form_frame = ctk.CTkScrollableFrame(parent)
        self.form_frame.pack(fill="both", expand=True)
        
        # Create centered container within the scrollable content
        centered_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        centered_container.pack(expand=True, pady=20)
        
        self._create_form(centered_container)
    
    def _create_form(self, content):
        """Create the registration form UI"""
        title = ctk.CTkLabel(
            content,
            text="Student Registration",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=20)
        
        # Image Preview at top
        self.preview_label = ctk.CTkLabel(
            content,
            text="👤",
            font=ctk.CTkFont(size=80),
            width=150,
            height=150,
            fg_color="#2b2b2b",
            corner_radius=10
        )
        self.preview_label.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Image buttons
        image_btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        image_btn_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        ctk.CTkButton(
            image_btn_frame,
            text="Choose Image",
            width=140,
            command=self.choose_image
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            image_btn_frame,
            text="Cancel Image",
            width=140,
            fg_color="#8B0000",
            hover_color="#A52A2A",
            command=self.cancel_image
        ).pack(side="left", padx=5)
        
        # Student Name
        ctk.CTkLabel(content, text="Student Name:", font=ctk.CTkFont(size=14)).grid(
            row=3, column=0, sticky="w", padx=20, pady=10
        )
        self.student_name_entry = ctk.CTkEntry(content, width=300)
        self.student_name_entry.grid(row=3, column=1, padx=20, pady=10)
        Formatters.apply_name_formatting(self.student_name_entry)
        self.error_labels['student_name'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['student_name'].grid(row=3, column=1, sticky="w", padx=20, pady=(60, 0))
        
        # Date of Birth with auto-formatting
        ctk.CTkLabel(content, text="Date of Birth (YYYY-MM-DD):", font=ctk.CTkFont(size=14)).grid(
            row=4, column=0, sticky="w", padx=20, pady=10
        )
        self.dob_entry = ctk.CTkEntry(content, width=300, placeholder_text="20050115")
        self.dob_entry.grid(row=4, column=1, padx=20, pady=10)
        Formatters.apply_date_formatting(self.dob_entry)
        self.error_labels['dob'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['dob'].grid(row=4, column=1, sticky="w", padx=20, pady=(60, 0))
        
        # Grade
        ctk.CTkLabel(content, text="Grade:", font=ctk.CTkFont(size=14)).grid(
            row=5, column=0, sticky="w", padx=20, pady=10
        )
        grade_options = [f"Grade {i}" for i in range(1, 14)]
        self.grade_dropdown = ctk.CTkOptionMenu(content, values=grade_options, width=300)
        self.grade_dropdown.set("Grade 1")
        self.grade_dropdown.grid(row=5, column=1, padx=20, pady=10, sticky="w")
        
        # Registration Date
        ctk.CTkLabel(content, text="Registration Date (YYYY-MM-DD):", font=ctk.CTkFont(size=14)).grid(
            row=6, column=0, sticky="w", padx=20, pady=10
        )
        self.reg_date_entry = ctk.CTkEntry(content, width=300)
        # Set current date as default
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.reg_date_entry.insert(0, current_date)
        self.reg_date_entry.grid(row=6, column=1, padx=20, pady=10)
        Formatters.apply_date_formatting(self.reg_date_entry)
        self.error_labels['reg_date'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['reg_date'].grid(row=6, column=1, sticky="w", padx=20, pady=(60, 0))
        
        # Gender
        ctk.CTkLabel(content, text="Gender:", font=ctk.CTkFont(size=14)).grid(
            row=7, column=0, sticky="w", padx=20, pady=10
        )
        self.gender_var = ctk.StringVar(value="Male")
        gender_frame = ctk.CTkFrame(content, fg_color="transparent")
        gender_frame.grid(row=7, column=1, sticky="w", padx=20, pady=10)
        ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side="left", padx=10)
        ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side="left", padx=10)
        
        # Address
        ctk.CTkLabel(content, text="Address:", font=ctk.CTkFont(size=14)).grid(
            row=8, column=0, sticky="w", padx=20, pady=10
        )
        self.address_entry = ctk.CTkEntry(content, width=300)
        self.address_entry.grid(row=8, column=1, padx=20, pady=10)
        self.error_labels['address'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['address'].grid(row=8, column=1, sticky="w", padx=20, pady=(60, 0))
        
        # Guardian Name
        ctk.CTkLabel(content, text="Guardian Name:", font=ctk.CTkFont(size=14)).grid(
            row=9, column=0, sticky="w", padx=20, pady=10
        )
        self.guardian_name_entry = ctk.CTkEntry(content, width=300)
        self.guardian_name_entry.grid(row=9, column=1, padx=20, pady=10)
        Formatters.apply_name_formatting(self.guardian_name_entry)
        self.error_labels['guardian_name'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['guardian_name'].grid(row=9, column=1, sticky="w", padx=20, pady=(60, 0))
        
        # Guardian NIC
        ctk.CTkLabel(content, text="Guardian NIC (12 digits):", font=ctk.CTkFont(size=14)).grid(
            row=10, column=0, sticky="w", padx=20, pady=10
        )
        self.guardian_nic_entry = ctk.CTkEntry(content, width=300, placeholder_text="200212345678")
        self.guardian_nic_entry.grid(row=10, column=1, padx=20, pady=10)
        Formatters.apply_nic_formatting(self.guardian_nic_entry)
        self.error_labels['guardian_nic'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['guardian_nic'].grid(row=10, column=1, sticky="w", padx=20, pady=(60, 0))
        
        # Guardian Contact with digit limit
        ctk.CTkLabel(content, text="Guardian Contact (10 digits):", font=ctk.CTkFont(size=14)).grid(
            row=11, column=0, sticky="w", padx=20, pady=10
        )
        self.guardian_contact_entry = ctk.CTkEntry(content, width=300, placeholder_text="0771234567")
        self.guardian_contact_entry.grid(row=11, column=1, padx=20, pady=10)
        Formatters.apply_contact_formatting(self.guardian_contact_entry)
        self.error_labels['guardian_contact'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['guardian_contact'].grid(row=11, column=1, sticky="w", padx=20, pady=(60, 0))
        
        # Separator for certificates section
        separator = ctk.CTkFrame(content, height=2, fg_color="gray")
        separator.grid(row=12, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        
        # Certificates Section Title
        ctk.CTkLabel(
            content,
            text="Certificates (Optional)",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=13, column=0, columnspan=2, pady=(10, 5))
        
        # Certificate buttons
        cert_btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        cert_btn_frame.grid(row=14, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(
            cert_btn_frame,
            text="📁 Add Certificates",
            width=180,
            fg_color="#1E88E5",
            hover_color="#1976D2",
            command=self.add_certificates
        ).pack(side="left", padx=5)
        
        # Certificates display frame
        self.certificates_display_frame = ctk.CTkFrame(content, fg_color="transparent")
        self.certificates_display_frame.grid(row=15, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Error/Success message
        self.form_message = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=12))
        self.form_message.grid(row=16, column=0, columnspan=2, pady=10)
        
        # Submit button
        ctk.CTkButton(
            content,
            text="Register Student",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=45,
            fg_color="#43A047",
            hover_color="#388E3C",
            command=self.submit_student
        ).grid(row=17, column=0, columnspan=2, pady=(20, 40))
    
    def choose_image(self):
        """Open file dialog to choose student image"""
        file_path = filedialog.askopenfilename(
            title="Select Student Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            # Show preview
            try:
                img = Image.open(file_path)
                img.thumbnail((150, 150))
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
                self.preview_label.configure(
                    image=photo,
                    text="",
                    fg_color="transparent"
                )
                self.preview_label.image = photo
            except Exception as e:
                self.form_message.configure(text=f"Error loading image: {e}", text_color="red")
    
    def cancel_image(self):
        """Remove selected image and clear preview"""
        self.image_path = None
        try:
            # Remove the image attribute first
            if hasattr(self.preview_label, 'image'):
                delattr(self.preview_label, 'image')
            # Configure without image parameter to avoid warning
            self.preview_label.configure(
                text="👤",
                font=ctk.CTkFont(size=80),
                fg_color="#2b2b2b"
            )
        except:
            pass
    
    def add_certificates(self):
        """Open file dialog to add multiple certificates"""
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
            ).pack(pady=10)
            return
        
        # Display each certificate with preview and note field
        for idx, cert_data in enumerate(self.certificates):
            cert_path, cert_note = cert_data
            
            # Certificate card
            cert_card = ctk.CTkFrame(self.certificates_display_frame, fg_color="#000000", corner_radius=8)
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
    
    def _clear_all_errors(self):
        """Clear all error messages"""
        for error_label in self.error_labels.values():
            error_label.configure(text="")
    
    def submit_student(self):
        """Handle student registration form submission"""
        # Clear previous errors
        self._clear_all_errors()
        self.form_message.configure(text="")
        
        student_name = self.student_name_entry.get().strip()
        dob = self.dob_entry.get().strip()
        grade = self.grade_dropdown.get().strip()
        reg_date = self.reg_date_entry.get().strip()
        gender = self.gender_var.get()
        address = self.address_entry.get().strip()
        guardian_name = self.guardian_name_entry.get().strip()
        guardian_nic = self.guardian_nic_entry.get().strip()
        guardian_contact = self.guardian_contact_entry.get().strip()
        
        # Validate all fields using centralized validators
        has_error = False
        
        # Validate student name
        result = Validators.validate_student_name(student_name)
        if not result.is_valid:
            self.error_labels['student_name'].configure(text=result.error_message)
            has_error = True
        
        # Validate date of birth
        result = Validators.validate_date_of_birth(dob)
        if not result.is_valid:
            self.error_labels['dob'].configure(text=result.error_message)
            has_error = True
        
        # Validate registration date
        result = Validators.validate_registration_date(reg_date)
        if not result.is_valid:
            self.error_labels['reg_date'].configure(text=result.error_message)
            has_error = True
        
        # Validate address
        result = Validators.validate_address(address)
        if not result.is_valid:
            self.error_labels['address'].configure(text=result.error_message)
            has_error = True
        
        # Validate guardian name
        result = Validators.validate_guardian_name(guardian_name)
        if not result.is_valid:
            self.error_labels['guardian_name'].configure(text=result.error_message)
            has_error = True
        
        # Validate guardian NIC
        result = Validators.validate_guardian_nic(guardian_nic)
        if not result.is_valid:
            self.error_labels['guardian_nic'].configure(text=result.error_message)
            has_error = True
        
        # Validate guardian contact
        result = Validators.validate_guardian_contact(guardian_contact)
        if not result.is_valid:
            self.error_labels['guardian_contact'].configure(text=result.error_message)
            has_error = True
        
        # Validate grade
        result = Validators.validate_grade_level(grade)
        if not result.is_valid:
            self.form_message.configure(text=result.error_message, text_color="red")
            has_error = True
        
        if has_error:
            self.form_message.configure(text="Please fix the errors above", text_color="red")
            return
        
        # Add to database first without image/certificates
        student_data = (student_name, dob, gender, address, guardian_name, guardian_nic, guardian_contact, 
                       None, reg_date, grade)
        
        success, result = self.db.add_student(student_data, None)
        
        if success:
            student_id = result
            
            # Now save image and certificates to student folder
            saved_image_path = None
            if self.image_path:
                try:
                    # Ensure student folder exists and save profile image
                    saved_image_path = save_student_profile_image(self.image_path, student_name, student_id)
                    if saved_image_path:
                        # Update student record with image path
                        update_data = (student_name, dob, gender, address, guardian_name, guardian_nic, 
                                     guardian_contact, saved_image_path, reg_date, grade)
                        self.db.update_student(student_id, update_data)
                except Exception as e:
                    self.form_message.configure(text=f"Student registered but error saving image: {e}", text_color="orange")
            
            # Save certificates to student folder
            if self.certificates:
                try:
                    # Ensure student folder exists
                    ensure_student_folder_exists(student_name, student_id)
                    
                    for cert_path, cert_note in self.certificates:
                        # Save certificate to student folder
                        saved_cert_path = save_student_certificate(cert_path, student_name, student_id, cert_note)
                        if saved_cert_path:
                            # Add certificate record to database
                            self.db.add_certificate(student_id, saved_cert_path, cert_note)
                except Exception as e:
                    self.form_message.configure(text=f"Student registered but error saving certificates: {e}", text_color="orange")
            
            self.form_message.configure(text=f"Student registered successfully! ID: {student_id}", text_color="green")
            # Clear form
            self.student_name_entry.delete(0, 'end')
            self.dob_entry.delete(0, 'end')
            self.grade_dropdown.set("Grade 1")
            self.reg_date_entry.delete(0, 'end')
            self.reg_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            self.address_entry.delete(0, 'end')
            self.guardian_name_entry.delete(0, 'end')
            self.guardian_nic_entry.delete(0, 'end')
            self.guardian_contact_entry.delete(0, 'end')
            self.image_path = None
            self.certificates = []
            self._update_certificates_display()
            # Remove the image attribute first
            if hasattr(self.preview_label, 'image'):
                delattr(self.preview_label, 'image')
            # Configure without image parameter to avoid warning
            self.preview_label.configure(
                text="👤",
                font=ctk.CTkFont(size=80),
                fg_color="#2b2b2b"
            )
        else:
            self.form_message.configure(text=f"Error: {result}", text_color="red")
