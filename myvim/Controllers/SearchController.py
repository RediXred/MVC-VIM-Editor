#from ...mymvc.BaseController.IController import IController
from mymvc.BaseController.IController import IController
from ..Commands.SearchCommand import SearchCommand
#from ...mymvc.BaseController.BaseController import BaseController
from mymvc.BaseController.BaseController import BaseController

from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT

class SearchModeController(IController):
    def __init__(self, base_controller: BaseController):
        self.base_controller = base_controller
        self.commands = {}
        self.cmd = ""
        self.copystr = ""

    def register_commands(self):
        self.commands[27] = SearchCommand(self.base_controller, 'navigation') #esc
        self.commands[10] = SearchCommand(self.base_controller, 'navigation')
        
    def handle_key(self, key: int) -> str:
        if key == 10 or key == 27: #enter
            t = self.base_controller.models['text'].typee
            command = self.commands[key]
            if key == 10:
                res = command.execute(key, self.cmd, t)
            else:
                res = command.execute(key, self.cmd)
            self.cmd = ""
            return res
        else:
            self.cmd += chr(key)
            _, window_width, window_height = self.base_controller.models['text'].get_rendered_lines()
            pos_y = window_height - 2
            pos_x = window_width - 10
            return {
                'model': ['text', 'cursor'],
                'update': {
                    'update_text': {'input_bar': 1, 'text': self.cmd, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_cursor': {'nth': 1}
                }
            }