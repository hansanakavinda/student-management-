"""Student Profiles view for Student Management System"""
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog
import tkinter.messagebox as messagebox
from PIL import Image
import shutil
import os
from widgets import SearchWidget, EditDialog, ConfirmDeleteDialog


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
        
        # Make window resizable (allows maximize button)
        detail_window.resizable(True, True)
        detail_window.minsize(500, 600)
        
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
        
        # Get and display student notes
        notes = self.db.get_student_notes(student[0])
        
        # Notes section
        notes_frame = ctk.CTkFrame(content, fg_color="transparent")
        notes_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            notes_frame,
            text="Additional Notes:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        notes_display = ctk.CTkTextbox(
            notes_frame,
            height=80,
            font=ctk.CTkFont(size=12),
            wrap="word",
            state="disabled"
        )
        notes_display.pack(fill="x", padx=10, pady=5)
        
        if notes:
            notes_display.configure(state="normal")
            notes_display.insert("1.0", notes)
            notes_display.configure(state="disabled")
        
        # Buttons frame
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
            command=lambda: self._edit_student_notes(student, detail_window)
        ).pack(side="left", padx=10)
        
        # View Results button
        ctk.CTkButton(
            button_frame,
            text="View Exam Results",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180,
            height=40,
            command=lambda: self._show_exam_results(student)
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
            command=lambda: self._show_certificates(student)
        ).pack(side="left", padx=10)
        
        # Close button
        ctk.CTkButton(
            button_frame,
            text="Close",
            font=ctk.CTkFont(size=14),
            width=120,
            height=40,
            fg_color="#666666",
            hover_color="#888888",
            command=detail_window.destroy
        ).pack(side="left", padx=10)
    
    def _show_exam_results(self, student, filters=None):
        """Show exam results in a separate window"""
        if filters is None:
            filters = {}
        
        # Apply filters
        exam_name_filter = filters.get("exam_name")
        exam_year_filter = filters.get("exam_year")
        
        # Get all results for student
        all_results = self.db.get_student_results(student[0])
        
        # Filter results
        results = all_results
        if exam_name_filter:
            results = [r for r in results if r[2] == exam_name_filter]
        if exam_year_filter:
            results = [r for r in results if str(r[3]) == str(exam_year_filter)]
        
        # Create results window
        results_window = ctk.CTkToplevel(self.parent)
        results_window.title(f"Exam Results - {student[1]}")
        results_window.geometry("600x600")
        
        # Make window resizable (allows maximize button)
        results_window.resizable(True, True)
        results_window.minsize(500, 400)
        
        results_window.grab_set()
        results_window.focus_force()
        
        # Center window
        results_window.update_idletasks()
        x = (results_window.winfo_screenwidth() // 2) - 300
        y = (results_window.winfo_screenheight() // 2) - 300
        results_window.geometry(f"600x600+{x}+{y}")
        
        # Content
        content = ctk.CTkFrame(results_window)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            content,
            text=f"Exam Results for {student[1]}",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 10))
        
        # Filter frame
        filter_frame = ctk.CTkFrame(content)
        filter_frame.pack(pady=10, fill="x")
        
        # Exam Name Dropdown
        ctk.CTkLabel(
            filter_frame,
            text="Exam Name:",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        exam_options = ["All", "First Term", "Second Term", "Third Term"]
        exam_name_dropdown = ctk.CTkOptionMenu(
            filter_frame,
            values=exam_options,
            width=150
        )
        current_exam = filters.get("exam_name") or "All"
        exam_name_dropdown.set(current_exam)
        exam_name_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Exam Year Dropdown
        ctk.CTkLabel(
            filter_frame,
            text="Exam Year:",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        # Get unique years from student's results
        unique_years = ["All"] + sorted(list(set([str(r[3]) for r in all_results])), reverse=True)
        exam_year_dropdown = ctk.CTkOptionMenu(
            filter_frame,
            values=unique_years if len(unique_years) > 1 else ["All"],
            width=120
        )
        current_year = filters.get("exam_year") or "All"
        exam_year_dropdown.set(current_year)
        exam_year_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        def apply_filters():
            exam_name = exam_name_dropdown.get()
            exam_year = exam_year_dropdown.get()
            new_filters = {
                "exam_name": None if exam_name == "All" else exam_name,
                "exam_year": None if exam_year == "All" else exam_year
            }
            results_window.destroy()
            self._show_exam_results(student, new_filters)
        
        def clear_filters():
            results_window.destroy()
            self._show_exam_results(student, {})
        
        # Buttons
        button_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=4, pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 Apply Filters",
            width=120,
            command=apply_filters
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Clear Filters",
            width=110,
            fg_color="#666666",
            hover_color="#888888",
            command=clear_filters
        ).pack(side="left", padx=5)
        
        if not results:
            ctk.CTkLabel(
                content,
                text="No exam results found for this student.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
        else:
            # Scrollable frame for results
            scroll_frame = ctk.CTkScrollableFrame(content)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Table container
            table_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            table_frame.pack(fill="x", padx=5, pady=5)
            
            # Table headers
            header_frame = ctk.CTkFrame(table_frame)
            header_frame.pack(fill="x", padx=5, pady=5)
            
            headers = ["Exam", "Year", "Marks", "Grade"]
            widths = [150, 100, 100, 80]
            
            for i, (header, width) in enumerate(zip(headers, widths)):
                ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    width=width,
                    anchor="center"
                ).grid(row=0, column=i, padx=3, pady=5, sticky="ew")
            
            # Table rows
            for result in results:
                row_frame = ctk.CTkFrame(table_frame, fg_color="#2b2b2b")
                row_frame.pack(fill="x", padx=5, pady=2)
                
                values = [
                    result[2],  # Exam name
                    result[3],  # Exam year
                    result[4],  # Marks obtained
                    result[5]   # Grade
                ]
                
                for i, (value, width) in enumerate(zip(values, widths)):
                    ctk.CTkLabel(
                        row_frame,
                        text=str(value),
                        font=ctk.CTkFont(size=11),
                        width=width,
                        anchor="center"
                    ).grid(row=0, column=i, padx=3, pady=8, sticky="ew")
        
        # Close button
        ctk.CTkButton(
            content,
            text="Close",
            width=150,
            command=results_window.destroy
        ).pack(pady=15)
    
    def _edit_student_notes(self, student, detail_window):
        """Show dialog to edit student notes"""
        # Create notes dialog
        notes_window = ctk.CTkToplevel(self.parent)
        notes_window.title(f"Edit Notes - {student[1]}")
        notes_window.geometry("600x450")
        notes_window.transient(self.parent)
        notes_window.grab_set()
        
        # Center window
        notes_window.update_idletasks()
        x = (notes_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (notes_window.winfo_screenheight() // 2) - (450 // 2)
        notes_window.geometry(f"+{x}+{y}")
        
        # Main container
        main_frame = ctk.CTkFrame(notes_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            main_frame,
            text=f"Additional Notes for {student[1]}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(0, 20))
        
        # Notes text area
        notes_textbox = ctk.CTkTextbox(
            main_frame,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        notes_textbox.pack(fill="both", expand=True, pady=10)
        
        # Load existing notes
        current_notes = self.db.get_student_notes(student[0])
        if current_notes:
            notes_textbox.insert("1.0", current_notes)
        
        # Character count label
        char_label = ctk.CTkLabel(
            main_frame,
            text=f"Characters: {len(current_notes)}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        char_label.pack(pady=(5, 10))
        
        def update_char_count(event=None):
            """Update character count"""
            text = notes_textbox.get("1.0", "end-1c")
            char_label.configure(text=f"Characters: {len(text)}")
        
        notes_textbox.bind("<KeyRelease>", update_char_count)
        
        # Status label
        status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        status_label.pack(pady=5)
        
        def save_notes():
            """Save notes to database"""
            notes_text = notes_textbox.get("1.0", "end-1c").strip()
            success, message = self.db.save_student_notes(student[0], notes_text)
            
            if success:
                status_label.configure(text="✓ Notes saved successfully", text_color="green")
                # Refresh the detail window to show updated notes
                detail_window.destroy()
                self._show_student_details(student)
                notes_window.after(1000, notes_window.destroy)
            else:
                status_label.configure(text=f"Error: {message}", text_color="red")
        
        # Button frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Save Notes",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=140,
            height=40,
            fg_color="#2b7a0b",
            hover_color="#3a9b1a",
            command=save_notes
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=14),
            width=140,
            height=40,
            fg_color="#666666",
            hover_color="#888888",
            command=notes_window.destroy
        ).pack(side="left", padx=10)
    
    def _show_certificates(self, student):
        """Show student certificates in a gallery view"""
        # Create certificates window
        certificates_window = ctk.CTkToplevel(self.parent)
        certificates_window.title(f"Certificates - {student[1]}")
        certificates_window.geometry("900x700")
        
        # Make window resizable (allows maximize button)
        certificates_window.resizable(True, True)
        certificates_window.minsize(600, 400)
        
        certificates_window.grab_set()
        certificates_window.focus_force()
        
        # Center window
        certificates_window.update_idletasks()
        x = (certificates_window.winfo_screenwidth() // 2) - (900 // 2)
        y = (certificates_window.winfo_screenheight() // 2) - (700 // 2)
        certificates_window.geometry(f"+{x}+{y}")
        
        # Content frame (matching exam results structure)
        content = ctk.CTkFrame(certificates_window)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            content,
            text=f"Certificates for {student[1]}",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 10))
        
        # Get certificates for this student
        certificates = self.db.get_certificates_by_student(student[0])
        
        if not certificates:
            ctk.CTkLabel(
                content,
                text="No certificates found for this student.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
        else:
            # Scrollable frame for gallery
            scroll_frame = ctk.CTkScrollableFrame(content)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Gallery container with grid layout
            gallery_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            gallery_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Display certificates in grid (2 columns)
            for idx, cert in enumerate(certificates):
                cert_id, student_id, image_path, note, created_at, student_name = cert
                
                # Calculate row and column
                row = idx // 2
                col = idx % 2
                
                # Certificate card
                card = ctk.CTkFrame(gallery_frame, fg_color="#2b2b2b", corner_radius=10)
                card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
                
                # Configure grid weights for responsive layout
                gallery_frame.grid_columnconfigure(0, weight=1)
                gallery_frame.grid_columnconfigure(1, weight=1)
                
                # Image container
                image_container = ctk.CTkFrame(card, fg_color="#1a1a1a", corner_radius=8)
                image_container.pack(padx=10, pady=10, fill="both", expand=True)
                
                # Display certificate image
                if image_path and os.path.exists(image_path):
                    try:
                        # Load and display image
                        if image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                            img = Image.open(image_path)
                            img.thumbnail((350, 300))
                            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(350, 300))
                            img_label = ctk.CTkLabel(
                                image_container,
                                image=photo,
                                text=""
                            )
                            img_label.image = photo
                            img_label.pack(pady=10)
                        else:
                            # For PDF or other files
                            ctk.CTkLabel(
                                image_container,
                                text=f"📄 {os.path.basename(image_path)}",
                                font=ctk.CTkFont(size=14)
                            ).pack(pady=50)
                    except Exception as e:
                        ctk.CTkLabel(
                            image_container,
                            text=f"❌ Error loading image",
                            font=ctk.CTkFont(size=12),
                            text_color="red"
                        ).pack(pady=50)
                else:
                    ctk.CTkLabel(
                        image_container,
                        text="❌ Image not found",
                        font=ctk.CTkFont(size=12),
                        text_color="red"
                    ).pack(pady=50)
                
                # Note section
                note_frame = ctk.CTkFrame(card, fg_color="transparent")
                note_frame.pack(fill="x", padx=10, pady=(0, 10))
                
                # Date label
                ctk.CTkLabel(
                    note_frame,
                    text=f"Added: {created_at[:10]}",
                    font=ctk.CTkFont(size=11),
                    text_color="gray"
                ).pack(anchor="w", pady=(5, 5))
                
                # Note content
                if note:
                    ctk.CTkLabel(
                        note_frame,
                        text="Note:",
                        font=ctk.CTkFont(size=12, weight="bold")
                    ).pack(anchor="w", pady=(5, 2))
                    
                    note_textbox = ctk.CTkTextbox(
                        note_frame,
                        height=60,
                        font=ctk.CTkFont(size=11),
                        wrap="word",
                        state="disabled"
                    )
                    note_textbox.pack(fill="x", pady=2)
                    note_textbox.configure(state="normal")
                    note_textbox.insert("1.0", note)
                    note_textbox.configure(state="disabled")
                else:
                    ctk.CTkLabel(
                        note_frame,
                        text="No note added",
                        font=ctk.CTkFont(size=11),
                        text_color="gray"
                    ).pack(anchor="w", pady=5)
                
                # Delete button
                ctk.CTkButton(
                    card,
                    text="🗑 Delete",
                    font=ctk.CTkFont(size=12),
                    width=100,
                    height=30,
                    fg_color="#e74c3c",
                    hover_color="#c0392b",
                    command=lambda cid=cert_id: self._delete_certificate(cid, student, certificates_window)
                ).pack(pady=(0, 10))
        
        # Close button (matching exam results structure)
        ctk.CTkButton(
            content,
            text="Close",
            width=150,
            command=certificates_window.destroy
        ).pack(pady=15)
    
    def _delete_certificate(self, cert_id, student, certificates_window):
        """Delete a certificate after confirmation"""
        from widgets import ConfirmDeleteDialog
        
        def delete_confirmed():
            """Execute deletion after confirmation"""
            success, message = self.db.delete_certificate(cert_id)
            if success:
                # Refresh the certificates window
                certificates_window.destroy()
                self._show_certificates(student)
            else:
                messagebox.showerror("Error", f"Failed to delete certificate: {message}")
        
        # Show confirmation dialog
        ConfirmDeleteDialog(
            self.parent,
            title="Confirm Delete",
            main_message="Are you sure you want to delete\nthis certificate?",
            warning_message="This action cannot be undone!",
            on_confirm=delete_confirmed
        )
    
    def _show_edit_form(self, student):
        """Show edit form for student"""
        # Create edit dialog using reusable component
        edit_window = EditDialog(
            self.parent,
            title=f"Edit Student - {student[1]}",
            width=600,
            height=750
        )
        
        # Add title
        edit_window.add_title("Edit Student Information")
        
        # Get content frame
        content = edit_window.content
        
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
        
        # Add standard button frame
        edit_window.add_button_frame(update_student, save_text="Update Student")
    
    def _confirm_delete(self, student):
        """Show confirmation dialog before deleting"""
        def delete_confirmed():
            """Execute deletion after confirmation"""
            success, message = self.db.delete_student(student[0])
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
        
        # Show custom confirmation dialog
        ConfirmDeleteDialog(
            self.parent,
            title="Confirm Delete",
            main_message=f"Are you sure you want to delete\n{student[1]}?",
            warning_message="This will also delete all exam results.\nThis action cannot be undone!",
            on_confirm=delete_confirmed
        )
