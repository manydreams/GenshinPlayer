import unittest
import win32con
from unittest.mock import patch
from Game import Game

class TestGame(unittest.TestCase):
    
    @patch('win32gui.FindWindow')
    def test_get_window_not_found(self, mock_find_window):
        """Test if the game window is not found"""
        try:
            mock_find_window.return_value = 0
            Game()
        except Exception as e:
            self.assertRaises(Exception, e)
            return
        self.fail("Game window not found")
    
    @patch('win32gui.FindWindow')
    def test_get_window_found(self, mock_find_window):
        """Test if the game window is found"""
        try:
            mock_find_window.return_value = 1234
            game = Game()
        except Exception as e:
            self.fail(e)
        self.assertEqual(game.game_window_hwnd, 1234)
        
    @patch('win32gui.ShowWindow')
    @patch('win32gui.SetForegroundWindow')
    @patch.object(Game, '__init__', lambda self: None)  # bypass init
    def test_show_window(self, mock_set_foreground, mock_show):
        """Test if the show_window function works"""
        game = Game()
        game.game_window_hwnd = 1234  # mock window handle
        
        game.show_window()
        
        mock_show.assert_called_once_with(1234, win32con.SW_RESTORE)
        mock_set_foreground.assert_called_once_with(1234)

    @patch('win32gui.PostMessage')
    @patch('win32api.VkKeyScan')
    @patch('win32api.MapVirtualKey')
    @patch.object(Game, '__init__', lambda self: None)  # bypass init
    def test_key_press(self, mock_map, mock_vk, mock_post):
        """Test if the key press function works for all letters"""
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        game = Game()
        game.game_window_hwnd = 1234  # mock window handle
        
        for letter in letters:
            vk_code = ord(letter)  # ASCII code for the letter
            scan_code = vk_code  # Simplified for test
            mock_vk.return_value = vk_code
            mock_map.return_value = scan_code
            
            game.key_press(letter)
            
            expected_lparam = (scan_code << 16) | 1
            mock_vk.assert_called_with(letter)
            mock_post.assert_called_with(1234, win32con.WM_KEYDOWN, vk_code, expected_lparam)
        
        self.assertEqual(mock_vk.call_count, len(letters))
        self.assertEqual(mock_post.call_count, len(letters))
    
    @patch('win32gui.PostMessage')
    @patch('win32api.VkKeyScan')
    @patch('win32api.MapVirtualKey')
    @patch.object(Game, '__init__', lambda self: None)  # bypass init
    def test_key_release(self, mock_map, mock_vk, mock_post):
        """Test if the key release function works for all letters"""
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        game = Game()
        game.game_window_hwnd = 1234  # mock window handle
        
        for letter in letters:
            vk_code = ord(letter)  # ASCII code for the letter
            scan_code = vk_code  # Simplified for test
            mock_vk.return_value = vk_code
            mock_map.return_value = scan_code
            
            game.key_release(letter)
            
            expected_lparam = (scan_code << 16) | 0xC0000001
            mock_vk.assert_called_with(letter)
            mock_post.assert_called_with(1234, win32con.WM_KEYUP, vk_code, expected_lparam)
        
        self.assertEqual(mock_vk.call_count, len(letters))
        self.assertEqual(mock_post.call_count, len(letters))
        