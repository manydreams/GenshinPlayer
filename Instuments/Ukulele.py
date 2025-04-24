from .Instument import Instrument

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