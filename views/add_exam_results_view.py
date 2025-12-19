"""Add Exam Results view for Student Management System"""
import customtkinter as ctk
from datetime import datetime
from widgets import SearchWidget, FieldWithClearButton


class AddExamResultsView:
    """View for adding exam results with persistent fields"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        # Create main frame
        self.form_frame = ctk.CTkScrollableFrame(parent)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the exam results form"""
        # Title
        title = ctk.CTkLabel(
            self.form_frame,
            text="Add Exam Results",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=20)
        
        # Get students
        students = self.db.get_all_students()
        if not students:
            ctk.CTkLabel(
                self.form_frame,
                text="No students registered. Please add students first.",
                font=ctk.CTkFont(size=14)
            ).grid(row=1, column=0, columnspan=2, pady=50)
            return
        
        # Search frame for students
        search_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
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
        
        # Subject with clear button
        ctk.CTkLabel(self.form_frame, text="Subject:", font=ctk.CTkFont(size=14)).grid(
            row=2, column=0, sticky="w", padx=20, pady=10
        )
        self.subject_field = FieldWithClearButton(self.form_frame, placeholder="Mathematics", width=240)
        self.subject_field.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        
        # Exam Name with clear button
        ctk.CTkLabel(self.form_frame, text="Exam Name:", font=ctk.CTkFont(size=14)).grid(
            row=3, column=0, sticky="w", padx=20, pady=10
        )
        self.exam_name_field = FieldWithClearButton(self.form_frame, placeholder="Mid-term Exam", width=240)
        self.exam_name_field.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        
        # Exam Date with clear button
        ctk.CTkLabel(self.form_frame, text="Exam Date (YYYY-MM-DD):", font=ctk.CTkFont(size=14)).grid(
            row=4, column=0, sticky="w", padx=20, pady=10
        )
        self.exam_date_field = FieldWithClearButton(self.form_frame, placeholder="2025-12-19", width=240)
        self.exam_date_field.grid(row=4, column=1, padx=20, pady=10, sticky="w")
        
        # Total Marks with clear button
        ctk.CTkLabel(self.form_frame, text="Total Marks:", font=ctk.CTkFont(size=14)).grid(
            row=5, column=0, sticky="w", padx=20, pady=10
        )
        self.total_marks_field = FieldWithClearButton(self.form_frame, placeholder="100", width=240)
        self.total_marks_field.grid(row=5, column=1, padx=20, pady=10, sticky="w")
        
        # Separator
        separator = ctk.CTkFrame(self.form_frame, height=2, fg_color="gray")
        separator.grid(row=6, column=0, columnspan=2, sticky="ew", padx=20, pady=15)
        
        # === STUDENT-SPECIFIC FIELDS ===
        
        # Student Selection
        ctk.CTkLabel(self.form_frame, text="Select Student:", font=ctk.CTkFont(size=14)).grid(
            row=7, column=0, sticky="w", padx=20, pady=10
        )
        self.student_select = ctk.CTkOptionMenu(self.form_frame, values=student_options, width=300)
        self.student_select.grid(row=7, column=1, padx=20, pady=10)
        
        # Marks Obtained
        ctk.CTkLabel(self.form_frame, text="Marks Obtained:", font=ctk.CTkFont(size=14)).grid(
            row=8, column=0, sticky="w", padx=20, pady=10
        )
        self.marks_obtained_entry = ctk.CTkEntry(self.form_frame, width=300, placeholder_text="85")
        self.marks_obtained_entry.grid(row=8, column=1, padx=20, pady=10)
        
        # Grade
        ctk.CTkLabel(self.form_frame, text="Grade:", font=ctk.CTkFont(size=14)).grid(
            row=9, column=0, sticky="w", padx=20, pady=10
        )
        self.grade_entry = ctk.CTkEntry(self.form_frame, width=300, placeholder_text="A")
        self.grade_entry.grid(row=9, column=1, padx=20, pady=10)
        
        # Message label
        self.result_message = ctk.CTkLabel(self.form_frame, text="", font=ctk.CTkFont(size=12))
        self.result_message.grid(row=10, column=0, columnspan=2, pady=10)
        
        # Submit button
        ctk.CTkButton(
            self.form_frame,
            text="Add Result",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=45,
            command=self._submit_result
        ).grid(row=11, column=0, columnspan=2, pady=(20, 40))
    
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
    
    def _submit_result(self):
        """Handle exam result submission"""
        # Get student ID from selection
        selected = self.student_select.get()
        if not selected or selected == "No students found":
            self.result_message.configure(text="Please select a student!", text_color="red")
            return
        
        student_id = int(selected.split(" - ")[0])
        
        # Get form values
        subject = self.subject_field.get().strip()
        exam_name = self.exam_name_field.get().strip()
        exam_date = self.exam_date_field.get().strip()
        marks_obtained = self.marks_obtained_entry.get().strip()
        total_marks = self.total_marks_field.get().strip()
        grade = self.grade_entry.get().strip()
        
        # Validate
        if not all([subject, exam_name, exam_date, marks_obtained, total_marks]):
            self.result_message.configure(text="All fields except grade are required!", text_color="red")
            return
        
        try:
            marks_obtained = float(marks_obtained)
            total_marks = float(total_marks)
        except ValueError:
            self.result_message.configure(text="Marks must be numbers!", text_color="red")
            return
        
        # Validate date
        try:
            datetime.strptime(exam_date, "%Y-%m-%d")
        except ValueError:
            self.result_message.configure(text="Invalid date format! Use YYYY-MM-DD", text_color="red")
            return
        
        # Add to database
        result_data = (student_id, subject, exam_name, exam_date, marks_obtained, total_marks, grade)
        success, message = self.db.add_exam_result(result_data)
        
        if success:
            self.result_message.configure(text="Exam result added successfully! (Exam details kept for next entry)", text_color="green")
            # Clear only student-specific fields
            self.marks_obtained_entry.delete(0, 'end')
            self.grade_entry.delete(0, 'end')
        else:
            self.result_message.configure(text=f"Error: {message}", text_color="red")
