from tkinter import Tk, Frame
from .Sidebar import Sidebar

class Viewer(Tk):
    def __init__(self, title):
        super().__init__()
        
        self.title(title)
        self.geometry("1280x720")
        
        # Initialize page container
        self.page_container = Frame(self)
        self.page_container.pack(side="right", fill="both", expand=True)
        
        # Initialize sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.pack(side="left", fill="y")
        
        # Page management
        self.pages = []
        self.current_page = None

    def add_page(self, page_frame: Frame, title: str):
        """Add a new page to the viewer"""
        self.pages.append(page_frame)
        index = len(self.pages) - 1
        self.sidebar.add_button(
            text=title,
            command=lambda: self.show_page(index)
        )
        return index

    def show_page(self, index: int):
        """Show the specified page"""
        if self.current_page is not None:
            self.current_page.pack_forget()
            
        self.current_page = self.pages[index]
        self.current_page.pack(in_=self.page_container, fill="both", expand=True)
        self.sidebar.set_active_button(index)