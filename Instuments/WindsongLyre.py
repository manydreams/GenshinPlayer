from .Instument import Instrument
from Game import Game

class WindsongLyre(Instrument):

    def __init__(self, game: Game):
        super().__init__(game)
        self.__key_map__.update({
            "C4": "z", "c4": "z", "D4": "x", "d4": "x", "E4": "c", "e4": "c",
            "F4": "v", "f4": "v", "G4": "b", "g4": "b", "A4": "n", "a4": "n",
            "B4": "m", "b4": "m", "C5": "a", "c5": "a", "D5": "s", "d5": "s",
            "E5": "d", "e5": "d", "F5": "f", "f5": "f", "G5": "g", "g5": "g",
            "A5": "h", "a5": "h", "B5": "j", "b5": "j", "C6": "q", "c6": "q",
            "D6": "w", "d6": "w", "E6": "e", "e6": "e", "F6": "r", "f6": "r",
            "G6": "t", "g6": "t", "A6": "y", "a6": "y", "B6": "u", "b6": "u",
        })