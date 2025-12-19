"""Student Profiles view for Student Management System"""
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog
import tkinter.messagebox as messagebox
from PIL import Image
import shutil
import os
from widgets import SearchWidget


class StudentProfilesView:
    """View for displaying, searching, editing, and deleting student profiles"""
    
    def __init__(self, parent, db, on_refresh=None):
        self.parent = parent
        self.db = db
        self.on_refresh = on_refresh
        
        # Create main frame
        self.profiles_frame = ctk.CTkFrame(parent)
        self.profiles_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_ui()
    
    def _create_ui(self, search_term=None):
        """Create the profiles UI"""
        # Clear existing widgets
        for widget in self.profiles_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_text = "Student Profiles - Search Results" if search_term else "Student Profiles"
        title = ctk.CTkLabel(
            self.profiles_frame,
            text=title_text,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(20, 10))
        
        # Search widget
        search_widget = SearchWidget(
            self.profiles_frame,
            placeholder="Enter student name...",
            on_search=self._perform_search,
            on_clear=self._clear_search
        )
        search_widget.pack(pady=10)
        
        if search_term:
            search_widget.set_search_term(search_term)
        
        # Scrollable frame for students
        scroll_frame = ctk.CTkScrollableFrame(self.profiles_frame, height=400)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get students
        students = self.db.search_students(search_term) if search_term else self.db.get_all_students()
        
        if not students:
            no_results_msg = f"No students found matching '{search_term}'." if search_term else "No students registered yet."
            ctk.CTkLabel(
                scroll_frame,
                text=no_results_msg,
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        # Header
        header_frame = ctk.CTkFrame(scroll_frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        headers = ["ID", "Name", "DOB", "Gender", "Guardian", "Guardian NIC"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=100
            ).grid(row=0, column=i, padx=5, pady=5)
        
        # Student rows
        for student in students:
            self._create_student_row(scroll_frame, student)
    
    def _create_student_row(self, parent, student):
        """Create a single student row with buttons"""
        student_frame = ctk.CTkFrame(parent)
        student_frame.pack(fill="x", padx=10, pady=2)
        
        values = [student[0], student[1], student[2], student[3], student[5], student[6]]
        for i, value in enumerate(values):
            ctk.CTkLabel(
                student_frame,
                text=str(value),
                font=ctk.CTkFont(size=11),
                width=100
            ).grid(row=0, column=i, padx=5, pady=5)
        
        # View button
        ctk.CTkButton(
            student_frame,
            text="View",
            width=60,
            command=lambda: self._show_student_details(student)
        ).grid(row=0, column=len(values), padx=5)
        
        # Edit button
        ctk.CTkButton(
            student_frame,
            text="Edit",
            width=60,
            fg_color="#FF8C00",
            hover_color="#FFA500",
            command=lambda: self._show_edit_form(student)
        ).grid(row=0, column=len(values)+1, padx=5)
        
        # Delete button
        ctk.CTkButton(
            student_frame,
            text="Delete",
            width=60,
            fg_color="#DC143C",
            hover_color="#B22222",
            command=lambda: self._confirm_delete(student)
        ).grid(row=0, column=len(values)+2, padx=5)
    
    def _perform_search(self, search_term):
        """Handle search"""
        self._create_ui(search_term)
    
    def _clear_search(self):
        """Clear search and show all students"""
        self._create_ui()
    
    def _show_student_details(self, student):
        """Show detailed view of a student"""
        detail_window = ctk.CTkToplevel(self.parent)
        detail_window.title(f"Student Details - {student[1]}")
        detail_window.geometry("550x700")
        detail_window.grab_set()
        detail_window.focus_force()
        
        # Center window
        detail_window.update_idletasks()
        x = (detail_window.winfo_screenwidth() // 2) - 275
        y = (detail_window.winfo_screenheight() // 2) - 350
        detail_window.geometry(f"550x700+{x}+{y}")
        
        # Content
        content = ctk.CTkScrollableFrame(detail_window)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content,
            text="Student Profile",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(10, 20))
        
        # Display image if available
        if student[8] and os.path.exists(student[8]):
            try:
                img = Image.open(student[8])
                img.thumbnail((150, 150))
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
                img_label = ctk.CTkLabel(content, image=photo, text="")
                img_label.image = photo
                img_label.pack(pady=10)
            except:
                pass
        
        # Display fields
        fields = [
            ("Student ID:", student[0]),
            ("Name:", student[1]),
            ("Date of Birth:", student[2]),
            ("Gender:", student[3]),
            ("Address:", student[4]),
            ("Guardian Name:", student[5]),
            ("Guardian NIC:", student[6]),
            ("Guardian Contact:", student[7]),
            ("Registered:", student[9] if len(student) > 9 else "N/A")
        ]
        
        for label, value in fields:
            frame = ctk.CTkFrame(content, fg_color="transparent")
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
        
        # Get exam results
        results = self.db.get_student_results(student[0])
        
        if results:
            ctk.CTkLabel(
                content,
                text="\nExam Results:",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(pady=(20, 10))
            
            for result in results:
                result_frame = ctk.CTkFrame(content)
                result_frame.pack(fill="x", pady=5, padx=10)
                
                ctk.CTkLabel(
                    result_frame,
                    text=f"{result[2]} - {result[3]} ({result[4]})\nMarks: {result[5]}/{result[6]} | Grade: {result[7] or 'N/A'}",
                    font=ctk.CTkFont(size=12),
                    justify="left"
                ).pack(padx=10, pady=10)
        
        ctk.CTkButton(
            content,
            text="Close",
            command=detail_window.destroy
        ).pack(pady=20)
    
    def _show_edit_form(self, student):
        """Show edit form for student"""
        edit_window = ctk.CTkToplevel(self.parent)
        edit_window.title(f"Edit Student - {student[1]}")
        edit_window.geometry("600x750")
        edit_window.grab_set()
        edit_window.focus_force()
        
        # Center window
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - 300
        y = (edit_window.winfo_screenheight() // 2) - 375
        edit_window.geometry(f"600x750+{x}+{y}")
        
        # Content
        content = ctk.CTkScrollableFrame(edit_window)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content,
            text="Edit Student Information",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(10, 20))
        
        # Image preview
        preview_label = ctk.CTkLabel(content, text="", width=150, height=150)
        preview_label.pack(pady=10)
        
        # Display current image
        current_image_path = student[8] if len(student) > 8 and student[8] else None
        if current_image_path and os.path.exists(current_image_path):
            try:
                img = Image.open(current_image_path)
                img.thumbnail((150, 150))
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
                preview_label.configure(image=photo, text="")
                preview_label.image = photo
            except:
                pass
        
        selected_image = [current_image_path]
        
        def choose_image():
            file_path = filedialog.askopenfilename(
                title="Select Student Image",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
            )
            if file_path:
                selected_image[0] = file_path
                try:
                    img = Image.open(file_path)
                    img.thumbnail((150, 150))
                    photo = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
                    preview_label.configure(image=photo, text="")
                    preview_label.image = photo
                except:
                    pass
        
        def cancel_image():
            selected_image[0] = None
            preview_label.configure(image="", text="")
            if hasattr(preview_label, 'image'):
                delattr(preview_label, 'image')
        
        # Image buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=5)
        
        ctk.CTkButton(btn_frame, text="Choose Image", width=130, command=choose_image).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel Image", width=130, fg_color="#8B0000", hover_color="#A52A2A", command=cancel_image).pack(side="left", padx=5)
        
        # Form fields
        form_frame = ctk.CTkFrame(content, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=10)
        
        # Create entries
        entries = {}
        fields_config = [
            ("Student Name:", student[1], 0),
            ("Date of Birth:", student[2], 1),
            ("Address:", student[4], 3),
            ("Guardian Name:", student[5], 4),
            ("Guardian NIC:", student[6], 5),
            ("Guardian Contact:", student[7], 6),
        ]
        
        for label, value, row in fields_config:
            ctk.CTkLabel(form_frame, text=label, font=ctk.CTkFont(size=14)).grid(row=row, column=0, sticky="w", padx=10, pady=10)
            entry = ctk.CTkEntry(form_frame, width=300)
            entry.insert(0, value)
            entry.grid(row=row, column=1, padx=10, pady=10)
            entries[label] = entry
        
        # Gender
        ctk.CTkLabel(form_frame, text="Gender:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        gender_var = ctk.StringVar(value=student[3])
        gender_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        gender_frame.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        ctk.CTkRadioButton(gender_frame, text="Male", variable=gender_var, value="Male").pack(side="left", padx=10)
        ctk.CTkRadioButton(gender_frame, text="Female", variable=gender_var, value="Female").pack(side="left", padx=10)
        
        # Message label
        message_label = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=12))
        message_label.pack(pady=10)
        
        # Update function
        def update_student():
            student_name = entries["Student Name:"].get().strip()
            dob = entries["Date of Birth:"].get().strip()
            gender = gender_var.get()
            address = entries["Address:"].get().strip()
            guardian_name = entries["Guardian Name:"].get().strip()
            guardian_nic = entries["Guardian NIC:"].get().strip()
            guardian_contact = entries["Guardian Contact:"].get().strip()
            
            # Validate
            if not all([student_name, dob, address, guardian_name, guardian_nic, guardian_contact]):
                message_label.configure(text="All fields except image are required!", text_color="red")
                return
            
            if len(guardian_contact) != 10 or not guardian_contact.isdigit():
                message_label.configure(text="Guardian contact must be exactly 10 digits!", text_color="red")
                return
            
            try:
                datetime.strptime(dob, "%Y-%m-%d")
            except ValueError:
                message_label.configure(text="Invalid date format! Use YYYY-MM-DD", text_color="red")
                return
            
            # Handle image
            saved_image_path = selected_image[0]
            if selected_image[0] and selected_image[0] != current_image_path:
                try:
                    if not os.path.exists("student_images"):
                        os.makedirs("student_images")
                    ext = os.path.splitext(selected_image[0])[1]
                    new_filename = f"{student_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
                    saved_image_path = os.path.join("student_images", new_filename)
                    shutil.copy2(selected_image[0], saved_image_path)
                except Exception as e:
                    message_label.configure(text=f"Error saving image: {e}", text_color="red")
                    return
            
            # Update database
            student_data = (student_name, dob, gender, address, guardian_name, guardian_nic, guardian_contact, saved_image_path)
            success, message = self.db.update_student(student[0], student_data)
            
            if success:
                message_label.configure(text="Student updated successfully!", text_color="green")
                edit_window.after(1000, edit_window.destroy)
                self._create_ui()  # Refresh the list
            else:
                message_label.configure(text=f"Error: {message}", text_color="red")
        
        # Buttons
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Update Student",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=150,
            height=40,
            command=update_student
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=16),
            width=150,
            height=40,
            fg_color="#666666",
            hover_color="#888888",
            command=edit_window.destroy
        ).pack(side="left", padx=10)
    
    def _confirm_delete(self, student):
        """Show confirmation dialog before deleting"""
        confirm_window = ctk.CTkToplevel(self.parent)
        confirm_window.title("Confirm Delete")
        confirm_window.geometry("450x280")
        confirm_window.grab_set()
        confirm_window.focus_force()
        
        # Center window
        confirm_window.update_idletasks()
        x = (confirm_window.winfo_screenwidth() // 2) - 225
        y = (confirm_window.winfo_screenheight() // 2) - 140
        confirm_window.geometry(f"450x280+{x}+{y}")
        
        # Content
        content = ctk.CTkFrame(confirm_window)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content,
            text="⚠️ Warning",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#DC143C"
        ).pack(pady=(10, 20))
        
        ctk.CTkLabel(
            content,
            text=f"Are you sure you want to delete\n{student[1]}?",
            font=ctk.CTkFont(size=14),
            justify="center"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            content,
            text="This will also delete all exam results.\nThis action cannot be undone!",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="center"
        ).pack(pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(pady=30)
        
        def delete_confirmed():
            success, message = self.db.delete_student(student[0])
            confirm_window.destroy()
            if success:
                # Delete image file if exists
                if len(student) > 8 and student[8] and os.path.exists(student[8]):
                    try:
                        os.remove(student[8])
                    except:
                        pass
                self._create_ui()  # Refresh the list
            else:
                messagebox.showerror("Error", f"Failed to delete student: {message}")
        
        ctk.CTkButton(
            button_frame,
            text="Yes, Delete",
            width=150,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#DC143C",
            hover_color="#B22222",
            command=delete_confirmed
        ).pack(side="left", padx=15)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=150,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#666666",
            hover_color="#888888",
            command=confirm_window.destroy
        ).pack(side="left", padx=15)
