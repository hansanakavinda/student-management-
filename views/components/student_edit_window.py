"""Student edit form window"""
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog
from PIL import Image
import shutil
import os
from widgets import EditDialog
from student_folder_utils import save_student_profile_image, ensure_student_folder_exists
from validators import Validators
from formatters import Formatters


class StudentEditWindow:
    """Window for editing student information"""
    
    def __init__(self, parent, student, db, on_success):
        self.parent = parent
        self.student = student
        self.db = db
        self.on_success = on_success
        self.error_labels = {}  # Store error label widgets
        
        self._create_window()
    
    def _create_window(self):
        """Create the edit window"""
        # Create edit dialog using reusable component
        self.edit_window = EditDialog(
            self.parent,
            title=f"Edit Student - {self.student[1]}",
            width=700,
            height=750
        )
        
        # Get content frame and configure for centering
        content = self.edit_window.content
        
        # Create centered container within the scrollable content
        centered_container = ctk.CTkFrame(content, fg_color="transparent")
        centered_container.pack(expand=True, pady=20)
        
        # Add title
        ctk.CTkLabel(
            centered_container,
            text="Edit Student Information",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(10, 20))
        
        # Initialize selected image
        self.current_image_path = self.student[8] if len(self.student) > 8 and self.student[8] else None
        self.selected_image = [self.current_image_path]
        
        # Create form
        self._create_form(centered_container)
    
    def _create_form(self, content):
        """Create the edit form"""
        # Image preview
        self.preview_label = ctk.CTkLabel(content, text="", width=150, height=150)
        self.preview_label.pack(pady=10)
        
        # Display current image
        if self.current_image_path and os.path.exists(self.current_image_path):
            self._display_image(self.current_image_path)
        
        # Image buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Choose Image",
            width=130,
            fg_color="#1E88E5",
            hover_color="#1976D2",
            command=self._choose_image
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel Image",
            width=130,
            fg_color="#E53935",
            hover_color="#D32F2F",
            command=self._cancel_image
        ).pack(side="left", padx=5)
        
        # Form fields
        form_frame = ctk.CTkFrame(content, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=10)
        
        # Create entries with formatters and error labels
        self.entries = {}
        
        # Student Name
        ctk.CTkLabel(form_frame, text="Student Name:", font=ctk.CTkFont(size=14)).grid(
            row=0, column=0, sticky="w", padx=10, pady=10
        )
        entry = ctk.CTkEntry(form_frame, width=300)
        entry.insert(0, self.student[1])
        entry.grid(row=0, column=1, padx=10, pady=10)
        Formatters.apply_name_formatting(entry)
        self.entries["Student Name:"] = entry
        self.error_labels['student_name'] = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['student_name'].grid(row=0, column=1, sticky="w", padx=10, pady=(60, 0))
        
        # Date of Birth
        ctk.CTkLabel(form_frame, text="Date of Birth:", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, sticky="w", padx=10, pady=10
        )
        entry = ctk.CTkEntry(form_frame, width=300)
        entry.insert(0, self.student[2])
        entry.grid(row=1, column=1, padx=10, pady=10)
        Formatters.apply_date_formatting(entry)
        self.entries["Date of Birth:"] = entry
        self.error_labels['dob'] = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['dob'].grid(row=1, column=1, sticky="w", padx=10, pady=(60, 0))
        
        # Address
        ctk.CTkLabel(form_frame, text="Address:", font=ctk.CTkFont(size=14)).grid(
            row=4, column=0, sticky="w", padx=10, pady=10
        )
        entry = ctk.CTkEntry(form_frame, width=300)
        entry.insert(0, self.student[4])
        entry.grid(row=4, column=1, padx=10, pady=10)
        self.entries["Address:"] = entry
        self.error_labels['address'] = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['address'].grid(row=4, column=1, sticky="w", padx=10, pady=(60, 0))
        
        # Guardian Name
        ctk.CTkLabel(form_frame, text="Guardian Name:", font=ctk.CTkFont(size=14)).grid(
            row=5, column=0, sticky="w", padx=10, pady=10
        )
        entry = ctk.CTkEntry(form_frame, width=300)
        entry.insert(0, self.student[5])
        entry.grid(row=5, column=1, padx=10, pady=10)
        Formatters.apply_name_formatting(entry)
        self.entries["Guardian Name:"] = entry
        self.error_labels['guardian_name'] = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['guardian_name'].grid(row=5, column=1, sticky="w", padx=10, pady=(60, 0))
        
        # Guardian NIC
        ctk.CTkLabel(form_frame, text="Guardian NIC (12 digits):", font=ctk.CTkFont(size=14)).grid(
            row=6, column=0, sticky="w", padx=10, pady=10
        )
        entry = ctk.CTkEntry(form_frame, width=300)
        entry.insert(0, self.student[6])
        entry.grid(row=6, column=1, padx=10, pady=10)
        Formatters.apply_nic_formatting(entry)
        self.entries["Guardian NIC:"] = entry
        self.error_labels['guardian_nic'] = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['guardian_nic'].grid(row=6, column=1, sticky="w", padx=10, pady=(60, 0))
        
        # Guardian Contact
        ctk.CTkLabel(form_frame, text="Guardian Contact (10 digits):", font=ctk.CTkFont(size=14)).grid(
            row=7, column=0, sticky="w", padx=10, pady=10
        )
        entry = ctk.CTkEntry(form_frame, width=300)
        entry.insert(0, self.student[7])
        entry.grid(row=7, column=1, padx=10, pady=10)
        Formatters.apply_contact_formatting(entry)
        self.entries["Guardian Contact:"] = entry
        self.error_labels['guardian_contact'] = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['guardian_contact'].grid(row=7, column=1, sticky="w", padx=10, pady=(60, 0))
        
        # Grade dropdown (after DOB)
        ctk.CTkLabel(
            form_frame,
            text="Grade:",
            font=ctk.CTkFont(size=14)
        ).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        
        grade_options = [f"Grade {i}" for i in range(1, 14)]
        self.grade_dropdown = ctk.CTkOptionMenu(form_frame, values=grade_options, width=300)
        current_grade = self.student[10] if len(self.student) > 10 and self.student[10] else "Grade 1"
        self.grade_dropdown.set(current_grade)
        self.grade_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Registration Date
        ctk.CTkLabel(
            form_frame,
            text="Registration Date:",
            font=ctk.CTkFont(size=14)
        ).grid(row=3, column=0, sticky="w", padx=10, pady=10)
        
        reg_date_entry = ctk.CTkEntry(form_frame, width=300)
        reg_date_value = self.student[9] if len(self.student) > 9 and self.student[9] else datetime.now().strftime("%Y-%m-%d")
        reg_date_entry.insert(0, reg_date_value)
        reg_date_entry.grid(row=3, column=1, padx=10, pady=10)
        Formatters.apply_date_formatting(reg_date_entry)
        self.entries["Registration Date:"] = reg_date_entry
        self.error_labels['reg_date'] = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['reg_date'].grid(row=3, column=1, sticky="w", padx=10, pady=(60, 0))
        
        # Gender
        ctk.CTkLabel(
            form_frame,
            text="Gender:",
            font=ctk.CTkFont(size=14)
        ).grid(row=8, column=0, sticky="w", padx=10, pady=10)
        
        self.gender_var = ctk.StringVar(value=self.student[3])
        gender_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        gender_frame.grid(row=8, column=1, sticky="w", padx=10, pady=10)
        
        ctk.CTkRadioButton(
            gender_frame,
            text="Male",
            variable=self.gender_var,
            value="Male"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            gender_frame,
            text="Female",
            variable=self.gender_var,
            value="Female"
        ).pack(side="left", padx=10)
        
        # Message label
        self.message_label = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=12))
        self.message_label.pack(pady=10)
        
        # Add standard button frame
        self.edit_window.add_button_frame(self._update_student, save_text="Update Student")
    
    def _display_image(self, image_path):
        """Display image in preview"""
        try:
            img = Image.open(image_path)
            img.thumbnail((150, 150))
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo
        except:
            pass
    
    def _choose_image(self):
        """Open file dialog to choose image"""
        file_path = filedialog.askopenfilename(
            title="Select Student Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            self.selected_image[0] = file_path
            self._display_image(file_path)
    
    def _cancel_image(self):
        """Remove selected image"""
        self.selected_image[0] = None
        # Remove the image attribute first
        if hasattr(self.preview_label, 'image'):
            delattr(self.preview_label, 'image')
        # Configure without image parameter to avoid warning
        self.preview_label.configure(text="")
    
    def _clear_all_errors(self):
        """Clear all error messages"""
        for error_label in self.error_labels.values():
            error_label.configure(text="")
    
    def _update_student(self):
        """Update student in database"""
        # Clear previous errors
        self._clear_all_errors()
        self.message_label.configure(text="")
        
        student_name = self.entries["Student Name:"].get().strip()
        dob = self.entries["Date of Birth:"].get().strip()
        gender = self.gender_var.get()
        address = self.entries["Address:"].get().strip()
        guardian_name = self.entries["Guardian Name:"].get().strip()
        guardian_nic = self.entries["Guardian NIC:"].get().strip()
        guardian_contact = self.entries["Guardian Contact:"].get().strip()
        grade = self.grade_dropdown.get().strip()
        reg_date = self.entries["Registration Date:"].get().strip()
        
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
            self.message_label.configure(text=result.error_message, text_color="red")
            has_error = True
        
        if has_error:
            self.message_label.configure(text="Please fix the errors above", text_color="red")
            return
        
        # Handle image
        saved_image_path = self.selected_image[0]
        if self.selected_image[0] and self.selected_image[0] != self.current_image_path:
            try:
                # Ensure student folder exists and save profile image
                saved_image_path = save_student_profile_image(
                    self.selected_image[0], 
                    student_name, 
                    self.student[0]
                )
                if not saved_image_path:
                    self.message_label.configure(
                        text="Error saving image to student folder",
                        text_color="red"
                    )
                    return
            except Exception as e:
                self.message_label.configure(
                    text=f"Error saving image: {e}",
                    text_color="red"
                )
                return
        
        # Update database
        student_data = (
            student_name, dob, gender, address,
            guardian_name, guardian_nic, guardian_contact, saved_image_path,
            reg_date, grade
        )
        success, message = self.db.update_student(self.student[0], student_data)
        
        if success:
            self.message_label.configure(
                text="Student updated successfully!",
                text_color="green"
            )
            self.edit_window.after(1000, self.edit_window.destroy)
            if self.on_success:
                self.on_success()
        else:
            self.message_label.configure(
                text=f"Error: {message}",
                text_color="red"
            )
