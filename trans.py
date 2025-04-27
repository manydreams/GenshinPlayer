from mido import MidiFile, MidiTrack, Message, tempo2bpm

def midi_to_lyre(file_path: str, offset: int = 0) -> dict:
    """read midi file and return a dict string of melody.
    Args:
        file_path (str): path of the midi file.
    
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
    ret = []
    mid = MidiFile(file_path)
    cur = 0.0
    def get_track():
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on' or msg.type == 'note_off':
                    return track
    def get_time_signature():
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'time_signature':
                    return (msg.numerator, msg.denominator)
        return (4, 4)
    def get_bpm():
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'set_tempo':
                    return tempo2bpm(msg.tempo, get_time_signature())
        return None
    for msg in get_track():
        cur += msg.time
        
        match msg.type:
            # case 'note_on' | 'note_off':
            case 'note_on':
                note = msg.note + offset
                # if note in key_map:
                ret.append((cur/mid.ticks_per_beat, key_map[note], True))
                ret.append((cur/mid.ticks_per_beat, key_map[note], False))
                    
    return {'melody': ret, 'bpm': get_bpm()}