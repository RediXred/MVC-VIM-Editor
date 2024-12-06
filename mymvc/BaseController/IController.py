from abc import ABC, abstractmethod

class IController(ABC):
    @abstractmethod
    def handle_key(self, key: int) -> str:
        """
        Обрабатывает нажатую клавишу.
        :param key: Код нажатой клавиши
        :return: Результат обработки
        """
        pass
    
    def register_commands(self) -> None:
        """
        Регистрирует команды для конкретного контроллера.
        Каждому контроллеру будет свой набор команд.
        """
        pass