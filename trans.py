from mido import MidiFile, MidiTrack, Message, tempo2bpm

def __midi_trans(file_path: str, offset: int = 0, only_press: bool = True, key_map: dict = None) -> dict:
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
            "melody": [[time(float), note(str), is_on(bool)], [...], [...],...],
            "bpm": float | None
        }
    """
    if key_map is None:
        return {'melody': [], 'bpm': None}
    ret = []
    mid = MidiFile(file_path)
    
    tempo = None
    time_signature = None
    bpm = None
    
    for t in mid.tracks:
        cur = 0.0
        for msg in t:
            cur += msg.time
            if msg.type == 'note_on' or msg.type == 'note_off':
                note = msg.note + offset
                if note not in key_map:
                    continue
                if msg.type == 'note_on':
                    ret.append((cur/mid.ticks_per_beat, key_map[note], True))
                    if only_press:
                        ret.append((cur/mid.ticks_per_beat, key_map[note], False))
                if msg.type == 'note_off' and not only_press:
                    ret.append((cur/mid.ticks_per_beat, key_map[note], False))
                    
            elif msg.type == 'time_signature' and time_signature == None:
                time_signature = (msg.numerator, msg.denominator)
            elif msg.type =='set_tempo' and tempo == None:
                tempo = msg.tempo
                
    if tempo and time_signature:
        bpm = tempo2bpm(tempo, time_signature)
        
    ret.sort(key=lambda x: x[0])
    return {'melody': ret, 'bpm': bpm}


def midi_to_lyre(file_path: str, offset: int = 0) -> dict:
    """read midi file and return a dict string of melody.
    Args:
        file_path (str): path of the midi file.
        offset (int): the offset of the midi file.
    
    Returns:
        a dict like:
        {
            "melody": [[time(float), note(str), is_on(bool)], [...], [...],...],
            "bpm": float | None
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
            "melody": [[time(float), note(str), is_on(bool)], [...], [...],...],
            "bpm": float | None
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
            "melody": [[time(float), note(str), is_on(bool)], [...], [...],...],
            "bpm": float | None
        }
    """
    key_map = {
        48: 'C4', 50: 'D4', 52: 'E4', 53: 'F4',
        55: 'G4', 57: 'A4', 59: 'B4', 72: 'C6',
        74: 'D6', 76: 'E6', 77: 'F6', 79: 'G6',
        81: 'A6', 83: 'B6',
    }
    return __midi_trans(file_path, offset, only_press=False, key_map=key_map)