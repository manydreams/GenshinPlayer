import unittest
from Game import Game
from unittest.mock import MagicMock
from Instuments.WindsongLyre import WindsongLyre
from Instuments.Ukulele import Ukulele 
from Instuments.NightwindHorn import NightwindHorn

class TestWindsongLyre(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock(spec=Game)
        self.lyre = WindsongLyre(self.mock_game)
    
    def test_normal_play(self):
        melody = [(0.0, "C4", True), (0.5, "C4", False)]
        self.lyre.play(melody, 120)
        self.mock_game.key_press.assert_called_once_with('z')
        self.mock_game.key_release.assert_called_once_with('z')

class TestUkulele(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock(spec=Game)
        self.ukulele = Ukulele(self.mock_game)
    
    def test_normal_play(self):
        melody = [(0.0, "C5", True), (0.5, "C5", False)]
        self.ukulele.play(melody, 120)
        self.mock_game.key_press.assert_called_once_with('z')
        self.mock_game.key_release.assert_called_once_with('z')
    
    def test_chord_play(self):
        melody = [(0.0, "CM", True)]
        self.ukulele.play(melody, 120)
        self.mock_game.key_press.assert_called_once_with('q')

class TestNightwindHorn(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock(spec=Game)
        self.horn = NightwindHorn(self.mock_game)
    
    def test_normal_play(self):
        melody = [(0.0, "C4", True), (0.5, "C4", False)]
        self.horn.play(melody, 120)
        self.mock_game.key_press.assert_called_once_with('a')
        self.mock_game.key_release.assert_called_once_with('a')

