from tkinter import Frame, Button, Label, filedialog, Listbox, Scrollbar, TclError
from typing import Callable, Optional, List
import os

class FileSelector(Frame):
    def __init__(self, master, on_file_select: Optional[Callable] = None):
        super().__init__(master)
        self.on_file_select = on_file_select
        
        # UI Elements
        self.label = Label(self, text="No directory selected")
        self.label.pack(pady=5)
        
        self.btn_select = Button(
            self,
            text="Select Directory",
            command=self._select_directory
        )
        self.btn_select.pack(pady=5)
        
        # File list components
        self.scrollbar = Scrollbar(self, orient="vertical")
        self.file_list = Listbox(
            self,
            yscrollcommand=self.scrollbar.set,
            selectmode="single"
        )
        self.scrollbar.config(command=self.file_list.yview)
        
        self.file_list.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.file_list.bind("<<ListboxSelect>>", self._on_file_select)
        
        self.selected_directory = None
        self.current_files: List[str] = []
    
    def _select_directory(self):
        """Open directory dialog and handle selection"""
        dir_path = filedialog.askdirectory(title="Select Directory")
        
        if dir_path:
            self.selected_directory = dir_path
            self.label.config(text=f"Selected: {dir_path}")
            self._update_file_list(dir_path)
    
    def _update_file_list(self, directory: str):
        """Update the file list with supported files from selected directory"""
        self.file_list.delete(0, "end")
        self.current_files.clear()
        
        try:
            files = os.listdir(directory)
            for file in sorted(files):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path) and file.lower().endswith(('.mid', '.midi', '.json')):
                    self.file_list.insert("end", file)
                    self.current_files.append(file)
        except (PermissionError, OSError) as e:
            self.label.config(text=f"Error: {str(e)}")
    
    def _on_file_select(self, event=None):
        """Handle file selection from list
        Args:
            event: Optional event parameter from Tkinter callback
        """
        try:
            selection = self.file_list.curselection()
            if selection and self.selected_directory:
                selected_file = self.current_files[selection[0]]
                full_path = os.path.join(self.selected_directory, selected_file)
                if self.on_file_select:
                    self.on_file_select(full_path)
        except TclError:
            pass
    
    def get_selected_file(self) -> Optional[str]:
        """Get currently selected file path"""
        if self.selected_directory and self.file_list.curselection():
            index = self.file_list.curselection()[0]
            return os.path.join(self.selected_directory, self.current_files[index])
        return None
