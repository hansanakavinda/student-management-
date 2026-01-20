"""Reusable UI widgets for the Student Management System"""
import customtkinter as ctk
from typing import Callable, Optional
from PIL import Image, ImageTk
import tkinter as tk
import os


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
        self.is_destroyed = False
        
        # Center window first
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Grab and focus after positioning
        self.grab_set()
        # Use after() to delay focus to avoid race condition
        self.after(10, self._set_focus)
        
        # Content frame (scrollable)
        self.content = ctk.CTkScrollableFrame(self)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)
    
    def _set_focus(self):
        """Safely set focus if window still exists"""
        if not self.is_destroyed:
            try:
                self.focus_force()
            except:
                pass
    
    def _safe_destroy(self):
        """Safely destroy the dialog"""
        if not self.is_destroyed:
            self.is_destroyed = True
            try:
                self.grab_release()
            except:
                pass
            try:
                self.destroy()
            except:
                pass
    
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
            command=cancel_command or self._safe_destroy
        ).pack(side="left", padx=10)


class ConfirmDeleteDialog(ctk.CTkToplevel):
    """Reusable confirmation dialog for delete operations"""
    
    def __init__(self, parent, title: str, main_message: str, 
                 warning_message: str, on_confirm, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.title(title)
        self.geometry("500x380")
        self.is_destroyed = False
        
        # Center window first
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 250
        y = (self.winfo_screenheight() // 2) - 190
        self.geometry(f"500x380+{x}+{y}")
        
        # Grab and focus after positioning
        self.grab_set()
        # Use after() to delay focus to avoid race condition
        self.after(10, self._set_focus)
        
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
            self._safe_destroy()
        
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
            command=self._safe_destroy
        ).pack(side="left", padx=15)
    
    def _set_focus(self):
        """Safely set focus if window still exists"""
        if not self.is_destroyed:
            try:
                # Check if window still exists before focusing
                if self.winfo_exists():
                    self.focus_force()
            except:
                pass
    
    def _safe_destroy(self):
        """Safely destroy the dialog"""
        if not self.is_destroyed:
            self.is_destroyed = True
            try:
                self.grab_release()
            except:
                pass
            try:
                self.destroy()
            except:
                pass


class WatermarkWidget(ctk.CTkLabel):
    """Reusable watermark widget that displays a logo with configurable opacity"""
    
    def __init__(self, parent, image_path: str = "logo.png", opacity: float = 0.3, 
                 size: tuple = None, **kwargs):
        from utils import resource_path
        """
        Create a watermark widget with logo image
        
        Args:
            parent: Parent widget
            image_path: Path to the logo image file
            opacity: Opacity level (0.0 to 1.0), default 0.3
            size: Tuple (width, height) for image size, if None uses original size
            **kwargs: Additional CTkLabel arguments
        """
        super().__init__(parent, text="", **kwargs)
        
        self.image_path = image_path
        self.opacity = max(0.0, min(1.0, opacity))  # Clamp between 0 and 1
        self.size = size
        self.photo = None
        
        # Load and display the watermark
        self._load_watermark()
    
    def _load_watermark(self):
        """Load and process the watermark image"""
        from utils import resource_path
        try:
            resolved_path = resource_path(self.image_path)
            if not os.path.exists(resolved_path):
                self.configure(text="Logo not found", text_color="gray")
                return
            
            # Load image with PIL
            img = Image.open(resolved_path)
            
            # Resize if size is specified
            if self.size:
                img = img.resize(self.size, Image.Resampling.LANCZOS)
            
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Adjust opacity
            alpha = img.split()[3]
            alpha = alpha.point(lambda p: int(p * self.opacity))
            img.putalpha(alpha)
            
            # Convert to CTkImage for customtkinter
            self.photo = ctk.CTkImage(light_image=img, dark_image=img, 
                                     size=self.size if self.size else img.size)
            self.configure(image=self.photo)
            
        except Exception as e:
            self.configure(text=f"Error loading logo: {e}", text_color="red")
    
    def update_opacity(self, new_opacity: float):
        """Update the watermark opacity"""
        self.opacity = max(0.0, min(1.0, new_opacity))
        self._load_watermark()


class ToolTip:
    """Tooltip widget that displays text on hover"""
    
    def __init__(self, widget, text: str):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        
        # Bind hover events
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        """Show the tooltip"""
        if self.tooltip_window or not self.text:
            return
        
        # Get widget position
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        # Create tooltip window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Create label with text
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#ffffe0",
            foreground="#000000",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10),
            padx=5,
            pady=3
        )
        label.pack()
    
    def hide_tooltip(self, event=None):
        """Hide the tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def truncate_text(text: str, max_length: int = 25) -> str:
    """
    Truncate text to a maximum length, adding '...' if truncated
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        
    Returns:
        Truncated text with '...' if needed
    """
    if not text:
        return ""
    
    text = str(text)
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def create_label_with_tooltip(parent, text: str, max_length: int = 25, **label_kwargs):
    """
    Create a label with truncated text and tooltip showing full text
    
    Args:
        parent: Parent widget
        text: Text to display
        max_length: Maximum length before truncation
        **label_kwargs: Additional arguments for CTkLabel
        
    Returns:
        CTkLabel widget with tooltip
    """
    full_text = str(text) if text else ""
    display_text = truncate_text(full_text, max_length)
    
    label = ctk.CTkLabel(parent, text=display_text, **label_kwargs)
    
    # Add tooltip if text was truncated
    if len(full_text) > max_length:
        ToolTip(label, full_text)
    
    return label
