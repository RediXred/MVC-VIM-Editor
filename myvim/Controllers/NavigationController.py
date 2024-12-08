#from ...mymvc.BaseController.IController import IController
from mymvc.BaseController.IController import IController
from ..Commands.NavigationCommand import NavigationCommand
#from ...mymvc.BaseController.BaseController import BaseController
from mymvc.BaseController.BaseController import BaseController

from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT

class NavigationModeController(IController):
    def __init__(self, base_controller: BaseController):
        self.base_controller = base_controller
        self.commands = {}

    def register_commands(self):
        self.commands[KEY_UP] = NavigationCommand(self.base_controller, 'navigation')
        self.commands[KEY_DOWN] = NavigationCommand(self.base_controller, 'navigation')
        self.commands[KEY_LEFT] = NavigationCommand(self.base_controller, 'navigation')
        self.commands[KEY_RIGHT] = NavigationCommand(self.base_controller, 'navigation')
        self.commands[105] = NavigationCommand(self.base_controller, 'input') # i
        self.commands[48] = NavigationCommand(self.base_controller, 'edit') # 0
        self.commands[36] = NavigationCommand(self.base_controller, 'edit') # $

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
