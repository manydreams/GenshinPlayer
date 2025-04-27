from GUI.Viewer import Viewer
from GUI.FilePage import FilePage
from Instuments.WindsongLyre import WindsongLyre
from Game import Game
from tkinter import simpledialog
from tkinter import Tk
import trans


class GenshinPlayer:
    def __init__(self):
        self.game = Game()
        self.windsong_lyre = WindsongLyre(self.game)
        
    def _setup_main_page(self):
        """Setup the main application page"""
        # Create and register file page with playback controls
        self.file_page = FilePage(
            self.window.page_container,
            on_play=self._handle_play,
            on_pause=self._handle_pause,
            on_resume=self._handle_resume,
            on_stop=self._handle_stop,
            on_bpm_change=self._handle_bpm_change,
            on_offset_change=self._handle_offset_change,
            update_melody=self._handle_melody_change
        )
        self.window.add_page(self.file_page, "Music Player")
        self.window.show_page(0)
        self.current_bpm = 120
        self.current_offset = 0

    def _handle_bpm_change(self, bpm):
        """Handle BPM parameter change"""
        self.current_bpm = bpm

    def _handle_offset_change(self, offset):
        """Handle offset parameter change"""
        self.current_offset = offset
        
    def _handle_melody_change(self, melody):
        """Handle melody change"""
        self.melody = melody

    def _handle_play(self):
        """Handle play button click"""
        self.game.show_window()
        self.windsong_lyre.play_new_thread(self.melody, self.current_bpm)

    def _handle_pause(self):
        """Handle pause button click"""
        self.windsong_lyre.pause()

    def _handle_resume(self):
        """Handle resume button click"""
        self.game.show_window()
        self.windsong_lyre.resume()
    
    def _handle_stop(self):
        """Handle stop button click"""
        self.windsong_lyre.stop()

    def run(self):
        """Start the application"""
        self.window = Viewer(title="Genshin Lyre Player")
        self._setup_main_page()
        input("Press any key to exit...")
