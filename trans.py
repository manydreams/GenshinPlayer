from mido import MidiFile, MidiTrack, Message, tempo2bpm

def __midi_trans(file_path: str, offset: int = 0, only_press: bool = True,
                 key_map: dict = None) -> dict:
    """read midi file and return a dict string of melody.
    Args:
        file_path (str): path of the midi file.
        offset (int): the offset of the midi file.
        only_press (bool): 
            - if True, record pressing and releasing keys when note_on.
            - if False, record all notes.
        key_map (dict): the key map of the midi file.
    
    Returns:
        a dict like:
        {
            "melody": [
                [time(float), setbpm(str), bpm(float)],
                [time(float), note(str), is_on(bool)] or 
                    [time(float), setbpm(str), bpm(float)],
                [...], [...], [...],]
        }
    """
    if key_map is None:
        return {'melody': []}
    ret = []
    mid = MidiFile(file_path)
    
    tempo = 500000
    time_signature = (4, 4)
    ret.append((0.0, "set_bpm", tempo2bpm(tempo, time_signature)))
    
    ofst = offset
    
    for t in mid.tracks:
        cur = 0.0
        for msg in t:
            cur += msg.time
            if msg.type in ['note_on', 'note_off'] and msg.velocity > 0:
                note = msg.note + offset
                if note not in key_map:
                    continue
                if msg.type == 'note_on':
                    ret.append((cur/mid.ticks_per_beat, key_map[note], True))
                    if only_press:
                        ret.append((cur/mid.ticks_per_beat, key_map[note], False))
                if msg.type == 'note_off' and not only_press:
                    ret.append((cur/mid.ticks_per_beat, key_map[note], False))
                    
            elif msg.type == 'time_signature':
                time_signature = (msg.numerator, msg.denominator)
                ret.append((cur/mid.ticks_per_beat, "set_bpm", tempo2bpm(tempo, time_signature)))
            elif msg.type =='set_tempo':
                tempo = msg.tempo
                ret.append((cur/mid.ticks_per_beat, "set_bpm", tempo2bpm(tempo, time_signature)))
            elif msg.type == 'key_signature':
                offset = ofst + {
                    "C": 0, "C#":-1, "Db": -1, "D": -2, "D#": -3, "Eb": -3,
                    "E": -4, "F": -5, "F#": -6, "Gb": -6, "G": -7, "G#": -8,
                    "Ab": -8, "A": -9, "A#": -10, "Bb": -10, "B": -11
                }[msg.key]
    
    
    
    ret.sort(key=lambda x: x[0])
    return {'melody': ret}


def midi_to_lyre(file_path: str, offset: int = 0) -> dict:
    """read midi file and return a dict string of melody.
    Args:
        file_path (str): path of the midi file.
        offset (int): the offset of the midi file.
    
    Returns:
        a dict like:
        {
            "melody": [
                [time(float), setbpm(str), bpm(float)],
                [time(float), note(str), is_on(bool)] or 
                    [time(float), setbpm(str), bpm(float)],
                [...], [...], [...]]
        }
    """
    key_map = {
        48: 'C4', 50: 'D4', 52: 'E4', 53: 'F4',
        55: 'G4', 57: 'A4', 59: 'B4', 60: 'C5',
        62: 'D5', 64: 'E5', 65: 'F5', 67: 'G5',
        69: 'A5', 71: 'B5', 72: 'C6', 74: 'D6',
        76: 'E6', 77: 'F6', 79: 'G6', 81: 'A6',
        83: 'B6',
    }
    
    return __midi_trans(file_path, offset, only_press=True, key_map=key_map)

def midi_to_ukulele(file_path: str, offset: int = 0) -> dict:
    """read midi file and return a dict string of melody.
    Args:
        file_path (str): path of the midi file.
        offset (int): the offset of the midi file.
    
    Returns:
        a dict like:
        {
            "melody": [
                [time(float), setbpm(str), bpm(float)],
                [time(float), note(str), is_on(bool)] or 
                    [time(float), setbpm(str), bpm(float)],
                [...], [...], [...],]
        }
    """
    key_map = {
        60: 'C5', 62: 'D5', 64: 'E5', 65: 'F5',
        67: 'G5', 69: 'A5', 71: 'B5', 72: 'C6',
        74: 'D6', 76: 'E6', 77: 'F6', 79: 'G6',
        81: 'A6', 83: 'B6',
    }
    return __midi_trans(file_path, offset, only_press=True, key_map=key_map)

def midi_to_horn(file_path: str, offset: int = 0) -> dict:
    """read midi file and return a dict string of melody.
    Args:
        file_path (str): path of the midi file.
        offset (int): the offset of the midi file.
    
    Returns:
        a dict like:
        {
            "melody": [
                [time(float), setbpm(str), bpm(float)],
                [time(float), note(str), is_on(bool)] or 
                    [time(float), setbpm(str), bpm(float)],
                [...], [...], [...],]
        }
    """
    key_map = {
        48: 'C4', 50: 'D4', 52: 'E4', 53: 'F4',
        55: 'G4', 57: 'A4', 59: 'B4', 72: 'C6',
        74: 'D6', 76: 'E6', 77: 'F6', 79: 'G6',
        81: 'A6', 83: 'B6',
    }
    return __midi_trans(file_path, offset, only_press=False, key_map=key_map)