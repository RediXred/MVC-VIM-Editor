#from ...mymvc.BaseController.IController import IController
from mymvc.BaseController.IController import IController
from ..Commands.InputCommand import InputCommand
#from ...mymvc.BaseController.BaseController import BaseController
from mymvc.BaseController.BaseController import BaseController

from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT

class InputModeController(IController):
    def __init__(self, base_controller: BaseController):
        self.base_controller = base_controller
        self.commands = {}

    def register_commands(self):
        self.commands[KEY_UP] = InputCommand(self.base_controller, 'input')
        self.commands[KEY_DOWN] = InputCommand(self.base_controller, 'input')
        self.commands[KEY_LEFT] = InputCommand(self.base_controller, 'input')
        self.commands[KEY_RIGHT] = InputCommand(self.base_controller, 'input')
        self.commands[27] = InputCommand(self.base_controller, 'navigation') #esc
        self.commands[10] = InputCommand(self.base_controller, 'input') #enter
        self.commands[8] = InputCommand(self.base_controller, 'input') #backspace
        self.commands[330] = InputCommand(self.base_controller, 'input') #del
        
    def handle_key(self, key: int) -> str:
        if key in self.commands:
            command = self.commands[key]
            if key == KEY_UP:
                key = 1
            elif key == KEY_DOWN:
                key = 2
            elif key == KEY_LEFT:
                key = 3
            elif key == KEY_RIGHT:
                key = 4
            """
            elif key == TO_SWITCH_MODE:
                base_controller.switch_controller(command.mode)
            """
            return command.execute(key)
        else:
            char = chr(key)
            
            cur_input_x = self.base_controller.models['cursor'].cursor_x
            cur_y = self.base_controller.models['cursor'].cursor_y
            
            cur_posx = self.base_controller.models['cursor'].posx
            cur_posy = self.base_controller.models['cursor'].posy
            _, window_width = self.base_controller.models['text'].get_rendered_lines()
            
            # Перенос строки
            cur_input_x += 1
            #cur_posx += 1
            if cur_input_x == window_width:
                cur_y += 1
                cur_input_x = 0
                
            return {
                'model': ['text', 'cursor'],
                'update': {
                    'update_cursor': {'dir': 'r', 'cx': cur_input_x, 'cy': cur_y, 'pos_x': cur_posx + 1, 'pos_y': cur_posy},
                    'update_text': {'input': 1, 'text': char, 'pos_x': cur_posx, 'pos_y': cur_posy}
                }
            }
