"""View Exam Results view for Student Management System"""
import customtkinter as ctk
from datetime import datetime
import tkinter.messagebox as messagebox
from widgets import FilterWidget


class ViewExamResultsView:
    """View for displaying exam results with filtering options"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.filters = {}
        
        # Create main frame
        self.results_frame = ctk.CTkFrame(parent)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
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
        
        # Filter widget
        filter_fields = [
            ("Student Name:", "Enter student name...", 180),
            ("Exam Name:", "Enter exam name...", 180),
            ("Exam Date:", "YYYY-MM-DD", 180)
        ]
        
        filter_widget = FilterWidget(
            self.results_frame,
            filters=filter_fields,
            on_apply=self._apply_filters,
            on_clear=self._clear_filters
        )
        filter_widget.pack(pady=10, padx=20, fill="x")
        
        # Results display area
        scroll_frame = ctk.CTkScrollableFrame(self.results_frame, height=450)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get results
        student_name = self.filters.get("Student Name:")
        exam_name = self.filters.get("Exam Name:")
        exam_date = self.filters.get("Exam Date:")
        
        results = self.db.get_all_exam_results(student_name, exam_name, exam_date)
        
        if not results:
            no_results_msg = "No results match your filters." if any(self.filters.values()) else "No exam results found."
            ctk.CTkLabel(
                scroll_frame,
                text=no_results_msg,
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        # Header
        header_frame = ctk.CTkFrame(scroll_frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        headers = ["ID", "Student", "Subject", "Exam", "Date", "Marks", "Grade"]
        widths = [50, 120, 100, 120, 100, 80, 60]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width
            ).grid(row=0, column=i, padx=5, pady=5)
        
        # Result rows
        for result in results:
            self._create_result_row(scroll_frame, result, widths)
        
        # Summary info
        summary_frame = ctk.CTkFrame(self.results_frame)
        summary_frame.pack(pady=10)
        
        ctk.CTkLabel(
            summary_frame,
            text=f"Total Results: {len(results)}",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(padx=20, pady=10)
    
    def _create_result_row(self, parent, result, widths):
        """Create a single result row"""
        result_frame = ctk.CTkFrame(parent)
        result_frame.pack(fill="x", padx=10, pady=2)
        
        # Calculate percentage
        percentage = (result[6] / result[7] * 100) if result[7] > 0 else 0
        marks_display = f"{result[6]}/{result[7]} ({percentage:.1f}%)"
        
        values = [
            result[0],  # ID
            result[2],  # Student name
            result[3],  # Subject
            result[4],  # Exam name
            result[5],  # Exam date
            marks_display,  # Marks with percentage
            result[8] or "N/A"  # Grade
        ]
        
        for i, (value, width) in enumerate(zip(values, widths)):
            ctk.CTkLabel(
                result_frame,
                text=str(value),
                font=ctk.CTkFont(size=11),
                width=width
            ).grid(row=0, column=i, padx=5, pady=5)
        
        # View student button
        ctk.CTkButton(
            result_frame,
            text="View Student",
            width=100,
            command=lambda: self._view_student(result[1])
        ).grid(row=0, column=len(values), padx=5)
    
    def _apply_filters(self, filter_values):
        """Apply filters and refresh results"""
        # Validate date if provided
        exam_date = filter_values.get("Exam Date:")
        if exam_date:
            try:
                datetime.strptime(exam_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format for date")
                return
        
        self.filters = filter_values
        self._create_ui()
    
    def _clear_filters(self):
        """Clear all filters and show all results"""
        self.filters = {}
        self._create_ui()
    
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
