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
            cur_input_x = self.base_controller.models['cursor'].cursor_x
            cur_y = self.base_controller.models['cursor'].cursor_y
            
            return {
                'model': ['text', 'cursor'],
                'update': {
                    'update_cursor': {'dir': 'e', 'max_x': 0, 'dy': cur_y + 1},
                    'update_text': {'enter': 1,'text': char, 'pos_x': cur_input_x, 'pos_y': cur_y},
                }
            }
        elif key == 8:  # Backspace
            char = '\b'
            cur_input_x = self.base_controller.models['cursor'].cursor_x
            cur_y = self.base_controller.models['cursor'].cursor_y
            
            if cur_input_x == 0 and cur_y > 0:
                cur_y -= 1
                prev_line_len = len(self.base_controller.models['text'].lines[cur_y])
                cur_input_x = prev_line_len
                self.base_controller.models['cursor'].total_lines -= 1
                return {
                        'model': ['text', 'cursor'],
                        'update': {
                            'update_cursor': {'dir': 'l', 'max_x': cur_input_x - 1, 'dy': cur_y},
                            'update_text': {'backspace': 1, 'text': '\b', 'pos_x': 0, 'pos_y': cur_y+1},
                        }
                    }
            elif cur_input_x > 0:
                cur_input_x = max(0, cur_input_x - 1)
                
                return {
                    'model': ['text', 'cursor'],
                    'update': {
                        'update_cursor': {'dir': 'l', 'max_x': cur_input_x, 'dy': cur_y},
                        'update_text': {'backspace': 1, 'text': char, 'pos_x': cur_input_x + 1 if cur_input_x > 0 else 1, 'pos_y': cur_y},
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
    
    def move_cursor_up(self):
        curr_y = max(0, self.base_controller.models['cursor'].cursor_y - 1)
        max_x = len(self.base_controller.models['text'].lines[curr_y]) - 1 if curr_y < len(self.base_controller.models['text'].lines) - 1 else len(self.base_controller.models['text'].lines[curr_y])
        return {
            'model': ['cursor'], 
            'update': {
                'update_cursor': {'dir': 'u', 'max_x': max_x, 'dy': curr_y}
            }
        }

    def move_cursor_down(self):
        curr_y = min(len(self.base_controller.models['text'].lines) - 1, self.base_controller.models['cursor'].cursor_y + 1)
        max_x = len(self.base_controller.models['text'].lines[curr_y]) - 1 if curr_y < len(self.base_controller.models['text'].lines) - 1 else len(self.base_controller.models['text'].lines[curr_y])
        return {
            'model': ['cursor'], 
            'update': {
                'update_cursor': {'dir': 'd', 'max_x': max_x, 'dy': curr_y},
            }
        }

    def move_cursor_left(self):
        pos_x = max(0, self.base_controller.models['cursor'].cursor_x - 1)
        curr_y = self.base_controller.models['cursor'].cursor_y
        return {
            'model': ['cursor'], 
            'update': {
                'update_cursor': {'dir': 'l', 'max_x': pos_x, 'dy': curr_y}
            }
        }

    def move_cursor_right(self):
        len_ = len(self.base_controller.models['text'].lines[self.base_controller.models['cursor'].cursor_y]) - 1 if self.base_controller.models['cursor'].cursor_y < len(self.base_controller.models['text'].lines) - 1 else len(self.base_controller.models['text'].lines[self.base_controller.models['cursor'].cursor_y])
        pos_x = min(len_, self.base_controller.models['cursor'].cursor_x + 1)
        curr_y = self.base_controller.models['cursor'].cursor_y
        return {
            'model': ['cursor'], 
            'update': {
                'update_cursor': {'dir': 'r', 'max_x': pos_x, 'dy': curr_y}
            }
        }