from typing import List, Dict, Any
#from ...mymvc.BaseModel.BaseModel import BaseModel
from mymvc.BaseModel.BaseModel import BaseModel

class StatusBarModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.mode: str = "Navigation"
        self.file_name: str = "Untitled" 
        self.current_line: int = 1  
        self.total_lines: int = 1 

    def update_data(self, update: Dict[str, Any]) -> None:
        self.update_status(
            mode=update.get('mode', self.mode),
            file_name=update.get('filename', self.file_name),
            current_line=update.get('current_line', self.current_line),
            total_lines=update.get('total_lines', self.total_lines)
        )

    def update_status(self, mode: str, file_name: str, current_line: int, total_lines: int) -> None:
        if self.mode == mode:
            self.mode = mode
            self.file_name = file_name
            self.total_lines += total_lines
            self.current_line = min(max(self.current_line + current_line, 1), self.total_lines)
            self.notify_observers()
        else:
            self.mode = mode
            self.file_name = file_name
            self.notify_observers()
    
    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update_status_bar(self.mode, self.file_name, self.current_line, self.total_lines)