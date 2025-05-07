from .Instument import Instrument
from Game import Game

class NightwindHorn(Instrument):

    def __init__(self, game: Game):
        super().__init__(game)
        self.__key_map__.update({
            "C4": "a", "c4": "a", "D4": "s", "d4": "s", "E4": "d", "e4": "d",
            "F4": "f", "f4": "f", "G4": "g", "g4": "g", "A4": "h", "a4": "h",
            "B4": "j", "b4": "j",
            "C6": "q", "c6": "q", "D6": "w", "d6": "w", "E6": "e", "e6": "e",
            "F6": "r", "f6": "r", "G6": "t", "g6": "t", "A6": "y", "a6": "y",
            "B6": "u", "b6": "u",
        })