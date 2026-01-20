"""Add Exam Results view for Student Management System"""
import customtkinter as ctk
from widgets import SearchWidget, FieldWithClearButton
from validators import Validators
from formatters import Formatters


class AddExamResultsView:
    """View for adding exam results with persistent fields"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.error_labels = {}  # Store error label widgets
        
        # Create main frame
        self.form_frame = ctk.CTkScrollableFrame(parent)
        self.form_frame.pack(fill="both", expand=True)

        # Create centered container within the scrollable content
        centered_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        centered_container.pack(expand=True, pady=20)
        
        self._create_ui(centered_container)
    
    def _create_ui(self, content):
        """Create the exam results form"""
        # Title
        title = ctk.CTkLabel(
            content,
            text="Add Exam Results",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=20)
        
        # Get students
        students = self.db.get_all_students()
        if not students:
            ctk.CTkLabel(
                content,
                text="No students registered. Please add students first.",
                font=ctk.CTkFont(size=14)
            ).grid(row=1, column=0, columnspan=2, pady=50)
            return
        
        # Search frame for students
        search_frame = ctk.CTkFrame(content, fg_color="transparent")
        search_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ctk.CTkLabel(search_frame, text="Search Student:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)
        self.exam_search_entry = ctk.CTkEntry(search_frame, width=200, placeholder_text="Enter student name...")
        self.exam_search_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            search_frame,
            text="Search",
            width=80,
            command=lambda: self._filter_students(students)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            search_frame,
            text="Clear",
            width=80,
            fg_color="#666666",
            hover_color="#888888",
            command=lambda: self._clear_search(students)
        ).pack(side="left", padx=5)
        
        self.all_students = students
        student_options = [f"{s[0]} - {s[1]}" for s in students]
        
        # === PERSISTENT FIELDS AT TOP ===
        
        # Exam Name dropdown
        ctk.CTkLabel(content, text="Exam Name:", font=ctk.CTkFont(size=14)).grid(
            row=2, column=0, sticky="w", padx=20, pady=10
        )
        exam_options = ["First Term", "Second Term", "Third Term"]
        self.exam_name_field = ctk.CTkOptionMenu(content, values=exam_options, width=300)
        self.exam_name_field.set("First Term")
        self.exam_name_field.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        
        # Exam Year with clear button
        ctk.CTkLabel(content, text="Exam Year (4 digits):", font=ctk.CTkFont(size=14)).grid(
            row=3, column=0, sticky="w", padx=20, pady=10
        )
        self.exam_year_field = FieldWithClearButton(content, placeholder="2025", width=240)
        self.exam_year_field.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        Formatters.apply_year_formatting(self.exam_year_field.entry)
        self.error_labels['exam_year'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['exam_year'].grid(row=3, column=1, sticky="w", padx=20, pady=(60, 0))
        
        # Separator
        separator = ctk.CTkFrame(content, height=2, fg_color="gray")
        separator.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=15)
        
        # === STUDENT-SPECIFIC FIELDS ===
        
        # Student Selection
        ctk.CTkLabel(content, text="Select Student:", font=ctk.CTkFont(size=14)).grid(
            row=5, column=0, sticky="w", padx=20, pady=10
        )
        self.student_select = ctk.CTkOptionMenu(content, values=student_options, width=300)
        self.student_select.grid(row=5, column=1, padx=20, pady=10)
        
        # Marks Obtained
        ctk.CTkLabel(content, text="Marks Obtained (0-100):", font=ctk.CTkFont(size=14)).grid(
            row=6, column=0, sticky="w", padx=20, pady=10
        )
        self.marks_obtained_entry = ctk.CTkEntry(content, width=300, placeholder_text="85")
        self.marks_obtained_entry.grid(row=6, column=1, padx=20, pady=10)
        Formatters.apply_marks_formatting(self.marks_obtained_entry)
        # Bind to auto-calculate grade when marks change
        self.marks_obtained_entry.bind('<KeyRelease>', self._auto_calculate_grade)
        self.error_labels['marks'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=10), text_color="red")
        self.error_labels['marks'].grid(row=6, column=1, sticky="w", padx=20, pady=(60, 0))
        
        # Grade (Auto-calculated)
        ctk.CTkLabel(content, text="Grade (Auto-calculated):", font=ctk.CTkFont(size=14)).grid(
            row=7, column=0, sticky="w", padx=20, pady=10
        )
        self.grade_entry = ctk.CTkEntry(content, width=300, placeholder_text="A", state="readonly")
        self.grade_entry.grid(row=7, column=1, padx=20, pady=10)
        
        # Message label
        self.result_message = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=12))
        self.result_message.grid(row=8, column=0, columnspan=2, pady=10)
        
        # Submit button
        ctk.CTkButton(
            content,
            text="Add Result",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=45,
            command=self._submit_result
        ).grid(row=9, column=0, columnspan=2, pady=(20, 40))
    
    def _filter_students(self, all_students):
        """Filter students based on search"""
        search_term = self.exam_search_entry.get().strip()
        if search_term:
            filtered_students = self.db.search_students(search_term)
        else:
            filtered_students = all_students
        
        if filtered_students:
            student_options = [f"{s[0]} - {s[1]}" for s in filtered_students]
            self.student_select.configure(values=student_options)
            self.student_select.set(student_options[0])
        else:
            self.student_select.configure(values=["No students found"])
    
    def _clear_search(self, all_students):
        """Clear search and reset dropdown"""
        self.exam_search_entry.delete(0, 'end')
        student_options = [f"{s[0]} - {s[1]}" for s in all_students]
        self.student_select.configure(values=student_options)
        if student_options:
            self.student_select.set(student_options[0])
    
    def _auto_calculate_grade(self, event=None):
        """Auto-calculate grade based on marks"""
        marks_text = self.marks_obtained_entry.get().strip()
        if marks_text:
            grade = Validators.calculate_grade(marks_text)
            if grade:
                # Temporarily enable to update value
                self.grade_entry.configure(state="normal")
                self.grade_entry.delete(0, 'end')
                self.grade_entry.insert(0, grade)
                self.grade_entry.configure(state="readonly")
        else:
            self.grade_entry.configure(state="normal")
            self.grade_entry.delete(0, 'end')
            self.grade_entry.configure(state="readonly")
    
    def _clear_all_errors(self):
        """Clear all error messages"""
        for error_label in self.error_labels.values():
            error_label.configure(text="")
    
    def _submit_result(self):
        """Handle exam result submission"""
        # Clear previous errors
        self._clear_all_errors()
        self.result_message.configure(text="")
        
        # Get student ID from selection
        selected = self.student_select.get()
        if not selected or selected == "No students found":
            self.result_message.configure(text="Please select a student!", text_color="red")
            return
        
        student_id = int(selected.split(" - ")[0])
        
        # Get form values
        exam_name = self.exam_name_field.get().strip()
        exam_year = self.exam_year_field.get().strip()
        marks_obtained = self.marks_obtained_entry.get().strip()
        grade = self.grade_entry.get().strip()
        
        # Validate all required fields
        has_error = False
        
        # Validate exam year
        result = Validators.validate_exam_year(exam_year)
        if not result.is_valid:
            self.error_labels['exam_year'].configure(text=result.error_message)
            has_error = True
        
        # Validate marks
        result = Validators.validate_marks_obtained(marks_obtained)
        if not result.is_valid:
            self.error_labels['marks'].configure(text=result.error_message)
            has_error = True
        
        # Check if grade is present (should be auto-calculated)
        if not grade:
            self.result_message.configure(text="Grade cannot be empty. Please enter valid marks.", text_color="red")
            has_error = True
        
        if has_error:
            self.result_message.configure(text="Please fix the errors above", text_color="red")
            return
        
        # Convert to proper types
        exam_year = int(exam_year)
        marks_obtained = float(marks_obtained)
        
        # Add to database
        result_data = (student_id, exam_name, exam_year, marks_obtained, grade)
        success, message = self.db.add_exam_result(result_data)
        
        if success:
            self.result_message.configure(text="Exam result added successfully! (Exam details kept for next entry)", text_color="green")
            # Clear only student-specific fields
            self.marks_obtained_entry.delete(0, 'end')
            self.grade_entry.delete(0, 'end')
        else:
            self.result_message.configure(text=f"Error: {message}", text_color="red")
