"""
Build script to package the application into a standalone executable
"""
import os
import subprocess
import sys

# ============= CONFIGURATION =============
# Change this to switch between build methods: "pyinstaller" or "nuitka"
BUILD_METHOD = "pyinstaller"
# got some error with nuitka on windows will have to check some time later
# BUILD_METHOD = "nuitka" 

# ========================================

def build_with_pyinstaller():
    """Build the executable using PyInstaller"""
    
    print("Building with PyInstaller...")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=StudentManager",
        "--windowed",  # No console window
        "--onefile",   # Single executable file
        "--icon=logo.ico",  # App icon for .exe file in Explorer
        "--add-data=logo.ico;.",  # Bundle icon inside exe for taskbar
        "--add-data=venv/Lib/site-packages/customtkinter;customtkinter/",
        "--add-data=logo.png;.",  # Include logo.png in root of app
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "--collect-all=customtkinter",
        "main.py"
    ]

    # PyInstaller command
    cmdonedir = [
        sys.executable, "-m", "PyInstaller",
        "--name=StudentManager",
        "--windowed",  # No console window
        "--onedir",   # Directory with executable and dependencies
        "--icon=logo.ico",  # App icon for .exe file in Explorer
        "--add-data=logo.ico;.",  # Bundle icon inside exe for taskbar
        "--add-data=venv/Lib/site-packages/customtkinter;customtkinter/",
        "--add-data=logo.png;.",  # Include logo.png in root of app
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "--collect-all=customtkinter",
        "main.py"
    ]
    
    try:
        subprocess.run(cmdonedir, check=True)
        print("\n✓ Build successful!")
        print("Your executable is in the 'dist' folder: dist/StudentManager")
        print("\nTo distribute:")
        print("1. Copy dist/StudentManager.exe to the target PC")
        print("2. Run it - the database will be created automatically on first run")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False
    
    return True

def build_with_nuitka():
    """Build the executable using Nuitka"""
    
    print("Building with Nuitka...")
    
    # Nuitka command
    cmd = [
        sys.executable, "-m", "nuitka",
        "--onefile",
        "--standalone",
        "--enable-plugin=tk-inter",
        "--include-package-data=customtkinter",
        "--include-package=PIL",
        "--include-package=reportlab",
        "--windows-disable-console",
        "--windows-icon-from-ico=logo.ico",  # App icon
        "--include-data-file=logo.png=logo.png",  # Include logo.png
        "--output-filename=StudentManager.exe",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Build successful!")
        print("Your executable is in the current folder: StudentManager.exe")
        print("\nTo distribute:")
        print("1. Copy StudentManager.exe to the target PC")
        print("2. Run it - the database will be created automatically on first run")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False
    
    return True

def build_exe():
    """Build the executable using the selected method"""
    
    if BUILD_METHOD.lower() == "pyinstaller":
        return build_with_pyinstaller()
    elif BUILD_METHOD.lower() == "nuitka":
        return build_with_nuitka()
    else:
        print(f"✗ Error: Unknown build method '{BUILD_METHOD}'")
        print("   Valid options: 'pyinstaller' or 'nuitka'")
        return False

if __name__ == "__main__":
    print(f"Selected build method: {BUILD_METHOD.upper()}")
    print("-" * 50)
    build_exe()
