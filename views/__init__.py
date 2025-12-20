"""Views package for Student Management System"""

from .home_view import HomeView
from .add_student_view import AddStudentView
from .student_profiles_view import StudentProfilesView
from .add_exam_results_view import AddExamResultsView
from .view_exam_results_view import ViewExamResultsView
from .add_certificate_view import AddCertificateView

__all__ = [
    'HomeView',
    'AddStudentView',
    'StudentProfilesView',
    'AddExamResultsView',
    'ViewExamResultsView',
    'AddCertificateView',
]
