import pygame as pg
import tkinter as tk
import ptlib as ptl


class _TkObjectPlaceholder:

    def __getattr__(self, attr):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __getitem__(self, key):
        return 0

    def __setitem__(self, key, value):
        pass


def tk_rect_coords_to_pg(x1, y1, x2, y2):
    return [x1, y1, x2 - x1, y2 - y1]


def anchored_surface_rect_coords(x, y, width, height, anchor='nw'):
    rect_coords = [0, 0, width, height]
    if 'w' in anchor:
        rect_coords[0] = x
    elif 'e' in anchor:
        rect_coords[0] = x - width
    else:
        rect_coords[0] = x - width // 2
    if 'n' in anchor:
        rect_coords[1] = y
    elif 's' in anchor:
        rect_coords[1] = y - height
    else:
        rect_coords[1] = y - height // 2
    return rect_coords


def pg_font_size(size):
    return round(size * 4 / 3)


class Canvas(_TkObjectPlaceholder):

    def __init__(self, master=None, cnf={}, **kw):
        self._items = {}
        self._next_item_id = 1
        self._surface = None
        self._background_color = (0, 0, 0, 0)
        self.configure(**kw)

    def _new_item_id(self):
        self._next_item_id += 1

    def _add_item(self, value):
        id_ = self._next_item_id
        self._new_item_id()
        self._items[id_] = value
        return id_

    def _remove_item(self, id_):
        self._items.pop(id_)

    def get_surface(self):
        return self._surface

    def _get_draw_rect(self, id_):
        item = self._items[id_]
        if item['type'] in {'arc', 'oval', 'rectangle'}:
            draw_rect = tk_rect_coords_to_pg(*item['args'])
            draw_outline_rect = [draw_rect[0], draw_rect[1], draw_rect[2] + 1, draw_rect[3] + 1]
        elif item['type'] == 'bitmap':
            draw_rect = [0, 0, 0, 0]
            draw_outline_rect = [0, 0, 0, 0]
        elif item['type'] == 'image':
            x, y = item['args']
            width = item['kwargs']['image'].width()
            height = item['kwargs']['image'].height()
            draw_rect = anchored_surface_rect_coords(x, y, width, height, item['kwargs']['anchor'])
            draw_outline_rect = [0, 0, 0, 0]
        elif item['type'] == 'line':
            draw_rect = [0, 0, 0, 0]
            draw_outline_rect = [0, 0, 0, 0]
        elif item['type'] == 'polygon':
            draw_rect = [0, 0, 0, 0]
            draw_outline_rect = [0, 0, 0, 0]
        elif item['type'] == 'text':
            draw_rect = [0, 0, 0, 0]
            draw_outline_rect = [0, 0, 0, 0]
        elif item['type'] == 'window':
            draw_rect = [0, 0, 0, 0]
            draw_outline_rect = [0, 0, 0, 0]
        else:
            draw_rect = [0, 0, 0, 0]
            draw_outline_rect = [0, 0, 0, 0]
        return draw_rect, draw_outline_rect

    def draw(self):
        self._surface.fill(self._background_color)
        for id_ in self._items:
            item = self._items[id_]
            
            draw_rect, draw_outline_rect = self._get_draw_rect(id_)
            surface = pg.Surface(draw_rect[2:4], pg.SRCALPHA)
            outline_surface = pg.Surface(draw_outline_rect[2:4], pg.SRCALPHA)
            
            color = ptl.tkinter_color_to_rgb(item['kwargs'].get('fill', ''))
            outline_color = ptl.tkinter_color_to_rgb(item['kwargs'].get('outline', '#000000'))
            
            if item['type'] == 'arc':
                pass
            elif item['type'] == 'bitmap':
                pass
            elif item['type'] == 'image':
                surface.blit(item['kwargs']['image'].get_surface(), (0, 0))
            elif item['type'] == 'line':
                pass
            elif item['type'] == 'oval':
                pg.draw.ellipse(surface, color, pg.Rect([0, 0] + draw_rect[2:4]))
                pg.draw.ellipse(outline_surface, outline_color, pg.Rect([0, 0] + draw_outline_rect[2:4]), 1)
            elif item['type'] == 'polygon':
                pass
            elif item['type'] == 'rectangle':
                pg.draw.rect(surface, color, pg.Rect([0, 0] + draw_rect[2:4]))
                pg.draw.rect(outline_surface, outline_color, pg.Rect([0, 0] + draw_outline_rect[2:4]), 1)
            elif item['type'] == 'text':
                font_name, font_size = item['kwargs']['font'].split()
                font_size = int(font_size)
                font_size = pg_font_size(font_size)
                font = pg.font.SysFont(font_name, font_size)
                text_surface = font.render(item['kwargs']['text'], True, color)
                x, y = item['args']
                width = text_surface.get_width()
                height = text_surface.get_height()
                anchor = item['kwargs'].get('anchor', 'c')
                draw_rect = anchored_surface_rect_coords(x, y, width, height, anchor)
                surface = pg.Surface(draw_rect[2:4], pg.SRCALPHA)
                surface.blit(text_surface, (0, 0))
            elif item['type'] == 'window':
                pass

            self._surface.blit(surface, draw_rect[0:2])
            self._surface.blit(outline_surface, draw_outline_rect[0:2])

    def configure(self, **kwargs):
        if 'width' in kwargs and 'height' in kwargs:
            self._surface = pg.Surface((kwargs['width'], kwargs['height']))
        if 'background' in kwargs:
            self._background_color = ptl.tkinter_color_to_rgb(kwargs['background'])
        elif 'bg' in kwargs:
            self._background_color = ptl.tkinter_color_to_rgb(kwargs['bg'])

    config = configure

    def cget(self, key):
        if key == 'width':
            return self._surface.get_width()
        elif key == 'height':
            return self._surface.get_height()

    __getitem__ = cget

    def coords(self, *args):
        id_ = args[0]
        if len(args) == 1:
            return self._items[id_]['args']
        else:
            self._items[id_]['args'] = args[1:]

    def _create(self, itemType, args, kw):
        data = {'type': itemType, 'args': args, 'kwargs': kw}
        return self._add_item(data)

    create_arc = tk.Canvas.create_arc
    create_bitmap = tk.Canvas.create_bitmap
    create_image = tk.Canvas.create_image
    create_line = tk.Canvas.create_line
    create_oval = tk.Canvas.create_oval
    create_polygon = tk.Canvas.create_polygon
    create_rectangle = tk.Canvas.create_rectangle
    create_text = tk.Canvas.create_text
    create_window = tk.Canvas.create_window

    def itemconfigure(self, tagOrId, cnf=None, **kw):
        if tagOrId == None:
            return
        self._items[tagOrId]['kwargs'].update(kw)

    itemconfig = itemconfigure

    def delete(self, *args):
        id_ = args[0]
        if id_ == None:
            return
        self._remove_item(id_)


