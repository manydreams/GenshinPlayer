from Instuments.NightwindHorn import NightwindHorn
from Game import Game

from time import sleep

game = Game()
nightwindHorn = NightwindHorn(game)

melody = [
    (0, "C6", 2), (0, "E6", 2), (2, "D6", 4), (2, "G4", 4),
    (4, "C6", 6), (4, "A4", 6), (6, "B4", 8), (6, "E4", 8),
    (8, "A4", 10), (8, "F4", 10), (10, "G4", 12), (10, "E4", 12),
    (12, "A4", 14), (12, "F4", 14), (14, "B4", 16), (14, "G4", 16),
    ]

melody2 = [
    (0, "C6", 1), (1, "D6", 2), (2, "E6", 3), (3, "F6", 4),
    (4, "G6", 5), (5, "A6", 6), (6, "B6", 7), (7, "A6", 8),
    (8, "G6", 9), (9, "F6", 10), (10, "E6", 11), (11, "D6", 12),
    (12, "C6", 13),
    
    (13, "C4", 14), (14, "D4", 15), (15, "E4", 16), (16, "F4", 17),
    (17, "G4", 18), (18, "A4", 19), (19, "B4", 20), (20, "A4", 21),
    (21, "G4", 22), (22, "F4", 23), (23, "E4", 24), (24, "D4", 25),
    (25, "C4", 26),
    ]
game.show_window()
nightwindHorn.play(melody, bpm=150)
nightwindHorn.play(melody2, bpm=360)