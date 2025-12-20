"""
Build script to package the application into a standalone executable
"""
import os
import subprocess
import sys

def build_exe():
    """Build the executable using PyInstaller"""
    
    print("Building executable...")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=StudentManager",
        "--windowed",  # No console window
        "--onefile",   # Single executable file
        "--icon=NONE", # Add your .ico file here if you have one
        "--add-data=.venv/Lib/site-packages/customtkinter;customtkinter/",
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "--collect-all=customtkinter",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Build successful!")
        print("Your executable is in the 'dist' folder: dist/ModernApp.exe")
        print("\nTo distribute:")
        print("1. Copy dist/ModernApp.exe to the target PC")
        print("2. Run it - the database will be created automatically on first run")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    build_exe()
