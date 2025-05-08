import unittest
from unittest.mock import MagicMock, patch
import os
from GUI.FileSelector import FileSelector

class TestFileSelector(unittest.TestCase):
    def setUp(self):
        # Create mock master and callback
        self.mock_master = MagicMock()
        self.mock_callback = MagicMock()
        
        # Create real test directory path
        self.test_dir = os.path.abspath("test_directory")
        self.test_files = ["file1.mid", "file2.json", "ignore.txt"]
        
        # Create and store mock objects directly
        self.mock_listdir = patch('GUI.FileSelector.os.listdir', 
                                return_value=self.test_files).start()
        self.mock_isfile = patch('GUI.FileSelector.os.path.isfile',
                               return_value=True).start()
        self.mock_abspath = patch('GUI.FileSelector.os.path.abspath',
                                 return_value=self.test_dir).start()
        
        # Patch filedialog
        self.filedialog_patch = patch('GUI.FileSelector.filedialog')
        self.mock_filedialog = self.filedialog_patch.start()
        self.mock_filedialog.askdirectory.return_value = self.test_dir
        
        # Create FileSelector instance
        self.selector = FileSelector(self.mock_master, self.mock_callback)
        
        # Track label text changes
        self.label_text = "No directory selected"
        self.selector.label.config = lambda **kwargs: setattr(self, 'label_text', kwargs.get('text', self.label_text))
        
    def tearDown(self):
        patch.stopall()
        self.filedialog_patch.stop()
        
    def test_initial_state(self):
        """Test initial state of FileSelector"""
        self.assertEqual(self.label_text, "No directory selected")
        self.assertEqual(self.selector.selected_directory, None)
        self.assertEqual(len(self.selector.current_files), 0)
        
    def test_select_directory(self):
        """Test directory selection"""
        # Trigger directory selection
        self.selector._select_directory()
        
        # Verify dialog was called
        self.mock_filedialog.askdirectory.assert_called_once_with(title="Select Directory")
        
        # Verify directory was set
        self.assertEqual(self.selector.selected_directory, self.test_dir)
        self.assertEqual(self.label_text, f"Selected: {self.test_dir}")
        
        # Verify file list was updated
        self.mock_listdir.assert_called_once_with(self.test_dir)
        self.assertEqual(len(self.selector.current_files), 2)  # Only .mid and .json files
        
    def test_file_selection(self):
        """Test file selection handling"""
        # Setup test data
        test_file = "test.mid"
        
        # Configure mocks
        self.selector.selected_directory = self.test_dir
        self.selector.current_files = [test_file]
        self.selector.file_list.curselection = lambda: (0,)
        
        # Trigger file selection
        self.selector._on_file_select()
        
        # Verify callback was called with a string path
        self.mock_callback.assert_called_once()
        callback_arg = self.mock_callback.call_args[0][0]
        self.assertIsInstance(callback_arg, str)
        self.assertTrue(callback_arg.endswith(test_file))
        
    def test_get_selected_file(self):
        """Test get_selected_file method"""
        # Case 1: No selection
        self.assertIsNone(self.selector.get_selected_file())
        
        # Case 2: With selection
        test_file = "test.json"
        
        self.selector.selected_directory = self.test_dir
        self.selector.current_files = [test_file]
        self.selector.file_list.curselection = lambda: (0,)
        
        result = self.selector.get_selected_file()
        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith(test_file))

if __name__ == '__main__':
    unittest.main()