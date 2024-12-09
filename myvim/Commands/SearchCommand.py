#from ...mymvc.Commands.ICommand import ICommand
from mymvc.Commands.ICommand import ICommand
#from ...mymvc.BaseController.BaseController import BaseController
from mymvc.BaseController.BaseController import BaseController


class SearchCommand(ICommand):
    def __init__(self, base_controller: BaseController, mode: str):
        self.base_controller = base_controller
        self.mode = mode

    def execute(self, key, n, t=-1) -> str:
        if key == 27: #esc
            self.base_controller.switch_controller(self.mode)
            lines = self.base_controller.models['text'].lines
            top_scroll = self.base_controller.models['text'].scroll_top
            return {'model': ['text', 'cursor'], 
                    'update': {
                        'update_cursor': {'switch': 1, 'mode': self.mode},
                        'update_text': {'update_text': 1, 'text': lines, 'scroll_top': top_scroll}
                        }
                    }
        if key == 10 and t == 0: #enter
            self.base_controller.switch_controller(self.mode)
            pos_x = self.base_controller.models['cursor'].old_posx
            pos_y = self.base_controller.models['cursor'].old_posy
            px = self.base_controller.models['cursor'].old_cx
            py = self.base_controller.models['cursor'].old_cy
            _, window_width, _ = self.base_controller.models['text'].get_rendered_lines()
            top_scroll = self.base_controller.models['text'].scroll_top
            tmp = top_scroll
            lines = self.base_controller.models['text'].lines
            word = lines[pos_y][pos_x:pos_x + len(n.rstrip('\n'))]
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
                    else:
                        self.base_controller.models['text'].search_text = ""
                        pos_x = self.base_controller.models['cursor'].old_posx
                        pos_y = self.base_controller.models['cursor'].old_posy
                        px = self.base_controller.models['cursor'].old_cx
                        py = self.base_controller.models['cursor'].old_cy
                        return {
                            'model': ['text', 'cursor'],
                            'update': {
                                'update_text': {'update_text': 1, 'text': lines, 'scroll_top': tmp},
                                'update_cursor': {'switch': 1, 'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y, 'mode': self.mode},
                            }          
                        }
        elif t == 1:
            self.base_controller.switch_controller(self.mode)
            pos_x = self.base_controller.models['cursor'].old_posx
            pos_y = self.base_controller.models['cursor'].old_posy
            px = self.base_controller.models['cursor'].old_cx
            py = self.base_controller.models['cursor'].old_cy
            _, window_width, _ = self.base_controller.models['text'].get_rendered_lines()
            top_scroll = self.base_controller.models['text'].scroll_top
            tmp = top_scroll
            lines = self.base_controller.models['text'].lines
            word = lines[pos_y][pos_x:pos_x + len(n.rstrip('\n'))]
            if 1:
                flag = False
                if pos_y >= 0:
                    while pos_y >= 0 and not flag:
                        current_line = lines[pos_y]
                        k, m = len(current_line.rstrip('\n')), len(n.rstrip('\n'))
                        i = pos_x
                        while i >= 0: #<= k - m:  # Проверяем, чтобы оставшийся текст был не короче подстроки
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
                    else:
                        self.base_controller.models['text'].search_text = ""
                        pos_x = self.base_controller.models['cursor'].old_posx
                        pos_y = self.base_controller.models['cursor'].old_posy
                        px = self.base_controller.models['cursor'].old_cx
                        py = self.base_controller.models['cursor'].old_cy
                        return {
                            'model': ['text', 'cursor'],
                            'update': {
                                'update_text': {'update_text': 1, 'text': lines, 'scroll_top': tmp},
                                'update_cursor': {'switch': 1, 'dir': 'B', 'cx': px, 'cy': py, 'pos_x': pos_x, 'pos_y': pos_y, 'mode': self.mode},
                            }          
                        }