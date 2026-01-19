"""Utility functions for managing student folder structure"""
import os
import shutil
from datetime import datetime


def get_student_folder_name(student_name, student_id):
    """
    Generate folder name for a student based on their name and ID
    Format: StudentName_StudentID
    
    Args:
        student_name: Student's full name
        student_id: Student's database ID
    
    Returns:
        Folder name string
    """
    # Replace spaces with underscores and remove special characters
    safe_name = student_name.replace(' ', '_')
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
    return f"{safe_name}_{student_id}"


def get_student_folder_path(student_name, student_id):
    """
    Get the full path to a student's folder
    
    Args:
        student_name: Student's full name
        student_id: Student's database ID
    
    Returns:
        Full path to student folder
    """
    folder_name = get_student_folder_name(student_name, student_id)
    return os.path.join("students", folder_name)


def ensure_student_folder_exists(student_name, student_id):
    """
    Ensure that a student's folder structure exists
    Creates: students/<StudentName_StudentID>/
    
    Args:
        student_name: Student's full name
        student_id: Student's database ID
    
    Returns:
        Full path to student folder
    """
    folder_path = get_student_folder_path(student_name, student_id)
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    
    return folder_path


def save_student_profile_image(image_path, student_name, student_id):
    """
    Save a student's profile image to their folder
    
    Args:
        image_path: Path to the source image file
        student_name: Student's full name
        student_id: Student's database ID
    
    Returns:
        Path to saved image file, or None if error
    """
    try:
        # Ensure folder exists
        folder_path = ensure_student_folder_exists(student_name, student_id)
        
        # Get file extension
        ext = os.path.splitext(image_path)[1]
        
        # Create filename: profile_<timestamp><ext>
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"profile_{timestamp}{ext}"
        
        # Full destination path
        dest_path = os.path.join(folder_path, filename)
        
        # Copy the file
        shutil.copy2(image_path, dest_path)
        
        return dest_path
    except Exception as e:
        print(f"Error saving profile image: {e}")
        return None


def save_student_certificate(cert_path, student_name, student_id, cert_note=""):
    """
    Save a student's certificate to their folder
    Format: <student_name>_certificate_<note>_<timestamp><ext>
    
    Args:
        cert_path: Path to the source certificate file
        student_name: Student's full name
        student_id: Student's database ID
        cert_note: Optional note/name for the certificate
    
    Returns:
        Path to saved certificate file, or None if error
    """
    try:
        # Ensure folder exists
        folder_path = ensure_student_folder_exists(student_name, student_id)
        
        # Get file extension
        ext = os.path.splitext(cert_path)[1]
        
        # Sanitize student name and cert note for filename
        safe_name = student_name.replace(' ', '_')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
        
        # Create filename based on whether there's a note
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        if cert_note and cert_note.strip():
            safe_note = cert_note.strip().replace(' ', '_')
            safe_note = ''.join(c for c in safe_note if c.isalnum() or c == '_')
            filename = f"{safe_name}_certificate_{safe_note}_{timestamp}{ext}"
        else:
            filename = f"{safe_name}_certificate_{timestamp}{ext}"
        
        # Full destination path
        dest_path = os.path.join(folder_path, filename)
        
        # Copy the file
        shutil.copy2(cert_path, dest_path)
        
        return dest_path
    except Exception as e:
        print(f"Error saving certificate: {e}")
        return None


def delete_student_file(file_path):
    """
    Delete a student file (image or certificate)
    
    Args:
        file_path: Path to the file to delete
    
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False