class PhotoImage:

    def __init__(self, name=None, cnf={}, master=None, **kw):
        kwargs = kw
        if 'surface' in kwargs:
            self._surface = kwargs['surface']
        elif 'file' in kwargs:
            surface = pg.image.load(kwargs['file'])
            self._surface = surface.convert_alpha()
        elif 'width' in kwargs and 'height' in kwargs:
            self._surface = pg.Surface((kwargs['width'], kwargs['height']), pg.SRCALPHA)
        else:
            self._surface = pg.Surface((0, 0), pg.SRCALPHA)

        self._image_resized = False
        self._size = (self._surface.get_width(), self._surface.get_height())

    def get_surface(self):
        if self._image_resized:
            self._resize()
        return self._surface

    def height(self):
        return self._size[1]

    def width(self):
        return self._size[0]

    def copy(self):
        return PhotoImage(surface = self._surface)

    def _resize(self):
        resized_surface = pg.transform.scale(self._surface, self._size)
        self._surface = resized_surface
        self._image_resized = False

    def zoom(self, x, y=''):
        if y == '':
            y = x
        new_image = self.copy()
        new_image._image_resized = True
        new_image._size = (self.width() * x, self.height() * y)
        return new_image

    def subsample(self, x, y=''):
        if y == '':
            y = x
        new_image = self.copy()
        new_image._image_resized = True
        new_image._size = (self.width() // x, self.height() // y)
        return new_image

    def get(self, x, y):
        color = self._surface.get_at((x, y))
        return color[:3]

    def put(self, data, to):
        color = ptl.tkinter_color_to_rgb(data)
        self._surface.set_at(to, color)

    def transparency_get(self, x, y):
        return self._surface.get_at((x, y))[3] == 0

    def transparency_set(self, x, y, boolean):
        color = self._surface.get_at((x, y))
        color[3] = 255 * (not boolean)
        self._surface.set_at((x, y), color)
