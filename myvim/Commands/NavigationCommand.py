#from ...mymvc.Commands.ICommand import ICommand
from mymvc.Commands.ICommand import ICommand
#from ...mymvc.BaseController.BaseController import BaseController
from mymvc.BaseController.BaseController import BaseController
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT


class NavigationCommand(ICommand):
    def __init__(self, base_controller: BaseController, mode: str):
        self.base_controller = base_controller
        self.mode = mode

    def execute(self, key, n=-1) -> str:
        if n != -1 and key != 'p' and key != 'r':
            return self.move_to(n)
        if key == KEY_UP:
            return self.move_cursor_up()
        elif key == KEY_DOWN:
            return self.move_cursor_down()
        elif key == KEY_LEFT:
            return self.move_cursor_left()
        elif key == KEY_RIGHT:
            return self.move_cursor_right()
        elif key == "gg":
            return self.scroll_up()
        elif key == "G":
            return self.scroll_down()
        elif key == "diw":
            return self.delete_word_under_cursor()
        elif key == 36:
            return self.at_end()
        elif key == 94:
            return self.at_start()
        elif key == 338:
            return self.pgdown()
        elif key == 98:
            return self.move_cursor_to_previous_word()
        elif key == 119:
            return self.move_cursor_to_next_word()
        elif key == 120:
            return self.delete_character_after_cursor()
        elif key == "dd":
            return self.cut_current_line()
        elif key == "yy":
            return self.copy_current_line()
        elif key == "yw":
            return self.copy_current_word()
        elif key == "p" and n != -1:
            return self.paste(n)
        elif key == "n":
            return self.next_find(self.base_controller.models['text'].search_text)
        elif key == "N":
            return self.back_find(self.base_controller.models['text'].search_text)
        elif key == "I":
            return self.input_start()
        elif key == "A":
            return self.input_end()
        elif key == "S":
            return self.input_s()
        elif key == "r":
            return self.swap(n)
        elif key == 105:
            self.base_controller.switch_controller(self.mode)
            return {'model': ['cursor'], 
                    'update': {
                        'update_cursor': {'switch': 1, 'mode': self.mode}
                        }
                    }
        elif key == '/':
            self.base_controller.switch_controller(self.mode)
            return {'model': ['text', 'cursor'], 
                    'update': {
                        'update_cursor': {'switch': 1, 'mode': self.mode},
                        'update_text': {'update_typee': 0, 'text': '', 'pos_y': 0, 'pos_x': 0}
                        }
                    }
        elif key == '?':
            self.base_controller.switch_controller(self.mode)
            return {'model': ['text', 'cursor'], 
                    'update': {
                        'update_cursor': {'switch': 1, 'mode': self.mode},
                        'update_text': {'update_typee': 1, 'text': '', 'pos_y': 0, 'pos_x': 0}
                        }
                    }
    
    def swap(self, c):
        pos_x = self.base_controller.models['cursor'].posx
        pos_y = self.base_controller.models['cursor'].posy
        px = self.base_controller.models['cursor'].cursor_x
        py = self.base_controller.models['cursor'].cursor_y
        lines = self.base_controller.models['text'].lines
        top_scroll = self.base_controller.models['text'].scroll_top
        lines[pos_y] = lines[pos_y][:pos_x] + c + lines[pos_y][pos_x + 1:]
        return {'model': ['text', 'cursor'], 
                'update': {
                    'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'update_text': 1, 'text': lines, 'scroll_top': top_scroll}
                    }
                }
    
    def input_s(self):
        result = self.cut_current_line()
        top_scroll = result['update']['update_text']['scroll_top']
        px = result['update']['update_cursor']['cx']
        py = result['update']['update_cursor']['cy']
        pos_x = result['update']['update_cursor']['pos_x']
        pos_y = result['update']['update_cursor']['pos_y']
        lines = result['update']['update_text']['text']
        
        if len(lines) == 1:
            if lines[0] == '':
                pos_x = 0
                pos_y = 0
                py = 0
                px = 0
                top_scroll = 0
            else:
                if pos_y == 0:
                    lines.insert(pos_y, '\n')
                else:
                    pass
        else:
            if pos_y + 1 < len(lines):
                lines.insert(pos_y + 1, '\n')
                pos_y += 1
                py += 1
                if py > 4:
                    py -= 1
                    top_scroll += 1
                pos_x = 0
                px = 0
                self.base_controller.models['cursor'].total_lines += 1
            else:
                lines[pos_y] += '\n'
                pos_y += 1
                lines.insert(pos_y, '')
                px = 0
                py += 1
                if py > 4:
                    py -= 1
                    top_scroll += 1
                self.base_controller.models['cursor'].total_lines += 1
                
        
        self.base_controller.switch_controller(self.mode)
        return {'model': ['text', 'cursor'], 
                'update': {
                    'update_cursor': {'switch': 1, 'mode': self.mode, 'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'update_text': 1, 'text': lines, 'scroll_top': top_scroll}
                    }
                }
    
    def input_end(self):
        result = self.at_end()
        top_scroll = result['update']['update_text']['scroll_top']
        px = result['update']['update_cursor']['cx']
        py = result['update']['update_cursor']['cy']
        pos_x = result['update']['update_cursor']['pos_x']
        pos_y = result['update']['update_cursor']['pos_y']
        self.base_controller.switch_controller(self.mode)
        return {'model': ['text', 'cursor'], 
                'update': {
                    'update_cursor': {'switch': 1, 'mode': self.mode, 'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'scroll_down': 1, 'text': '', 'scroll_top': top_scroll}
                    }
                }
    
    def input_start(self):
        result = self.at_start()
        top_scroll = result['update']['update_text']['scroll_top']
        px = result['update']['update_cursor']['cx']
        py = result['update']['update_cursor']['cy']
        pos_x = result['update']['update_cursor']['pos_x']
        pos_y = result['update']['update_cursor']['pos_y']
        self.base_controller.switch_controller(self.mode)
        return {'model': ['text', 'cursor'], 
                'update': {
                    'update_cursor': {'switch': 1, 'mode': self.mode, 'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'scroll_down': 1, 'text': '', 'scroll_top': top_scroll}
                    }
                }
    
    def back_find(self, n):
            self.base_controller.switch_controller(self.mode)
            pos_x = self.base_controller.models['cursor'].posx
            pos_y = self.base_controller.models['cursor'].posy
            px = self.base_controller.models['cursor'].cursor_x
            py = self.base_controller.models['cursor'].cursor_y
            _, window_width, _ = self.base_controller.models['text'].get_rendered_lines()
            top_scroll = self.base_controller.models['text'].scroll_top
            tmp = top_scroll
            lines = self.base_controller.models['text'].lines
            word = lines[pos_y][pos_x:pos_x + len(n.rstrip('\n'))]
            """if pos_y < len(lines[pos_y].rstrip('\n')):
                pos_x += 1
                if pos_x < window_width - 1:
                    px += 1
                else:
                    px = pos_x % window_width
                    py += 1
                    if py > 4:
                        py -= 1
                        top_scroll += 1"""
            if pos_y >= 0 and pos_x - 1 >= 0:
                pos_x -= 1
                if pos_x < window_width - 1:
                    px -= 1
                else:
                    px = pos_x % window_width
                    if pos_x + 1 % window_width == 0:
                        py -= 1
                        if py <= 4 and top_scroll > 0:
                            py += 1
                            top_scroll -= 1
            if 1:
                flag = False
                if pos_y >= 0:
                    while pos_y >= 0 and not flag:
                        current_line = lines[pos_y]
                        k, m = len(current_line.rstrip('\n')), len(n.rstrip('\n'))
                        i = pos_x
                        while i <= k - m:  # Проверяем, чтобы оставшийся текст был не короче подстроки
                            word = current_line[i:i + m]
                            if word == n:
                                flag = True
                                break
                            i -= 1
                            pos_x -= 1
                            px -= 1
                            if px == -1 and pos_x > 0:
                                py -= 1
                                px = window_width - 1
                                if py <= 4 and top_scroll > 0:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                                    py += 1
                                    top_scroll -= 1
                        
                        if pos_y - 1 >= 0 and not flag:
                            pos_y -= 1
                            pos_x = len(lines[pos_y].rstrip('\n'))
                            px = pos_x % window_width
                            py -= 1
                            if py <= 4 and top_scroll > 0:
                                py += 1
                                top_scroll -= 1
                        else:
                            break
                    
                    if flag == True:
                        self.base_controller.models['text'].search_text = word
                        return {
                            'model': ['text', 'cursor'],
                            'update': {
                                'update_text': {'update_text': 1, 'text': lines, 'scroll_top': top_scroll},
                                'update_cursor': {'switch': 1, 'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y, 'mode': self.mode},
                            }          
                        }
    def next_find(self, n):
            self.base_controller.switch_controller(self.mode)
            pos_x = self.base_controller.models['cursor'].posx
            pos_y = self.base_controller.models['cursor'].posy
            px = self.base_controller.models['cursor'].cursor_x
            py = self.base_controller.models['cursor'].cursor_y
            _, window_width, _ = self.base_controller.models['text'].get_rendered_lines()
            top_scroll = self.base_controller.models['text'].scroll_top
            tmp = top_scroll
            lines = self.base_controller.models['text'].lines
            word = lines[pos_y][pos_x:pos_x + len(n.rstrip('\n'))]
            if pos_x < len(lines[pos_y].rstrip('\n')):
                pos_x += 1
                if pos_x < window_width - 1:
                    px += 1
                else:
                    px = pos_x % window_width
                    if pos_x - 1 % window_width == 0:
                        py += 1
                        if py > 4:
                            py -= 1
                            top_scroll += 1
            if 1:
                flag = False
                if pos_y < len(lines):
                    while pos_y < len(lines) and not flag:
                        current_line = lines[pos_y]
                        k, m = len(current_line.rstrip('\n')), len(n.rstrip('\n'))
                        i = pos_x
                        while i <= k - m:  # Проверяем, чтобы оставшийся текст был не короче подстроки
                            word = current_line[i:i + m]
                            if word == n:
                                flag = True
                                break
                            i += 1
                            pos_x += 1
                            px += 1
                            if px == window_width:
                                py += 1
                                px = 0
                                if py > 4:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                                    py -= 1
                                    top_scroll += 1
                        
                        if pos_y + 1 < len(lines) and not flag:
                            pos_y += 1
                            pos_x = 0
                            px = 0
                            py += 1
                            if py > 4:
                                py -= 1
                                top_scroll += 1
                        else:
                            break
                    
                    if flag == True:
                        self.base_controller.models['text'].search_text = word
                        return {
                            'model': ['text', 'cursor'],
                            'update': {
                                'update_text': {'update_text': 1, 'text': lines, 'scroll_top': top_scroll},
                                'update_cursor': {'switch': 1, 'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y, 'mode': self.mode},
                            }          
                        }
                    
    
    def paste(self, copystr):
        lines = self.base_controller.models['text'].lines
        pos_x = self.base_controller.models['cursor'].posx  # Текущая позиция по горизонтали
        pos_y = self.base_controller.models['cursor'].posy  # Текущая позиция по вертикали
        rendered_lines, window_width, height = self.base_controller.models['text'].get_rendered_lines()
        py = self.base_controller.models['cursor'].cursor_y
        px = self.base_controller.models['cursor'].cursor_x
        top_scroll = self.base_controller.models['text'].scroll_top
        # Проверяем, что текущая строка не пуста
        if pos_y < len(lines):
            current_line = lines[pos_y]

            while pos_x < len(current_line):
                pos_x += 1
                px += 1
                if px == window_width:
                    py += 1
                    px = 0
                    if py > 4:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                        py -= 1
                        top_scroll += 1
            lines[pos_y] = lines[pos_y].rstrip('\n')
            lines[pos_y] += '\n'
            copystr = copystr.rstrip('\n')
            if pos_y < len(lines) - 1:
                copystr += '\n'
            lines.insert(pos_y + 1, copystr)
            pos_y += 1
            pos_x = 0
            px = 0
            py += 1
            if py > 4:
                py -= 1
                top_scroll += 1
            self.base_controller.models['cursor'].total_lines += 1

        # Обновляем позицию курсора
        self.base_controller.models['cursor'].posx = pos_x
        self.base_controller.models['cursor'].posy = pos_y

        return {
            'model': ['text', 'cursor'],
            'update': {
                'update_text': {'update_text': 1, 'text': lines, 'scroll_top': top_scroll},
                'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y}
            }          
        }
    
    def copy_current_word(self):
        lines = self.base_controller.models['text'].lines
        pos_y = self.base_controller.models['cursor'].posy  # Текущая позиция по вертикали
        pos_x = self.base_controller.models['cursor'].posx  # Текущая позиция по горизонтали
        px = self.base_controller.models['cursor'].cursor_x
        py = self.base_controller.models['cursor'].cursor_y
        _, window_width, _ = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        
        current_line = lines[pos_y]
        end_pos = pos_x
        start_pos = pos_x
        while end_pos < len(current_line) and not current_line[end_pos].isspace():
            end_pos += 1
        while start_pos > 0 and not current_line[start_pos].isspace():
            start_pos -= 1
        
        copystr = current_line[start_pos:end_pos]
        copystr = copystr.strip(' ')
        return {
            'model': ['text', 'cursor'],
            'update': {
                'update_text': {'update_text': 1, 'text': lines, 'scroll_top': top_scroll},
                'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y}
            },
            'update_copystr': copystr            
        }
        
    def copy_current_line(self):
        lines = self.base_controller.models['text'].lines
        pos_y = self.base_controller.models['cursor'].posy  # Текущая позиция по вертикали
        pos_x = self.base_controller.models['cursor'].posx  # Текущая позиция по горизонтали
        px = self.base_controller.models['cursor'].cursor_x
        py = self.base_controller.models['cursor'].cursor_y
        _, window_width, _ = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        
        copystr = lines[pos_y]
        return {
            'model': ['text', 'cursor'],
            'update': {
                'update_text': {'update_text': 1, 'text': lines, 'scroll_top': top_scroll},
                'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y}
            },
            'update_copystr': copystr            
        }
        
    def cut_current_line(self):
        lines = self.base_controller.models['text'].lines
        pos_y = self.base_controller.models['cursor'].posy  # Текущая позиция по вертикали
        pos_x = self.base_controller.models['cursor'].posx  # Текущая позиция по горизонтали
        px = self.base_controller.models['cursor'].cursor_x
        py = self.base_controller.models['cursor'].cursor_y
        _, window_width, _ = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        # Проверяем, что есть строки для удаления
        if pos_y < len(lines):
            current_line = lines[pos_y].rstrip('\n')
            while pos_x > 0: #and not current_line[pos_x - 1].isspace():
                pos_x -= 1  # Двигаемся к началу слова
                px -= 1
                if px == -1:
                    py -= 1
                    px = window_width - 1
                    if py <= 4 and top_scroll > 0:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                        py += 1
                        top_scroll -= 1
            # Удаляем текущую строку
            copy = lines[pos_y]
            del lines[pos_y]
            self.base_controller.models['cursor'].total_lines = max(0, self.base_controller.models['cursor'].total_lines - 1)
            if pos_y > 0:
                pos_y -= 1
                py -= 1
                
            if len(lines) == 0:
                #pos_y += 1
                #py += 1
                lines.append('')
                self.base_controller.models['cursor'].total_lines += 1
            if pos_y == 0 and len(lines) == 1:
                lines[pos_y] = lines[pos_y].rstrip('\n')
                pos_x = len(lines[pos_y].rstrip('\n'))
                px = pos_x % window_width
            else:
                if pos_y + 1 >= len(lines):
                    lines[pos_y] = lines[pos_y].rstrip('\n')
                pos_x = len(lines[pos_y].rstrip('\n'))
                px = pos_x % window_width
                if top_scroll > 0:
                    top_scroll -= 1
                    py += 1                
        # Обновляем модели
        self.base_controller.models['cursor'].posx = pos_x
        self.base_controller.models['cursor'].posy = pos_y

        return {
            'model': ['text', 'cursor'],
            'update': {
                'update_text': {'update_text': 1, 'text': lines, 'scroll_top': top_scroll},
                'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y}
            },
            'update_copystr': copy            
        }

    
    def delete_word_under_cursor(self):
        lines = self.base_controller.models['text'].lines
        pos_x = self.base_controller.models['cursor'].posx  # Текущая позиция по горизонтали
        pos_y = self.base_controller.models['cursor'].posy  # Текущая позиция по вертикали
        top_scroll = self.base_controller.models['text'].scroll_top
        px = self.base_controller.models['cursor'].cursor_x
        py = self.base_controller.models['cursor'].cursor_y
        _, window_width, _ = self.base_controller.models['text'].get_rendered_lines()

        # Проверяем, что текущая строка не пуста
        if pos_y < len(lines):
            current_line = lines[pos_y]
            
            # Находим конец текущего слова
            end_pos = pos_x
            start_pos = pos_x
            while end_pos < len(current_line) and not current_line[end_pos].isspace():
                end_pos += 1
            while start_pos > 0 and not current_line[start_pos].isspace():
                start_pos -= 1
                px -= 1
                if px == -1:
                    py -= 1
                    px = window_width - 1
                    if py <= 4 and top_scroll > 0:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                        py += 1
                        top_scroll -= 1
            # Пропускаем пробелы после слова
            while end_pos < len(current_line) and current_line[end_pos].isspace():
                end_pos += 1
            
            while start_pos > 0 and not current_line[start_pos].isspace():
                start_pos -= 1
                px -= 1
                if px == -1:
                    py -= 1
                    px = window_width - 1
                    if py <= 4 and top_scroll > 0:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                        py += 1
                        top_scroll -= 1

            # Удаляем слово и пробелы справа
            lines[pos_y] = current_line[:start_pos] + current_line[end_pos:]
            
            if not lines[pos_y].strip():
                if pos_y > 0:  # Переход на предыдущую строку, если она существует
                    lines.pop(pos_y)
                    pos_y -= 1
                    pos_x = len(lines[pos_y].rstrip('\n'))  # В конец предыдущей строки
                    self.base_controller.models['cursor'].total_lines -= 1
                    self.base_controller.models['cursor'].current_line -= 1
                    py -= 1
                    px = pos_x % window_width
                else:
                    pos_x = 0  # Если строка единственная, курсор в начало
                    px = 0
                    py = 0
            else:
                pos_x = min(pos_x, len(lines[pos_y]))  # Убедиться, что курсор не выходит за пределы строки
                px = pos_x % window_width

        return {
            'model': ['text', 'cursor'],
            'update': {
                'update_text': {'text': lines, 'update_text': 1, 'scroll_top': top_scroll},
                'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y}
            }
        }
    
    def delete_character_after_cursor(self):
        lines = self.base_controller.models['text'].lines
        pos_x = self.base_controller.models['cursor'].posx  # Текущая позиция по горизонтали
        pos_y = self.base_controller.models['cursor'].posy  # Текущая позиция по вертикали
        top_scroll = self.base_controller.models['text'].scroll_top
        px = self.base_controller.models['cursor'].cursor_x
        py = self.base_controller.models['cursor'].cursor_y
        # Проверяем, что текущая строка не пуста
        if pos_y < len(lines):
            current_line = lines[pos_y]

            # Если курсор не в конце строки, удаляем символ после курсора
            if pos_x < len(current_line.rstrip('\n')):
                lines[pos_y] = current_line[:pos_x] + current_line[pos_x + 1:]
            elif pos_y < len(lines) - 1:  # Если курсор в конце строки, соединяем с следующей строкой
                next_line = lines[pos_y + 1]
                lines[pos_y] = current_line.rstrip('\n') + next_line
                del lines[pos_y + 1]
                self.base_controller.models['cursor'].total_lines -= 1

        return {
            'model': ['text', 'cursor'],
            'update': {
                'update_text': {'text': ' ', 'scroll_down': 1, 'scroll_top': top_scroll},
                'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y}
            }
        }
    
    def move_cursor_to_next_word(self):
        lines = self.base_controller.models['text'].lines
        pos_x = self.base_controller.models['cursor'].posx  # Текущая позиция по горизонтали
        pos_y = self.base_controller.models['cursor'].posy  # Текущая позиция по вертикали
        rendered_lines, window_width, height = self.base_controller.models['text'].get_rendered_lines()
        py = self.base_controller.models['cursor'].cursor_y
        px = self.base_controller.models['cursor'].cursor_x
        top_scroll = self.base_controller.models['text'].scroll_top
        # Проверяем, что текущая строка не пуста
        if pos_y < len(lines):
            current_line = lines[pos_y]

            # Если курсор находится в конце строки, переходим на следующую строку
            """if pos_x >= len(current_line.rstrip('\n')):
                if pos_y < len(lines) - 1:
                    pos_y += 1
                    current_line = lines[pos_y]
                    pos_x = 0  # В начало следующей строки
                else:
                    return  # Курсор уже в самом конце текста"""

            # Перемещаем курсор к концу текущего или следующего слова
            while pos_x < len(current_line) and not current_line[pos_x].isspace():
                pos_x += 1  # Двигаемся к концу слова
                px += 1
                if px == window_width:
                    py += 1
                    px = 0
                    if py > 4:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                        py -= 1
                        top_scroll += 1

            while pos_x < len(current_line) and current_line[pos_x].isspace():
                pos_x += 1  # Пропускаем пробелы справа
                px += 1
                if px == window_width:
                    py += 1
                    px = 0
                    if py > 4:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                        py -= 1
                        top_scroll += 1

        # Обновляем позицию курсора
        self.base_controller.models['cursor'].posx = pos_x
        self.base_controller.models['cursor'].posy = pos_y

        return {
            'model': ['text', 'cursor'],
            'update': {
                'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y},
                'update_text': {'scroll_down': 1, 'scroll_top': top_scroll, 'text': ' '}
            }
        }
    
    def move_cursor_to_previous_word(self):
        lines = self.base_controller.models['text'].lines
        pos_x = self.base_controller.models['cursor'].posx  # Текущая позиция по горизонтали
        pos_y = self.base_controller.models['cursor'].posy  # Текущая позиция по вертикали
        rendered_lines, window_width, height = self.base_controller.models['text'].get_rendered_lines()
        py = self.base_controller.models['cursor'].cursor_y
        px = self.base_controller.models['cursor'].cursor_x
        top_scroll = self.base_controller.models['text'].scroll_top
        # Проверяем, что текущая строка не пуста
        if pos_y < len(lines):
            current_line = lines[pos_y]
            
            # Если курсор находится в начале строки, переходим на предыдущую строку
            """if pos_x == 0:
                if py > 0:
                    pos_y -= 1
                    current_line = lines[pos_y]
                    pos_x = len(current_line.rstrip('\n'))  # В конец строки без символа переноса
                    py -= 1"""

            # Перемещаем курсор в начало текущего или предыдущего слова
            while pos_x > 0 and current_line[pos_x - 1].isspace():
                pos_x -= 1  # Пропускаем пробелы слева
                px -= 1
                if px == -1:
                    py -= 1
                    px = window_width - 1
                    if py <= 4 and top_scroll > 0:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                        py += 1
                        top_scroll -= 1

            while pos_x > 0 and not current_line[pos_x - 1].isspace():
                pos_x -= 1  # Двигаемся к началу слова
                px -= 1
                if px == -1:
                    py -= 1
                    px = window_width - 1
                    if py <= 4 and top_scroll > 0:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                        py += 1
                        top_scroll -= 1
        # Обновляем позицию курсора
        #self.base_controller.models['cursor'].posx = pos_x
        #self.base_controller.models['cursor'].posy = pos_y

        return {
            'model': ['text', 'cursor'],
            'update': {
                'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y},
                'update_text': {'scroll_down': 1, 'scroll_top': top_scroll, 'text': ' '}
            }
        }

    
    def pgdown(self):
        #TODO доделать
        rendered_lines, window_width, height = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        lines = self.base_controller.models['text'].lines
        cy = self.base_controller.models['cursor'].cursor_y
        cx = self.base_controller.models['cursor'].cursor_x
        pos_y = self.base_controller.models['cursor'].posy
        pos_x = self.base_controller.models['cursor'].posx
        
        new_scroll = top_scroll + height

        max_scroll = max(0, len(rendered_lines) - height - 1)
        new_scroll = min(new_scroll, max_scroll)
        i = pos_y
        py = (len(lines[i]) + window_width - 1) // window_width
        px = len(lines[i]) - 1 if lines[i][-1]=='\n' else len(lines[i])
        while py < height + 4 - 1:
            i += 1
            py += (len(lines[i]) + window_width - 1) // window_width
            px = len(lines[i]) - 1 if lines[i][-1]=='\n' else len(lines[i])
            if py > height:
                break
        if i != pos_y:
            pos_y = i
            pos_x = px
            cx = pos_x % window_width
        top_scroll = new_scroll
        
        rendered_lines = rendered_lines[top_scroll:top_scroll + height - 1]
        
        if len(rendered_lines) > height - 4:
            cy = height - 4 - 1
            
            #top_scroll = cy
            #top_scroll -= height - 4 - 1
            #top_scroll = 0 if top_scroll < 0 else top_scroll
            #if top_scroll != 0:
            #    cy = height - 4 - 1
        
        
        return {
                    'model': ['text','cursor'], 
                    'update': {
                        'update_cursor': {'dir': 'NG', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y},
                        'update_text': {'scroll_down': 1, 'scroll_top': top_scroll, 'text': ' '}
                    }
                }
        
        
        
    
    def move_to(self, n):
        n -= 1
        rendered_lines, window_width, height = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        lines = self.base_controller.models['text'].lines
        cy = self.base_controller.models['cursor'].cursor_y
        cx = self.base_controller.models['cursor'].cursor_x
        pos_y = self.base_controller.models['cursor'].posy
        pos_x = self.base_controller.models['cursor'].posx
        if n <= len(lines) - 1 and n >= 0:
            pos_y = n
            cy = sum((len(line) + window_width - 1) // window_width for line in lines[:pos_y])
            cx = 0
            pos_x = 0
            
            if len(rendered_lines) > height - 4:
                
                top_scroll = cy
                top_scroll -= height - 4 - 1
                top_scroll = 0 if top_scroll < 0 else top_scroll
                if top_scroll != 0:
                    cy = height - 4 - 1
            
        
            
            return {
                    'model': ['text','cursor'], 
                    'update': {
                        'update_cursor': {'dir': 'NG', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y},
                        'update_text': {'scroll_down': 1, 'scroll_top': top_scroll, 'text': ' '}
                    }
                }
    
    def scroll_down(self):
        rendered_lines, window_width, height = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        lines = self.base_controller.models['text'].lines
        cy = self.base_controller.models['cursor'].cursor_y
        cx = self.base_controller.models['cursor'].cursor_x
        pos_y = self.base_controller.models['cursor'].posy
        pos_x = self.base_controller.models['cursor'].posx
        
        
        cy = len(rendered_lines) - 1
        cx = len(rendered_lines[cy]) - 1 if rendered_lines[cy][-1]=='\n' else len(rendered_lines[cy])
        
        pos_y = len(lines) - 1
        pos_x = len(lines[pos_y]) - 1 if lines[pos_y][-1]=='\n' else len(lines[pos_y])
        
        if len(rendered_lines) > height - 4:
            top_scroll = cy
            top_scroll -= height - 4 - 1
            cy = height - 4 - 1
            
        return {
                'model': ['text','cursor'], 
                'update': {
                    'update_cursor': {'dir': 'G', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'scroll_down': 1, 'scroll_top': top_scroll, 'text': ' '}
                }
            }
    
    def at_start(self):
        _, window_width, _ = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        lines = self.base_controller.models['text'].lines
        py = self.base_controller.models['cursor'].cursor_y
        px = self.base_controller.models['cursor'].cursor_x
        pos_y = self.base_controller.models['cursor'].posy
        pos_x = self.base_controller.models['cursor'].posx
        if pos_y < len(lines):
            current_line = lines[pos_y].rstrip('\n')

            while pos_x > 0: #and not current_line[pos_x - 1].isspace():
                pos_x -= 1  # Двигаемся к началу слова
                px -= 1
                if px == -1:
                    py -= 1
                    px = window_width - 1
                    if py <= 4 and top_scroll > 0:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                        py += 1
                        top_scroll -= 1

            # Обновляем позицию курсора
            self.base_controller.models['cursor'].posx = pos_x
            self.base_controller.models['cursor'].posy = pos_y

            return {
                'model': ['text', 'cursor'],
                'update': {
                    'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'scroll_down': 1, 'scroll_top': top_scroll, 'text': ' '}
                }
            }
    
    def at_end(self):
        _, window_width, _ = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        lines = self.base_controller.models['text'].lines
        py = self.base_controller.models['cursor'].cursor_y
        px = self.base_controller.models['cursor'].cursor_x
        pos_y = self.base_controller.models['cursor'].posy
        pos_x = self.base_controller.models['cursor'].posx
        if pos_y < len(lines):
            current_line = lines[pos_y].rstrip('\n')

            while pos_x < len(current_line): #and current_line[pos_x].isspace():
                pos_x += 1  # Пропускаем пробелы справа
                px += 1
                if px == window_width:
                    py += 1
                    px = 0
                    if py > 4:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                        py -= 1
                        top_scroll += 1

            # Обновляем позицию курсора
            self.base_controller.models['cursor'].posx = pos_x
            self.base_controller.models['cursor'].posy = pos_y

            return {
                'model': ['text', 'cursor'],
                'update': {
                    'update_cursor': {'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'scroll_down': 1, 'scroll_top': top_scroll, 'text': ' '}
                }
            }
        
    
    def scroll_up(self):
        return {
                'model': ['text','cursor'], 
                'update': {
                    'update_cursor': {'dir': 's', 'cx': 0, 'cy': 0, 'pos_x': 0, 'pos_y': 0},
                    'update_text': {'scroll_down': 1, 'scroll_top': 0, 'text': ' '}
                }
            }
    
    def move_cursor_up(self):
        rendered_lines, window_width, height = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        cy = self.base_controller.models['cursor'].cursor_y
        cx = self.base_controller.models['cursor'].cursor_x
        if top_scroll > 0:
            px = self.base_controller.models['cursor'].posx
            py = self.base_controller.models['cursor'].posy
            
            l = len(self.base_controller.models['text'].lines[py - 1])
            l2 = len(self.base_controller.models['text'].lines[py])
            offset_ = (l + window_width - 1) // window_width
            if px > l:
                offset = (px//window_width) + 1#offset_ - (px // window_width)
            else:
                offset = ((l + window_width - 1) // window_width)
                #k = offset_ - (px // window_width)
                #offset = offset_ - (px // window_width)
            if cy - offset <= 3: #TODO доделать смещение
                if top_scroll - offset < 0:
                    cy -= offset
                    cy += top_scroll
                    self.base_controller.models['text'].scroll_top = 0
                    top_scroll = 0
                else:
                    #cy -= offset#1
                    self.base_controller.models['text'].scroll_top -= offset#1
                    top_scroll -= offset#1
        else:
            pos_y = self.base_controller.models['cursor'].posy
            if pos_y > 0:
                lines = self.base_controller.models['text'].lines
                rendered_lines = rendered_lines[top_scroll:]
                pos_x = self.base_controller.models['cursor'].posx
                offset = pos_x // window_width
                pos_y -= 1
                l = len(lines[pos_y + 1])
                l2 = len(lines[pos_y])
                #cy = sum((len(line) + window_width - 1) // window_width for line in lines[:pos_y]) + offset
                if pos_x > l2:
                    offset = (pos_x//window_width) + 1#offset_ - (pos_x // window_width)
                else:
                    offset = ((l2 + window_width - 1) // window_width)
                    #k = offset_ - (pos_x // window_width)
                    #offset = offset_ - (pos_x // window_width)
                cy -= offset
                pos_y += 1
        lines = self.base_controller.models['text'].lines
        rendered_lines = rendered_lines[top_scroll:]
        pos_x = self.base_controller.models['cursor'].posx
        pos_y = self.base_controller.models['cursor'].posy #- top_scroll
        if pos_y > 0:
            if pos_x > len(lines[pos_y-1]):
                if len(lines[pos_y-1]) and lines[pos_y-1][-1] == '\n':
                    l = len(lines[pos_y-1]) - 1    
                    pos_x = len(lines[pos_y-1]) - 1
                else:
                    l = len(lines[pos_y-1])
                    pos_x = len(lines[pos_y-1])
                cx = (l % window_width)
            else:
                cx = pos_x % window_width
                if pos_x == len(lines[pos_y-1]) and len(lines[pos_y-1]) and lines[pos_y-1][-1] == '\n':
                    pos_x -= 1
                    cx -= 1
                    
            pos_y -= 1
            return {
                'model': ['text','cursor'], 
                'update': {
                    'update_cursor': {'dir': 'u', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'scroll_down': 1, 'scroll_top': top_scroll, 'text': ' '}
                }
            }

    def move_cursor_down(self):
        cy = self.base_controller.models['cursor'].cursor_y
        cx = self.base_controller.models['cursor'].cursor_x
        rendered_lines, window_width, window_height = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        #TODO доделать смещение
        #offset = len(self.base_controller.models['text'].lines[self.base_controller.models['cursor'].posy]) // window_width - self.base_controller.models['cursor'].posx // window_width
        if self.base_controller.models['cursor'].posy + 1 < len(self.base_controller.models['text'].lines):
            px = self.base_controller.models['cursor'].posx
            py = self.base_controller.models['cursor'].posy# - top_scroll
            #offset_ = sum((len(line) + window_width - 1) // window_width for line in self.base_controller.models['text'].lines[py])
            l = len(self.base_controller.models['text'].lines[py])
            l2 = len(self.base_controller.models['text'].lines[py + 1])
            
            if (px > l2):
                k = (l + window_width - 1) // window_width
                offset = (k - (px // window_width + 1)) + 1
                offset += l2 // window_width
            else:
                offset_ = (l + window_width - 1) // window_width
                offset = offset_
            if (cy + offset) >= (window_height - 4):#(cy + offset) % (window_height - 4) == 0:
                top_scroll += offset
                
                self.base_controller.models['text'].scroll_top += offset
                #if (cy + 1) % (window_height - 4) == 0: #TODO poch 4?
                cy -= offset#1
        
        
        
        #lines = self.base_controller.models['text'].lines[top_scroll:]
        lines = self.base_controller.models['text'].lines
        rendered_lines = rendered_lines[top_scroll:]
        pos_x = self.base_controller.models['cursor'].posx
        pos_y = self.base_controller.models['cursor'].posy #- top_scroll
        
        if pos_y + 1 < len(lines):
            offset = pos_x // window_width
            pos_y += 1
            #cy = sum((len(line) + window_width - 1) // window_width for line in lines[:pos_y]) + offset
            l = len(lines[pos_y-1])
            l2 = len(lines[pos_y])
            if pos_x > l2:
                k = (l + window_width - 1) // window_width
                offset = (k - (pos_x // window_width + 1)) + 1
                offset += l2 // window_width
            else:
                offset_ = (l + window_width - 1) // window_width
                offset = offset_
            cy += offset
            pos_y -= 1
            if len(lines[pos_y + 1]) < pos_x:
                if len(lines[pos_y+1]) and lines[pos_y+1][-1] == '\n':
                    l = len(lines[pos_y+1]) - 1
                    pos_x = len(lines[pos_y + 1]) - 1
                else:
                    l = len(lines[pos_y+1])
                    pos_x = len(lines[pos_y + 1])
                cx = (l % window_width)
                
            else:
                cx = pos_x % window_width
                if pos_x == len(lines[pos_y+1]) and len(lines[pos_y+1]) > 0 and lines[pos_y+1][-1] == '\n':
                    pos_x -= 1
                    cx -= 1
            pos_y += 1
            return {
                'model': ['text', 'cursor'], 
                'update': {
                    'update_cursor': {'dir': 'd', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'scroll_down': 1, 'scroll_top': top_scroll, 'text': ' '}
                }
            }
        
        
        

    
    def move_cursor_left(self):
        _, window_width, window_height = self.base_controller.models['text'].get_rendered_lines()
        cx = self.base_controller.models['cursor'].cursor_x
        cy = self.base_controller.models['cursor'].cursor_y
        
        
        
        top_scroll = self.base_controller.models['text'].scroll_top
        pos_x = self.base_controller.models['cursor'].posx
        pos_y = self.base_controller.models['cursor'].posy
        if pos_x - 1 >= 0:
            cx -= 1
            pos_x -= 1
            if cx == -1:
                cx = window_width - 1
                cy -= 1
                if cy <= 4 and top_scroll > 0:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                    cy += 1
                    top_scroll -= 1
            return {
                'model': ['text', 'cursor'], 
                'update': {
                    'update_cursor': {'dir': 'l', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'scroll_down': 1, 'scroll_top': top_scroll, 'text': ' '}
                }
            }

    def move_cursor_right(self):
        len_posy = len(self.base_controller.models['text'].lines[self.base_controller.models['cursor'].posy]) - 1 if self.base_controller.models['cursor'].posy < len(self.base_controller.models['text'].lines) - 1 else len(self.base_controller.models['text'].lines[self.base_controller.models['cursor'].posy])
        _, window_width, window_height = self.base_controller.models['text'].get_rendered_lines()
        cx = self.base_controller.models['cursor'].cursor_x
        cy = self.base_controller.models['cursor'].cursor_y
        
        pos_x = self.base_controller.models['cursor'].posx
        pos_y = self.base_controller.models['cursor'].posy
        if pos_x + 1 <= len_posy:
            cx += 1
            pos_x += 1
            if cx == window_width:
                cx = 0
                cy += 1
                if (cy + 1) % (window_height - 3) == 0: #TODO poch 3?
                    cy -= 1
                    self.base_controller.models['text'].scroll_top += 1
            return {
                'model': ['text', 'cursor'], 
                'update': {
                    'update_cursor': {'dir': 'r', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y},
                    'update_text': {'scroll_down': 1, 'scroll_top': self.base_controller.models['text'].scroll_top, 'text': ' '}
                }
            }