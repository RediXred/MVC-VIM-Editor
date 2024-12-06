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
        self.commands[10] = InputCommand(self.base_controller, 'navigation') #enter
        self.commands[8] = InputCommand(self.base_controller, 'navigation') #backspace
        
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
            return {
                'model': ['cursor', 'text', 'status_bar'],
                'update': {
                    'update_cursor': {'dx': 1, 'dy': 0, 'max_y': 0},
                    'update_text': {'text': char},
                    'update_status_bar': {'current_line': 0, 'total_lines': 0}
                }
            }
