#from ...mymvc.Commands.ICommand import ICommand
from mymvc.Commands.ICommand import ICommand
#from ...mymvc.BaseController.BaseController import BaseController
from mymvc.BaseController.BaseController import BaseController

class NavigationCommand(ICommand):
    def __init__(self, base_controller: BaseController, mode: str):
        self.base_controller = base_controller
        self.mode = mode

    def execute(self, key: int) -> str:
        if key == 1:
            return self.move_cursor_up()
        elif key == 2:
            return self.move_cursor_down()
        elif key == 3:
            return self.move_cursor_left()
        elif key == 4:
            return self.move_cursor_right()
        elif key == 48:
            return self.scroll_up()
        elif key == 36:
            return self.at_end()
        elif key == 105:
            self.base_controller.switch_controller(self.mode)
            return {'model': ['cursor'], 
                    'update': {
                        'update_cursor': {'switch': 1, 'mode': self.mode}
                        }
                    }
        else:
            return {'model': None, 'update': None}
    
    def at_end(self):
        rendered_lines, window_width, height = self.base_controller.models['text'].get_rendered_lines()
        top_scroll = self.base_controller.models['text'].scroll_top
        lines = self.base_controller.models['text'].lines
        cy = self.base_controller.models['cursor'].cursor_y
        cx = self.base_controller.models['cursor'].cursor_x
        pos_y = self.base_controller.models['cursor'].posy
        pos_x = len(self.base_controller.models['text'].lines[pos_y]) - 1 if self.base_controller.models['text'].lines[pos_y][-1]=='\n' else len(self.base_controller.models['text'].lines[pos_y])
        rendered_lines = rendered_lines[top_scroll:top_scroll + height - 1]
        if self.base_controller.models['cursor'].posx < len(lines[pos_y]):
            if pos_x > window_width:
                cx = pos_x % window_width
                #k = len(rendered_lines) - 1
                #cy = k
                visual_line_count = (pos_x + window_width - 1) // window_width
                cy = sum((len(lines[i]) + window_width - 1) // window_width for i in range(pos_y))
                if visual_line_count > 1:
                    cy += visual_line_count - 1
                if cy >= (height - 4):
                    l = len(self.base_controller.models['text'].lines[pos_y])
                    if l > window_width:
                        k = (l + window_width - 1) // window_width
                        off = (self.base_controller.models['cursor'].posx // window_width + 1)
                        top_scroll += k - (k - off)
                    #top_scroll += cy - visual_line_count
                    cy = height - 4 - 1 
                
            else:
                cx = pos_x
            return {
                    'model': ['text','cursor'], 
                    'update': {
                        'update_cursor': {'dir': 'r', 'cx': cx, 'cy': cy, 'pos_x': pos_x, 'pos_y': pos_y},
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
                if cy <= 4:#(cy + 1) % (window_height - 3) == 0: #TODO poch 3?
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