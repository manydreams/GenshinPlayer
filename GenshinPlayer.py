from GUI.Viewer import Viewer
from GUI.FilePage import FilePage
from GUI.TransPage import TransPage
from Instuments.WindsongLyre import WindsongLyre
from Instuments.Ukulele import Ukulele
from Instuments.NightwindHorn import NightwindHorn
from Instuments.Types import Types
from Game import Game


class GenshinPlayer:
    def __init__(self):
        self.game = Game()
        self.windsong_lyre = WindsongLyre(self.game)
        self.ukulele = Ukulele(self.game)
        self.nightwind_horn = NightwindHorn(self.game)
        self.current_instument = self.windsong_lyre
        
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
            on_instrument_change=self._handle_instrument_change,
            update_melody=self._handle_melody_change
        )
        self.window.add_page(self.file_page, "Music Player")
        
        # Add standalone trans page
        self.trans_page = TransPage(self.window.page_container)
        self.window.add_page(self.trans_page, "Translation")
        
        self.window.show_page(0)
        self.current_bpm = 120

    def _handle_bpm_change(self, bpm):
        """Handle BPM parameter change"""
        self.current_bpm = bpm
        
    def _handle_instrument_change(self, instrument):
        """Handle instrument change"""
        match instrument:
            case Types.Horn.value:
                self.current_instument = self.nightwind_horn
            case Types.Ukulele.value:
                self.current_instument = self.ukulele
            case Types.Lyre.value:
                self.current_instument = self.windsong_lyre
        
    def _handle_melody_change(self, melody):
        """Handle melody change"""
        self.melody = melody

    def _handle_play(self):
        """Handle play button click"""
        self.game.show_window()
        self.current_instument.play_new_thread(self.melody, self.current_bpm)

    def _handle_pause(self):
        """Handle pause button click"""
        self.current_instument.pause()

    def _handle_resume(self):
        """Handle resume button click"""
        self.game.show_window()
        self.current_instument.resume()
    
    def _handle_stop(self):
        """Handle stop button click"""
        self.current_instument.stop()

    def run(self):
        """Start the application"""
        self.window = Viewer(title="Genshin Lyre Player")
        self._setup_main_page()
        input("Press any key to exit...")
