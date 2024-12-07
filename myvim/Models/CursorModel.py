#from ...mymvc.BaseModel.BaseModel import BaseModel
from mymvc.BaseModel.BaseModel import BaseModel
from typing import List, Dict, Any


class CursorModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.cursor_x: int = 0
        self.cursor_y: int = 0
        self.max_y: int = 0
        
        self.mode: str = "Navigation"
        self.file_name: str = "Untitled" 
        self.current_line: int = 1  
        self.total_lines: int = 1 

    def update_data(self, update: Dict[str, Any]) -> None:
        if update:
            if 'dir' in update:
                self.move_cursor(update['dir'], update['max_x'], update['dy'])
            elif 'switch' in update:
                self.update_mode_sb(update['mode'])
            #self.move_cursor(update['dx'], update['dy'], update['max_y'])
        else:
            raise ValueError(f"Неизвестная операция")
        self.notify_observers()

    def update_mode_sb(self, mode: str):
        self.mode = mode

    def move_cursor(self, dir:str, max_x: int, dy: int) -> None:
        self.cursor_y = dy
        self.cursor_x = min(self.cursor_x, max_x)
        if dir == 'r':
            self.cursor_x = max_x
        elif dir == 'l':
            self.cursor_x = max_x
        elif dir == 'e':
            self.total_lines += 1
        self.current_line = self.cursor_y + 1
        
        
    
    def notify_observers(self) -> None:
        #for observer in self._observers:
        self._observers[0].update_cursor(self.cursor_x, self.cursor_y)
        self._observers[1].update_status_bar(self.mode, self.file_name, self.current_line, self.total_lines)