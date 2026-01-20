"""Student exam results view - displays exam results with filtering"""
import customtkinter as ctk
import os
import tkinter.messagebox as messagebox
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from student_folder_utils import get_student_folder_path, ensure_student_folder_exists
from utils import resource_path


class StudentExamResultsView(ctk.CTkFrame):
    """View displaying student's exam results with filters"""
    
    def __init__(self, parent, student, db, on_back, filters=None):
        super().__init__(parent)
        self.student = student
        self.db = db
        self.on_back = on_back
        self.filters = filters or {}
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_content()
    
    def _create_content(self):
        """Create view content"""
        # Main scrollable frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Create centered container
        centered_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        centered_container.pack(expand=True, fill="both", pady=20)
        
        # Back button at the top
        ctk.CTkButton(
            centered_container,
            text="← Back to Student Profiles",
            width=200,
            font=ctk.CTkFont(size=14),
            command=self.on_back
        ).pack(anchor="w", pady=(0, 20))
        
        # Title
        ctk.CTkLabel(
            centered_container,
            text=f"Exam Results - {self.student[1]}",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(0, 20))
        
        # Get all results for filtering options
        all_results = self.db.get_student_results(self.student[0])
        
        # Create filter section
        self._create_filter_section(centered_container, all_results)
        
        # Filter and display results
        filtered_results = self._filter_results(all_results)
        
        if not filtered_results:
            ctk.CTkLabel(
                centered_container,
                text="No exam results found for this student.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
        else:
            # Info text
            ctk.CTkLabel(
                centered_container,
                text=f"Showing {len(filtered_results)} result(s)",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(pady=(10, 5))
            
            self._create_results_table(centered_container, filtered_results)
    
    def _create_filter_section(self, parent, all_results):
        """Create filter controls"""
        filter_frame = ctk.CTkFrame(parent)
        filter_frame.pack(pady=10, fill="x")
        
        # Filter controls row
        controls_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        controls_frame.pack(pady=10)
        
        # Exam Name Dropdown
        ctk.CTkLabel(
            controls_frame,
            text="Exam Name:",
            font=ctk.CTkFont(size=13)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        exam_options = ["All", "First Term", "Second Term", "Third Term"]
        self.exam_name_dropdown = ctk.CTkOptionMenu(
            controls_frame,
            values=exam_options,
            width=180
        )
        current_exam = self.filters.get("exam_name") or "All"
        self.exam_name_dropdown.set(current_exam)
        self.exam_name_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Exam Year Dropdown
        ctk.CTkLabel(
            controls_frame,
            text="Exam Year:",
            font=ctk.CTkFont(size=13)
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        # Get unique years from student's results
        unique_years = ["All"] + sorted(list(set([str(r[3]) for r in all_results])), reverse=True)
        self.exam_year_dropdown = ctk.CTkOptionMenu(
            controls_frame,
            values=unique_years if len(unique_years) > 1 else ["All"],
            width=120
        )
        current_year = self.filters.get("exam_year") or "All"
        self.exam_year_dropdown.set(current_year)
        self.exam_year_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=4, pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 Apply Filters",
            width=130,
            command=self._apply_filters
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Clear Filters",
            width=120,
            fg_color="#666666",
            hover_color="#888888",
            command=self._clear_filters
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="📄 Export to PDF",
            width=130,
            command=self._export_to_pdf,
            fg_color="#c12c2a",
            hover_color="#FB3636"
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
    
    def _create_results_table(self, parent, results):
        """Create table of exam results"""
        # Scrollable frame for results (matching student list component structure)
        scroll_frame = ctk.CTkScrollableFrame(parent, height=400)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Create centered container within the scrollable content
        centered_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        centered_container.pack(expand=True, pady=20)

        # Table headers
        header_frame = ctk.CTkFrame(centered_container)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        headers = ["Exam", "Year", "Marks", "Grade"]
        widths = [250, 150, 150, 120]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width,
                anchor="w"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # Table rows (matching student list component structure)
        for result in results:
            row_frame = ctk.CTkFrame(centered_container, fg_color="#363535")
            row_frame.pack(fill="x", padx=10, pady=2)
            
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
                    anchor="w"
                ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
    
    def _apply_filters(self):
        """Apply selected filters and refresh"""
        exam_name = self.exam_name_dropdown.get()
        exam_year = self.exam_year_dropdown.get()
        
        new_filters = {
            "exam_name": None if exam_name == "All" else exam_name,
            "exam_year": None if exam_year == "All" else exam_year
        }
        
        # Recreate the view with new filters
        for widget in self.winfo_children():
            widget.destroy()
        self.filters = new_filters
        self._create_content()
    
    def _clear_filters(self):
        """Clear all filters and refresh"""
        # Recreate the view with no filters
        for widget in self.winfo_children():
            widget.destroy()
        self.filters = {}
        self._create_content()
    
    def _export_to_pdf(self):
        """Export exam results to PDF respecting current filters"""
        try:
            # Get filtered results
            all_results = self.db.get_student_results(self.student[0])
            filtered_results = self._filter_results(all_results)
            
            if not filtered_results:
                messagebox.showwarning(
                    "No Data",
                    "No exam results to export with current filters."
                )
                return
            
            # Ensure student folder exists
            student_folder = ensure_student_folder_exists(self.student[1], self.student[0])
            
            # Generate filename with date
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = self.student[1].replace(' ', '_')
            filename = f"{safe_name}_{self.student[0]}_exam_results_{date_str}.pdf"
            pdf_path = os.path.join(student_folder, filename)
            
            # Create PDF
            self._generate_pdf(pdf_path, filtered_results)
            
            messagebox.showinfo(
                "Success",
                f"PDF exported successfully!\n\nSaved to:\n{pdf_path}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Export Failed",
                f"Failed to export PDF:\n{str(e)}"
            )
    
    def _generate_pdf(self, pdf_path, results):
        """Generate PDF document with exam results"""
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for PDF elements
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1f6aa5'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=0,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6,
            alignment=TA_CENTER
        )
        
        # Add logo and school name header side by side
        logo_path = resource_path("logo.png")
        if os.path.exists(logo_path):
            # Create logo image with appropriate size
            logo = Image(logo_path, width=1*inch, height=1*inch)
            
            # Create left-aligned title style for header
            header_title_style = ParagraphStyle(
                'HeaderTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#1f6aa5'),
                spaceAfter=0,
                alignment=TA_LEFT,
                fontName='Helvetica-Bold',
                leftIndent=10
            )
            
            # Create table with logo and school name side by side
            header_table = Table(
                [[logo, Paragraph("Siri Seelananda Daham Pasala", header_title_style)]],
                colWidths=[1.2*inch, 5*inch]
            )
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            elements.append(header_table)
        else:
            # Fallback if logo doesn't exist
            elements.append(Paragraph("Siri Seelananda Daham Pasala", title_style))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Report generation date and time
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        elements.append(Paragraph(f"Report Generated: {report_date}", normal_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Student name
        elements.append(Paragraph(f"Student: {self.student[1]}", heading_style))
        elements.append(Spacer(1, 0.005*inch))

        # use student registration date and grade to calculate current grade
        current_year = datetime.now().year
        registration_year = int(self.student[9].split("-")[0]) if self.student[9] else current_year
        grade_at_registration = int(self.student[10]) if len(self.student) > 10 and self.student[10].isdigit() else 1
        current_grade = grade_at_registration + (current_year - registration_year)

        elements.append(Paragraph(f"Grade: {current_grade}", heading_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add filter information if filters are applied
        filter_info = []
        if self.filters.get("exam_name"):
            filter_info.append(f"Exam: {self.filters['exam_name']}")
        if self.filters.get("exam_year"):
            filter_info.append(f"Year: {self.filters['exam_year']}")
        
        if filter_info:
            filter_text = "Filters Applied: " + ", ".join(filter_info)
            elements.append(Paragraph(filter_text, normal_style))
            elements.append(Spacer(1, 0.2*inch))
        
        # Prepare table data
        table_data = [
            ['Exam', 'Year', 'Marks', 'Grade']  # Headers
        ]
        
        # Add result rows
        for result in results:
            table_data.append([
                result[2],  # Exam name
                str(result[3]),  # Exam year
                str(result[4]),  # Marks obtained
                result[5]   # Grade
            ])
        
        # Create table with specified column widths
        col_widths = [2.5*inch, 1.2*inch, 1.2*inch, 1.2*inch]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Table style
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f6aa5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Alternating row colors for better readability
            *[('BACKGROUND', (0, i), (-1, i), colors.lightgrey if i % 2 == 0 else colors.beige)
              for i in range(1, len(table_data))]
        ]))
        
        elements.append(table)
        
        # Add signature section at the end (only on last page)
        # Create signature style aligned to left
        signature_style = ParagraphStyle(
            'SignatureStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            alignment=TA_LEFT,
            fontName='Helvetica'
        )
        
        # Group signature elements to keep them together and avoid overlay
        signature_elements = []
        signature_elements.append(Spacer(1, 0.5*inch))
        signature_elements.append(Paragraph("Principal's Signature", signature_style))
        signature_elements.append(Spacer(1, 0.3*inch))
        signature_elements.append(Paragraph("_" * 30, signature_style))
        
        # Use KeepTogether to ensure signature doesn't split across pages
        # This will automatically create a new page if there's not enough space
        elements.append(KeepTogether(signature_elements))
        
        # Build PDF
        doc.build(elements)
