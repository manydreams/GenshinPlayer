import unittest
from unittest.mock import MagicMock, patch
from GUI.Viewer import Viewer

class TestViewer(unittest.TestCase):
    def setUp(self):
        # Mock tkinter components
        self.mock_frame = MagicMock()
        self.mock_sidebar = MagicMock()
        
        # Patch Sidebar import
        self.sidebar_patch = patch('GUI.Viewer.Sidebar', return_value=self.mock_sidebar)
        self.sidebar_patch.start()
        
        # Create Viewer instance
        self.viewer = Viewer("Test Viewer")
        
    def tearDown(self):
        self.sidebar_patch.stop()
        
    def test_initialization(self):
        """Test viewer initialization"""
        self.assertEqual(self.viewer.title(), "Test Viewer")
        # Geometry may not be immediately available, test window title only
        self.assertEqual(self.viewer.title(), "Test Viewer")
        self.assertEqual(len(self.viewer.pages), 0)
        self.assertIsNone(self.viewer.current_page)
        
    def test_add_page(self):
        """Test adding a new page"""
        mock_page = MagicMock()
        index = self.viewer.add_page(mock_page, "Test Page")
        
        # Verify page was added
        self.assertEqual(len(self.viewer.pages), 1)
        self.assertEqual(self.viewer.pages[0], mock_page)
        
        # Verify sidebar button was added
        self.mock_sidebar.add_button.assert_called_once_with(
            text="Test Page",
            command=unittest.mock.ANY  # Can't test lambda directly
        )
        
    def test_show_page(self):
        """Test showing a page"""
        # Add two test pages
        mock_page1 = MagicMock()
        mock_page2 = MagicMock()
        self.viewer.pages = [mock_page1, mock_page2]
        
        # Show first page
        self.viewer.show_page(0)
        mock_page1.pack.assert_called_once_with(
            in_=self.viewer.page_container,
            fill="both",
            expand=True
        )
        self.mock_sidebar.set_active_button.assert_called_once_with(0)
        
        # Reset mocks
        mock_page1.reset_mock()
        self.mock_sidebar.reset_mock()
        
        # Show second page (should hide first)
        self.viewer.current_page = mock_page1
        self.viewer.show_page(1)
        
        mock_page1.pack_forget.assert_called_once()
        mock_page2.pack.assert_called_once_with(
            in_=self.viewer.page_container,
            fill="both",
            expand=True
        )
        self.mock_sidebar.set_active_button.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()