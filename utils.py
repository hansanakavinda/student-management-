"""Utility functions for the application"""
import os
import sys


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    
    When running as a PyInstaller bundle, resources are extracted to a 
    temporary folder and stored in sys._MEIPASS. This function ensures
    the correct path is used in both development and production.
    
    Args:
        relative_path: Relative path to the resource file
        
    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
