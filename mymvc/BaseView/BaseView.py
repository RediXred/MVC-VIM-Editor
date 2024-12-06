
#from Observer import Observer
from mymvc.Observer.Observer import Observer
from mymvc.BaseView.ITUIAdapter import ITUIAdapter


class ViewBase(Observer):
    def __init__(self, adapter: ITUIAdapter) -> None:
        self.__adapter = adapter

    def get_tui_adapter(self) -> ITUIAdapter:
        return self.__adapter

    def update_status_bar(self, mode: str, f_name: str, current_line: int, total_lines: int) -> None:
        raise NotImplementedError("Метод update_status_bar должен быть реализован в подклассе.")

    def update_text(self, text: str) -> None:
        raise NotImplementedError("Метод update_text должен быть реализован в подклассе.")

    def update_cursor(self, cursor_x: int, cursor_y: int) -> None:
        raise NotImplementedError("Метод update_cursor должен быть реализован в подклассе.")
