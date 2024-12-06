#from ...mymvc.BaseModel.BaseModel import BaseModel
from mymvc.BaseModel.BaseModel import BaseModel
from typing import List, Dict, Any


class CursorModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.cursor_x: int = 0
        self.cursor_y: int = 0
        self.max_y: int = 0

    def update_data(self, update: Dict[str, Any]) -> None:
        if update:
            self.move_cursor(update['dx'], update['dy'], update['max_y'])
        else:
            raise ValueError(f"Неизвестная операция")
        self.notify_observers()

    def move_cursor(self, dx: int, dy: int, max_y: int) -> None:
        self.cursor_x = max(0, self.cursor_x + dx)
        new_cursor_y = self.cursor_y + dy
        self.max_y += max_y
        self.cursor_y = max(0, min(new_cursor_y, self.max_y))
    
    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update_cursor(self.cursor_x, self.cursor_y)