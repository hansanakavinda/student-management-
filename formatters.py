"""Centralized formatting module for Student Management System"""
import re


class Formatters:
    """Collection of formatting functions for auto-formatting input fields"""
    
    @staticmethod
    def format_date(text, event_widget=None):
        """
        Auto-format date as YYYY-MM-DD while typing
        Removes non-digits and inserts hyphens at correct positions
        
        Args:
            text: Current text in the field
            event_widget: The widget (Entry) being formatted (optional, for cursor positioning)
            
        Returns:
            Formatted date string
        """
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, text))
        
        # Limit to 8 digits (YYYYMMDD)
        if len(digits_only) > 8:
            digits_only = digits_only[:8]
        
        # Format as YYYY-MM-DD
        formatted = digits_only
        if len(digits_only) > 4:
            formatted = digits_only[:4] + "-" + digits_only[4:]
        if len(digits_only) > 6:
            formatted = digits_only[:4] + "-" + digits_only[4:6] + "-" + digits_only[6:]
        
        return formatted
    
    @staticmethod
    def format_contact_number(text, max_digits=10):
        """
        Format contact number - digits only, limited to max_digits
        
        Args:
            text: Current text in the field
            max_digits: Maximum number of digits allowed
            
        Returns:
            Formatted contact string (digits only)
        """
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, text))
        
        # Limit to max_digits
        if len(digits_only) > max_digits:
            digits_only = digits_only[:max_digits]
        
        return digits_only
    
    @staticmethod
    def format_nic(text, max_digits=12):
        """
        Format NIC - digits only, limited to max_digits
        
        Args:
            text: Current text in the field
            max_digits: Maximum number of digits allowed
            
        Returns:
            Formatted NIC string (digits only)
        """
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, text))
        
        # Limit to max_digits
        if len(digits_only) > max_digits:
            digits_only = digits_only[:max_digits]
        
        return digits_only
    
    @staticmethod
    def format_name(text):
        """
        Format name - letters, spaces, and periods only
        
        Args:
            text: Current text in the field
            
        Returns:
            Formatted name string (letters, spaces, and periods only)
        """
        # Keep only letters, spaces, and periods
        formatted = ''.join(char for char in text if char.isalpha() or char.isspace() or char == '.')
        
        # Replace multiple spaces with single space
        formatted = re.sub(r'\s+', ' ', formatted)
        
        return formatted
    
    @staticmethod
    def format_year(text, max_digits=4):
        """
        Format year - digits only, limited to max_digits
        
        Args:
            text: Current text in the field
            max_digits: Maximum number of digits allowed
            
        Returns:
            Formatted year string (digits only)
        """
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, text))
        
        # Limit to max_digits
        if len(digits_only) > max_digits:
            digits_only = digits_only[:max_digits]
        
        return digits_only
    
    @staticmethod
    def format_marks(text):
        """
        Format marks - allow digits and decimal point for numbers 0-100
        
        Args:
            text: Current text in the field
            
        Returns:
            Formatted marks string
        """
        # Allow digits and one decimal point
        # Remove any character that's not a digit or decimal point
        formatted = ''.join(char for char in text if char.isdigit() or char == '.')
        
        # Ensure only one decimal point
        if formatted.count('.') > 1:
            # Keep only the first decimal point
            parts = formatted.split('.')
            formatted = parts[0] + '.' + ''.join(parts[1:])
        
        # Limit to reasonable length (3 digits + decimal + 2 decimals = "100.00")
        if len(formatted) > 6:
            formatted = formatted[:6]
        
        # Check if value exceeds 100
        try:
            if formatted and float(formatted) > 100:
                formatted = "100"
        except ValueError:
            pass
        
        return formatted
    
    @staticmethod
    def apply_date_formatting(entry_widget):
        """
        Apply date formatting to an Entry widget
        Sets up event binding for auto-formatting
        
        Args:
            entry_widget: CTkEntry widget to apply formatting to
        """
        def on_key_release(event):
            current_text = entry_widget.get()
            current_pos = entry_widget.index("insert")
            
            formatted = Formatters.format_date(current_text)
            
            if current_text != formatted:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, formatted)
                
                # Adjust cursor position for hyphens
                new_pos = current_pos
                if current_pos == 5 and len(current_text) > 4:
                    new_pos = 5  # After first hyphen
                elif current_pos == 8 and len(current_text) > 6:
                    new_pos = 8  # After second hyphen
                
                try:
                    entry_widget.icursor(min(new_pos, len(formatted)))
                except:
                    pass
        
        entry_widget.bind('<KeyRelease>', on_key_release)
    
    @staticmethod
    def apply_contact_formatting(entry_widget, max_digits=10):
        """
        Apply contact number formatting to an Entry widget
        
        Args:
            entry_widget: CTkEntry widget to apply formatting to
            max_digits: Maximum number of digits allowed
        """
        def on_key_release(event):
            current_text = entry_widget.get()
            current_pos = entry_widget.index("insert")
            
            formatted = Formatters.format_contact_number(current_text, max_digits)
            
            if current_text != formatted:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, formatted)
                try:
                    entry_widget.icursor(min(current_pos, len(formatted)))
                except:
                    pass
        
        entry_widget.bind('<KeyRelease>', on_key_release)
    
    @staticmethod
    def apply_nic_formatting(entry_widget, max_digits=12):
        """
        Apply NIC formatting to an Entry widget
        
        Args:
            entry_widget: CTkEntry widget to apply formatting to
            max_digits: Maximum number of digits allowed
        """
        def on_key_release(event):
            current_text = entry_widget.get()
            current_pos = entry_widget.index("insert")
            
            formatted = Formatters.format_nic(current_text, max_digits)
            
            if current_text != formatted:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, formatted)
                try:
                    entry_widget.icursor(min(current_pos, len(formatted)))
                except:
                    pass
        
        entry_widget.bind('<KeyRelease>', on_key_release)
    
    @staticmethod
    def apply_name_formatting(entry_widget):
        """
        Apply name formatting to an Entry widget
        
        Args:
            entry_widget: CTkEntry widget to apply formatting to
        """
        def on_key_release(event):
            current_text = entry_widget.get()
            current_pos = entry_widget.index("insert")
            
            formatted = Formatters.format_name(current_text)
            
            if current_text != formatted:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, formatted)
                try:
                    entry_widget.icursor(min(current_pos, len(formatted)))
                except:
                    pass
        
        entry_widget.bind('<KeyRelease>', on_key_release)
    
    @staticmethod
    def apply_year_formatting(entry_widget, max_digits=4):
        """
        Apply year formatting to an Entry widget
        
        Args:
            entry_widget: CTkEntry widget to apply formatting to
            max_digits: Maximum number of digits allowed
        """
        def on_key_release(event):
            current_text = entry_widget.get()
            current_pos = entry_widget.index("insert")
            
            formatted = Formatters.format_year(current_text, max_digits)
            
            if current_text != formatted:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, formatted)
                try:
                    entry_widget.icursor(min(current_pos, len(formatted)))
                except:
                    pass
        
        entry_widget.bind('<KeyRelease>', on_key_release)
    
    @staticmethod
    def apply_marks_formatting(entry_widget):
        """
        Apply marks formatting to an Entry widget
        
        Args:
            entry_widget: CTkEntry widget to apply formatting to
        """
        def on_key_release(event):
            current_text = entry_widget.get()
            current_pos = entry_widget.index("insert")
            
            formatted = Formatters.format_marks(current_text)
            
            if current_text != formatted:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, formatted)
                try:
                    entry_widget.icursor(min(current_pos, len(formatted)))
                except:
                    pass
        
        entry_widget.bind('<KeyRelease>', on_key_release)
