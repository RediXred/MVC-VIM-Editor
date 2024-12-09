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
        self.cmd = ""
        self.copystr = ""

    def register_commands(self):
        self.commands[KEY_UP] = NavigationCommand(self.base_controller, 'navigation')
        self.commands[KEY_DOWN] = NavigationCommand(self.base_controller, 'navigation')
        self.commands[KEY_LEFT] = NavigationCommand(self.base_controller, 'navigation')
        self.commands[KEY_RIGHT] = NavigationCommand(self.base_controller, 'navigation')
        self.commands[105] = NavigationCommand(self.base_controller, 'input') # i
        self.commands['/'] = NavigationCommand(self.base_controller, 'search') # /
        self.commands['?'] = NavigationCommand(self.base_controller, 'search') # ?
        self.commands[94] = NavigationCommand(self.base_controller, 'navigation') # ^
        self.commands[36] = NavigationCommand(self.base_controller, 'navigation') # $
        self.commands["gg"] = NavigationCommand(self.base_controller, 'navigation')
        self.commands["G"] = NavigationCommand(self.base_controller, 'navigation')
        self.commands["NG"] = NavigationCommand(self.base_controller, 'navigation')
        self.commands["diw"] = NavigationCommand(self.base_controller, 'navigation')
        self.commands["dd"] = NavigationCommand(self.base_controller, 'navigation')
        self.commands["yy"] = NavigationCommand(self.base_controller, 'navigation')
        self.commands["yw"] = NavigationCommand(self.base_controller, 'navigation')
        self.commands[98] = NavigationCommand(self.base_controller, 'navigation') #b
        self.commands["p"] = NavigationCommand(self.base_controller, 'navigation') #p
        self.commands["n"] = NavigationCommand(self.base_controller, 'navigation') #n #TODO
        self.commands["N"] = NavigationCommand(self.base_controller, 'navigation') #n #TODO
        self.commands["I"] = NavigationCommand(self.base_controller, 'input')
        self.commands["A"] = NavigationCommand(self.base_controller, 'input')
        self.commands["S"] = NavigationCommand(self.base_controller, 'input') #TODO
        self.commands["r"] = NavigationCommand(self.base_controller, 'input')
        self.commands[119] = NavigationCommand(self.base_controller, 'navigation') #w
        self.commands[120] = NavigationCommand(self.base_controller, 'navigation') #x
        self.commands[339] = NavigationCommand(self.base_controller, 'navigation') #PGUP  #TODO
        self.commands[338] = NavigationCommand(self.base_controller, 'navigation') #PGDWN #TODO

    def handle_key(self, key: int) -> str:
        if 32 <= key <= 126:
            if 'r' in self.cmd:
                char = chr(key)
                command = self.commands["r"]
                self.cmd = ""
                return command.execute("r", char)
            
            if key == ord('G') and self.cmd.isdigit():
                line_number = int(self.cmd)  # Получаем номер строки из команды
                self.cmd = ""  # Сбрасываем буфер после обработки команды
                command = self.commands["NG"]
                # Выполняем переход на строку
                return command.execute(key, line_number)
            
            self.cmd += chr(key)

            # Ограничиваем длину буфера
            if len(self.cmd) > 3:
                self.cmd = self.cmd[-3:]
            
            # Если введённая строка совпадает с командой
            if self.cmd in self.commands and chr(key) != 'r':
                command = self.commands[self.cmd]
                if self.cmd == "p":
                    result = command.execute(self.cmd, self.copystr)
                else:
                    result = command.execute(self.cmd)
                self.cmd = ""  # Сбрасываем буфер после выполнения команды
                if result is not None and 'update_copystr' in result:
                    self.copystr = result['update_copystr']
                return result

            # Если команда не может быть продолжена
            if not any(
                cmd.startswith(self.cmd) or self.cmd.isdigit()  # Добавляем проверку на цифры
                for cmd in self.commands if isinstance(cmd, str)
            ):
                self.cmd = ""

        # Если это односимвольная команда (число)
        if key in self.commands and self.cmd == "":
            command = self.commands[key]
            return command.execute(key)