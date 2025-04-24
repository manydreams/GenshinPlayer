from Instuments.NightwindHorn import NightwindHorn
from Game import Game

from time import sleep

game = Game()
nightwindHorn = NightwindHorn(game)

melody = [(0, 'C6', True), (0, 'E6', True), (2, 'C6', False), (2, 'E6', False), (2, 'D6', True), (2, 'G4', True), (4, 'D6', False), (4, 'G4', False), (4, 'C6', True), (4, 'A4', True), (6, 'C6', False), (6, 'A4', False), (6, 'B4', True), (6, 'E4', True), (8, 'B4', False), (8, 'E4', False), (8, 'A4', True), (8, 'F4', True), (10, 'A4', False), (10, 'F4', False), (10, 'G4', True), (10, 'E4', True), (12, 'G4', False), (12, 'E4', False), (12, 'A4', True), (12, 'F4', True), (14, 'A4', False), (14, 'F4', False), (14, 'B4', True), (14, 'G4', True), (16, 'B4', False), (16, 'G4', False)]

melody2 = [(0, 'C6', True), (1, 'C6', False), (1, 'D6', True), (2, 'D6', False), (2, 'E6', True), (3, 'E6', False), (3, 'F6', True), (4, 'F6', False), (4, 'G6', True), (5, 'G6', False), (5, 'A6', True), (6, 'A6', False), (6, 'B6', True), (7, 'B6', False), (7, 'A6', True), (8, 'A6', False), (8, 'G6', True), (9, 'G6', False), (9, 'F6', True), (10, 'F6', False), (10, 'E6', True), (11, 'E6', False), (11, 'D6', True), (12, 'D6', False), (12, 'C6', True), (13, 'C6', False), (13, 'C4', True), (14, 'C4', False), (14, 'D4', True), (15, 'D4', False), (15, 'E4', True), (16, 'E4', False), (16, 'F4', True), (17, 'F4', False), (17, 'G4', True), (18, 'G4', False), (18, 'A4', True), (19, 'A4', False), (19, 'B4', True), (20, 'B4', False), (20, 'A4', True), (21, 'A4', False), (21, 'G4', True), (22, 'G4', False), (22, 'F4', True), (23, 'F4', False), (23, 'E4', True), (24, 'E4', False), (24, 'D4', True), (25, 'D4', False), (25, 'C4', True), (26, 'C4', False)]    

game.show_window()
nightwindHorn.play(melody, bpm=150)
nightwindHorn.play(melody2, bpm=360)