from tkinter import Frame, Button, Label, filedialog
from typing import Callable, Optional

class FileSelector(Frame):
    def __init__(self, master, on_file_select: Optional[Callable] = None):
        super().__init__(master)
        self.on_file_select = on_file_select
        
        # UI Elements
        self.label = Label(self, text="No file selected")
        self.label.pack(pady=10)
        
        self.btn_select = Button(
            self,
            text="Select File",
            command=self._select_file
        )
        self.btn_select.pack(pady=5)
        
        self.selected_file = None
    
    def _select_file(self):
        """Open file dialog and handle selection"""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("All Files", "*.*")]
        )
        
        if file_path:
            self.selected_file = file_path
            self.label.config(text=f"Selected: {file_path}")
            
            if self.on_file_select:
                self.on_file_select(file_path)
    
    def get_selected_file(self) -> Optional[str]:
        """Get currently selected file path"""
        return self.selected_file
