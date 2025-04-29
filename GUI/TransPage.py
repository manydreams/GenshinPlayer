from tkinter import Frame, Label, Button, Entry, Text, ttk, filedialog
from .FileSelector import FileSelector
from Instuments.Types import Types
import tkinter as tk
import os
import json
import trans

class TransPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the conversion page UI"""
        # File selector
        self.file_selector = FileSelector(
            self,
            on_file_select=self._handle_file_select
        )
        self.file_selector.pack(pady=20)

        # Status display
        self.status_label = Label(self, text="No file selected")
        self.status_label.pack(pady=10)

        # Parameter controls
        self.param_frame = Frame(self)
        self.param_frame.pack(pady=10)

        # Offset control
        Label(self.param_frame, text="Offset(half step):").pack(side="left")
        self.offset_entry = Entry(self.param_frame, width=5)
        self.offset_entry.insert(0, "0")
        self.offset_entry.pack(side="left", padx=5)
        
        # Instrument control
        Label(self.param_frame, text="Instrument:").pack(side="left")
        self.instrument_combobox = ttk.Combobox(self.param_frame, values=["Nightwind Horn", "Ukulele", "Windsong Lyre"])
        self.instrument_combobox.current(2)
        self.instrument_combobox.pack(side="left", padx=5)
        self.instrument_combobox.bind("<<ComboboxSelected>>", lambda e: self._handle_instrument_select())
        self._handle_instrument_select()

        # Convert button
        self.convert_btn = Button(
            self,
            text="Convert",
            state="disabled",
            command=self._handle_convert
        )
        self.convert_btn.pack(pady=10)

        # Result display frame
        result_frame = Frame(self)
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Text widget with scrollbar
        self.result_text = Text(
            result_frame, 
            height=10, 
            state="disabled",
            yscrollcommand=scrollbar.set
        )
        self.result_text.pack(side="left", fill="both", expand=True)
        
        scrollbar.config(command=self.result_text.yview)

        # Save button
        self.save_btn = Button(
            self,
            text="Save Result",
            state="disabled",
            command=self._handle_save
        )
        self.save_btn.pack(pady=10)

    def _handle_file_select(self, file_path: str):
        """Handle file selection"""
        if os.path.isfile(file_path) and file_path.lower().endswith(('.mid', '.midi')):
            self.selected_file = file_path
            self.status_label.config(text=f"Selected: {file_path}")
            self.convert_btn.config(state="normal")
        else:
            self.status_label.config(text="Please select a MIDI file")
            self.convert_btn.config(state="disabled")
        
    def _handle_instrument_select(self):
        """Handle instrument combobox selection"""
        self.selected_instrument = self.instrument_combobox.current()

    def _handle_convert(self):
        """Handle convert button click"""
        if hasattr(self, 'selected_file'):
            try:
                offset = int(self.offset_entry.get())
                match self.selected_instrument:
                    case Types.Horn.value:
                        self.result = trans.midi_to_horn(self.selected_file, offset)
                    case Types.Ukulele.value:
                        self.result = trans.midi_to_ukulele(self.selected_file, offset)
                    case Types.Lyre.value:
                        self.result = trans.midi_to_lyre(self.selected_file, offset)
                    case _:
                        pass
                self.result['instrument'] = self.selected_instrument
                
                self.result_text.config(state="normal")
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", json.dumps(self.result, indent=2))
                self.result_text.config(state="disabled")
                
                self.save_btn.config(state="normal")
                self.status_label.config(text="Conversion successful!")
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")

    def _handle_save(self):
        """Handle save button click"""
        if hasattr(self, 'result'):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")]
            )
            if file_path:
                try:
                    with open(file_path, 'w') as f:
                        json.dump(self.result, f, indent=2)
                    self.status_label.config(text=f"Saved to: {file_path}")
                except Exception as e:
                    self.status_label.config(text=f"Save error: {str(e)}")
