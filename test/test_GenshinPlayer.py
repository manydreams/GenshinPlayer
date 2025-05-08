import unittest
from unittest.mock import patch, MagicMock
from GenshinPlayer import GenshinPlayer
from Instuments.Types import Types

class TestGenshinPlayer(unittest.TestCase):
    def setUp(self):
        # Mock all dependencies
        self.game_patch = patch('GenshinPlayer.Game')
        self.mock_game = self.game_patch.start()
        
        self.lyre_patch = patch('GenshinPlayer.WindsongLyre')
        self.mock_lyre = self.lyre_patch.start()
        
        self.ukulele_patch = patch('GenshinPlayer.Ukulele')
        self.mock_ukulele = self.ukulele_patch.start()
        
        self.horn_patch = patch('GenshinPlayer.NightwindHorn')
        self.mock_horn = self.horn_patch.start()
        
        self.viewer_patch = patch('GenshinPlayer.Viewer')
        self.mock_viewer = self.viewer_patch.start()
        
        self.filepage_patch = patch('GenshinPlayer.FilePage')
        self.mock_filepage = self.filepage_patch.start()
        
        self.transpage_patch = patch('GenshinPlayer.TransPage')
        self.mock_transpage = self.transpage_patch.start()

    def tearDown(self):
        self.game_patch.stop()
        self.lyre_patch.stop()
        self.ukulele_patch.stop()
        self.horn_patch.stop()
        self.viewer_patch.stop()
        self.filepage_patch.stop()
        self.transpage_patch.stop()

    def test_initialization(self):
        """Test program initialization and instrument setup"""
        player = GenshinPlayer()
        
        # Verify game and instruments were created
        self.mock_game.assert_called_once()
        self.mock_lyre.assert_called_once_with(self.mock_game.return_value)
        self.mock_ukulele.assert_called_once_with(self.mock_game.return_value)
        self.mock_horn.assert_called_once_with(self.mock_game.return_value)
        
        # Verify default instrument
        self.assertEqual(player.current_instument, self.mock_lyre.return_value)

    def test_run_setup(self):
        """Test main window setup"""
        player = GenshinPlayer()
        player.run()
        
        # Verify viewer was created with correct title
        self.mock_viewer.assert_called_once_with(title="Genshin Lyre Player")
        
        # Verify pages were added
        viewer_instance = self.mock_viewer.return_value
        self.assertEqual(viewer_instance.add_page.call_count, 2)
        
        # Verify first page is shown
        viewer_instance.show_page.assert_called_once_with(0)

    def test_page_setup(self):
        """Test page creation and configuration"""
        player = GenshinPlayer()
        player.run()
        
        # Verify FilePage was created with correct callbacks
        self.mock_filepage.assert_called_once()
        filepage_args = self.mock_filepage.call_args[1]
        self.assertEqual(filepage_args['on_play'], player._handle_play)
        self.assertEqual(filepage_args['on_pause'], player._handle_pause)
        self.assertEqual(filepage_args['on_resume'], player._handle_resume)
        self.assertEqual(filepage_args['on_stop'], player._handle_stop)
        self.assertEqual(filepage_args['on_bpm_change'], player._handle_bpm_change)
        self.assertEqual(filepage_args['on_instrument_change'], player._handle_instrument_change)
        self.assertEqual(filepage_args['update_melody'], player._handle_melody_change)
        
        # Verify TransPage was created
        self.mock_transpage.assert_called_once()

    def test_instrument_change(self):
        """Test instrument change handling"""
        player = GenshinPlayer()
        
        # Test Lyre selection
        player._handle_instrument_change(Types.Lyre.value)
        self.assertEqual(player.current_instument, self.mock_lyre.return_value)
        
        # Test Ukulele selection
        player._handle_instrument_change(Types.Ukulele.value)
        self.assertEqual(player.current_instument, self.mock_ukulele.return_value)
        
        # Test Horn selection
        player._handle_instrument_change(Types.Horn.value)
        self.assertEqual(player.current_instument, self.mock_horn.return_value)

    def test_playback_handlers(self):
        """Test playback event handlers"""
        player = GenshinPlayer()
        player.melody = [[0.0, "set_bpm", 120], [0.0, "C5", True]]
        
        # Test play handler
        player._handle_play()
        self.mock_game.return_value.show_window.assert_called_once()
        player.current_instument.play_new_thread.assert_called_once_with(player.melody)
        
        # Test pause handler
        player._handle_pause()
        player.current_instument.pause.assert_called_once()
        
        # Test resume handler
        player._handle_resume()
        self.mock_game.return_value.show_window.assert_called()
        player.current_instument.resume.assert_called_once()
        
        # Test stop handler
        player._handle_stop()
        player.current_instument.stop.assert_called_once()

    def test_main_loop(self):
        """Test main loop execution"""
        player = GenshinPlayer()
        player.run()
        
        # Verify mainloop was called
        self.mock_viewer.return_value.mainloop.assert_called_once()

if __name__ == '__main__':
    unittest.main()
