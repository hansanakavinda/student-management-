"""Add Student view for Student Management System"""
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog
from PIL import Image
import shutil
import os
from widgets import WatermarkWidget


class AddStudentView:
    """Student registration form view"""
    
    def __init__(self, parent, db, form_message_callback=None):
        self.parent = parent
        self.db = db
        self.image_path = None
        self.certificates = []  # List to store (path, note) tuples
        self.form_message_callback = form_message_callback
        
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
        
        # Date of Birth with auto-formatting
        ctk.CTkLabel(content, text="Date of Birth (YYYY-MM-DD):", font=ctk.CTkFont(size=14)).grid(
            row=4, column=0, sticky="w", padx=20, pady=10
        )
        self.dob_entry = ctk.CTkEntry(content, width=300, placeholder_text="20050115")
        self.dob_entry.grid(row=4, column=1, padx=20, pady=10)
        self.dob_entry.bind('<KeyRelease>', self._format_dob)
        
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
        
        # Guardian Name
        ctk.CTkLabel(content, text="Guardian Name:", font=ctk.CTkFont(size=14)).grid(
            row=9, column=0, sticky="w", padx=20, pady=10
        )
        self.guardian_name_entry = ctk.CTkEntry(content, width=300)
        self.guardian_name_entry.grid(row=9, column=1, padx=20, pady=10)
        
        # Guardian NIC
        ctk.CTkLabel(content, text="Guardian NIC:", font=ctk.CTkFont(size=14)).grid(
            row=10, column=0, sticky="w", padx=20, pady=10
        )
        self.guardian_nic_entry = ctk.CTkEntry(content, width=300, placeholder_text="123456789V")
        self.guardian_nic_entry.grid(row=10, column=1, padx=20, pady=10)
        
        # Guardian Contact with digit limit
        ctk.CTkLabel(content, text="Guardian Contact (10 digits):", font=ctk.CTkFont(size=14)).grid(
            row=11, column=0, sticky="w", padx=20, pady=10
        )
        self.guardian_contact_entry = ctk.CTkEntry(content, width=300, placeholder_text="0771234567")
        self.guardian_contact_entry.grid(row=11, column=1, padx=20, pady=10)
        self.guardian_contact_entry.bind('<KeyRelease>', self._limit_contact_digits)
        
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
            self.preview_label.configure(
                image="",
                text="👤",
                font=ctk.CTkFont(size=80),
                fg_color="#2b2b2b"
            )
            if hasattr(self.preview_label, 'image'):
                delattr(self.preview_label, 'image')
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
            cert_card = ctk.CTkFrame(self.certificates_display_frame, fg_color="#f0f0f0", corner_radius=8)
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
    
    def _format_dob(self, event):
        """Auto-format date of birth as YYYY-MM-DD"""
        text = self.dob_entry.get().replace("-", "")
        text = ''.join(filter(str.isdigit, text))
        
        if len(text) > 8:
            text = text[:8]
        
        formatted = text
        if len(text) > 4:
            formatted = text[:4] + "-" + text[4:]
        if len(text) > 6:
            formatted = text[:4] + "-" + text[4:6] + "-" + text[6:]
        
        current_pos = self.dob_entry.index("insert")
        if self.dob_entry.get() != formatted:
            self.dob_entry.delete(0, 'end')
            self.dob_entry.insert(0, formatted)
            if current_pos > 4 and len(text) > 4:
                current_pos += 1
            if current_pos > 7 and len(text) > 6:
                current_pos += 1
            try:
                self.dob_entry.icursor(min(current_pos, len(formatted)))
            except:
                pass
    
    def _limit_contact_digits(self, event):
        """Limit guardian contact to 10 digits only"""
        text = self.guardian_contact_entry.get()
        text = ''.join(filter(str.isdigit, text))
        if len(text) > 10:
            text = text[:10]
        
        if self.guardian_contact_entry.get() != text:
            current_pos = self.guardian_contact_entry.index("insert")
            self.guardian_contact_entry.delete(0, 'end')
            self.guardian_contact_entry.insert(0, text)
            try:
                self.guardian_contact_entry.icursor(min(current_pos, len(text)))
            except:
                pass
    
    def submit_student(self):
        """Handle student registration form submission"""
        student_name = self.student_name_entry.get().strip()
        dob = self.dob_entry.get().strip()
        grade = self.grade_dropdown.get().strip()
        reg_date = self.reg_date_entry.get().strip()
        gender = self.gender_var.get()
        address = self.address_entry.get().strip()
        guardian_name = self.guardian_name_entry.get().strip()
        guardian_nic = self.guardian_nic_entry.get().strip()
        guardian_contact = self.guardian_contact_entry.get().strip()
        
        # Validate
        if not all([student_name, dob, grade, reg_date, address, guardian_name, guardian_nic, guardian_contact]):
            self.form_message.configure(text="All fields except image and certificates are required!", text_color="red")
            return
        
        if len(guardian_contact) != 10 or not guardian_contact.isdigit():
            self.form_message.configure(text="Guardian contact must be exactly 10 digits!", text_color="red")
            return
        
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            self.form_message.configure(text="Invalid date of birth format! Use YYYY-MM-DD", text_color="red")
            return
        
        try:
            datetime.strptime(reg_date, "%Y-%m-%d")
        except ValueError:
            self.form_message.configure(text="Invalid registration date format! Use YYYY-MM-DD", text_color="red")
            return
        
        # Handle image if provided
        saved_image_path = None
        if self.image_path:
            try:
                if not os.path.exists("student_images"):
                    os.makedirs("student_images")
                
                ext = os.path.splitext(self.image_path)[1]
                new_filename = f"{student_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
                saved_image_path = os.path.join("student_images", new_filename)
                shutil.copy2(self.image_path, saved_image_path)
            except Exception as e:
                self.form_message.configure(text=f"Error saving image: {e}", text_color="red")
                return
        
        # Add to database
        student_data = (student_name, dob, gender, address, guardian_name, guardian_nic, guardian_contact, 
                       saved_image_path, reg_date, grade)
        
        # Prepare certificates data if any
        certificates_data = None
        if self.certificates:
            try:
                # Create certificates directory
                if not os.path.exists("student_certificates"):
                    os.makedirs("student_certificates")
                
                certificates_data = []
                for cert_path, cert_note in self.certificates:
                    # Copy certificate file
                    ext = os.path.splitext(cert_path)[1]
                    cert_filename = f"{student_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(certificates_data)}{ext}"
                    saved_cert_path = os.path.join("student_certificates", cert_filename)
                    shutil.copy2(cert_path, saved_cert_path)
                    certificates_data.append((saved_cert_path, cert_note))
            except Exception as e:
                self.form_message.configure(text=f"Error saving certificates: {e}", text_color="red")
                return
        
        success, result = self.db.add_student(student_data, certificates_data)
        
        if success:
            self.form_message.configure(text=f"Student registered successfully! ID: {result}", text_color="green")
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
            self.preview_label.configure(
                image="",
                text="👤",
                font=ctk.CTkFont(size=80),
                fg_color="#2b2b2b"
            )
            if hasattr(self.preview_label, 'image'):
                delattr(self.preview_label, 'image')
        else:
            self.form_message.configure(text=f"Error: {result}", text_color="red")
