from Game import Game
import time as tm

class Instrument:
    __key_map__ = {}

    def __init__(self, game: Game):
        self.game = game
        
    def __key_map(self, note: str) -> str:
        if note not in self.__key_map__:
            return "None"
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
            key = self.__key_map(note[1])
            if key == "None":
                continue
            if note[2]:
                self.game.key_press(key)
            else:
                self.game.key_release(key)
    
