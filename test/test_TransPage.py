import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import json
from GUI.TransPage import TransPage
from Instuments.Types import Types

class TestTransPage(unittest.TestCase):
    def setUp(self):
        # Create root window
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Mock trans module with proper return values
        self.trans_patch = patch('GUI.TransPage.trans')
        self.mock_trans = self.trans_patch.start()
        
        # Create test melody data
        self.test_melody = [
            [0.0, "set_bpm", 120],
            [0.0, "C5", True],
            [1.0, "D5", False]
        ]
        
        # Setup return values
        self.mock_trans.midi_to_lyre.return_value = self.test_melody
        self.mock_trans.midi_to_ukulele.return_value = self.test_melody
        self.mock_trans.midi_to_horn.return_value = self.test_melody
        
        # Mock filedialog with tempfile
        self.filedialog_patch = patch('GUI.TransPage.filedialog')
        self.mock_filedialog = self.filedialog_patch.start()
        self.mock_filedialog.asksaveasfilename.return_value = None  # Simulate cancel operation
        
        # Create TransPage instance
        self.trans_page = TransPage(master=self.root)

    def tearDown(self):
        self.trans_patch.stop()
        self.filedialog_patch.stop()
        self.root.destroy()

    def test_file_selection(self):
        """Test file selection handling"""
        # Simulate valid file selection
        test_file = "test.mid"
        with patch('os.path.isfile', return_value=True):
            self.trans_page._handle_file_select(test_file)
            self.assertEqual(self.trans_page.status_label['text'], f"Selected: {test_file}")
            self.assertEqual(self.trans_page.convert_btn['state'], "normal")

    def test_conversion(self):
        """Test MIDI conversion functionality"""
        # Setup with selected file
        test_file = "test.mid"
        with patch('os.path.isfile', return_value=True):
            self.trans_page._handle_file_select(test_file)
        
        # Test conversion
        self.trans_page._handle_convert()
        
        # Verify result
        result_text = self.trans_page.result_text.get("1.0", "end").strip()
        try:
            result_data = json.loads(result_text)
            self.assertEqual(result_data['instrument'], Types.Lyre.value)
            self.assertEqual(len(result_data['melody']), 3)
            self.assertEqual(self.trans_page.save_btn['state'], "normal")
        except json.JSONDecodeError:
            self.fail("Failed to decode JSON result")

    def test_save_result(self):
        """Test result saving functionality"""
        # Setup with converted result
        test_file = "test.mid"
        with patch('os.path.isfile', return_value=True):
            self.trans_page._handle_file_select(test_file)
            self.trans_page._handle_convert()
        
        # Test save
        self.trans_page._handle_save()
        self.mock_filedialog.asksaveasfilename.assert_called_once()

if __name__ == '__main__':
    unittest.main()
