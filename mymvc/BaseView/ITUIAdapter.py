from typing import Protocol
#from ...MyString import MyString
from MyString import MyString

class ITUIAdapter(Protocol):
    def display_text(self, text: MyString) -> None:
        pass

    def clear_screen(self) -> None:
        pass
    
    def set_screen(self, screen) -> None:
        pass
    
    def switch_screen(self, screen) -> None:
        pass
    
    def refresh(self) -> None:
        pass