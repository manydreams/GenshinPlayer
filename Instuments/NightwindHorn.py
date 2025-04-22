from .Instument import Instrument
from Game import Game
import time as tm

class NightwindHorn(Instrument):

    __key_map__ = {
        "C4": "a", "c4": "a", "D4": "s", "d4": "s", "E4": "d", "e4": "d",
        "F4": "f", "f4": "f", "G4": "g", "g4": "g", "A4": "h", "a4": "h",
        "B4": "j", "b4": "j",
        "C6": "q", "c6": "q", "D6": "w", "d6": "w", "E6": "e", "e6": "e",
        "F6": "r", "f6": "r", "G6": "t", "g6": "t", "A6": "y", "a6": "y",
        "B6": "u", "b6": "u",
    }

    def __init__(self, game: Game):
        super().__init__(game)
        
    def __key_map(self, note: str) -> str:
        return self.__key_map__[note]
        
    def play(self, melody: list[(float, str, float)], bpm: int):
        """plays the melody use ukulele

        Args:
            melody (list[(start: float, note: str, end: float)]): the list must be sorted by time
            bpm (int): beats per minute
        """
        timeforbeat = 60/bpm
        time = []
        for start, note, end in melody:
            time.append((start, note, True))
            time.append((end, note, False))
        
        time.sort(key=lambda x: x[0])
        melody = time
        time = []
        for t1, t2 in zip([(0,"",False)] + melody, melody):
            time.append(t2[0] - t1[0])
        
        for i, (_,note,down) in enumerate(melody):
            if time[i] > 0.00000001:
                tm.sleep(time[i] * timeforbeat)
            if down:
                self.play_single_note_down(note)
            else:
                self.play_single_note_up(note)
    
    def play_single_note_down(self, note: str) -> None:
        try:
            key = self.__key_map(note)
            self.game.key_press(key)
        except Exception as e:
            raise e
        
    def play_single_note_up(self, note: str) -> None:
        try:
            key = self.__key_map(note)
            self.game.key_release(key)
        except Exception as e:
            raise e
        