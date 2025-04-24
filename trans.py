from mido import MidiFile, MidiTrack, Message

def midi_to_melody(file_path) -> list[(float, str, bool)]:
    """read midi file and return a list of `(time, note, is_on)` tuples.
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
    print(len(mid.tracks))
    for msg in mid.tracks[3]:
        cur += msg.time
        
        match msg.type:
            case 'note_on':
                if msg.note in key_map:
                    ret.append((cur/mid.ticks_per_beat, key_map[msg.note], True))
            case 'note_off':
                if msg.note in key_map:
                    ret.append((cur/mid.ticks_per_beat, key_map[msg.note], False))
    return ret