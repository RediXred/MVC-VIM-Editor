#from ...mymvc.BaseModel.BaseModel import BaseModel
from mymvc.BaseModel.BaseModel import BaseModel
from typing import List, Dict, Any


class TextModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.lines: List[str] = []


    def update_data(self, update: Dict[str, Any]) -> None:
        text = update.get('text', '')
        if not text:
            return
        self.insert_text(text)
        self.notify_observers()
    
    def insert_text(self, text: str) -> None:
        if len(self.lines) == 0 and text != '\b':
            self.lines.append(text)
        else:
            if text != '\b':
                self.lines[-1] += text
            else:
                self.lines[-1] = self.lines[-1][:-1]
    
    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update_text(*self.lines)