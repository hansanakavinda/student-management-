"""Add Exam Results view for Student Management System"""
import customtkinter as ctk
from widgets import SearchWidget, FieldWithClearButton


class AddExamResultsView:
    """View for adding exam results with persistent fields"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        # Create main frame
        self.form_frame = ctk.CTkScrollableFrame(parent)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)

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
        ctk.CTkLabel(content, text="Exam Year:", font=ctk.CTkFont(size=14)).grid(
            row=3, column=0, sticky="w", padx=20, pady=10
        )
        self.exam_year_field = FieldWithClearButton(content, placeholder="2025", width=240)
        self.exam_year_field.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        
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
        ctk.CTkLabel(content, text="Marks Obtained:", font=ctk.CTkFont(size=14)).grid(
            row=6, column=0, sticky="w", padx=20, pady=10
        )
        self.marks_obtained_entry = ctk.CTkEntry(content, width=300, placeholder_text="85")
        self.marks_obtained_entry.grid(row=6, column=1, padx=20, pady=10)
        
        # Grade (Required)
        ctk.CTkLabel(content, text="Grade (Required):", font=ctk.CTkFont(size=14)).grid(
            row=7, column=0, sticky="w", padx=20, pady=10
        )
        self.grade_entry = ctk.CTkEntry(content, width=300, placeholder_text="A")
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
    
    def _submit_result(self):
        """Handle exam result submission"""
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
        if not all([exam_name, exam_year, marks_obtained, grade]):
            self.result_message.configure(text="All fields are required!", text_color="red")
            return
        
        # Validate marks
        try:
            marks_obtained = float(marks_obtained)
            if marks_obtained < 0:
                self.result_message.configure(text="Marks must be a positive number!", text_color="red")
                return
        except ValueError:
            self.result_message.configure(text="Marks must be a valid number!", text_color="red")
            return
        
        # Validate year
        try:
            exam_year = int(exam_year)
            if exam_year < 1900 or exam_year > 2100:
                self.result_message.configure(text="Please enter a valid year (1900-2100)!", text_color="red")
                return
        except ValueError:
            self.result_message.configure(text="Exam year must be a valid number!", text_color="red")
            return
        
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
