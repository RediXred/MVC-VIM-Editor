from mymvc.Input.IInput import IInput
import curses

class InputConsole(IInput):
    """
    Реализация IInput для консольного ввода с использованием curses.
    """
    def __init__(self, stdscr: curses.window) -> None:
        self._stdscr = stdscr

    def get_key(self):
        """
        Считывает и возвращает код нажатой клавиши.
        """
        try:
            key = self._stdscr.getch()
            return key
        except curses.error:
            return None