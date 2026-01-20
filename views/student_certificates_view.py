"""Student certificates gallery view"""
import customtkinter as ctk
from PIL import Image
import os
import tkinter.messagebox as messagebox
from widgets import ConfirmDeleteDialog


class StudentCertificatesView(ctk.CTkFrame):
    """View displaying student's certificates in a gallery"""
    
    def __init__(self, parent, student, db, on_back):
        super().__init__(parent)
        self.student = student
        self.db = db
        self.on_back = on_back
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_content()
    
    def _create_content(self):
        """Create view content"""
        # Content frame
        content = ctk.CTkFrame(self)
        content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(2, weight=1)
        
        # Back button at the top
        ctk.CTkButton(
            content,
            text="← Back to Student Profiles",
            width=200,
            font=ctk.CTkFont(size=14),
            command=self.on_back
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Title
        ctk.CTkLabel(
            content,
            text=f"Certificates for {self.student[1]}",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=1, column=0, pady=10)
        
        # Get certificates for this student
        certificates = self.db.get_certificates_by_student(self.student[0])
        
        # Scrollable frame for certificates
        scroll_frame = ctk.CTkScrollableFrame(content)
        scroll_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        
        if not certificates:
            ctk.CTkLabel(
                scroll_frame,
                text="No certificates found for this student.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
        else:
            self._create_certificates_gallery(scroll_frame, certificates)
    
    def _create_certificates_gallery(self, content, certificates):
        """Create gallery of certificates"""
        # Gallery container with grid layout
        gallery_frame = ctk.CTkFrame(content, fg_color="transparent")
        gallery_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Display certificates in grid (2 columns)
        for idx, cert in enumerate(certificates):
            cert_id, student_id, image_path, note, created_at, student_name = cert
            
            # Calculate row and column
            row = idx // 2
            col = idx % 2
            
            # Create certificate card
            self._create_certificate_card(gallery_frame, cert, row, col)
        
        # Configure grid weights for responsive layout
        gallery_frame.grid_columnconfigure(0, weight=1)
        gallery_frame.grid_columnconfigure(1, weight=1)
    
    def _create_certificate_card(self, parent, cert, row, col):
        """Create a single certificate card"""
        cert_id, student_id, image_path, note, created_at, student_name = cert
        
        # Certificate card
        card = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=10)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Image container
        image_container = ctk.CTkFrame(card, fg_color="#1a1a1a", corner_radius=8)
        image_container.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Display certificate image
        self._display_certificate_image(image_container, image_path)
        
        # Note section
        self._create_note_section(card, note, created_at)
        
        # Delete button
        ctk.CTkButton(
            card,
            text="🗑 Delete",
            font=ctk.CTkFont(size=12),
            width=100,
            height=30,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=lambda: self._delete_certificate(cert_id)
        ).pack(pady=(0, 10))
    
    def _display_certificate_image(self, container, image_path):
        """Display the certificate image"""
        if image_path and os.path.exists(image_path):
            try:
                # Load and display image
                if image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    img = Image.open(image_path)
                    img.thumbnail((350, 300))
                    photo = ctk.CTkImage(light_image=img, dark_image=img, size=(350, 300))
                    img_label = ctk.CTkLabel(
                        container,
                        image=photo,
                        text=""
                    )
                    img_label.image = photo
                    img_label.pack(pady=10)
                else:
                    # For PDF or other files
                    ctk.CTkLabel(
                        container,
                        text=f"📄 {os.path.basename(image_path)}",
                        font=ctk.CTkFont(size=14)
                    ).pack(pady=50)
            except Exception as e:
                ctk.CTkLabel(
                    container,
                    text=f"❌ Error loading image",
                    font=ctk.CTkFont(size=12),
                    text_color="red"
                ).pack(pady=50)
        else:
            ctk.CTkLabel(
                container,
                text="❌ Image not found",
                font=ctk.CTkFont(size=12),
                text_color="red"
            ).pack(pady=50)
    
    def _create_note_section(self, card, note, created_at):
        """Create note display section"""
        note_frame = ctk.CTkFrame(card, fg_color="transparent")
        note_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Date label
        ctk.CTkLabel(
            note_frame,
            text=f"Added: {created_at[:10]}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w", pady=(5, 5))
        
        # Note content
        if note:
            ctk.CTkLabel(
                note_frame,
                text="Note:",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(anchor="w", pady=(5, 2))
            
            note_textbox = ctk.CTkTextbox(
                note_frame,
                height=60,
                font=ctk.CTkFont(size=11),
                wrap="word",
                state="disabled"
            )
            note_textbox.pack(fill="x", pady=2)
            note_textbox.configure(state="normal")
            note_textbox.insert("1.0", note)
            note_textbox.configure(state="disabled")
        else:
            ctk.CTkLabel(
                note_frame,
                text="No note added",
                font=ctk.CTkFont(size=11),
                text_color="gray"
            ).pack(anchor="w", pady=5)
    
    def _delete_certificate(self, cert_id):
        """Delete a certificate after confirmation"""
        def delete_confirmed():
            """Execute deletion after confirmation"""
            success, message = self.db.delete_certificate(cert_id)
            if success:
                # Refresh the certificates view
                for widget in self.winfo_children():
                    widget.destroy()
                self._create_content()
            else:
                messagebox.showerror("Error", f"Failed to delete certificate: {message}")
        
        # Show confirmation dialog
        ConfirmDeleteDialog(
            self,
            title="Confirm Delete",
            main_message="Are you sure you want to delete\nthis certificate?",
            warning_message="This action cannot be undone!",
            on_confirm=delete_confirmed
        )
