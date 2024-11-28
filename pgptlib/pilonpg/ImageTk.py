import pygame as pg
import pgptlib.tkinteronpg as tkonpg


class PhotoImage(tkonpg.PhotoImage):

    def __init__(self, image=None, size=None, **kw):
        surface = pg.Surface(image.size, pg.SRCALPHA)
        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                color = image.getpixel((x, y))
                surface.set_at((x, y), color)
        super().__init__(surface = surface, **kw)
