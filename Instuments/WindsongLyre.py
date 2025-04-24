from .Instument import Instrument
from Game import Game
import time as tm

class WindsongLyre(Instrument):

    __key_map__ = {
        "C4": "z", "c4": "z", "D4": "x", "d4": "x", "E4": "c", "e4": "c",
        "F4": "v", "f4": "v", "G4": "b", "g4": "b", "A4": "n", "a4": "n",
        "B4": "m", "b4": "m", "C5": "a", "c5": "a", "D5": "s", "d5": "s",
        "E5": "d", "e5": "d", "F5": "f", "f5": "f", "G5": "g", "g5": "g",
        "A5": "h", "a5": "h", "B5": "j", "b5": "j", "C6": "q", "c6": "q",
        "D6": "w", "d6": "w", "E6": "e", "e6": "e", "F6": "r", "f6": "r",
        "G6": "t", "g6": "t", "A6": "y", "a6": "y", "B6": "u", "b6": "u",
    }

    def __init__(self, game: Game):
        super().__init__(game)
        
    def __key_map(self, note: str) -> str:
        return self.__key_map__[note]
        
    def play(self, melody: list[(float, str, bool)], bpm: int):
        """plays the melody use ukulele

        Args:
            melody (list[(time: float, note: str, state: bool)]): the list must be sorted by time
            bpm (int): beats per minute
        """
        timeforbeat = 60/bpm
        time = []
        for t1, t2 in zip([(0,"",False)] + melody, melody):
            time.append(t2[0] - t1[0])
        for i, note in enumerate(melody):
            if time[i] > 0.00000001:
                tm.sleep(time[i]*timeforbeat)
            if note[1] not in self.__key_map__:
                print(f"note {note[1]} not in key map")
                continue
            if note[2]:
                self.game.key_press(self.__key_map(note[1]))
            else:
                self.game.key_release(self.__key_map(note[1]))
        