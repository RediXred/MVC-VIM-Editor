from mymvc.BaseView.BaseView import ViewBase
from mymvc.BaseView.ITUIAdapter import ITUIAdapter


class ViewText(ViewBase):
    def __init__(self, adapter: ITUIAdapter) -> None:
        super().__init__(adapter)

    def update_text(self, text: str) -> None:
        """
        Обновляет отображение текста в редакторе.
        :param text: Текст, который нужно отобразить
        """
        self.get_tui_adapter().update_text_display(text)
