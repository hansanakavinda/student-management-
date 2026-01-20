"""Views package for Student Management System"""

from .home_view import HomeView
from .add_student_view import AddStudentView
from .student_profiles_view import StudentProfilesView
from .add_exam_results_view import AddExamResultsView
from .view_exam_results_view import ViewExamResultsView
from .add_certificate_view import AddCertificateView
from .student_detail_view import StudentDetailView
from .student_edit_view import StudentEditView
from .student_exam_results_view import StudentExamResultsView
from .student_certificates_view import StudentCertificatesView

__all__ = [
    'HomeView',
    'AddStudentView',
    'StudentProfilesView',
    'AddExamResultsView',
    'ViewExamResultsView',
    'AddCertificateView',
    'StudentDetailView',
    'StudentEditView',
    'StudentExamResultsView',
    'StudentCertificatesView',
]
