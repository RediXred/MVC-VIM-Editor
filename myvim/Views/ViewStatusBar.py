from mymvc.BaseView.BaseView import ViewBase
from mymvc.BaseView.ITUIAdapter import ITUIAdapter


class ViewStatusBar(ViewBase):
    def __init__(self, adapter: ITUIAdapter) -> None:
        super().__init__(adapter)

    def update_status_bar(self, mode: str, f_name: str, current_line: int, total_lines: int) -> None:
        """
        Обновляет статусную строку, отображая текущий режим, имя файла и строки.
        :param mode: Режим работы редактора (например, "Навигация")
        :param f_name: Имя файла
        :param current_line: Текущая строка
        :param total_lines: Общее количество строк
        """
        status_message = f"Mode: {mode} | File: {f_name} | Line: {current_line}/{total_lines}"
        self.get_tui_adapter().update_status_bar(status_message)
