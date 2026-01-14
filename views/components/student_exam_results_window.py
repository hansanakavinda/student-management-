"""Student exam results window - displays exam results with filtering"""
import customtkinter as ctk


class StudentExamResultsWindow:
    """Window displaying student's exam results with filters"""
    
    def __init__(self, parent, student, db, filters=None):
        self.parent = parent
        self.student = student
        self.db = db
        self.filters = filters or {}
        
        self._create_window()
    
    def _create_window(self):
        """Create the exam results window"""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title(f"Exam Results - {self.student[1]}")
        self.window.geometry("600x600")
        
        # Make window resizable
        self.window.resizable(True, True)
        self.window.minsize(500, 400)
        
        self.window.grab_set()
        self.window.focus_force()
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 300
        y = (self.window.winfo_screenheight() // 2) - 300
        self.window.geometry(f"600x600+{x}+{y}")
        
        # Content
        content = ctk.CTkFrame(self.window)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_content(content)
    
    def _create_content(self, content):
        """Create window content"""
        # Title
        ctk.CTkLabel(
            content,
            text=f"Exam Results for {self.student[1]}",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 10))
        
        # Get all results for filtering options
        all_results = self.db.get_student_results(self.student[0])
        
        # Create filter section
        self._create_filter_section(content, all_results)
        
        # Filter and display results
        filtered_results = self._filter_results(all_results)
        
        if not filtered_results:
            ctk.CTkLabel(
                content,
                text="No exam results found for this student.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
        else:
            self._create_results_table(content, filtered_results)
        
        # Close button
        ctk.CTkButton(
            content,
            text="Close",
            width=150,
            command=self.window.destroy
        ).pack(pady=15)
    
    def _create_filter_section(self, content, all_results):
        """Create filter controls"""
        filter_frame = ctk.CTkFrame(content)
        filter_frame.pack(pady=10, fill="x")
        
        # Exam Name Dropdown
        ctk.CTkLabel(
            filter_frame,
            text="Exam Name:",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        exam_options = ["All", "First Term", "Second Term", "Third Term"]
        self.exam_name_dropdown = ctk.CTkOptionMenu(
            filter_frame,
            values=exam_options,
            width=150
        )
        current_exam = self.filters.get("exam_name") or "All"
        self.exam_name_dropdown.set(current_exam)
        self.exam_name_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Exam Year Dropdown
        ctk.CTkLabel(
            filter_frame,
            text="Exam Year:",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        # Get unique years from student's results
        unique_years = ["All"] + sorted(list(set([str(r[3]) for r in all_results])), reverse=True)
        self.exam_year_dropdown = ctk.CTkOptionMenu(
            filter_frame,
            values=unique_years if len(unique_years) > 1 else ["All"],
            width=120
        )
        current_year = self.filters.get("exam_year") or "All"
        self.exam_year_dropdown.set(current_year)
        self.exam_year_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=4, pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 Apply Filters",
            width=120,
            command=self._apply_filters
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Clear Filters",
            width=110,
            fg_color="#666666",
            hover_color="#888888",
            command=self._clear_filters
        ).pack(side="left", padx=5)
    
    def _filter_results(self, all_results):
        """Apply filters to results"""
        results = all_results
        
        exam_name_filter = self.filters.get("exam_name")
        exam_year_filter = self.filters.get("exam_year")
        
        if exam_name_filter:
            results = [r for r in results if r[2] == exam_name_filter]
        if exam_year_filter:
            results = [r for r in results if str(r[3]) == str(exam_year_filter)]
        
        return results
    
    def _create_results_table(self, content, results):
        """Create table of exam results"""
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
    
    def _apply_filters(self):
        """Apply selected filters and refresh"""
        exam_name = self.exam_name_dropdown.get()
        exam_year = self.exam_year_dropdown.get()
        
        new_filters = {
            "exam_name": None if exam_name == "All" else exam_name,
            "exam_year": None if exam_year == "All" else exam_year
        }
        
        self.window.destroy()
        StudentExamResultsWindow(self.parent, self.student, self.db, new_filters)
    
    def _clear_filters(self):
        """Clear all filters and refresh"""
        self.window.destroy()
        StudentExamResultsWindow(self.parent, self.student, self.db, {})
