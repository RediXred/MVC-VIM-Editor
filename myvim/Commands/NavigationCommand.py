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
            return {'model': ['status_bar'], 
                    'update': {
                        'update_status_bar': {'mode': self.mode, 'file_name': 'Untitled'}
                        }
                    }
        else:
            return {'model': None, 'update': None}
    
    def move_cursor_up(self):
        return {
            'model': ['cursor', 'status_bar'], 
            'update': {
                'update_cursor': {'dx': 0, 'dy': -1, 'max_y': 0},
                'update_status_bar': {'current_line': -1, 'total_lines': 0}
            }
        }

    def move_cursor_down(self):
        return {
            'model': ['cursor', 'status_bar'], 
            'update': {
                'update_cursor': {'dx': 0, 'dy': 1, 'max_y': 0},
                'update_status_bar': {'current_line': 1, 'total_lines': 0}
            }
        }

    def move_cursor_left(self):
        return {
            'model': ['cursor'], 
            'update': {
                'update_cursor': {'dx': -1, 'dy': 0, 'max_y': 0}
            }
        }

    def move_cursor_right(self):
        return {
            'model': ['cursor'], 
            'update': {
                'update_cursor': {'dx': 1, 'dy': 0, 'max_y': 0}
            }
        }