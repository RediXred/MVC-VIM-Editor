#from ...mymvc.Commands.ICommand import ICommand
from mymvc.Commands.ICommand import ICommand
#from ...mymvc.BaseController.BaseController import BaseController
from mymvc.BaseController.BaseController import BaseController

class InputCommand(ICommand):
    def __init__(self, base_controller: BaseController, mode: str):
        self.base_controller = base_controller
        self.mode = mode

    def execute(self, key: int) -> str:
        if key == 1:
            return self.move_cursor_up()
        elif key == 2:
            return self.move_cursor_down()
        elif key == 3:
            return self.move_cursor_left()
        elif key == 4:
            return self.move_cursor_right()
        elif key == 27:
            self.base_controller.switch_controller(self.mode)
            return {'model': ['cursor'], 
                    'update': {
                        'update_cursor': {'switch': 1, 'mode': self.mode}
                        }
                    }
        elif key == 10:  # Enter (перенос строки)
            char = '\n'
            cx = self.base_controller.models['cursor'].cursor_x
            cy = self.base_controller.models['cursor'].cursor_y
            
            pos_x = self.base_controller.models['cursor'].posx
            pos_y = self.base_controller.models['cursor'].posy
            
            _, window_width = self.base_controller.models['text'].get_rendered_lines()
            
            cx = 0
            cy += 1
            
            return {
                'model': ['text', 'cursor'],
                'update': {
                    'update_cursor': {'dir': 'e', 'cx': cx, 'cy': cy, 'pos_x': 0, 'pos_y': pos_y + 1},
                    'update_text': {'enter': 1,'text': char, 'pos_x': pos_x, 'pos_y': pos_y},
                }
            }
        
        elif key == 8:  # Backspace
            char = '\b'
            
            
            cx = self.base_controller.models['cursor'].cursor_x
            cy = self.base_controller.models['cursor'].cursor_y
            
            pos_x = self.base_controller.models['cursor'].posx
            pos_y = self.base_controller.models['cursor'].posy
            tmp = pos_x - 1
            _, window_width = self.base_controller.models['text'].get_rendered_lines()

            if pos_x - 1 >= 0:
                cx -= 1
                if cx == -1:
                    cx = window_width - 1
                    cy -= 1
            
                return {
                    'model': ['text', 'cursor'],
                    'update': {
                        'update_cursor': {'dir': 'l', 'cx': cx, 'cy': cy, 'pos_x': pos_x - 1, 'pos_y': pos_y},
                        'update_text': {'backspace': 1,'text': char, 'pos_x': pos_x, 'pos_y': pos_y},
                    }
                }
            elif pos_x == 0 and pos_y > 0:
                if self.base_controller.models['text'].lines[pos_y] == '' or self.base_controller.models['text'].lines[pos_y] == '\n':
                    if self.base_controller.models['text'].lines[pos_y - 1][-1] == '\n':
                        l = len(self.base_controller.models['text'].lines[pos_y - 1]) - 1
                        tmp = len(self.base_controller.models['text'].lines[pos_y - 1]) - 1
                    else:
                        l = len(self.base_controller.models['text'].lines[pos_y - 1])
                        tmp = len(self.base_controller.models['text'].lines[pos_y - 1])
                    cx = l % window_width
                    #if pos_x == len(self.base_controller.models['text'].lines[pos_y-1]) and self.base_controller.models['text'].lines[pos_y-1][-1] == '\n':
                    #    pos_x -= 1
                    #    cx -= 1
                    cy -= 1
                    self.base_controller.models['cursor'].total_lines -= 1
                    self.base_controller.models['cursor'].current_line -= 1
                    return {
                        'model': ['text', 'cursor'],
                        'update': {
                            'update_cursor': {'dir': 'l', 'cx': cx, 'cy': cy, 'pos_x': tmp, 'pos_y': pos_y - 1},
                            'update_text': {'backspace': 1,'text': char, 'pos_x': pos_x, 'pos_y': pos_y},
                        }
                    }
                else: #MERGE LINES
                    self.base_controller.models['cursor'].total_lines -= 1
                    self.base_controller.models['cursor'].current_line -= 1
                    
                    
                    tmp = len(self.base_controller.models['text'].lines[pos_y-1]) - 1 if (self.base_controller.models['text'].lines[pos_y-1][-1] == '\n' and len(self.base_controller.models['text'].lines[pos_y-1]) > 1) else len(self.base_controller.models['text'].lines[pos_y-1])
                    cx = tmp % window_width
                    if cx != 0:
                        cy -= 1
                    if self.base_controller.models['text'].lines[pos_y-1] == '\n':
                        tmp -= 1
                        cx -= 1
                    return {
                        'model': ['text', 'cursor'],
                        'update': {
                            'update_cursor': {'dir': 'l', 'cx': cx, 'cy': cy, 'pos_x': tmp, 'pos_y': pos_y - 1},
                            'update_text': {'merge': 1,'text': char, 'pos_x': pos_x, 'pos_y': pos_y},
                        }
                    }
                    
        elif key == 330:  # Delete
            char = ' '  # Delete character is represented as an empty string
            cur_input_x = self.base_controller.models['cursor'].cursor_x
            cur_y = self.base_controller.models['cursor'].cursor_y

            if cur_input_x == len(self.base_controller.models['text'].lines[cur_y])-1 and cur_y + 1 < len(self.base_controller.models['text'].lines):
                # If at the end of the current line and there is a next line, merge lines
                self.base_controller.models['cursor'].total_lines -= 1
                return {
                    'model': ['text', 'cursor'],
                    'update': {
                        'update_cursor': {'dir': 'n', 'max_x': cur_input_x, 'dy': cur_y},
                        'update_text': {'delete': 1, 'text': char, 'pos_x': cur_input_x, 'pos_y': cur_y + 1},
                    }
                }
            elif cur_input_x < len(self.base_controller.models['text'].lines[cur_y]):
                # If inside the current line, delete the character at the cursor position
                return {
                    'model': ['text', 'cursor'],
                    'update': {
                        'update_cursor': {'dir': 'n', 'max_x': cur_input_x, 'dy': cur_y},
                        'update_text': {'delete': 1, 'text': char, 'pos_x': cur_input_x, 'pos_y': cur_y},
                    }
                }
    
    """def move_cursor_up(self):
        curr_y = max(0, self.base_controller.models['cursor'].cursor_y - 1)
        max_x = len(self.base_controller.models['text'].lines[curr_y]) - 1 if curr_y < len(self.base_controller.models['text'].lines) - 1 else len(self.base_controller.models['text'].lines[curr_y])
        return {
            'model': ['cursor'], 
            'update': {
                'update_cursor': {'dir': 'u', 'max_x': max_x, 'dy': curr_y}
            }
        }"""

    """def move_cursor_down(self):
        curr_y = min(len(self.base_controller.models['text'].lines) - 1, self.base_controller.models['cursor'].cursor_y + 1)
        max_x = len(self.base_controller.models['text'].lines[curr_y]) - 1 if curr_y < len(self.base_controller.models['text'].lines) - 1 else len(self.base_controller.models['text'].lines[curr_y])
        return {
            'model': ['cursor'], 
            'update': {
                'update_cursor': {'dir': 'd', 'max_x': max_x, 'dy': curr_y},
            }
        }"""
    def move_cursor_up(self):
        rendered_lines, window_width = self.base_controller.models['text'].get_rendered_lines()
        lines = self.base_controller.models['text'].lines
        cy = self.base_controller.models['cursor'].cursor_y
        cx = self.base_controller.models['cursor'].cursor_x
        pos_x = self.base_controller.models['cursor'].posx
        pos_y = self.base_controller.models['cursor'].posy
        
        if pos_y > 0:
            if pos_x > len(lines[pos_y-1]):
                if len(lines[pos_y-1]) and lines[pos_y-1][-1] == '\n':
                    l = len(lines[pos_y-1]) - 1    
                    pos_x = len(lines[pos_y-1]) - 1
                else:
                    l = len(lines[pos_y-1])
                    pos_x = len(lines[pos_y-1])
                cx = (l % window_width)
            else:
                cx = pos_x % window_width
                if pos_x == len(lines[pos_y-1]) and len(lines[pos_y-1]) and lines[pos_y-1][-1] == '\n':
                    pos_x -= 1
                    cx -= 1
            offset = pos_x // window_width
            pos_y -= 1
            cy = sum((len(line) + window_width - 1) // window_width for line in lines[:pos_y]) + offset
            #cx = (pos_x % window_width)
            
            return {
                'model': ['cursor'], 
                'update': {
                    'update_cursor': {'dir': 'u', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y}
                }
            }
        
        
    def move_cursor_down(self):
        #window_width = self.base_controller.models['text'].max_len
        rendered_lines, window_width = self.base_controller.models['text'].get_rendered_lines()
        lines = self.base_controller.models['text'].lines
        cy = self.base_controller.models['cursor'].cursor_y
        cx = self.base_controller.models['cursor'].cursor_x
        pos_x = self.base_controller.models['cursor'].posx
        pos_y = self.base_controller.models['cursor'].posy
        
        if pos_y + 1 < len(self.base_controller.models['text'].lines):
            if len(lines[pos_y + 1]) < pos_x:
                if len(lines[pos_y+1]) and lines[pos_y+1][-1] == '\n':
                    l = len(lines[pos_y+1]) - 1
                    pos_x = len(lines[pos_y + 1]) - 1
                else:
                    l = len(lines[pos_y+1])
                    pos_x = len(lines[pos_y + 1])
                cx = (l % window_width)
                
            else:
                cx = pos_x % window_width
                if pos_x == len(lines[pos_y+1]) and len(lines[pos_y+1]) > 0 and lines[pos_y+1][-1] == '\n':
                    pos_x -= 1
                    cx -= 1
            offset = pos_x // window_width
            pos_y += 1
            cy = sum((len(line) + window_width - 1) // window_width for line in lines[:pos_y]) + offset
            
            return {
                'model': ['cursor'], 
                'update': {
                    'update_cursor': {'dir': 'd', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y}
                }
            }
        
        
        

    
    def move_cursor_left(self):
        """pos_x = max(0, self.base_controller.models['cursor'].cursor_x - 1)
        curr_y = self.base_controller.models['cursor'].cursor_y
        return {
            'model': ['cursor'], 
            'update': {
                'update_cursor': {'dir': 'l', 'max_x': pos_x, 'dy': curr_y}
            }
        }"""
        _, window_width = self.base_controller.models['text'].get_rendered_lines()
        cx = self.base_controller.models['cursor'].cursor_x
        cy = self.base_controller.models['cursor'].cursor_y
        pos_x = self.base_controller.models['cursor'].posx
        pos_y = self.base_controller.models['cursor'].posy
        if pos_x - 1 >= 0:
            cx -= 1
            pos_x -= 1
            if cx == -1:
                cx = window_width - 1
                cy -= 1
            return {
                'model': ['cursor'], 
                'update': {
                    'update_cursor': {'dir': 'l', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y}
                }
            }

    def move_cursor_right(self):
        #len_posy = len(self.base_controller.models['text'].lines[self.base_controller.models['cursor'].pos_y]) - 1 if self.base_controller.models['cursor'].pos_y < len(self.base_controller.models['text'].lines) - 1 else len(self.base_controller.models['text'].lines[self.base_controller.models['cursor'].pos_y])
        #pos_x = min(len_posy, self.base_controller.models['cursor'].cursor_x + 1)
        #curr_y = self.base_controller.models['cursor'].cursor_y
        len_posy = len(self.base_controller.models['text'].lines[self.base_controller.models['cursor'].posy]) - 1 if self.base_controller.models['cursor'].posy < len(self.base_controller.models['text'].lines) - 1 else len(self.base_controller.models['text'].lines[self.base_controller.models['cursor'].posy])
        _, window_width = self.base_controller.models['text'].get_rendered_lines()
        cx = self.base_controller.models['cursor'].cursor_x
        cy = self.base_controller.models['cursor'].cursor_y
        pos_x = self.base_controller.models['cursor'].posx
        pos_y = self.base_controller.models['cursor'].posy
        if pos_x + 1 <= len_posy:
            cx += 1
            pos_x += 1
            if cx == window_width:
                cx = 0
                cy += 1
            return {
                'model': ['cursor'], 
                'update': {
                    'update_cursor': {'dir': 'r', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y}
                }
            }