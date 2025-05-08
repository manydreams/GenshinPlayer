import unittest
from unittest.mock import MagicMock, patch
import time
from Game import Game
from Instuments.WindsongLyre import WindsongLyre
from Instuments.Ukulele import Ukulele
from Instuments.NightwindHorn import NightwindHorn

class TestWindsongLyre(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock(spec=Game)
        self.lyre = WindsongLyre(self.mock_game)
        self.test_melody = [
            (0.0, "set_bpm", 120),
            (0.0, "C4", True),
            (0.5, "C4", False),
            (1.0, "D4", True),
            (1.5, "D4", False)
        ]

    def test_single_note_play(self):
        """Test playing a single note"""
        melody = [
            (0.0, "set_bpm", 120),
            (0.0, "C4", True),
            (0.5, "C4", False)
        ]
        self.lyre.play(melody)
        
        # Verify key press/release sequence
        self.mock_game.key_press.assert_any_call('z')
        self.mock_game.key_release.assert_any_call('z')

    def test_note_sequence_play(self):
        """Test playing a sequence of notes"""
        self.lyre.play(self.test_melody)
        
        # Verify all notes were played
        self.mock_game.key_press.assert_any_call('z')
        self.mock_game.key_press.assert_any_call('x')
        self.mock_game.key_release.assert_any_call('z')
        self.mock_game.key_release.assert_any_call('x')

    def test_play_with_different_bpm_in_melody(self):
        """Test playing with different BPM values in melody"""
        fast_melody = [
            (0.0, "set_bpm", 240),
            (0.0, "C4", True),
            (0.5, "C4", False)
        ]
        self.lyre.play(fast_melody)

        slow_melody = [
            (0.0, "set_bpm", 60),
            (0.0, "C4", True),
            (0.5, "C4", False)
        ]
        self.lyre.play(slow_melody)

    def test_pause_and_resume(self):
        """Test pause and resume functionality"""
        # Start playback in thread
        self.lyre.play_new_thread(self.test_melody)
        time.sleep(0.1)  # Allow thread to start
        
        # Pause and verify
        self.lyre.pause()
        self.assertTrue(self.lyre._play_event.is_set() == False)
        
        # Resume and verify
        self.lyre.resume()
        self.assertTrue(self.lyre._play_event.is_set())
        
        # Stop playback
        self.lyre.stop()

    def test_stop_playback(self):
        """Test stopping playback"""
        self.lyre.play_new_thread(self.test_melody)
        time.sleep(0.1)  # Allow thread to start
        self.lyre.stop()
        self.assertTrue(self.lyre._stop_playback)

class TestUkulele(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock(spec=Game)
        self.ukulele = Ukulele(self.mock_game)
        self.test_melody = [
            (0.0, "set_bpm", 120),
            (0.0, "C5", True),
            (0.5, "C5", False),
            (1.0, "D5", True),
            (1.5, "D5", False)
        ]

    def test_single_note_play(self):
        """Test playing a single note"""
        melody = [
            (0.0, "set_bpm", 120),
            (0.0, "C5", True),
            (0.5, "C5", False)
        ]
        self.ukulele.play(melody)
        self.mock_game.key_press.assert_any_call('z')
        self.mock_game.key_release.assert_any_call('z')

    def test_chord_play(self):
        """Test playing chords"""
        chord_melody = [
            (0.0, "set_bpm", 120),
            (0.0, "CM", True),
            (1.0, "CM", False)
        ]
        self.ukulele.play(chord_melody)
        self.mock_game.key_press.assert_any_call('q')

class TestNightwindHorn(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock(spec=Game)
        self.horn = NightwindHorn(self.mock_game)
        self.test_melody = [
            (0.0, "set_bpm", 120),
            (0.0, "C4", True),
            (0.5, "C4", False),
            (1.0, "D4", True),
            (1.5, "D4", False)
        ]

    def test_single_note_play(self):
        """Test playing a single note"""
        melody = [
            (0.0, "set_bpm", 120),
            (0.0, "C4", True),
            (0.5, "C4", False)
        ]
        self.horn.play(melody)
        self.mock_game.key_press.assert_any_call('a')
        self.mock_game.key_release.assert_any_call('a')

    def test_concurrent_notes(self):
        """Test handling of concurrent notes"""
        concurrent_melody = [
            (0.0, "set_bpm", 120),
            (0.0, "C4", True),
            (0.1, "D4", True),
            (0.5, "C4", False),
            (0.6, "D4", False)
        ]
        self.horn.play(concurrent_melody)
        self.assertGreaterEqual(self.mock_game.key_press.call_count, 2)

if __name__ == '__main__':
    unittest.main()
