from mymvc.BaseView.BaseView import ViewBase
from mymvc.BaseView.ITUIAdapter import ITUIAdapter


class ViewCursor(ViewBase):
    def __init__(self, adapter: ITUIAdapter) -> None:
        super().__init__(adapter)

    def update_cursor(self, cursor_x: int, cursor_y: int) -> None:
        #cursor_position = f"Cursor at: ({cursor_x}, {cursor_y})"
        self.get_tui_adapter().update_cursor_position(cursor_x, cursor_y)
