import unittest
from Game import Game
from unittest.mock import patch
from Instuments import WindsongLyre

class TestInstuments(unittest.TestCase):
    pass

class TestWindsongLyre(unittest.TestCase):
    
    @patch.object(Game, "__init__", lambda self: None)
    def setUp(self):
        self.lyre = WindsongLyre.WindsongLyre(Game())
    
    def tearDown(self):
        del self.lyre
        
    @patch.object(Game, "key_press")
    @patch.object(Game, "key_release")
    @patch.object(WindsongLyre.WindsongLyre, "_WindsongLyre__key_map", lambda self, note: note)
    def test_play_single_note(self, mock_key_release, mock_key_press):
        notes = [i + j for j in "456" for i in "cdefgabCDEFGAB"]
        for note in notes:
            self.lyre.play_single_note(note)
            mock_key_press.assert_called_with(note)
            mock_key_release.assert_called_with(note)
            
    def test_play_single_note_not_exist(self):
        try:
            self.lyre.play_single_note("C3")
        except Exception as e:
            self.assertIsInstance(e, KeyError)

    @patch("time.sleep")
    @patch.object(WindsongLyre.WindsongLyre, "play_single_note")
    def test_play(self, mock_play_single_note, mock_sleep):
        melody = [(0, "C4"), (0.5, "C4")]
        self.lyre.play(melody, 60)
        mock_play_single_note.assert_any_call("C4")
        self.assertEqual(len(mock_sleep.call_args_list), 1)
        sleep_time = mock_sleep.call_args_list[0][0][0]
        self.assertAlmostEqual(sleep_time, 0.5, places=5)
        
        