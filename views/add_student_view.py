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
        self.form_message_callback = form_message_callback
        
        # Create the form
        self.form_frame = ctk.CTkScrollableFrame(parent)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add watermark as background using place() so it doesn't interfere with grid layout
        # self.watermark = WatermarkWidget(
        #     self.form_frame,
        #     image_path="logo.png",
        #     opacity=0.1,
        #     size=(600, 600)
        # )
        # # Place it at the center - it will be behind all grid elements
        # self.watermark.place(relx=0.5, rely=0.5, anchor="center")

        self._create_form()
    
    def _create_form(self):
        """Create the registration form UI"""
        title = ctk.CTkLabel(
            self.form_frame,
            text="Student Registration",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=20)
        
        # Image Preview at top
        self.preview_label = ctk.CTkLabel(
            self.form_frame,
            text="👤",
            font=ctk.CTkFont(size=80),
            width=150,
            height=150,
            fg_color="#2b2b2b",
            corner_radius=10
        )
        self.preview_label.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Image buttons
        image_btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
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
        ctk.CTkLabel(self.form_frame, text="Student Name:", font=ctk.CTkFont(size=14)).grid(
            row=3, column=0, sticky="w", padx=20, pady=10
        )
        self.student_name_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.student_name_entry.grid(row=3, column=1, padx=20, pady=10)
        
        # Date of Birth with auto-formatting
        ctk.CTkLabel(self.form_frame, text="Date of Birth (YYYY-MM-DD):", font=ctk.CTkFont(size=14)).grid(
            row=4, column=0, sticky="w", padx=20, pady=10
        )
        self.dob_entry = ctk.CTkEntry(self.form_frame, width=300, placeholder_text="20050115")
        self.dob_entry.grid(row=4, column=1, padx=20, pady=10)
        self.dob_entry.bind('<KeyRelease>', self._format_dob)
        
        # Gender
        ctk.CTkLabel(self.form_frame, text="Gender:", font=ctk.CTkFont(size=14)).grid(
            row=5, column=0, sticky="w", padx=20, pady=10
        )
        self.gender_var = ctk.StringVar(value="Male")
        gender_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        gender_frame.grid(row=5, column=1, sticky="w", padx=20, pady=10)
        ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side="left", padx=10)
        ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side="left", padx=10)
        
        # Address
        ctk.CTkLabel(self.form_frame, text="Address:", font=ctk.CTkFont(size=14)).grid(
            row=6, column=0, sticky="w", padx=20, pady=10
        )
        self.address_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.address_entry.grid(row=6, column=1, padx=20, pady=10)
        
        # Guardian Name
        ctk.CTkLabel(self.form_frame, text="Guardian Name:", font=ctk.CTkFont(size=14)).grid(
            row=7, column=0, sticky="w", padx=20, pady=10
        )
        self.guardian_name_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.guardian_name_entry.grid(row=7, column=1, padx=20, pady=10)
        
        # Guardian NIC
        ctk.CTkLabel(self.form_frame, text="Guardian NIC:", font=ctk.CTkFont(size=14)).grid(
            row=8, column=0, sticky="w", padx=20, pady=10
        )
        self.guardian_nic_entry = ctk.CTkEntry(self.form_frame, width=300, placeholder_text="123456789V")
        self.guardian_nic_entry.grid(row=8, column=1, padx=20, pady=10)
        
        # Guardian Contact with digit limit
        ctk.CTkLabel(self.form_frame, text="Guardian Contact (10 digits):", font=ctk.CTkFont(size=14)).grid(
            row=9, column=0, sticky="w", padx=20, pady=10
        )
        self.guardian_contact_entry = ctk.CTkEntry(self.form_frame, width=300, placeholder_text="0771234567")
        self.guardian_contact_entry.grid(row=9, column=1, padx=20, pady=10)
        self.guardian_contact_entry.bind('<KeyRelease>', self._limit_contact_digits)
        
        # Error/Success message
        self.form_message = ctk.CTkLabel(self.form_frame, text="", font=ctk.CTkFont(size=12))
        self.form_message.grid(row=10, column=0, columnspan=2, pady=10)
        
        # Submit button
        ctk.CTkButton(
            self.form_frame,
            text="Register Student",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=45,
            command=self.submit_student
        ).grid(row=11, column=0, columnspan=2, pady=(20, 40))
    
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
        gender = self.gender_var.get()
        address = self.address_entry.get().strip()
        guardian_name = self.guardian_name_entry.get().strip()
        guardian_nic = self.guardian_nic_entry.get().strip()
        guardian_contact = self.guardian_contact_entry.get().strip()
        
        # Validate
        if not all([student_name, dob, address, guardian_name, guardian_nic, guardian_contact]):
            self.form_message.configure(text="All fields except image are required!", text_color="red")
            return
        
        if len(guardian_contact) != 10 or not guardian_contact.isdigit():
            self.form_message.configure(text="Guardian contact must be exactly 10 digits!", text_color="red")
            return
        
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            self.form_message.configure(text="Invalid date format! Use YYYY-MM-DD", text_color="red")
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
        student_data = (student_name, dob, gender, address, guardian_name, guardian_nic, guardian_contact, saved_image_path)
        success, result = self.db.add_student(student_data)
        
        if success:
            self.form_message.configure(text=f"Student registered successfully! ID: {result}", text_color="green")
            # Clear form
            self.student_name_entry.delete(0, 'end')
            self.dob_entry.delete(0, 'end')
            self.address_entry.delete(0, 'end')
            self.guardian_name_entry.delete(0, 'end')
            self.guardian_nic_entry.delete(0, 'end')
            self.guardian_contact_entry.delete(0, 'end')
            self.image_path = None
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
