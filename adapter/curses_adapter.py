import curses
from mymvc.BaseView.ITUIAdapter import ITUIAdapter

class CursesAdapter(ITUIAdapter):
    def __init__(self):
        self.screen = None  # Основной экран curses
        self.height = 0     # Высота экрана
        self.width = 0      # Ширина экрана

    def create_screen(self):
        """Создает основной экран curses."""
        self.screen = curses.initscr()
        curses.noecho()  
        curses.cbreak()
        self.screen.keypad(True)
        self.height, self.width = self.screen.getmaxyx()

    def set_screen(self, screen):
        """Устанавливает новое окно для работы."""
        self.screen = screen
        self.height, self.width = self.screen.getmaxyx()

    def clear_screen(self):
        """Очищает экран."""
        if self.screen:
            self.screen.clear()

    def display_text(self, text, y=0, x=0):
        """Отображает текст в указанной позиции."""
        if self.screen:
            try:
                self.screen.addstr(y, x, text)
            except curses.error:
                pass

    def switch_screen(self, screen):
        """Переключает текущее окно."""
        self.set_screen(screen)
        self.clear_screen()
        self.refresh()

    def refresh(self):
        """Обновляет экран."""
        if self.screen:
            self.screen.refresh()

    def update_status_bar(self, status_message: str) -> None:
        """Обновляет строку состояния внизу экрана."""
        if self.screen:
            try:
                cursor_y, cursor_x = self.screen.getyx()
                self.screen.addstr(self.height - 1, 0, status_message.ljust(self.width - 1))
                self.screen.refresh()
                self.screen.move(cursor_y, cursor_x)
            except curses.error:
                pass

    def update_cursor_position(self, cursor_x: int, cursor_y: int) -> None:
        """Обновляет позицию курсора."""
        if self.screen:
            try:
                self.screen.move(cursor_y, cursor_x)
                self.screen.refresh()
            except curses.error:
                pass

    def update_text_display(self, text: str) -> None:
        """Обновляет область для текста."""
        if self.screen:
            try:
                self.clear_screen()
                self.screen.addstr(0, 0, text)
                self.screen.refresh()
            except curses.error:
                pass

    def __del__(self):
        """Очищает curses перед выходом."""
        if self.screen:
            curses.nocbreak()
            self.screen.keypad(False)
            curses.echo()
            curses.endwin()
