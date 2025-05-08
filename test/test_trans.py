import unittest
from unittest.mock import patch, MagicMock
import trans
from Instuments.Types import Types

class TestTransModule(unittest.TestCase):
    def setUp(self):
        # Create mock mido module
        self.mock_mido = MagicMock()
        self.mock_mido.Message = MagicMock
        self.mock_mido.MetaMessage = MagicMock
        self.mock_mido.tempo2bpm = lambda tempo, ts: 120
        
        # Patch entire mido module
        self.mido_patch = patch.dict('sys.modules', {'mido': self.mock_mido})
        self.mido_patch.start()
        
        # Patch trans module's mido reference
        self.trans_patch = patch.object(trans, 'MidiFile', self.mock_mido.MidiFile)
        self.trans_patch.start()

    def tearDown(self):
        self.mido_patch.stop()
        self.trans_patch.stop()

    def test_midi_to_lyre(self):
        """Test lyre conversion with mock MIDI data"""
        # Setup mock MIDI data for lyre (only_press=True)
        messages = [
            MagicMock(type='set_tempo', tempo=500000, time=0),
            MagicMock(type='note_on', note=60, velocity=100, time=480),
            MagicMock(type='note_off', note=60, velocity=0, time=0),
            MagicMock(type='set_tempo', tempo=500000, time=0)
        ]
        mock_track = MagicMock()
        mock_track.__iter__.return_value = messages
        mock_midi = MagicMock()
        mock_midi.tracks = [mock_track]
        mock_midi.ticks_per_beat = 480
        self.mock_mido.MidiFile.return_value = mock_midi
        
        result = trans.midi_to_lyre("test.mid", offset=0)
        
        # Verify lyre conversion (2 set_bpm + note_on + note_off + set_bpm)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0][1], "set_bpm")  # Initial bpm
        self.assertEqual(result[1][1], "set_bpm")   # First event bpm
        self.assertEqual(result[2][1], "C5")       # Note on
        self.assertEqual(result[3][1], "C5")       # Note off
        self.assertEqual(result[4][1], "set_bpm")  # Final bpm

    def test_midi_to_ukulele(self):
        """Test ukulele conversion with mock MIDI data"""
        # Setup mock MIDI data for ukulele (only_press=True)
        messages = [
            MagicMock(type='set_tempo', tempo=500000, time=0),
            MagicMock(type='note_on', note=60, velocity=100, time=0),
            MagicMock(type='note_off', note=60, velocity=0, time=480)
        ]
        mock_track = MagicMock()
        mock_track.__iter__.return_value = messages
        mock_midi = MagicMock()
        mock_midi.tracks = [mock_track]
        mock_midi.ticks_per_beat = 480
        self.mock_mido.MidiFile.return_value = mock_midi
        
        result = trans.midi_to_ukulele("test.mid", offset=0)
        
        # Verify ukulele conversion (actual implementation returns note_off as 4th event)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0][1], "set_bpm")  # Initial bpm
        self.assertEqual(result[1][1], "set_bpm")  # First event bpm
        self.assertEqual(result[2][1], "C5")       # Note on
        self.assertEqual(result[3][1], "C5")       # Note off

    def test_midi_to_horn(self):
        """Test horn conversion with mock MIDI data"""
        # Setup mock MIDI data for horn (only_press=False)
        messages = [
            MagicMock(type='set_tempo', tempo=500000, time=0),
            MagicMock(type='note_on', note=72, velocity=100, time=0),
            MagicMock(type='set_tempo', tempo=500000, time=480)
        ]
        mock_track = MagicMock()
        mock_track.__iter__.return_value = messages
        mock_midi = MagicMock()
        mock_midi.tracks = [mock_track]
        mock_midi.ticks_per_beat = 480
        self.mock_mido.MidiFile.return_value = mock_midi
        
        result = trans.midi_to_horn("test.mid", offset=0)
        
        # Verify horn conversion (actual implementation returns 4 events)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0][1], "set_bpm")  # Initial bpm
        self.assertEqual(result[1][1], "set_bpm")  # First event bpm
        self.assertEqual(result[2][1], "C6")       # Note on
        self.assertEqual(result[3][1], "set_bpm")  # Final bpm

    def test_offset_handling(self):
        """Test note offset functionality with range checks"""
        # Setup mock MIDI data with higher note (D5) for negative offset
        messages = [
            MagicMock(type='set_tempo', tempo=500000, time=0),
            MagicMock(type='note_on', note=62, velocity=100, time=0),  # D5 (62-2=60 -> C5)
            MagicMock(type='note_off', note=62, velocity=0, time=480)
        ]
        mock_track = MagicMock()
        mock_track.__iter__.return_value = messages
        mock_midi = MagicMock()
        mock_midi.tracks = [mock_track]
        mock_midi.ticks_per_beat = 480
        self.mock_mido.MidiFile.return_value = mock_midi
        
        # Test with valid offsets (D5=62)
        for offset, expected_note in [(0, "D5"), (2, "E5"), (-2, "C5")]:
            with self.subTest(offset=offset):
                result = trans.midi_to_lyre("test.mid", offset=offset)
                # Verify note conversion
                if offset == -2:
                    # Negative offset checks third event (index 2)
                    self.assertEqual(result[2][1], expected_note)
                else:
                    # Positive and zero offsets
                    self.assertGreaterEqual(len(result), 3)
                    self.assertEqual(result[2][1], expected_note)

if __name__ == '__main__':
    unittest.main()
