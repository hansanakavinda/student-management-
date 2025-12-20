"""Reusable UI widgets for the Student Management System"""
import customtkinter as ctk
from typing import Callable, Optional


class SearchWidget(ctk.CTkFrame):
    """Reusable search widget with search bar and clear button"""
    
    def __init__(self, parent, placeholder: str = "Search...", 
                 on_search: Optional[Callable] = None,
                 on_clear: Optional[Callable] = None,
                 **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.on_search = on_search
        self.on_clear = on_clear
        
        # Label
        ctk.CTkLabel(
            self, 
            text="Search:", 
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=5)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            self, 
            width=250, 
            placeholder_text=placeholder
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind('<Return>', lambda e: self._handle_search())
        
        # Search button
        self.search_btn = ctk.CTkButton(
            self,
            text="Search",
            width=100,
            command=self._handle_search
        )
        self.search_btn.pack(side="left", padx=5)
        
        # Clear button
        self.clear_btn = ctk.CTkButton(
            self,
            text="Clear",
            width=100,
            fg_color="#666666",
            hover_color="#888888",
            command=self._handle_clear
        )
        self.clear_btn.pack(side="left", padx=5)
    
    def _handle_search(self):
        """Handle search button click"""
        if self.on_search:
            self.on_search(self.get_search_term())
    
    def _handle_clear(self):
        """Handle clear button click"""
        self.search_entry.delete(0, 'end')
        if self.on_clear:
            self.on_clear()
    
    def get_search_term(self) -> str:
        """Get the current search term"""
        return self.search_entry.get().strip()
    
    def set_search_term(self, term: str):
        """Set the search term"""
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, term)


class FilterWidget(ctk.CTkFrame):
    """Reusable filter widget with multiple filter fields"""
    
    def __init__(self, parent, filters: list, 
                 on_apply: Optional[Callable] = None,
                 on_clear: Optional[Callable] = None,
                 **kwargs):
        """
        Args:
            parent: Parent widget
            filters: List of tuples (label, placeholder, width)
            on_apply: Callback when apply button is clicked
            on_clear: Callback when clear button is clicked
        """
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.on_apply = on_apply
        self.on_clear = on_clear
        self.filter_entries = {}
        
        # Create rows for filters
        current_row = 0
        filters_per_row = 2
        current_col = 0
        
        for label, placeholder, width in filters:
            if current_col >= filters_per_row * 2:
                current_row += 1
                current_col = 0
            
            # Create label
            ctk.CTkLabel(
                self, 
                text=label, 
                font=ctk.CTkFont(size=13)
            ).grid(row=current_row, column=current_col, padx=5, pady=5, sticky="w")
            
            # Create entry
            entry = ctk.CTkEntry(self, width=width, placeholder_text=placeholder)
            entry.grid(row=current_row, column=current_col + 1, padx=5, pady=5, sticky="w")
            self.filter_entries[label] = entry
            
            current_col += 2
        
        # Button row
        button_row = current_row + 1
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=button_row, column=0, columnspan=4, pady=10)
        
        # Apply button
        self.apply_btn = ctk.CTkButton(
            button_frame,
            text="🔍 Apply Filters",
            width=130,
            command=self._handle_apply
        )
        self.apply_btn.pack(side="left", padx=5)
        
        # Clear button
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear Filters",
            width=120,
            fg_color="#666666",
            hover_color="#888888",
            command=self._handle_clear
        )
        self.clear_btn.pack(side="left", padx=5)
    
    def _handle_apply(self):
        """Handle apply button click"""
        if self.on_apply:
            self.on_apply(self.get_filter_values())
    
    def _handle_clear(self):
        """Handle clear button click"""
        for entry in self.filter_entries.values():
            entry.delete(0, 'end')
        if self.on_clear:
            self.on_clear()
    
    def get_filter_values(self) -> dict:
        """Get all filter values as a dictionary"""
        return {label: entry.get().strip() or None 
                for label, entry in self.filter_entries.items()}
    
    def set_filter_values(self, values: dict):
        """Set filter values from a dictionary"""
        for label, value in values.items():
            if label in self.filter_entries and value:
                entry = self.filter_entries[label]
                entry.delete(0, 'end')
                entry.insert(0, value)


