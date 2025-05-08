import unittest
from unittest.mock import patch, MagicMock
from GUI.FilePage import FilePage

class TestFilePage(unittest.TestCase):
    def setUp(self):
        # Create mock callbacks
        self.mock_on_play = MagicMock()
        self.mock_on_pause = MagicMock()
        self.mock_on_resume = MagicMock()
        self.mock_on_stop = MagicMock()
        self.mock_on_bpm_change = MagicMock()
        self.mock_on_instrument_change = MagicMock()
        self.mock_update_melody = MagicMock()
        
        # Patch file selector
        self.file_selector_patch = patch('GUI.FilePage.FileSelector')
        self.mock_file_selector = self.file_selector_patch.start()
        
        # Create FilePage instance with correct parameters
        self.file_page = FilePage(
            master=None,
            on_play=self.mock_on_play,
            on_pause=self.mock_on_pause,
            on_resume=self.mock_on_resume,
            on_stop=self.mock_on_stop,
            on_bpm_change=self.mock_on_bpm_change,
            on_instrument_change=self.mock_on_instrument_change,
            update_melody=self.mock_update_melody
        )
        
        # Patch messagebox
        self.msgbox_patch = patch('GUI.FilePage.messagebox')
        self.mock_msgbox = self.msgbox_patch.start()

    def tearDown(self):
        self.file_selector_patch.stop()
        self.msgbox_patch.stop()

    def test_initialization(self):
        """Test UI components are initialized correctly"""
        self.assertIsNotNone(self.file_page.file_selector)
        self.assertIsNotNone(self.file_page.status_label)
        self.assertEqual(self.file_page.status_label['text'], "No file selected")

    def test_file_selection(self):
        """Test file selection handling"""
        test_file = "test.mid"
        with patch('os.path.isfile', return_value=True):
            self.file_page._handle_file_select(test_file)
            self.assertEqual(self.file_page.status_label['text'], f"Selected: {test_file}")

    def test_bpm_update(self):
        """Test BPM update functionality"""
        # Reset mock call count
        self.mock_on_bpm_change.reset_mock()
        
        # Test valid BPM update
        self.file_page.bpm_entry.delete(0, "end")
        self.file_page.bpm_entry.insert(0, "120")
        self.file_page._update_bpm()
        
        # Verify callback was called once
        self.assertEqual(self.mock_on_bpm_change.call_count, 1)
        self.mock_on_bpm_change.assert_called_with(120.0)

if __name__ == '__main__':
    unittest.main()
