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
        self.commands[KEY_UP] = SearchCommand(self.base_controller, 'navigation')
        self.commands[27] = SearchCommand(self.base_controller, 'navigation') #esc
        
        
    def handle_key(self, key: int) -> str:
        if 32 <= key <= 126:
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
            if self.cmd in self.commands:
                command = self.commands[self.cmd]
                if self.cmd == "p":
                    result = command.execute(self.cmd, self.copystr)
                else:
                    result = command.execute(self.cmd)
                self.cmd = ""  # Сбрасываем буфер после выполнения команды
                if 'update_copystr' in result:
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