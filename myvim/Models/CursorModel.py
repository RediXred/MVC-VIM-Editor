#from ...mymvc.BaseModel.BaseModel import BaseModel
from mymvc.BaseModel.BaseModel import BaseModel
from typing import List, Dict, Any


class CursorModel(BaseModel):
    def __init__(self):
        super().__init__()
        
        #VISUAL_POSITION
        self.cursor_x: int = 0
        self.cursor_y: int = 0
        
        #LOGICAL_POSITION
        self.posx: int = 0
        self.posy: int = 0
        
        self.mode: str = "Navigation"
        self.file_name: str = "Untitled" 
        self.current_line: int = 1  
        self.total_lines: int = 1 

    def update_data(self, update: Dict[str, Any]) -> None:
        if update:
            if 'dir' in update:
                self.move_cursor(update['dir'], update['cx'], update['cy'], update['pos_x'], update['pos_y'])
            elif 'switch' in update:
                self.update_mode_sb(update['mode'])
            #self.move_cursor(update['dx'], update['dy'], update['max_y'])
        else:
            raise ValueError(f"Неизвестная операция")
        self.notify_observers()

    def update_mode_sb(self, mode: str):
        self.mode = mode

    def move_cursor(self, dir:str, cx: int, cy: int, pos_x: int, pos_y: int) -> None:
        if dir == 'r':
            self.cursor_x = cx
            self.cursor_y = cy
            self.posx = pos_x
            self.posy = pos_y
        if dir == 'l':
            self.cursor_x = cx
            self.cursor_y = cy
            self.posx = pos_x
            self.posy = pos_y
        if dir == 'e':
            self.total_lines += 1
            self.current_line += 1
            self.cursor_x = cx
            self.cursor_y = cy
            self.posx = pos_x
            self.posy = pos_y
        if dir == 'u':
            self.current_line -= 1
            self.cursor_x = cx
            self.cursor_y = cy
            self.posx = pos_x
            self.posy = pos_y
        if dir == 'd':
            self.current_line += 1
            self.cursor_x = cx
            self.cursor_y = cy
            self.posx = pos_x
            self.posy = pos_y
        """self.cursor_y = dy
        self.cursor_x = min(self.cursor_x, max_x)
        if dir == 'r':
            self.cursor_x = max_x
        elif dir == 'l':
            self.cursor_x = max_x
        elif dir == 'e':
            self.total_lines += 1
            self.current_line += 1
        elif dir == 'd':
            self.current_line = min(self.total_lines, self.current_line + 1)
        else:
            self.current_line = self.cursor_y + 1"""
        
        
    
    def notify_observers(self) -> None:
        #for observer in self._observers:
        self._observers[0].update_cursor(self.cursor_x, self.cursor_y)
        self._observers[1].update_status_bar(self.mode, self.file_name, self.current_line, self.total_lines)