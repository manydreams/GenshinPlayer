import unittest
from Game import Game
from unittest.mock import patch
from Instuments import WindsongLyre
from Instuments import Ukulele
from Instuments import NightwindHorn

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
        
class TestUkulele(unittest.TestCase):
    
    @patch.object(Game, "__init__", lambda self: None)
    def setUp(self):
        self.ukulele = Ukulele.Ukulele(Game())
    
    def tearDown(self):
        del self.ukulele
        
    @patch.object(Game, "key_press")
    @patch.object(Game, "key_release")
    @patch.object(Ukulele.Ukulele, "_Ukulele__key_map", lambda self, note: note)
    def test_play_single_note(self, mock_key_release, mock_key_press):
        notes = [i + j for j in "456" for i in "cdefgabCDEFGAB"]
        for note in notes:
            self.ukulele.play_single_note(note)
            mock_key_press.assert_called_with(note)
            mock_key_release.assert_called_with(note)
            
    def test_play_single_note_not_exist(self):
        try:
            self.ukulele.play_single_note("C4")
        except Exception as e:
            self.assertIsInstance(e, KeyError)

    @patch("time.sleep")
    @patch.object(Ukulele.Ukulele, "play_single_note")
    def test_play(self, mock_play_single_note, mock_sleep):
        melody = [(0, "G7"), (0.5, "Am")]
        self.ukulele.play(melody, 60)
        mock_play_single_note.assert_any_call("G7")
        self.assertEqual(len(mock_sleep.call_args_list), 1)
        sleep_time = mock_sleep.call_args_list[0][0][0]
        self.assertAlmostEqual(sleep_time, 0.5, places=5)

class TestNightwindHorn(unittest.TestCase):
    
    @patch.object(Game, "__init__", lambda self: None)
    def setUp(self):
        from Instuments import NightwindHorn
        self.horn = NightwindHorn.NightwindHorn(Game())
    
    def tearDown(self):
        del self.horn
        
    @patch.object(Game, "key_press")
    @patch.object(NightwindHorn.NightwindHorn, "_NightwindHorn__key_map", lambda self, note: note)
    def test_play_single_note_down(self, mock_key_press):
        notes = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C6", "D6", "E6", "F6", "G6", "A6", "B6"]
        for note in notes:
            self.horn.play_single_note_down(note)
            mock_key_press.assert_called_with(note)
            
    @patch.object(Game, "key_release")
    @patch.object(NightwindHorn.NightwindHorn, "_NightwindHorn__key_map", lambda self, note: note)
    def test_play_single_note_up(self, mock_key_release):
        notes = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C6", "D6", "E6", "F6", "G6", "A6", "B6"]
        for note in notes:
            self.horn.play_single_note_up(note)
            mock_key_release.assert_called_with(note)
            
    def test_play_single_note_not_exist(self):
        try:
            self.horn.play_single_note_down("C3")
        except Exception as e:
            self.assertIsInstance(e, KeyError)
            
        try:
            self.horn.play_single_note_up("C3")
        except Exception as e:
            self.assertIsInstance(e, KeyError)

    @patch("time.sleep")
    @patch.object(NightwindHorn.NightwindHorn, "play_single_note_down")
    @patch.object(NightwindHorn.NightwindHorn, "play_single_note_up")
    def test_play(self, mock_play_single_note_up, mock_play_single_note_down, mock_sleep):
        melody = [(0, "C4", 0.5), (0.5, "D4", 1.0)]
        self.horn.play(melody, 60)
        mock_play_single_note_down.assert_any_call("C4")
        mock_play_single_note_up.assert_any_call("C4")
        self.assertEqual(len(mock_sleep.call_args_list), 2)
        