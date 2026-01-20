"""Student list/table component - displays all students in a searchable table with pagination"""
import customtkinter as ctk
from widgets import SearchWidget, create_label_with_tooltip


class StudentListComponent:
    """Component for displaying students in a table with search and pagination"""
    
    def __init__(self, parent, db, on_view_student, on_edit_student, on_delete_student, on_view_results=None, items_per_page=20):
        self.parent = parent
        self.db = db
        self.on_view_student = on_view_student
        self.on_edit_student = on_edit_student
        self.on_delete_student = on_delete_student
        self.on_view_results = on_view_results
        
        # Pagination settings
        self.items_per_page = items_per_page
        self.current_page = 1
        self.total_pages = 1
        self.current_search_term = None
        
        # Create main frame
        self.list_frame = ctk.CTkFrame(parent)
        self.list_frame.pack(fill="both", expand=True)
        
        self._create_ui()
    
    def _create_ui(self, search_term=None, reset_page=False):
        """Create the student list UI with pagination"""
        # Clear existing widgets
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        # Store search term for pagination
        if search_term is not None or reset_page:
            self.current_search_term = search_term
            if reset_page:
                self.current_page = 1
        
        # Title
        title_text = "Student Profiles"
        title = ctk.CTkLabel(
            self.list_frame,
            text=title_text,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(20, 10))
        
        # Search widget
        search_widget = SearchWidget(
            self.list_frame,
            placeholder="Enter student name...",
            on_search=self._perform_search,
            on_clear=self._clear_search
        )
        search_widget.pack(pady=10)
        
        if self.current_search_term:
            search_widget.set_search_term(self.current_search_term)
        
        # Get all students (for pagination calculation)
        all_students = self.db.search_students(self.current_search_term) if self.current_search_term else self.db.get_all_students()
        
        if not all_students:
            no_results_msg = f"No students found matching '{self.current_search_term}'." if self.current_search_term else "No students registered yet."
            ctk.CTkLabel(
                self.list_frame,
                text=no_results_msg,
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        # Calculate pagination
        total_students = len(all_students)
        self.total_pages = (total_students + self.items_per_page - 1) // self.items_per_page  # Ceiling division
        
        # Ensure current page is valid
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        if self.current_page < 1:
            self.current_page = 1
        
        # Get students for current page
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        students = all_students[start_idx:end_idx]
        
        # Info bar (showing results and pagination info)
        info_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        info_text = f"Showing {start_idx + 1}-{min(end_idx, total_students)} of {total_students} students"
        if self.total_pages > 1:
            info_text += f" | Page {self.current_page} of {self.total_pages}"
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(side="left")
        
        # Items per page selector
        if total_students > 10:
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
        
        # Scrollable frame for students (FIXED: removed orientation="horizontal")
        scroll_frame = ctk.CTkScrollableFrame(self.list_frame, height=400, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Header
        header_frame = ctk.CTkFrame(scroll_frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        headers = ["ID", "Name", "DOB", "Gender", "Guardian", "Guardian NIC"]
        header_widths = [50, 200, 100, 100, 200, 120]
        
        for i, (header, width) in enumerate(zip(headers, header_widths)):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width,
                anchor="w"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # Student rows (only current page)
        for student in students:
            self._create_student_row(scroll_frame, student, header_widths)
        
        # Pagination controls (only show if more than one page)
        if self.total_pages > 1:
            self._create_pagination_controls()
    
    def _create_student_row(self, parent, student, header_widths):
        """Create a single student row with action buttons"""
        student_frame = ctk.CTkFrame(parent, fg_color="#363535")
        student_frame.pack(fill="x", padx=10, pady=2)
        
        values = [student[0], student[1], student[2], student[3], student[5], student[6]]
        # Max lengths for truncation: ID (10), Name (30), DOB (12), Gender (10), Guardian (30), NIC (15)
        max_lengths = [10, 30, 12, 10, 30, 15]
        
        for i, (value, max_len, col_width) in enumerate(zip(values, max_lengths, header_widths)):
            label = create_label_with_tooltip(
                student_frame,
                str(value),
                max_length=max_len,
                font=ctk.CTkFont(size=11),
                width=col_width,
                anchor="w"
            )
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # View button
        ctk.CTkButton(
            student_frame,
            text="View",
            width=60,
            command=lambda: self.on_view_student(student)
        ).grid(row=0, column=len(values), padx=5)
        
        # View Results button (if callback provided)
        button_col = len(values) + 1
        if self.on_view_results:
            ctk.CTkButton(
                student_frame,
                text="Results",
                width=60,
                fg_color="#2f9f5a",
                hover_color="#147056",
                command=lambda: self.on_view_results(student)
            ).grid(row=0, column=button_col, padx=5)
            button_col += 1
        
        # Edit button
        ctk.CTkButton(
            student_frame,
            text="Edit",
            width=60,
            fg_color="#FF8C00",
            hover_color="#FFA500",
            command=lambda: self.on_edit_student(student)
        ).grid(row=0, column=button_col, padx=5)
        
        # Delete button
        ctk.CTkButton(
            student_frame,
            text="Delete",
            width=60,
            fg_color="#DC143C",
            hover_color="#B22222",
            command=lambda: self.on_delete_student(student)
        ).grid(row=0, column=button_col+1, padx=5)
    
    def _create_pagination_controls(self):
        """Create pagination navigation controls"""
        pagination_frame = ctk.CTkFrame(self.list_frame)
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
    
    def _perform_search(self, search_term):
        """Handle search (resets to page 1)"""
        self._create_ui(search_term, reset_page=True)
    
    def _clear_search(self):
        """Clear search and show all students (resets to page 1)"""
        self._create_ui(None, reset_page=True)
    
    def refresh(self):
        """Refresh the student list (maintains current page)"""
        self._create_ui()
