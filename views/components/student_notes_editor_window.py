"""Student notes editor window"""
import customtkinter as ctk


class StudentNotesEditorWindow:
    """Window for editing student notes"""
    
    def __init__(self, parent, student, db, detail_window=None):
        self.parent = parent
        self.student = student
        self.db = db
        self.detail_window = detail_window
        
        self._create_window()
    
    def _create_window(self):
        """Create the notes editor window"""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title(f"Edit Notes - {self.student[1]}")
        self.window.geometry("600x450")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (450 // 2)
        self.window.geometry(f"+{x}+{y}")
        
        self._create_content()
    
    def _create_content(self):
        """Create window content"""
        # Main container
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            main_frame,
            text=f"Additional Notes for {self.student[1]}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(0, 20))
        
        # Notes text area
        self.notes_textbox = ctk.CTkTextbox(
            main_frame,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.notes_textbox.pack(fill="both", expand=True, pady=10)
        
        # Load existing notes
        current_notes = self.db.get_student_notes(self.student[0])
        if current_notes:
            self.notes_textbox.insert("1.0", current_notes)
        
        # Character count label
        self.char_label = ctk.CTkLabel(
            main_frame,
            text=f"Characters: {len(current_notes)}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.char_label.pack(pady=(5, 10))
        
        self.notes_textbox.bind("<KeyRelease>", self._update_char_count)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)
        
        # Button frame
        self._create_buttons(main_frame)
    
    def _update_char_count(self, event=None):
        """Update character count"""
        text = self.notes_textbox.get("1.0", "end-1c")
        self.char_label.configure(text=f"Characters: {len(text)}")
    
    def _create_buttons(self, parent):
        """Create action buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Save Notes",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=140,
            height=40,
            fg_color="#2b7a0b",
            hover_color="#3a9b1a",
            command=self._save_notes
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=14),
            width=140,
            height=40,
            fg_color="#666666",
            hover_color="#888888",
            command=self.window.destroy
        ).pack(side="left", padx=10)
    
    def _save_notes(self):
        """Save notes to database"""
        notes_text = self.notes_textbox.get("1.0", "end-1c").strip()
        success, message = self.db.save_student_notes(self.student[0], notes_text)
        
        if success:
            self.status_label.configure(text="✓ Notes saved successfully", text_color="green")
            
            # Refresh the detail window if provided
            if self.detail_window:
                self.detail_window.refresh_notes()
            
            self.window.after(1000, self.window.destroy)
        else:
            self.status_label.configure(text=f"Error: {message}", text_color="red")
