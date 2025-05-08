import unittest
from unittest.mock import MagicMock, patch
from GUI.Sidebar import Sidebar

class TestSidebar(unittest.TestCase):
    def setUp(self):
        # Create mock master
        self.mock_master = MagicMock()
        
        # Patch tkinter components
        self.frame_patch = patch('GUI.Sidebar.Frame')
        self.button_patch = patch('GUI.Sidebar.Button')
        
        # Start patches and create mocks
        self.MockFrame = self.frame_patch.start()
        self.mock_button = self.button_patch.start()
        
        # Configure Frame mock
        self.mock_frame_instance = MagicMock()
        self.MockFrame.return_value = self.mock_frame_instance
        self.mock_frame_instance.pack_propagate = MagicMock()
        
        # Create Sidebar instance
        self.sidebar = Sidebar(self.mock_master, width=200, bg="#2c3e50")
        
    def tearDown(self):
        self.frame_patch.stop()
        self.button_patch.stop()
        
    def test_initialization(self):
        """Test Sidebar initialization"""
        # Verify initialization
        self.assertEqual(self.sidebar.buttons, [])
        
    def test_add_button(self):
        """Test add_button method"""
        mock_command = MagicMock()
        
        # Call add_button with custom parameter
        result = self.sidebar.add_button("Test", mock_command, activebackground="blue")
        
        # Verify button creation with any kwargs
        self.mock_button.assert_called_once()
        call_args = self.mock_button.call_args[1]
        self.assertEqual(call_args['text'], "Test")
        self.assertEqual(call_args['bg'], "#34495e")
        self.assertEqual(call_args['command'], mock_command)
        
        # Verify button was added to list
        self.assertEqual(len(self.sidebar.buttons), 1)
        self.assertEqual(result, self.mock_button.return_value)
        
        # Verify button packing
        result.pack.assert_called_once_with(fill="x", padx=5, pady=2)
        
    def test_set_active_button(self):
        """Test set_active_button method"""
        # Add test buttons
        mock_btn1 = MagicMock()
        mock_btn2 = MagicMock()
        self.sidebar.buttons = [mock_btn1, mock_btn2]
        
        # Set active button
        self.sidebar.set_active_button(0)
        
        # Verify button colors
        mock_btn1.config.assert_called_once_with(bg="#3498db")
        mock_btn2.config.assert_called_once_with(bg="#34495e")

if __name__ == '__main__':
    unittest.main()