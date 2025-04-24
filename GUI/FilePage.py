from tkinter import Frame, Label, Button
from .FileSelector import FileSelector
import threading

class FilePage(Frame):
    def __init__(self, master, on_play=None, on_pause=None, on_resume=None, on_stop=None):
        super().__init__(master)
        self.on_play = on_play
        self.on_pause = on_pause
        self.on_resume = on_resume
        self.on_stop = on_stop
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

    def _handle_file_select(self, file_path):
        """Handle file selection"""
        self.selected_file = file_path
        self.status_label.config(text=f"Selected: {file_path}")
        self.play_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.resume_btn.config(state="disabled")
        self.on_stop()
        self.is_playing = False

    def _handle_play(self):
        """Handle play button click"""
        if hasattr(self, 'selected_file'):
            if not self.is_playing:
                self.is_playing = True
                self.is_paused = False
                self.play_btn.config(state="disabled")
                self.pause_btn.config(state="normal")
                self.resume_btn.config(state="disabled")
                self.on_play(self.selected_file)

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
