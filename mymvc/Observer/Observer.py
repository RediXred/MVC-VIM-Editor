#from ...MyString import MyString
from MyString import MyString

class Observer:
    def update_status_bar(self, mode: MyString, f_name: MyString, current_line: int, total_lines: int) -> None:
        pass

    def update_text(self, text: MyString) -> None:
        pass

    def update_cursor(self, cursor_x: int, cursor_y: int) -> None:
        pass