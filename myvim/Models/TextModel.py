#from ...mymvc.BaseModel.BaseModel import BaseModel
from mymvc.BaseModel.BaseModel import BaseModel
from typing import List, Dict, Any


class TextModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.lines: List[str] = [""]
        self.max_len = 0#self._observers[0].get_width()
        self.scroll_top = 0

    def update_data(self, update: Dict[str, Any]) -> None:
        text = update.get('text', '')
        if not text:
            return
        if 'input' in update and update['input'] == 1:
            self.insert_text(text, update['pos_x'], update['pos_y'])
        if 'enter' in update and update['enter'] == 1:
            self.enter_line(update['pos_x'], update['pos_y'])
        if 'backspace' in update and update['backspace'] == 1:
            self.backspace(update['pos_x'], update['pos_y'])
        if 'delete' in update and update['delete'] == 1:
            self.delete_(update['pos_x'], update['pos_y'])
        if 'merge' in update and update['merge'] == 1:
            self.merge_lines(update['pos_y'], update['pos_x'])
        if 'scroll_down' in update and update['scroll_down'] == 1:
            self.scroll_down(update['scroll_top'])
        self.notify_observers()
    
    def scroll_down(self, scroll_top: int) -> None:
        self.scroll_top = scroll_top
    
    def merge_lines(self, pos_y: int, pos_x: int) -> None:
        if self.lines[pos_y-1][-1] == '\n':
            self.lines[pos_y-1] = self.lines[pos_y-1][:-1]
        self.lines[pos_y - 1] = self.lines[pos_y - 1] + self.lines[pos_y][pos_x:]
        self.lines.pop(pos_y)
        
    def insert_text(self, text: str, pos_x: int, pos_y: int) -> None:
        self.lines[pos_y] = self.lines[pos_y][:pos_x] + text + self.lines[pos_y][pos_x:]
    
    def enter_line(self, pos_x: int, pos_y: int) -> None:
        temp = self.lines[pos_y][pos_x:]
        self.lines[pos_y] = self.lines[pos_y][:pos_x] + '\n'
        self.lines.insert(pos_y + 1, temp)
    
    def backspace(self, pos_x: int, pos_y: int) -> None:
        if pos_x == 0 and pos_y > 0:
            self.lines.pop(pos_y)
        else:
            self.lines[pos_y] = self.lines[pos_y][:pos_x - 1] + self.lines[pos_y][pos_x:]
    
    def delete_(self, pos_x: int, pos_y: int) -> None:
        if pos_y > 0 and pos_x == len(self.lines[pos_y - 1]) - 1 and pos_y < len(self.lines) and len(self.lines) > 1:
            # Если в конце текущей строки и есть следующая строка
            if pos_y == len(self.lines) - 1:
                self.lines[pos_y - 1] = self.lines[pos_y - 1][:-1] + (self.lines[pos_y] if self.lines[pos_y] != '\n' else '')
            elif pos_y < len(self.lines) - 1:
                self.lines[pos_y - 1] = self.lines[pos_y - 1][:-1] + (self.lines[pos_y] if self.lines[pos_y] != '\n' else '\n')
            self.lines.pop(pos_y)
        elif pos_y < len(self.lines) and pos_x < len(self.lines[pos_y]):
            # Если внутри текущей строки, удалить символ на позиции курсора
            self.lines[pos_y] = self.lines[pos_y][:pos_x] + self.lines[pos_y][pos_x + 1:]

    def get_rendered_lines(self) -> tuple[List[str], int]:
        window_width = self._observers[0].get_width()
        window_height = self._observers[0].get_height()
        rendered_lines = []
        for line in self.lines:
            while len(line) > window_width:
                rendered_lines.append(line[:window_width])
                line = line[window_width:]
            rendered_lines.append(line)
        return (rendered_lines, window_width, window_height)
    
    def notify_observers(self) -> None:
        for observer in self._observers:
            rendered_lines, _, window_height = self.get_rendered_lines()
            text = ''.join(rendered_lines[self.scroll_top:self.scroll_top + window_height - 1])
            #text = ''.join(self.lines[self.scroll_top:self.scroll_top + window_height - 1])
            #text = ''.join(self.lines)
            observer.update_text(text)