#from ...mymvc.Commands.ICommand import ICommand
from mymvc.Commands.ICommand import ICommand
#from ...mymvc.BaseController.BaseController import BaseController
from mymvc.BaseController.BaseController import BaseController

class NavigationCommand(ICommand):
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
        elif key == 105:
            self.base_controller.switch_controller(self.mode)
            return {'model': ['cursor'], 
                    'update': {
                        'update_cursor': {'switch': 1, 'mode': self.mode}
                        }
                    }
        else:
            return {'model': None, 'update': None}
    
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