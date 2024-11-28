version = '0.1.0.1'
py_tanks_version = '1.15.0.11'

import sys
import ptlib as ptl
import pytanks as pt
import ctypes
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame as pg
import configparser as cp
import pgptlib.tkinteronpg as tkonpg
import pgptlib.pilonpg.ImageTk as pilimgtkonpg


class TkAfterCatcher:

    def __init__(self, *args, **kwargs):
        self._after_calls = []

    def after(self, ms, func=None, *args):
        self._after_calls.append([ms, func, args])

    def get_after_calls(self):
        after_calls = self._after_calls
        self._after_calls = []
        return after_calls

    def __getattr__(self, attr):
        return tkonpg._TkObjectPlaceholder() 


def rotate_image(image, direction):
    surface = image.get_surface()
    new_surface = pg.transform.rotate(surface, -direction)
    new_image = tkonpg.PhotoImage(surface = new_surface)
    return new_image


class StrCompatKeycode(int):

    def __repr__(self):
        return 'StrCompatKeycode({})'.format(int(self))

    def lower(self):
        return self

    def upper(self):
        return self


class TkKeyEvent:

    def __init__(self, keycode):
        self.keysym = keycode
        self.keycode = 0


class PyTanksApplication:

    def __init__(self, config0, config1, localization):
        self.config0 = config0
        pt.config0 = config0
        self.config1 = config1
        pt.config1 = config1
        self.localization = localization
        self._after_calls = {}
        self.tick = 0
        self.fps = round(1 / eval(config1['FrameStabilization']['update_delay']))
        self.pressed_keys = set()
        
        pg.init()
        self.clock = pg.time.Clock()
        pg.display.init()
        #if os.name == 'nt':
        #    set_window_icon(pg.display.get_wm_info()['window'], self.config0['General']['icon'])
        icon = pg.image.load(self.config0['General']['icon_png'])
        pg.display.set_icon(icon)
        pg.display.set_caption(localization['title'])
        self.display_flags = pg.RESIZABLE #| pg.SCALED
        size = int(self.config1['General']['width']), int(self.config1['General']['height'])
        pg.display.set_mode(size, self.display_flags)

        pt.StrCompatKeycode = StrCompatKeycode
        for tankid in eval(self.config1['General']['tanklist']):
            pg_tankid = '{}.pygame'.format(tankid)
            if pg_tankid not in self.config1:
                continue
            controls = eval(self.config1[pg_tankid]['controls'])
            for i in range(len(controls)):
                for j in range(len(controls[i])):
                    controls[i][j] = StrCompatKeycode(controls[i][j])
            self.config1[tankid]['controls'] = controls.__repr__()
        
        pt.main()

        self.pt_canvas = pt.c
        self.after_catcher = pt.root

    def pause(self, set_=None):
        if set_ == None:
            set_ = not pt.pause
        pt.pause = set_

    def mainloop(self):
        while True:
            #time1 = pt.clock()
            events = pg.event.get()
            #time2 = pt.clock()
            #print('Time: {:.6f}; Events: {}'.format(time2 - time1, len(events)))
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                elif event.type == pg.KEYDOWN:
                    self.pressed_keys.add(event.key)
                    if event.key == pg.K_F11:
                        self.display_flags ^= pg.FULLSCREEN
                        pg.display.set_mode(flags = self.display_flags)
                        #pg.display.toggle_fullscreen()
                    elif event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit(0)
                    elif event.key == pg.K_F10:
                        self.pause()
                    else:
                        pt.KeyPressController(TkKeyEvent(event.key))
                elif event.type == pg.KEYUP:
                    self.pressed_keys.remove(event.key)
                    pt.KeyReleaseController(TkKeyEvent(event.key))

            if self.tick in self._after_calls:
                cur_after_calls = self._after_calls.pop(self.tick)
            else:
                cur_after_calls = []
            for after_call in cur_after_calls:
                after_call[0](*after_call[1])
            
            for after_call in self.after_catcher.get_after_calls():
                ms = after_call[0]
                tick_n = self.tick + self.fps * ms // 1000
                if tick_n not in self._after_calls:
                    self._after_calls[tick_n] = []
                self._after_calls[tick_n].append([after_call[1], after_call[2]])
            
            self.pt_canvas.draw()
            pg.display.get_surface().blit(self.pt_canvas.get_surface(), (0, 0))
            pg.display.flip()
            self.tick += 1
            self.clock.tick(self.fps)


def set_pt_placeholders():
    pt.Toplevel = tkonpg._TkObjectPlaceholder()
    pt.Frame = tkonpg._TkObjectPlaceholder()
    pt.Label = tkonpg._TkObjectPlaceholder()
    pt.Progressbar = tkonpg._TkObjectPlaceholder()
    pt.Button = tkonpg._TkObjectPlaceholder()
    pt.F10Menu = tkonpg._TkObjectPlaceholder()


def _update_config(config, section_name_format='{}.pygame'):
    ptl.update_config_for_app(config, section_name_format)


def init(**kwargs):
    _dkwargs = {'config_file': 'settings.cfg', 'config_files_encoding': 'utf-8'}
    _dkwargs.update(kwargs)
    kwargs = _dkwargs
    del _dkwargs
    
    config_files_encoding = kwargs['config_files_encoding']
    config0 = cp.ConfigParser()
    config1 = cp.ConfigParser()
    config0.read(kwargs['config_file'], encoding = config_files_encoding)
    config1.read(config0['General']['config'], encoding = config_files_encoding)

    _update_config(config0)
    _update_config(config1)

    localization = ptl.readLngFile(config1['General']['localization_file'], 'Py Tanks')

    set_pt_placeholders()

    pt.Canvas = tkonpg.Canvas
    pt.Tk = TkAfterCatcher
    pt.PhotoImage = tkonpg.PhotoImage

    pt.rotate_image = rotate_image

    if hasattr(pt, 'Image'):
        del pt.Image
    if hasattr(pt, 'ImageTk'):
        del pt.ImageTk

    if hasattr(pt, 'ptt'):
        pt.ptt.ImageTk = pilimgtkonpg

    return config0, config1, localization


def main(**kwargs):
    global pta
    pta = PyTanksApplication(*init(**kwargs))
    pta.mainloop()


if __name__ == '__main__':
    main()
