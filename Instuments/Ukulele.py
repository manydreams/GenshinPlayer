from .Instument import Instrument
from Game import Game
import time as tm

class Ukulele(Instrument):

    __key_map__ = {
        "C5": "z", "c5": "z", "D5": "x", "d5": "x", "E5": "c", "e5": "c",
        "F5": "v", "f5": "v", "G5": "b", "g5": "b", "A5": "n", "a5": "n",
        "B5": "m", "b5": "m", "C6": "a", "c6": "a", "D6": "s", "d6": "s",
        "E6": "d", "e6": "d", "F6": "f", "f6": "f", "G6": "g", "g6": "g",
        "A6": "h", "a6": "h", "B6": "j", "b6": "j", "CM": "q", "Cmaj": "q",
        "Dm": "w", "Dmin": "w", "Em": "e", "Emin": "e", "FM": "r", "Fmaj": "r",
        "GM": "t", "Gmaj": "t", "Am": "y", "Amin": "y", "G7": "u", "GMm7": "u",
    }

    def __init__(self, game: Game):
        super().__init__(game)
        
    def __key_map(self, note: str) -> str:
        return self.__key_map__[note]
        
    def play(self, melody: list[(float, str)], bpm: int):
        """plays the melody use ukulele

        Args:
            melody (list[(time: float, note: str)]): the list must be sorted by time
            bpm (int): beats per minute
        """
        timeforbeat = 60/bpm
        
        time = []
        for t1, t2 in zip([(0,)] + melody, melody):
            time.append(t2[0] - t1[0])
        for i, note in enumerate(melody):
            if time[i] > 0.00000001:
                tm.sleep(time[i]*timeforbeat)
            self.play_single_note(note[1])
    
    def play_single_note(self, note: str) -> None:
        try:
            key = self.__key_map(note)
            self.game.key_press(key)
            self.game.key_release(key)
        except Exception as e:
            raise e
        