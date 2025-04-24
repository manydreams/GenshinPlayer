from GUI.Viewer import Viewer
from GUI.FilePage import FilePage
from Instuments.WindsongLyre import WindsongLyre
from Game import Game
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
        )
        self.window.add_page(self.file_page, "Music Player")
        self.window.show_page(0)

    def _handle_play(self, file_path):
        """Handle play button click"""
        self.melody = trans.midi_to_melody(file_path)
        self.game.show_window()
        self.windsong_lyre.play(self.melody, 86)

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
