"""View Exam Results view for Student Management System"""
import customtkinter as ctk
import tkinter.messagebox as messagebox
from widgets import FilterWidget, EditDialog, ConfirmDeleteDialog, create_label_with_tooltip


class ViewExamResultsView:
    """View for displaying exam results with filtering options and pagination"""
    
    def __init__(self, parent, db, items_per_page=20):
        self.parent = parent
        self.db = db
        self.filters = {}
        
        # Pagination settings
        self.items_per_page = items_per_page
        self.current_page = 1
        self.total_pages = 1
        
        # Create main frame
        self.results_frame = ctk.CTkFrame(parent)
        self.results_frame.pack(fill="both", expand=True)
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the results view UI"""
        # Clear existing widgets
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Title
        title = ctk.CTkLabel(
            self.results_frame,
            text="Exam Results",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(20, 10))
        
        # Custom filter frame
        filter_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        filter_frame.pack(pady=10, padx=20, fill="x")
        
        # Create centered container for filter elements
        filter_container = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_container.pack(expand=True, pady=10)
        
        # Row 1: Student Name
        ctk.CTkLabel(
            filter_container,
            text="Student Name:",
            font=ctk.CTkFont(size=13)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.student_name_entry = ctk.CTkEntry(
            filter_container,
            width=180,
            placeholder_text="Enter student name..."
        )
        self.student_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Restore student name if it exists in filters
        if self.filters.get("student_name"):
            self.student_name_entry.insert(0, self.filters["student_name"])
        
        # Row 1: Exam Name Dropdown
        ctk.CTkLabel(
            filter_container,
            text="Exam Name:",
            font=ctk.CTkFont(size=13)
        ).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        
        exam_options = ["All", "First Term", "Second Term", "Third Term"]
        self.exam_name_dropdown = ctk.CTkOptionMenu(
            filter_container,
            values=exam_options,
            width=180
        )
        # Restore exam name selection
        current_exam = self.filters.get("exam_name") or "All"
        self.exam_name_dropdown.set(current_exam)
        self.exam_name_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Row 2: Exam Year Dropdown
        ctk.CTkLabel(
            filter_container,
            text="Exam Year:",
            font=ctk.CTkFont(size=13)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        # Get unique years from database
        all_results = self.db.get_all_exam_results()
        unique_years = ["All"] + sorted(list(set([str(r[4]) for r in all_results])), reverse=True)
        
        self.exam_year_dropdown = ctk.CTkOptionMenu(
            filter_container,
            values=unique_years if len(unique_years) > 1 else ["All", "2025"],
            width=180
        )
        # Restore year selection
        current_year = self.filters.get("exam_year") or "All"
        self.exam_year_dropdown.set(current_year)
        self.exam_year_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(filter_container, fg_color="transparent")
        button_frame.grid(row=1, column=2, columnspan=2, pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 Apply Filters",
            width=130,
            command=self._apply_filters_from_controls
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Clear Filters",
            width=120,
            fg_color="#666666",
            hover_color="#888888",
            command=self._clear_filters
        ).pack(side="left", padx=5)
        
        # Get all filtered results (for pagination calculation)
        student_name = self.filters.get("student_name")
        exam_name = self.filters.get("exam_name")
        exam_year = self.filters.get("exam_year")
        
        all_results = self.db.get_all_exam_results(student_name, exam_name, exam_year)
        
        if not all_results:
            no_results_msg = "No results match your filters." if any(self.filters.values()) else "No exam results found."
            no_results_label = ctk.CTkLabel(
                self.results_frame,
                text=no_results_msg,
                font=ctk.CTkFont(size=14)
            )
            no_results_label.pack(pady=50)
            return
        
        # Calculate pagination
        total_results = len(all_results)
        self.total_pages = (total_results + self.items_per_page - 1) // self.items_per_page
        
        # Ensure current page is valid
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        if self.current_page < 1:
            self.current_page = 1
        
        # Get results for current page
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        results = all_results[start_idx:end_idx]
        
        # Info bar (showing results and pagination info)
        info_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=(10, 5))
        
        info_text = f"Showing {start_idx + 1}-{min(end_idx, total_results)} of {total_results} results"
        if self.total_pages > 1:
            info_text += f" | Page {self.current_page} of {self.total_pages}"
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(side="left")
        
        # Items per page selector
        if total_results > 10:
            ctk.CTkLabel(
                info_frame,
                text="Items per page:",
                font=ctk.CTkFont(size=12)
            ).pack(side="right", padx=(20, 5))
            
            items_options = ["10", "20", "50", "100", "All"]
            items_dropdown = ctk.CTkOptionMenu(
                info_frame,
                values=items_options,
                width=80,
                command=self._change_items_per_page
            )
            items_dropdown.set(str(self.items_per_page) if self.items_per_page < 1000 else "All")
            items_dropdown.pack(side="right")
        
        # Results display area
        scroll_frame = ctk.CTkScrollableFrame(self.results_frame, height=350, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(5, 10))
        
        # Header
        header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)
        
        headers = ["ID", "Student", "Exam", "Year", "Marks", "Grade"]
        widths = [50, 200, 120, 80, 100, 70, 150]  # Last width for action buttons
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width,
                anchor="w"
            ).grid(row=0, column=i, padx=5, pady=5)
        
        # Result rows (only current page)
        for result in results:
            self._create_result_row(scroll_frame, result, widths)
        
        # Pagination controls (only show if more than one page)
        if self.total_pages > 1:
            self._create_pagination_controls()
    
    def _create_result_row(self, parent, result, widths):
        """Create a single result row with truncated text and tooltips"""
        result_frame = ctk.CTkFrame(parent, fg_color="#363535")
        result_frame.pack(fill="x", padx=10, pady=2)
        
        values = [
            result[0],  # ID
            result[2],  # Student name
            result[3],  # Exam name
            result[4],  # Exam year
            result[5],  # Marks obtained
            result[6].upper()   # Grade
        ]
        
        # Max lengths for truncation: ID (8), Student (30), Exam (15), Year (8), Marks (12), Grade (8)
        max_lengths = [8, 30, 15, 8, 12, 8]
        
        for i, (value, width, max_len) in enumerate(zip(values, widths[:-1], max_lengths)):
            label = create_label_with_tooltip(
                result_frame,
                str(value),
                max_length=max_len,
                font=ctk.CTkFont(size=11),
                width=width,
                anchor="w",
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # Action buttons frame
        action_frame = ctk.CTkFrame(result_frame, fg_color="transparent")
        action_frame.grid(row=0, column=len(values), padx=5, pady=5)
        
        # Edit button
        ctk.CTkButton(
            action_frame,
            text="Edit",
            width=60,
            fg_color="#FF8C00",
            hover_color="#FFA500",
            command=lambda: self._edit_result(result[0])
        ).pack(side="left", padx=2)
        
        # Delete button
        ctk.CTkButton(
            action_frame,
            text="Delete",
            width=60,
            fg_color="#DC143C",
            hover_color="#B22222",
            command=lambda: self._delete_result(result[0])
        ).pack(side="left", padx=2)
    
    def _create_pagination_controls(self):
        """Create pagination navigation controls"""
        pagination_frame = ctk.CTkFrame(self.results_frame)
        pagination_frame.pack(fill="x", padx=20, pady=10)
        
        # Center the controls
        controls_container = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        controls_container.pack(expand=True)
        
        # First page button
        first_btn = ctk.CTkButton(
            controls_container,
            text="⏮ First",
            width=80,
            command=self._go_to_first_page,
            state="normal" if self.current_page > 1 else "disabled"
        )
        first_btn.pack(side="left", padx=2)
        
        # Previous page button
        prev_btn = ctk.CTkButton(
            controls_container,
            text="◀ Previous",
            width=90,
            command=self._go_to_previous_page,
            state="normal" if self.current_page > 1 else "disabled"
        )
        prev_btn.pack(side="left", padx=2)
        
        # Page indicator
        page_label = ctk.CTkLabel(
            controls_container,
            text=f"Page {self.current_page} of {self.total_pages}",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=120
        )
        page_label.pack(side="left", padx=10)
        
        # Next page button
        next_btn = ctk.CTkButton(
            controls_container,
            text="Next ▶",
            width=90,
            command=self._go_to_next_page,
            state="normal" if self.current_page < self.total_pages else "disabled"
        )
        next_btn.pack(side="left", padx=2)
        
        # Last page button
        last_btn = ctk.CTkButton(
            controls_container,
            text="Last ⏭",
            width=80,
            command=self._go_to_last_page,
            state="normal" if self.current_page < self.total_pages else "disabled"
        )
        last_btn.pack(side="left", padx=2)
        
        # Quick jump to page
        if self.total_pages > 5:
            ctk.CTkLabel(
                controls_container,
                text="Go to:",
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=(15, 5))
            
            page_entry = ctk.CTkEntry(controls_container, width=50)
            page_entry.pack(side="left", padx=2)
            page_entry.bind("<Return>", lambda e: self._jump_to_page(page_entry.get()))
            
            jump_btn = ctk.CTkButton(
                controls_container,
                text="Go",
                width=50,
                command=lambda: self._jump_to_page(page_entry.get())
            )
            jump_btn.pack(side="left", padx=2)
    
    def _go_to_first_page(self):
        """Navigate to first page"""
        self.current_page = 1
        self._create_ui()
    
    def _go_to_previous_page(self):
        """Navigate to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self._create_ui()
    
    def _go_to_next_page(self):
        """Navigate to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._create_ui()
    
    def _go_to_last_page(self):
        """Navigate to last page"""
        self.current_page = self.total_pages
        self._create_ui()
    
    def _jump_to_page(self, page_str):
        """Jump to specific page number"""
        try:
            page = int(page_str)
            if 1 <= page <= self.total_pages:
                self.current_page = page
                self._create_ui()
        except ValueError:
            pass  # Invalid input, ignore
    
    def _change_items_per_page(self, value):
        """Change number of items displayed per page"""
        if value == "All":
            self.items_per_page = 999999  # Very large number
        else:
            self.items_per_page = int(value)
        
        self.current_page = 1  # Reset to first page
        self._create_ui()
    
    def _apply_filters_from_controls(self):
        """Apply filters from the control values and reset to first page"""
        student_name = self.student_name_entry.get().strip() or None
        exam_name = self.exam_name_dropdown.get()
        exam_name = None if exam_name == "All" else exam_name
        exam_year = self.exam_year_dropdown.get()
        exam_year = None if exam_year == "All" else exam_year
        
        self.filters = {
            "student_name": student_name,
            "exam_name": exam_name,
            "exam_year": exam_year
        }
        self.current_page = 1  # Reset to first page when filters change
        self._create_ui()
    
    def _apply_filters(self, filter_values):
        """Apply filters and refresh results"""
        # Validate year if provided
        exam_year = filter_values.get("Exam Year:")
        if exam_year:
            try:
                year_val = int(exam_year)
                if year_val < 1900 or year_val > 2100:
                    messagebox.showerror("Invalid Year", "Please enter a valid year (1900-2100)")
                    return
            except ValueError:
                messagebox.showerror("Invalid Year", "Please enter a valid year")
                return
        
        self.filters = filter_values
        self._create_ui()
    
    def _clear_filters(self):
        """Clear all filters and show all results, reset to first page"""
        self.filters = {}
        self.current_page = 1  # Reset to first page when clearing filters
        self._create_ui()
    
    def _edit_result(self, result_id):
        """Edit exam result"""
        result = self.db.get_exam_result_by_id(result_id)
        if not result:
            messagebox.showerror("Error", "Result not found")
            return
        
        # Create edit dialog using reusable component
        dialog = EditDialog(
            self.parent,
            title=f"Edit Exam Result - {result[2]}",
            width=600,
            height=650
        )
        
        # Add title
        dialog.add_title("Edit Exam Result")
        
        # Add form frame
        form_frame = dialog.add_form_frame()

        # Create centered container within the scrollable content
        centered_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        centered_container.pack(expand=True, pady=20)
        
        # Student (read-only)
        ctk.CTkLabel(centered_container, text="Student:", font=ctk.CTkFont(size=12)).grid(
            row=0, column=0, sticky="w", padx=20, pady=10
        )
        student_label = ctk.CTkLabel(
            centered_container,
            text=result[2],
            font=ctk.CTkFont(size=12, weight="bold")
        )
        student_label.grid(row=0, column=1, sticky="w", padx=20, pady=10)
        
        # Exam Name (dropdown)
        ctk.CTkLabel(centered_container, text="Exam Name:", font=ctk.CTkFont(size=12)).grid(
            row=1, column=0, sticky="w", padx=20, pady=10
        )
        exam_options = ["First Term", "Second Term", "Third Term"]
        exam_name_dropdown = ctk.CTkOptionMenu(centered_container, values=exam_options, width=250)
        exam_name_dropdown.set(result[3])
        exam_name_dropdown.grid(row=1, column=1, sticky="w", padx=20, pady=10)
        
        # Exam Year
        ctk.CTkLabel(centered_container, text="Exam Year:", font=ctk.CTkFont(size=12)).grid(
            row=2, column=0, sticky="w", padx=20, pady=10
        )
        exam_year_entry = ctk.CTkEntry(centered_container, width=250, placeholder_text="2025")
        exam_year_entry.insert(0, str(result[4]))
        exam_year_entry.grid(row=2, column=1, sticky="w", padx=20, pady=10)
        
        # Marks Obtained
        ctk.CTkLabel(centered_container, text="Marks Obtained:", font=ctk.CTkFont(size=12)).grid(
            row=3, column=0, sticky="w", padx=20, pady=10
        )
        marks_obtained_entry = ctk.CTkEntry(centered_container, width=250)
        marks_obtained_entry.insert(0, str(result[5]))
        marks_obtained_entry.grid(row=3, column=1, sticky="w", padx=20, pady=10)
        
        # Grade (Required)
        ctk.CTkLabel(centered_container, text="Grade (Required):", font=ctk.CTkFont(size=12)).grid(
            row=4, column=0, sticky="w", padx=20, pady=10
        )
        grade_entry = ctk.CTkEntry(centered_container, width=250)
        grade_entry.insert(0, result[6])
        grade_entry.grid(row=4, column=1, sticky="w", padx=20, pady=10)
        
        def save_changes():
            """Save the updated exam result"""
            # Validate inputs
            exam_name = exam_name_dropdown.get().strip()
            exam_year = exam_year_entry.get().strip()
            marks_obtained = marks_obtained_entry.get().strip()
            grade = grade_entry.get().strip()
            
            if not all([exam_name, exam_year, marks_obtained, grade]):
                messagebox.showerror("Validation Error", "All fields are required")
                return
            
            # Validate year
            try:
                exam_year_val = int(exam_year)
                if exam_year_val < 1900 or exam_year_val > 2100:
                    messagebox.showerror("Invalid Year", "Please enter a valid year (1900-2100)")
                    return
            except ValueError:
                messagebox.showerror("Invalid Year", "Please enter a valid year")
                return
            
            # Validate marks
            try:
                marks_obtained_val = float(marks_obtained)
                
                if marks_obtained_val < 0:
                    messagebox.showerror("Invalid Marks", "Marks must be a positive number")
                    return
            except ValueError:
                messagebox.showerror("Invalid Marks", "Please enter a valid number for marks")
                return
            
            # Update the result
            result_data = (
                result[1],  # student_id (unchanged)
                exam_name,
                exam_year_val,
                marks_obtained_val,
                grade
            )
            
            success, message = self.db.update_exam_result(result_id, result_data)
            
            if success:
                dialog.destroy()
                self._create_ui()  # Refresh the table
            else:
                messagebox.showerror("Error", f"Failed to update result: {message}")
        
        # Add standard button frame
        dialog.add_button_frame(save_changes)
    
    def _delete_result(self, result_id):
        """Delete exam result after confirmation"""
        result = self.db.get_exam_result_by_id(result_id)
        if not result:
            messagebox.showerror("Error", "Result not found")
            return
        
        def delete_confirmed():
            """Execute deletion after confirmation"""
            success, message = self.db.delete_exam_result(result_id)
            if success:
                self._create_ui()  # Refresh the table
            else:
                messagebox.showerror("Error", f"Failed to delete result: {message}")
        
        # Show custom confirmation dialog
        ConfirmDeleteDialog(
            self.parent,
            title="Confirm Delete",
            main_message=f"Are you sure you want to delete\n{result[2]}'s exam result?\n\nExam: {result[3]}\nYear: {result[4]}",
            warning_message="This action cannot be undone!",
            on_confirm=delete_confirmed
        )
    
    def _view_student(self, student_id):
        """View student details from exam results"""
        student = self.db.get_student_by_id(student_id)
        if not student:
            messagebox.showerror("Error", "Student not found")
            return
        
        # Import here to avoid circular dependency
        from views.student_profiles_view import StudentProfilesView
        
        # Create a temporary instance just to call the detail method
        temp_view = StudentProfilesView.__new__(StudentProfilesView)
        temp_view.parent = self.parent
        temp_view.db = self.db
        temp_view._show_student_details(student)
