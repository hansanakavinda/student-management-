"""
Student Profiles View - Refactored to use separate components
This view orchestrates the student profile components
"""
import tkinter.messagebox as messagebox
import os
from widgets import ConfirmDeleteDialog
from .components import (
    StudentListComponent,
    StudentDetailWindow,
    StudentExamResultsWindow,
    StudentNotesEditorWindow,
    StudentCertificatesWindow,
    StudentEditWindow
)


class StudentProfilesView:
    """
    Main view for student profiles - orchestrates various components
    Separated into focused, single-responsibility components
    """
    
    def __init__(self, parent, db, on_refresh=None):
        self.parent = parent
        self.db = db
        self.on_refresh = on_refresh
        
        # Create the main list component
        self.list_component = StudentListComponent(
            parent,
            db,
            on_view_student=self._view_student,
            on_edit_student=self._edit_student,
            on_delete_student=self._delete_student,
            on_view_results=self._view_exam_results
        )
    
    def _view_student(self, student):
        """Show detailed view of a student"""
        StudentDetailWindow(
            self.parent,
            student,
            self.db,
            on_edit_notes=self._edit_notes,
            on_view_results=self._view_exam_results,
            on_view_certificates=self._view_certificates
        )
    
    def _edit_student(self, student):
        """Show edit form for student"""
        StudentEditWindow(
            self.parent,
            student,
            self.db,
            on_success=self._refresh_list
        )
    
    def _delete_student(self, student):
        """Delete student after confirmation"""
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
                self._refresh_list()
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
    
    def _view_exam_results(self, student):
        """Show exam results window"""
        StudentExamResultsWindow(self.parent, student, self.db)
    
    def _edit_notes(self, student, detail_window):
        """Show notes editor"""
        StudentNotesEditorWindow(detail_window.window, student, self.db, detail_window)
    
    def _view_certificates(self, student):
        """Show certificates window"""
        StudentCertificatesWindow(self.parent, student, self.db)
    
    def _refresh_list(self):
        """Refresh the student list"""
        self.list_component.refresh()
        if self.on_refresh:
            self.on_refresh()
