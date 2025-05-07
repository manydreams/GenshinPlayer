import win32gui, win32api, win32con

class Game:
    """
    This class represents a Genshin Impact game. It will get the game window
    and control something in the game.
    """
    
    titles = ["Genshin Impact", "原神", "YuanShen"]
    game_window_hwnd: int
    
    def __init__(self):
        try:
            self.game_window_hwnd = self.__getWindow()
        except Exception as e:
            raise e
    
    def __getWindow(self) -> int:
        """gets the Genshin Impact window hwnd.

        Raises:
            Exception: if Genshin Impact window not found.

        Returns:
            int: the hwnd of the Genshin Impact window.
        """
        for title in self.titles:
            hwnd = win32gui.FindWindow(None, title)
            if hwnd:
                return hwnd
        raise Exception("Genshin Impact window not found.")
    
    def show_window(self) -> None:
        """Brings the game window to foreground."""
        try:
            win32gui.ShowWindow(self.game_window_hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self.game_window_hwnd)
        except Exception as e:
            raise e
    
    def key_press(self, key: str) -> None:
        """Sends a key press event to the game window.

        Args:
            key (str): the key to press.
        """
        try:
            vk_code = win32api.VkKeyScan(key)
            scan_code = win32api.MapVirtualKey(vk_code, 0)
            lparam = (scan_code << 16) | 1
            win32gui.PostMessage(self.game_window_hwnd, win32con.WM_KEYDOWN, vk_code, lparam)
        except Exception as e:
            raise e
    
    def key_release(self, key: str) -> None:
        """Sends a key release event to the game window.

        Args:
            key (str): the key to release.
        """
        try:   
            vk_code = win32api.VkKeyScan(key)
            scan_code = win32api.MapVirtualKey(vk_code, 0)
            lparam = (scan_code << 16) | 0xC0000001
            win32gui.PostMessage(self.game_window_hwnd, win32con.WM_KEYUP, vk_code, lparam)
        except Exception as e:
            raise e

        