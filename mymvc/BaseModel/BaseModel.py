from typing import List
#from BaseController import BaseController
#from mymvc.BaseController.BaseController import BaseController
#from Observer import Observer
from mymvc.Observer.Observer import Observer

class BaseModel:
    def __init__(self) -> None:
        self._observers: List = []

    def add_observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify_observers(self) -> None:
        """for observer in self.__observers:
            observer.update_status_bar("default", "file_name", 0, 0)
            observer.update_text("Updated text")
            observer.update_cursor(0, 0)"""
        raise NotImplementedError("Метод notify_observers должен быть реализован в подклассе.")

    def update_data(self, data) -> None:
        raise NotImplementedError("Метод update_data должен быть реализован в подклассе.")
