import curses

from myvim.Models.TextModel import TextModel
from myvim.Models.CursorModel import CursorModel
from myvim.Models.SBModel import StatusBarModel

from myvim.Views.ViewText import ViewText
from myvim.Views.ViewCursor import ViewCursor
from myvim.Views.ViewStatusBar import ViewStatusBar

from myvim.input.InputConsole import InputConsole

from myvim.Controllers.NavigationController import NavigationModeController
from myvim.Controllers.InputController import InputModeController
from myvim.Controllers.SearchController import SearchModeController

from mymvc.BaseController.BaseController import BaseController


from adapter.curses_adapter import CursesAdapter


def main(stdscr: curses.window) -> None:
    curses.curs_set(1)
    stdscr.clear()
    
    text_model = TextModel()
    cursor_model = CursorModel()
    #status_bar_model = StatusBarModel()
    
    adapter = CursesAdapter()
    adapter.set_screen(stdscr)
    adapter.create_screen()
    
    view_text = ViewText(adapter)
    view_cursor = ViewCursor(adapter)
    view_status_bar = ViewStatusBar(adapter)
    
    text_model.add_observer(view_text)
    cursor_model.add_observer(view_cursor)
    cursor_model.add_observer(view_status_bar)
    #status_bar_model.add_observer(view_status_bar)
    
    input_handler = InputConsole(stdscr)
    
    base_controller = BaseController(input_handler)
    
    base_controller.add_controller('navigation', NavigationModeController(base_controller))
    base_controller.add_controller('input', InputModeController(base_controller))
    base_controller.add_controller('search', SearchModeController(base_controller))
    
    
    base_controller.add_model('text', text_model)
    base_controller.add_model('cursor', cursor_model)
    #base_controller.add_model('status_bar', status_bar_model)
    
    base_controller.switch_controller('navigation')
    
    base_controller.start_cycle()
    
if __name__ == "__main__":
    curses.wrapper(main)