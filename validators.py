"""Centralized validation module for Student Management System"""
from datetime import datetime
import re


class ValidationResult:
    """Container for validation results"""
    def __init__(self, is_valid, error_message=""):
        self.is_valid = is_valid
        self.error_message = error_message


class Validators:
    """Collection of validation functions"""
    
    @staticmethod
    def validate_student_name(name):
        """
        Validate student name - only letters and spaces allowed
        
        Args:
            name: Student name string
            
        Returns:
            ValidationResult
        """
        if not name or not name.strip():
            return ValidationResult(False, "Student name is required")
        
        # Check if name contains only letters and spaces
        if not re.match(r'^[a-zA-Z\s]+$', name.strip()):
            return ValidationResult(False, "Student name must contain only letters and spaces")
        
        if len(name.strip()) < 2:
            return ValidationResult(False, "Student name must be at least 2 characters")
        
        return ValidationResult(True)
    
    @staticmethod
    def validate_date_of_birth(dob):
        """
        Validate date of birth - YYYY-MM-DD format, valid date, not future
        
        Args:
            dob: Date of birth string
            
        Returns:
            ValidationResult
        """
        if not dob or not dob.strip():
            return ValidationResult(False, "Date of birth is required")
        
        # Check format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', dob.strip()):
            return ValidationResult(False, "Date of birth must be in YYYY-MM-DD format")
        
        # Check if valid date
        try:
            date_obj = datetime.strptime(dob.strip(), "%Y-%m-%d")
        except ValueError:
            return ValidationResult(False, "Invalid date - please check day and month values")
        
        # Check if not in future
        if date_obj > datetime.now():
            return ValidationResult(False, "Date of birth cannot be in the future")
        
        # Check reasonable age range (not too old)
        if date_obj.year < 1900:
            return ValidationResult(False, "Date of birth year must be after 1900")
        
        return ValidationResult(True)
    
    @staticmethod
    def validate_registration_date(reg_date):
        """
        Validate registration date - YYYY-MM-DD format, valid date, not future
        
        Args:
            reg_date: Registration date string
            
        Returns:
            ValidationResult
        """
        if not reg_date or not reg_date.strip():
            return ValidationResult(False, "Registration date is required")
        
        # Check format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', reg_date.strip()):
            return ValidationResult(False, "Registration date must be in YYYY-MM-DD format")
        
        # Check if valid date
        try:
            date_obj = datetime.strptime(reg_date.strip(), "%Y-%m-%d")
        except ValueError:
            return ValidationResult(False, "Invalid date - please check day and month values")
        
        # Check if not in future
        if date_obj > datetime.now():
            return ValidationResult(False, "Registration date cannot be in the future")
        
        return ValidationResult(True)
    
    @staticmethod
    def validate_guardian_name(name):
        """
        Validate guardian name - only letters and spaces allowed
        
        Args:
            name: Guardian name string
            
        Returns:
            ValidationResult
        """
        if not name or not name.strip():
            return ValidationResult(False, "Guardian name is required")
        
        # Check if name contains only letters and spaces
        if not re.match(r'^[a-zA-Z\s]+$', name.strip()):
            return ValidationResult(False, "Guardian name must contain only letters and spaces")
        
        if len(name.strip()) < 2:
            return ValidationResult(False, "Guardian name must be at least 2 characters")
        
        return ValidationResult(True)
    
    @staticmethod
    def validate_guardian_nic(nic):
        """
        Validate guardian NIC - exactly 12 digits
        
        Args:
            nic: Guardian NIC string
            
        Returns:
            ValidationResult
        """
        if not nic or not nic.strip():
            return ValidationResult(False, "Guardian NIC is required")
        
        # Remove any spaces
        nic = nic.strip().replace(" ", "")
        
        # Check if exactly 12 digits
        if not re.match(r'^\d{12}$', nic):
            return ValidationResult(False, "Guardian NIC must be exactly 12 digits")
        
        return ValidationResult(True)
    
    @staticmethod
    def validate_guardian_contact(contact):
        """
        Validate guardian contact - exactly 10 digits
        
        Args:
            contact: Guardian contact string
            
        Returns:
            ValidationResult
        """
        if not contact or not contact.strip():
            return ValidationResult(False, "Guardian contact is required")
        
        # Remove any spaces
        contact = contact.strip().replace(" ", "")
        
        # Check if exactly 10 digits
        if not re.match(r'^\d{10}$', contact):
            return ValidationResult(False, "Guardian contact must be exactly 10 digits")
        
        return ValidationResult(True)
    
    @staticmethod
    def validate_exam_year(year):
        """
        Validate exam year - 4 digits only
        
        Args:
            year: Exam year string or int
            
        Returns:
            ValidationResult
        """
        year_str = str(year).strip()
        
        if not year_str:
            return ValidationResult(False, "Exam year is required")
        
        # Check if 4 digits
        if not re.match(r'^\d{4}$', year_str):
            return ValidationResult(False, "Exam year must be exactly 4 digits")
        
        # Check reasonable year range
        year_int = int(year_str)
        current_year = datetime.now().year
        
        if year_int < 2000:
            return ValidationResult(False, "Exam year must be 2000 or later")
        
        if year_int > current_year + 1:
            return ValidationResult(False, f"Exam year cannot be more than {current_year + 1}")
        
        return ValidationResult(True)
    
    @staticmethod
    def validate_marks_obtained(marks):
        """
        Validate marks obtained - must be between 0 and 100
        
        Args:
            marks: Marks value (string or number)
            
        Returns:
            ValidationResult
        """
        if marks is None or str(marks).strip() == "":
            return ValidationResult(False, "Marks obtained is required")
        
        try:
            marks_float = float(str(marks).strip())
        except ValueError:
            return ValidationResult(False, "Marks must be a valid number")
        
        if marks_float < 0:
            return ValidationResult(False, "Marks cannot be negative")
        
        if marks_float > 100:
            return ValidationResult(False, "Marks cannot be more than 100")
        
        return ValidationResult(True)
    
    @staticmethod
    def calculate_grade(marks):
        """
        Calculate grade based on marks
        
        Args:
            marks: Marks value (string or number)
            
        Returns:
            Grade letter (A, B, C, S, W) or empty string if invalid
        """
        try:
            marks_float = float(str(marks).strip())
            
            if marks_float >= 75:
                return "A"
            elif marks_float >= 65:
                return "B"
            elif marks_float >= 55:
                return "C"
            elif marks_float >= 35:
                return "S"
            else:
                return "W"
        except (ValueError, AttributeError):
            return ""
    
    @staticmethod
    def validate_address(address):
        """
        Validate address - basic check for required field
        
        Args:
            address: Address string
            
        Returns:
            ValidationResult
        """
        if not address or not address.strip():
            return ValidationResult(False, "Address is required")
        
        if len(address.strip()) < 3:
            return ValidationResult(False, "Address must be at least 3 characters")
        
        return ValidationResult(True)
    
    @staticmethod
    def validate_grade_level(grade):
        """
        Validate grade level - must be valid grade
        
        Args:
            grade: Grade level string
            
        Returns:
            ValidationResult
        """
        if not grade or not grade.strip():
            return ValidationResult(False, "Grade is required")
        
        # Extract number from "Grade X" format
        grade_str = grade.strip()
        if grade_str.startswith("Grade "):
            grade_str = grade_str.replace("Grade ", "")
        
        try:
            grade_num = int(grade_str)
            if grade_num < 1 or grade_num > 13:
                return ValidationResult(False, "Grade must be between 1 and 13")
        except ValueError:
            return ValidationResult(False, "Invalid grade format")
        
        return ValidationResult(True)
