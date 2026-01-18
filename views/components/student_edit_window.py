"""Student edit form window"""
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog
from PIL import Image
import shutil
import os
from widgets import EditDialog


class StudentEditWindow:
    """Window for editing student information"""
    
    def __init__(self, parent, student, db, on_success):
        self.parent = parent
        self.student = student
        self.db = db
        self.on_success = on_success
        
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
            command=self._choose_image
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel Image",
            width=130,
            fg_color="#8B0000",
            hover_color="#A52A2A",
            command=self._cancel_image
        ).pack(side="left", padx=5)
        
        # Form fields
        form_frame = ctk.CTkFrame(content, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=10)
        
        # Create entries
        self.entries = {}
        fields_config = [
            ("Student Name:", self.student[1], 0),
            ("Date of Birth:", self.student[2], 1),
            ("Address:", self.student[4], 3),
            ("Guardian Name:", self.student[5], 4),
            ("Guardian NIC:", self.student[6], 5),
            ("Guardian Contact:", self.student[7], 6),
        ]
        
        for label, value, row in fields_config:
            ctk.CTkLabel(
                form_frame,
                text=label,
                font=ctk.CTkFont(size=14)
            ).grid(row=row, column=0, sticky="w", padx=10, pady=10)
            
            entry = ctk.CTkEntry(form_frame, width=300)
            entry.insert(0, value)
            entry.grid(row=row, column=1, padx=10, pady=10)
            self.entries[label] = entry
        
        # Gender
        ctk.CTkLabel(
            form_frame,
            text="Gender:",
            font=ctk.CTkFont(size=14)
        ).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        
        self.gender_var = ctk.StringVar(value=self.student[3])
        gender_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        gender_frame.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
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
        self.preview_label.configure(image="", text="")
        if hasattr(self.preview_label, 'image'):
            delattr(self.preview_label, 'image')
    
    def _update_student(self):
        """Update student in database"""
        student_name = self.entries["Student Name:"].get().strip()
        dob = self.entries["Date of Birth:"].get().strip()
        gender = self.gender_var.get()
        address = self.entries["Address:"].get().strip()
        guardian_name = self.entries["Guardian Name:"].get().strip()
        guardian_nic = self.entries["Guardian NIC:"].get().strip()
        guardian_contact = self.entries["Guardian Contact:"].get().strip()
        
        # Validate
        if not all([student_name, dob, address, guardian_name, guardian_nic, guardian_contact]):
            self.message_label.configure(
                text="All fields except image are required!",
                text_color="red"
            )
            return
        
        if len(guardian_contact) != 10 or not guardian_contact.isdigit():
            self.message_label.configure(
                text="Guardian contact must be exactly 10 digits!",
                text_color="red"
            )
            return
        
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            self.message_label.configure(
                text="Invalid date format! Use YYYY-MM-DD",
                text_color="red"
            )
            return
        
        # Handle image
        saved_image_path = self.selected_image[0]
        if self.selected_image[0] and self.selected_image[0] != self.current_image_path:
            try:
                if not os.path.exists("student_images"):
                    os.makedirs("student_images")
                ext = os.path.splitext(self.selected_image[0])[1]
                new_filename = f"{student_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
                saved_image_path = os.path.join("student_images", new_filename)
                shutil.copy2(self.selected_image[0], saved_image_path)
            except Exception as e:
                self.message_label.configure(
                    text=f"Error saving image: {e}",
                    text_color="red"
                )
                return
        
        # Update database
        student_data = (
            student_name, dob, gender, address,
            guardian_name, guardian_nic, guardian_contact, saved_image_path
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
