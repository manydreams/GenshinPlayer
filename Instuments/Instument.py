from Game import Game
import time as tm
import threading

class Instrument:
    __key_map__ = {}

    def __init__(self, game: Game):
        self.game = game
        self._play_event = threading.Event()
        self._play_thread = None
        self._stop_playback = False
        
    def __key_map(self, note: str) -> str:
        return self.__key_map__.get(note, "None")
        
    def play_new_thread(self, melody: list[(float, str, bool)], bpm: float):
        if self._play_thread and self._play_thread.is_alive():
            return
            
        self._stop_playback = False
        self._play_event.set()
        self._play_thread = threading.Thread(
            target=self._play_melody,
            args=(melody, bpm)
        )
        self._play_thread.daemon = True
        self._play_thread.start()

    def play(self, melody: list[(float, str, bool)], bpm: float):
        self._stop_playback = False
        self._play_event.set()
        self._play_melody(melody, bpm)

    def _play_melody(self, melody: list[(float, str, bool)], bpm: float):
        self._release_all_keys()
        time_per_beat = 60 / bpm
        prev_time = 0

        for note_time, note, state in melody:
            self._play_event.wait()
            if self._stop_playback:
                break
            
            delay = (note_time - prev_time) * time_per_beat
            if delay > 0:
                tm.sleep(delay)
            prev_time = note_time

            key = self.__key_map(note)
            if key != "None":
                if state:
                    self.game.key_press(key)
                else:
                    self.game.key_release(key)
        self._play_thread = None
        self._release_all_keys()

    def _release_all_keys(self):
        for key in self.__key_map__.values():
            self.game.key_release(key)

    def pause(self):
        self._play_event.clear()

    def resume(self):
        self._release_all_keys()
        self._play_event.set()

    def stop(self):
        self._release_all_keys()
        self._stop_playback = True
        self._play_event.set()
        if self._play_thread:
            self._play_thread.join()
            self._play_thread = None