class FieldWithClearButton(ctk.CTkFrame):
    """Reusable field with an adjacent clear button"""
    
    def __init__(self, parent, placeholder: str = "", width: int = 240, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        # Entry field
        self.entry = ctk.CTkEntry(self, width=width, placeholder_text=placeholder)
        self.entry.pack(side="left", padx=(0, 5))
        
        # Clear button
        self.clear_btn = ctk.CTkButton(
            self,
            text="Clear",
            width=50,
            fg_color="#666666",
            hover_color="#888888",
            command=self.clear
        )
        self.clear_btn.pack(side="left")
    
    def get(self) -> str:
        """Get the entry value"""
        return self.entry.get()
    
    def clear(self):
        """Clear the entry"""
        self.entry.delete(0, 'end')
    
    def insert(self, index, string):
        """Insert text into the entry"""
        self.entry.insert(index, string)
    
    def delete(self, first, last):
        """Delete text from the entry"""
        self.entry.delete(first, last)
    
    def bind(self, sequence, func):
        """Bind an event to the entry"""
        self.entry.bind(sequence, func)


class EditDialog(ctk.CTkToplevel):
    """Reusable edit dialog window with consistent styling"""
    
    def __init__(self, parent, title: str, width: int = 600, height: int = 750, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.grab_set()
        self.focus_force()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Content frame (scrollable)
        self.content = ctk.CTkScrollableFrame(self)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)
    
    def add_title(self, text: str):
        """Add a title label to the dialog"""
        ctk.CTkLabel(
            self.content,
            text=text,
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(10, 20))
    
    def add_form_frame(self):
        """Add and return a form frame for fields"""
        form_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=10)
        return form_frame
    
    def add_button_frame(self, save_command, cancel_command=None, 
                        save_text="Save Changes", cancel_text="Cancel"):
        """Add standard save/cancel button frame"""
        button_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text=save_text,
            font=ctk.CTkFont(size=16),
            width=150,
            height=40,
            command=save_command
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text=cancel_text,
            font=ctk.CTkFont(size=16),
            width=150,
            height=40,
            fg_color="#666666",
            hover_color="#888888",
            command=cancel_command or self.destroy
        ).pack(side="left", padx=10)


class ConfirmDeleteDialog(ctk.CTkToplevel):
    """Reusable confirmation dialog for delete operations"""
    
    def __init__(self, parent, title: str, main_message: str, 
                 warning_message: str, on_confirm, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.title(title)
        self.geometry("500x380")
        self.grab_set()
        self.focus_force()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 250
        y = (self.winfo_screenheight() // 2) - 190
        self.geometry(f"500x380+{x}+{y}")
        
        # Content
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Warning icon and title
        ctk.CTkLabel(
            content,
            text="⚠️ Warning",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#DC143C"
        ).pack(pady=(10, 20))
        
        # Main message
        ctk.CTkLabel(
            content,
            text=main_message,
            font=ctk.CTkFont(size=14),
            justify="center"
        ).pack(pady=10)
        
        # Warning message
        ctk.CTkLabel(
            content,
            text=warning_message,
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="center"
        ).pack(pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(pady=30)
        
        def confirm_action():
            on_confirm()
            self.destroy()
        
        ctk.CTkButton(
            button_frame,
            text="Yes, Delete",
            width=150,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#DC143C",
            hover_color="#B22222",
            command=confirm_action
        ).pack(side="left", padx=15)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=150,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#666666",
            hover_color="#888888",
            command=self.destroy
        ).pack(side="left", padx=15)
