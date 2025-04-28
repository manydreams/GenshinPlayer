from tkinter import Frame, Label, Button, Entry, ttk
from .FileSelector import FileSelector

import trans
import tkinter as tk
import os
import json

class FilePage(Frame):
    def __init__(self, master, on_play=None, on_pause=None, on_resume=None,
                 on_stop=None, on_bpm_change=None, on_offset_change=None,
                 on_instrument_change=None, update_melody=None):
        super().__init__(master)
        self.on_play = on_play
        self.on_pause = on_pause
        self.on_resume = on_resume
        self.on_stop = on_stop
        self.on_bpm_change = on_bpm_change
        self.on_offset_change = on_offset_change
        self.on_instrument_change = on_instrument_change
        self.update_melody = update_melody
        self.is_playing = False
        self.is_paused = False
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the page UI"""
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

        # BPM control
        Label(self.param_frame, text="BPM:").pack(side="left")
        self.bpm_entry = Entry(self.param_frame, width=5)
        self.bpm_entry.insert(0, "120")
        self.bpm_entry.pack(side="left", padx=5)
        self.bpm_entry.bind("<Return>", lambda e: self._update_bpm())
        self._update_bpm()

        # Offset control
        Label(self.param_frame, text="Offset(half step):").pack(side="left")
        self.offset_entry = Entry(self.param_frame, width=5)
        self.offset_entry.insert(0, "0")
        self.offset_entry.pack(side="left", padx=5)
        self.offset_entry.bind("<Return>", lambda e: self._update_offset())
        self._update_offset()
        
        # Instrument control
        Label(self.param_frame, text="Instrument:").pack(side="left")
        self.instrument_combobox = ttk.Combobox(self.param_frame, values=["Nightwind Horn", "Ukulele", "Windsong Lyre"])
        self.instrument_combobox.current(2)
        self.instrument_combobox.pack(side="left", padx=5)
        self.instrument_combobox.bind("<<ComboboxSelected>>", lambda e: self._update_instrument())
        self._update_instrument()

        # Play/Pause/Resume buttons
        self.control_frame = Frame(self)
        self.control_frame.pack(pady=10)
        
        self.play_btn = Button(
            self.control_frame,
            text="Play",
            state="disabled",
            command=self._handle_play
        )
        self.play_btn.pack(side="left", padx=5)
        
        self.pause_btn = Button(
            self.control_frame,
            text="Pause",
            state="disabled",
            command=self._handle_pause
        )
        self.pause_btn.pack(side="left", padx=5)

        self.resume_btn = Button(
            self.control_frame,
            text="Resume",
            state="disabled",
            command=self._handle_resume
        )
        self.resume_btn.pack(side="left", padx=5)

    def _handle_file_select(self, file_path: str):
        """Handle file selection"""
        if os.path.isfile(file_path):
            bpm = None
            melody = None
            if file_path.lower().endswith(('.mid', '.midi')):
                try:
                    # Parse and store melody data with current offset
                    melody_data = trans.midi_to_lyre(file_path, self.current_offset)
                    if melody_data and 'bpm' in melody_data and melody_data['bpm']:
                        bpm = melody_data['bpm']
                    if melody_data and'melody' in melody_data and melody_data['melody']:
                        melody = melody_data['melody']
                    self.instrument_combobox.current(2)
                    self.instrument_combobox.config(state="normal")
                    self._update_instrument()
                except Exception as e:
                    print(f"Error processing MIDI file: {e}")
            elif file_path.lower().endswith('json'):
                try:
                    with open(file_path, 'r') as f:
                        lyre_config = json.load(f)
                    if 'bpm' in lyre_config and lyre_config['bpm']:
                        bpm = lyre_config['bpm']
                    if 'melody' in lyre_config and lyre_config['melody']:
                        melody = lyre_config['melody']
                    
                    if 'instrument' in lyre_config and lyre_config['instrument'] != None:
                        self.instrument_combobox.current(lyre_config['instrument'])
                        self.instrument_combobox.config(state="disabled")
                        self._update_instrument()
                except Exception as e:
                    print("Error loading music score:", e)
                    self.instrument_combobox.current(2)
                    self.instrument_combobox.config(state="normal")
                    self._update_instrument()
            
            if bpm:
                self.bpm_entry.delete(0, tk.END)
                self.bpm_entry.insert(0, str(bpm))
                self._update_bpm()
            if melody:
                self.update_melody(melody)

            
            self.selected_file = file_path
            self.status_label.config(text=f"Selected: {file_path}")
            if bpm and melody:
                self.play_btn.config(state="normal")
            else:
                self.play_btn.config(state="disabled")
            self.pause_btn.config(state="disabled")
            self.resume_btn.config(state="disabled")
            self.on_stop()
            self.is_playing = False

    def _handle_play(self):
        """Handle play button click"""
        if not self.is_playing:
            self.is_playing = True
            self.is_paused = False
            self.play_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.resume_btn.config(state="disabled")
            self.on_play()

    def _handle_pause(self):
        """Handle pause button click"""
        if self.is_playing and self.on_pause:
            self.is_paused = True
            self.play_btn.config(state="disabled")
            self.pause_btn.config(state="disabled")
            self.resume_btn.config(state="normal")
            self.on_pause()

    def _handle_resume(self):
        """Handle resume button click"""
        if self.is_paused and self.on_resume:
            self.is_paused = False
            self.play_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.resume_btn.config(state="disabled")
            self.on_resume()

    def _update_bpm(self):
        """Update BPM parameter with validation"""
        try:
            value = float(self.bpm_entry.get())
            if self.on_bpm_change:
                self.on_bpm_change(value)
        except ValueError:
            self.bpm_entry.delete(0, tk.END)        

    def _update_offset(self):
        """Update offset parameter with validation"""
        try:
            value = int(self.offset_entry.get())
            self.current_offset = value
            if self.on_offset_change:
                self.on_offset_change(self.current_offset)
        except ValueError:
            self.offset_entry.delete(0, "end")
            self.offset_entry.insert(0, str(self.current_offset))
    
    def _update_instrument(self):
        """Update instrument parameter"""
        try:
            value = self.instrument_combobox.current()
            if self.on_instrument_change:
                self.on_instrument_change(value)
        except ValueError:
            pass
