import sys
from ptlib import *
from configparser import ConfigParser, SectionProxy


enableCrachHandler = False

try:
    config0 = ConfigParser()
    config0.read('settings.cfg', encoding = 'utf-8')
    enableCrachHandler = bool(int(config0['General']['enablecrachhandler']))
    sys.path.append(config0['General']['libdir'])
except KeyboardInterrupt:
    raise KeyboardInterrupt

if __name__ == '__main__' and enableCrachHandler:
    try:
        import crashhandler
        if crashhandler.main('settings.pyw'):
            sys.exit(0)
    except KeyboardInterrupt:
        raise KeyboardInterrupt

PTver = PyTanksVersion
encoding = 'utf-8'
from tkinter import *
from tkinter import font
import tkinter
import sys
from sys import exit
import os
import ptlib as ptl
import tkinter as tk


if os.name == 'nt':
    _os_path_join = os.path.join
    def _join(path, *paths):
        return _os_path_join(path, *paths).replace('\\', '/')

def terminate(master, code = 0):
    master.destroy()
    sys.exit(code)

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

import tkinter.colorchooser as tkcc
import functools as ft


config0 = ConfigParser()
config0.read('settings.cfg', encoding = encoding)
config = SectionProxy(config0, 'General')
config1 = ConfigParser()
config1.read(config['config'], encoding = encoding)
fileName = config['settings']

if os.name == 'nt' and eval(config0['General']['replacepathjoinonwindows']):
    os.path.join = _join

def save_changes():
    global clientDataCheck, config, seg_size, map_name, background_color, wall_color, defLng, useunstdtex, defaultColorScheme, background_image, networkPlayCheck, IP1entry, IP2entry, portEntry, role, wallTexture, rspwnFtrDstr, damageFromWalls, rammingDamage, colorSchemes, additionlTanks, aiFromName
    settings = open(config0['General']['config'], 'w', encoding = encoding)
    config1['General']['theme'] = str(colorSchemes.index(defaultColorScheme.get()))
    width, height = (int(el) * int(seg_size.get()) for el in (fieldWidth.get(), fieldHeight.get()))
    FS = fsv.index(fs.get())
    Height = height
    config1['General']['width'] = str(width)
    config1['General']['height'] = str(Height)
    config1['General']['seg_size'] = seg_size.get()
    config1['General']['textures'] = str(int(useunstdtex.get()))
    config1['General']['background_image'] = background_image.get()
    config1['General']['background_color'] = background_color.get()
    config1['General']['wall_color'] = wall_color.get()
    map_file_name = map_name.get()
    config1['General']['map'] = map_file_name
    config1['General']['localization_file'] = langsDescr[defLng.get()]
    config1['General']['wall_texture'] = wallTexture.get()
    config1['General']['display_mode'] = str(FS)
    
    config1['ConfigurationVersion']['pytanksversion'] = PTver
    config1['General']['respawnafterdestruction'] = str(int(rspwnFtrDstr.get()))
    config1['General']['damagefromwalls'] = str(int(damageFromWalls.get()))
    config1['General']['rammingdamage'] = str(int(rammingDamage.get()))
    config1['General']['ttkthemename'] = ttkThemeName.get()
    #config1['General']['animations'] = str(animations.get())
    config1['General']['newhpbar'] = str(hp_bar_types.index(hp_bar_type.get()))
    
    config1['General']['tanklist'] = str(tanklist)
    for tank in additionlTanks:
        config1[tank]['hp'] = additionlTanks[tank]['HP'].get()
        config1[tank]['speed'] = str(additionlTanks[tank]['speed'].get())
        config1[tank]['color'] = additionlTanks[tank]['color'].get()
        config1[tank]['texture'] = additionlTanks[tank]['texture'].get()
        config1[tank]['bullettexture'] = additionlTanks[tank]['bulletTexture'].get()
        config1[tank]['ai'] = aiFromName[additionlTanks[tank]['ai'].get()]
        controls = [entry.get() for entry in additionlTanks[tank]['controls']]
        config1[tank]['controls'] = str(controls)
        config1[tank]['initpos'] = str(additionlTanks[tank]['posmenu'].get_tank_pos()).lstrip('[').rstrip(']')
        config1[tank]['hppos'] = str(additionlTanks[tank]['posmenu'].get_hp_pos()).lstrip('[').rstrip(']')
        config1[tank]['direction'] = additionlTanks[tank]['posmenu'].get_tank_direction()
        config1[tank]['team'] = additionlTanks[tank]['team'].get()
        if additionlTanks[tank]['reload_type'].get():
            config1[tank]['reload'] = additionlTanks[tank]['reload_time'].get()
        else:
            config1[tank]['reload'] = '-1'
    
    config1.write(settings)
    settings.close()

def fok():
    save_changes()
    global root, config
    root.destroy()
    #startfile(config['menu'])
    exit(0)

def fcancel():
    global root, config
    root.destroy()
    #startfile(config['menu'])
    exit(0)

def fapply():
    save_changes()
    root.destroy()
    ptl.run_python_file(config0['General']['settings'])
    exit(0)

root = Tk()
root.withdraw()


try:
    img = PhotoImage(master=root)
    img.configure(width = 1, height = 1)
    img.transparency_set(0, 0, False)
    img.transparency_get(0, 0)
    add_tkinter_formats = True
except:
    tkinter.PhotoImage.transparency_get = PhotoImage_transparency_get
    tkinter.PhotoImage.transparency_set = PhotoImage_transparency_set
    PhotoImage.transparency_get = PhotoImage_transparency_get
    PhotoImage.transparency_set = PhotoImage_transparency_set
    add_tkinter_formats = True


def drawDefaultTank(canvas, color):
    SEG_SIZE = int(seg_size.get())
    segments = []
    cht = int(config0['General']['canvashighlightthickness'])
    for x, y in ((0, 0), (SEG_SIZE, 0), (2 * SEG_SIZE, 0), (0, SEG_SIZE), (SEG_SIZE, SEG_SIZE), (2 * SEG_SIZE, SEG_SIZE), (3 * SEG_SIZE, SEG_SIZE), (0, 2 * SEG_SIZE), (SEG_SIZE, 2 * SEG_SIZE), (2 * SEG_SIZE, 2 * SEG_SIZE)):
        segments.append(canvas.create_rectangle(x + cht, y + cht, x + SEG_SIZE + cht, y + SEG_SIZE + cht, fill = color))
    return segments

def drawDefaultBullet(canvas, color):
    SEG_SIZE = int(seg_size.get())
    cht = int(config0['General']['canvashighlightthickness'])
    return canvas.create_oval(cht, cht, SEG_SIZE + cht, SEG_SIZE + cht, fill = color)

def eraseDefaultTank(canvas, segments):
    for i in range(len(segments)):
        canvas.delete(segments[i])

def eraseDefaultBullet(canvas, segment):
    canvas.delete(segment)

def drawDefaultWall(canvas, color):
    SEG_SIZE = int(seg_size.get())
    return canvas.create_rectangle(*([int(config0['General']['canvashighlightthickness'])] * 2), *([SEG_SIZE + int(config0['General']['canvashighlightthickness'])] * 2), fill = color)

eraseDefaultWall = eraseDefaultBullet

canvasUpdateNeeded = {}
segmentMap = [{}, {}]
bSegmentMap = [{}, {}]
wSegment = None

def dynamicElementsControl():
    global useunstdtex, background_color, background_color_canvas, wall_color, wall_color_canvas, wallTexture, canvasUpdateNeeded, wSegment, dec
    if not dec:
        root.after(16, dynamicElementsControl)
        return
    if useunstdtex.get() and not UnStdTexLock:
        wallTexture.configure(state = 'normal')
        if canvasUpdateNeeded.get('wall', False):
            wallTexture.updateCanvas()
            eraseDefaultWall(wallTexture.canvas, wSegment)
            canvasUpdateNeeded['wall'] = False
        for tankid in additionlTanks:
            additionlTanks[tankid]['texture'].configure(state = 'normal')
            additionlTanks[tankid]['bulletTexture'].configure(state = 'normal')
            if canvasUpdateNeeded.get(tankid, False):
                additionlTanks[tankid]['texture'].updateCanvas()
                additionlTanks[tankid]['bulletTexture'].updateCanvas()
                eraseDefaultTank(additionlTanks[tankid]['texture'].canvas, segmentMap[0][tankid])
                eraseDefaultBullet(additionlTanks[tankid]['bulletTexture'].canvas, bSegmentMap[0][tankid])
                canvasUpdateNeeded[tankid] = False
    else:
        wallTexture.configure(state = 'disabled')
        if not canvasUpdateNeeded.get('wall', False):
            wallTexture.canvas.delete(wallTexture.image)
            wSegment = drawDefaultWall(wallTexture.canvas, wall_color.get())
            canvasUpdateNeeded['wall'] = True
        for tankid in additionlTanks:
            additionlTanks[tankid]['texture'].configure(state = 'disabled')
            additionlTanks[tankid]['bulletTexture'].configure(state = 'disabled')
            if not canvasUpdateNeeded.get(tankid, False):
                additionlTanks[tankid]['texture'].canvas.delete(additionlTanks[tankid]['texture'].image)
                additionlTanks[tankid]['bulletTexture'].canvas.delete(additionlTanks[tankid]['bulletTexture'].image)
                segmentMap[0][tankid] = drawDefaultTank(additionlTanks[tankid]['texture'].canvas, additionlTanks[tankid]['color'].get())
                bSegmentMap[0][tankid] = drawDefaultBullet(additionlTanks[tankid]['bulletTexture'].canvas, additionlTanks[tankid]['color'].get())
                canvasUpdateNeeded[tankid] = True
    try:
        background_color_canvas.configure(bg=background_color.get())
    except:
        pass
    try:
        wall_color_canvas.configure(bg=wall_color.get())
    except:
        pass

    if defaultColorScheme.get() == lang['ttktheme']:
        ttkThemeMenu.grid(row = 0, column = 2)
    else:
        ttkThemeMenu.grid_forget()

    for tankid in additionlTanks:
        try:
            additionlTanks[tankid]['colorCanvas'].configure(bg=additionlTanks[tankid]['color'].get())
        except:
            pass
    
    root.after(16, dynamicElementsControl)


class native:
    class Texture:
        def __init__(self, unzipDirectory = None, textureConfig = None, textureConfigEncoding = None, textureStates = [], textureDirections = []):
            self.tkTexture = {}
        def open(self, file):
            self.file = file
        def color(self, color, resizeX = 1, resizeY = 1):
            pass
        def tkImage(self, master = None):
            self.tkTexture['Normal'] = {}
            self.tkTexture['Normal']['Right'] = PhotoImage(master = master, file = self.file)
            #tempSize = (self.tkTexture['Normal']['Right'].width(), self.tkTexture['Normal']['Right'].height())
            #tempImg = self.tkTexture['Normal']['Right'].zoom(int(seg_size.get()) + 1, int(seg_size.get()) + 1)
            #self.tkTexture['Normal']['Right'] = tempImg.subsample(tempSize[0], tempSize[1])
        def __getitem__(self, key):
            try:
                return self.tkTexture[key]
            except:
                return None


formats = {}

if add_tkinter_formats:
    formats.update({'pgm': native, 'ppm': native, 'gif': native, 'png': native})

try:
    import PIL
    import ptt
    formats['ptt'] = ptt
    formats['zip'] = ptt
except:
    try:
        import ptt_tk as ptt
        formats['ptt'] = ptt
        formats['zip'] = ptt
    except:
        pass

if formats:
    UnStdTexLock = False
else:
    UnStdTexLock = True


def merge_kw(kw, dkw):
    kw1 = {key: kw[key] for key in set(kw) - set(dkw)}
    kw2 = {key: kw[key] if key in kw else dkw[key] for key in set(kw) | set(dkw)}
    return kw1, kw2


class TextureMenu(Frame):
    
    def updateCanvas(self):
        if not self.texturePathList:
            return
        texturePath = self.texturePathList[self.texturePathListPosition]
        texlib = formats[os.path.splitext(texturePath)[1][1:]]
        texture = texlib.Texture(unzipDirectory = os.path.abspath(config['tempDir']), textureConfig = config['textureconfig'], textureConfigEncoding = config['textureconfigencoding'], textureStates = config['texturestates'].split(',')[:1], textureDirections = config['texturedirections'].split(','))
        if texture.open(texturePath):
            texture.textureDirections = config['walltexturedirections'].split(',')
        texture.open(texturePath)
        color = self.colorEntry.get()
        try:
            img = texture.images['Normal'].get('Right', texture.images['Normal'].get('Std', None))
            resize = (int(self.canvas['width']) / img[0].width, int(self.canvas['height']) / img[0].height)
        except:
            resize = ()
        texture.color(tkinter_color_to_rgb(color), *resize)
        texture.tkImage(self.master)
        self.canvas.delete(self.image)
        self.photo_image = texture['Normal'].get('Right', texture['Normal'].get('Std', None))
        if type(self.photo_image) == PhotoImage:
            if self.photo_image.width() * self.photo_image.height() * int(self.canvas['width']) * int(self.canvas['height']) > 100000000:
                self.photo_image = self.photo_image.subsample(self.photo_image.width() // int(self.canvas['width']), self.photo_image.height() // int(self.canvas['height']))
            else:
                tempSize = (self.photo_image.width(), self.photo_image.height())
                tempImg = self.photo_image.zoom(int(self.canvas['width']), int(self.canvas['height']))
                self.photo_image = tempImg.subsample(tempSize[0], tempSize[1])
        self.image = self.canvas.create_image(*([int(config0['General']['canvashighlightthickness'])] * 2), anchor = "nw", image = self.photo_image)

    def prev(self):
        if len(self.texturePathList) != 0:
            self.texturePathListPosition = (self.texturePathListPosition - 1) % len(self.texturePathList)
            self.updateCanvas()
    
    def next(self):
        if len(self.texturePathList) != 0:
            self.texturePathListPosition = (self.texturePathListPosition + 1) % len(self.texturePathList)
            self.updateCanvas()
    
    def __init__(self, master = None, canvasWidth = 0, canvasHeight = 0, canvasBackground = None, texturePathList = [], currentTexturePath = '', colorEntry = None, text = None):
        Frame.__init__(self, master)
        canvasFrame = Frame(self, relief = config0['General']['canvasrelief'])
        canvas = Canvas(canvasFrame, width = canvasWidth, height = canvasHeight, background = canvasBackground, highlightthickness = int(config0['General']['canvashighlightthickness']))
        self.canvas = canvas
        self.leftButton = Button(self, text = '<', width = 2, command = self.prev)
        self.rightButton = Button(self, text = '>', width = 2, command = self.next)
        if text != None:
            Label(self, text = text).grid(row = 0, column = 0, columnspan = 3)
        self.leftButton.grid(row = 1, column = 0)
        canvasFrame.grid(row = 1, column = 1)
        canvas.grid(padx = 2, pady = 2)
        self.rightButton.grid(row = 1, column = 2)

        self.canvas = canvas
        self.texturePathList = texturePathList
        if currentTexturePath in texturePathList:
            self.texturePathListPosition = texturePathList.index(currentTexturePath)
        else:
            self.texturePathListPosition = 0
        self.colorEntry = colorEntry
        self.image = None

        self.updateCanvas()
    
    def get(self):
        try:
            return self.texturePathList[self.texturePathListPosition]
        except:
            return ''

    def configure(self, cnf=None, **kw):
        self.leftButton.configure(cnf = cnf, **kw)
        self.rightButton.configure(cnf = cnf, **kw)


def detectTextures(directory, formats):
    texturePathList = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1][1:] in formats:
                texturePathList.append(os.path.join(root, file))
    return texturePathList


def create_segment(canvas, x, y, seg_size, highlightthickness, fill):
    ol = {}
    if seg_size < 3:
        ol['outline'] = ''
    return canvas.create_rectangle(x * seg_size + highlightthickness, y * seg_size + highlightthickness, (x + 1) * seg_size + highlightthickness, (y + 1) * seg_size + highlightthickness, fill = fill, **ol)


class MapMenu(Frame):

    def _update(self):
        while self.canvasWallSet:
            self.canvas.delete(self.canvasWallSet.pop())
        walls = readPtmFile(self.mapPathList[self.mapPathListPosition], fastread = True)
        ol = {}
        if self.segSize < 3:
            ol['outline'] = ''
        for i in range(min(len(walls), self.fheight)):
            for j in range(min(len(walls[i]), self.fwidth)):
                if walls[i][j]:
                    self.canvasWallSet.add(create_segment(self.canvas, j, i, self.segSize, self.highlightthickness, self.colorEntry.get()))

    def prev(self):
        self.mapPathListPosition = (self.mapPathListPosition - 1) % len(self.mapPathList)
        self._update()

    def next(self):
        self.mapPathListPosition = (self.mapPathListPosition + 1) % len(self.mapPathList)
        self._update()
    
    def __init__(self, master=None, **kw):
        dkw = {'canvasWidth': 0, 'canvasHeight': 0, 'canvasBackground': None, 'mapPathList': [], 'currentMapPath': '', 'colorEntry': None, 'text': None, 'segSize': 0}
        fkw, kw = merge_kw(kw, dkw)
        Frame.__init__(self, master, **fkw)
        canvasFrame = Frame(self, relief = config0['General']['canvasrelief'])
        self.canvas = Canvas(canvasFrame, width = kw['canvasWidth'], height = kw['canvasHeight'], background = kw['canvasBackground'], highlightthickness = int(config0['General']['canvashighlightthickness']))
        self.highlightthickness = int(config0['General']['canvashighlightthickness'])
        self.leftButton = Button(self, text = '<', width = 2, command = self.prev)
        self.rightButton = Button(self, text = '>', width = 2, command = self.next)
        canvasFrame.grid(row = 1, column = 1)
        self.canvas.grid(padx = 2, pady = 2)
        self.leftButton.grid(row = 1, column = 0)
        self.rightButton.grid(row = 1, column = 2)
        if 'text' in kw:
            Label(self, text = kw['text']).grid(row = 0, column = 0, columnspan = 3)
        self.mapPathList = kw['mapPathList']
        self.segSize = kw['segSize']
        self.fwidth = kw['canvasWidth'] // self.segSize
        self.fheight = kw['canvasHeight'] // self.segSize
        if kw['currentMapPath'] in self.mapPathList:
            self.mapPathListPosition = self.mapPathList.index(kw['currentMapPath'])
        else:
            self.mapPathListPosition = 0
        self.colorEntry = kw['colorEntry']
        self.canvasWallSet = set()
        self._update()

    def get(self):
        return self.mapPathList[self.mapPathListPosition]

    def configure(self, **kwargs):
        if 'state' in kwargs:
            self.leftButton.config(state = kwargs['state'])
            self.rightButton.config(state = kwargs['state'])

    config = configure


class ColorMenu(Frame):

    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self.color_var = StringVar()
        self.entry = Entry(self, width = 8, textvariable = self.color_var)
        self.color_image = PhotoImage(master = master, width = config0['General']['colorCanvasWidth'], height = config0['General']['colorCanvasHeight'])
        self.button = Button(self, image = self.color_image, command = self.call_askcolor)
        self.color_var.trace_add('write', self.color_changed_callback)
        self.entry.grid(row = 0, column = 0)
        self.button.grid(row = 0, column = 1, padx = (1, 0))

    def color_changed_callback(self, var, index, mode):
        color = self.color_var.get()
        try:
            for x in range(self.color_image.width()):
                for y in range(self.color_image.height()):
                    self.color_image.put(color, to = (x, y))
        except:
            pass

    def _color_changed_callback(self):
        self.color_changed_callback(self.color_var.__str__(), '', 'write')
    
    def call_askcolor(self):
        color = tkcc.askcolor(self.color_var.get())[1]
        if color != None:
            self.color_var.set(color)

    def get(self):
        return self.entry.get()

    def set(self, color):
        self.color_var.set(color)
        self._color_changed_callback()


class ControlMenu(Frame):

    def __init__(self, master=None, **kw):
        dkw = {'KeySeparator': lambda master=None: Label(master, text = ', ')}
        wkw, kw = merge_kw(kw, dkw)
        Frame.__init__(self, master, **wkw)
        self.KeySeparator = kw['KeySeparator']
        self.key_list = set()
        self.key_list_frame = Frame(self)
        self.add_key_button = Button(self, width = 3, text = '+', command = self._ask_key)
        self.key_list_frame.pack(side = LEFT)
        self.add_key_button.pack(side = LEFT)
        self.widget_set = {self.add_key_button}

    def add_key(self, key):
        if key in self.key_list:
            return
        self.key_list.add(key)
        key_pos = len(self.key_list) - 1
        key_remove_button = Button(self.key_list_frame, text = key)
        key_separator = self.KeySeparator(self.key_list_frame)
        key_remove_button.pack(side = LEFT)
        key_separator.pack(side = LEFT)
        key_remove_button.config(command = ft.partial(self._remove_key, key, key_remove_button, key_separator))
        self.widget_set.add(key_remove_button)
        self.widget_set.add(key_separator)

    def _ask_key(self):
        window = Toplevel(self)
        window.focus()
        window.minsize(200, 150)
        window.rowconfigure(index=0, weight=1)
        window.columnconfigure(0, weight = 1)
        frame = Frame(window)
        frame.grid(row = 0, column = 0, sticky = 'nwse')
        centered_frame = Frame(frame)
        centered_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        Label(centered_frame, text = lang['pressnewkey']).pack(side = TOP)
        Label(centered_frame).pack(side = TOP)
        cancel_button = Button(centered_frame, text = lang['cancelButton'], command = window.destroy)
        cancel_button.pack(side = TOP)
        window.bind('<KeyPress>', ft.partial(self._ask_key_add_key, window))
        window.mainloop()

    def _ask_key_add_key(self, window, event):
        window.destroy()
        if ord('A') <= event.keycode <= ord('Z'):
            keysym = chr(event.keycode)
        else:
            keysym = event.keysym
        self.add_key(keysym)

    def _remove_key(self, key, key_remove_button, key_separator):
        self.key_list.remove(key)
        key_remove_button.pack_forget()
        key_separator.pack_forget()
        self.widget_set.remove(key_remove_button)
        self.widget_set.remove(key_separator)

    def set(self, key_list):
        for key in key_list:
            self.add_key(key)

    def get(self):
        return list(self.key_list)

    def configure(self, cnf=None, **kw):
        if 'state' in kw:
            for widget in self.widget_set:
                widget.configure(state = kw['state'])
            kw.pop('state')
        Frame.configure(self, cnf, **kw)

    config = configure


class PlacingMenu(Frame):

    def __init__(self, master=None, **kw):
        dkw = {'canvas_width': 0, 'canvas_height': 0, 'canvas_background': None, 'map_menu': None, 'color_entry': None, 'text': ''}
        wkw, kw = merge_kw(kw, dkw)
        Frame.__init__(self, master, **wkw)
        self.map_menu = kw['map_menu']
        self.canvas_segment_set = set()
        self.color_entry = kw['color_entry']
        canvas_frame = Frame(self, relief = config0['General']['canvasrelief'])
        self.highlightthickness = int(config0['General']['canvashighlightthickness'])
        self.canvas = Canvas(canvas_frame, width = kw['canvas_width'], height = kw['canvas_height'], background = kw['canvas_background'], highlightthickness = self.highlightthickness)
        self.rotate_button = Button(self, text = kw['text'], command = self.rotate)
        canvas_frame.grid(row = 0, column = 0)
        self.canvas.grid(padx = 2, pady = 2)
        self.rotate_button.grid(row = 0, column = 1)
        self.canvas.bind('<Button-1>', self.set_tank_pos_cnv)
        self.canvas.bind('<Button-3>', self.set_hp_pos_cnv)
        self.init = [False] * 3
        self.update_()

    class _MapMenuWrapper:
        def __init__(self, placing_menu, map_menu, canvas):
            self.canvas = canvas
            self.canvasWallSet = placing_menu.canvas_segment_set
            self.mapPathList = map_menu.mapPathList
            self.mapPathListPosition = map_menu.mapPathListPosition
            self.segSize = map_menu.segSize
            self.fheight = map_menu.fheight
            self.fwidth = map_menu.fwidth
            self.highlightthickness = placing_menu.highlightthickness
            self.colorEntry = map_menu.colorEntry

    def draw_walls(self):
        self.map_menu.__class__._update(self._MapMenuWrapper(self, self.map_menu, self.canvas))

    def draw_tank(self):
        segment_rel_pos_list = []
        for i in range(3):
            for j in range(3):
                segment_rel_pos_list.append((i, j))
        if self.direction == 'right':
            segment_rel_pos_list.append((3, 1))
        elif self.direction == 'up':
            segment_rel_pos_list.append((1, -1))
        elif self.direction == 'down':
            segment_rel_pos_list.append((1, 3))
        else:
            segment_rel_pos_list.append((-1, 1))
        for x, y in segment_rel_pos_list:
            self.canvas_segment_set.add(create_segment(self.canvas, x + self.pos[0], y + self.pos[1], self.map_menu.segSize, self.highlightthickness, self.color_entry.get()))

    def draw_hp(self):
        self.canvas_segment_set.add(self.canvas.create_text(*[el * self.map_menu.segSize for el in self.hppos], text = lang['hpsampletext'], font = config0['General']['canvasfont'] + ' ' + str(self.map_menu.segSize), fill = self.color_entry.get()))
    
    def update_(self):
        self.draw_walls()
        if not all(self.init):
            return
        self.draw_tank()
        self.draw_hp()

    def set_tank_pos(self, pos):
        self.pos = list(pos).copy()
        self.init[0] = True

    def get_tank_pos(self):
        return self.pos.copy()

    def set_hp_pos(self, pos):
        self.hppos = list(pos).copy()
        self.init[1] = True

    def get_hp_pos(self):
        return self.hppos.copy()

    def set_tank_direction(self, direction):
        self.direction = direction
        self.init[2] = True

    def get_tank_direction(self):
        return self.direction

    def _pos(self, event):
        return (event.x // self.map_menu.segSize, event.y // self.map_menu.segSize)

    def set_tank_pos_cnv(self, event):
        self.set_tank_pos(self._pos(event))
        self.update_()

    def set_hp_pos_cnv(self, event):
        self.set_hp_pos(self._pos(event))
        self.update_()

    def rotate(self):
        self.direction = {'right': 'down', 'down': 'left', 'left': 'up', 'up': 'right'}[self.direction]
        self.update_()


lngFileName = config1['General']['localization_file']

lang = readLngFile(config['fallbacklng'], 'Settings')
lang.update(readLngFile(lngFileName, 'Settings'))

WIDTH = int(config0['General']['textwidgetswidth'])
colorCanvasWidth = int(config['colorCanvasWidth'])
colorCanvasHeight = int(config['colorCanvasHeight'])

def close():
    global config
    startfile(config['menu'])
    terminate(root)
root.protocol("WM_DELETE_WINDOW", close)

if os.name == 'nt':
    root.iconbitmap(config['icon'])
root.title(lang['title'])


colorScheme = int(config1['General']['theme'])
try:
    from ttkthemes import ThemedStyle
    ttkthemesimported = True
except ImportError:
    ttkthemesimported = False
if colorScheme % 2 == 1:
    from tkinter.ttk import *
    if ttkthemesimported:
        Style = ThemedStyle
    style = Style(root)
    if colorScheme == 3:
        style.theme_use(config1['General']['ttkthemename'])
        if style.theme_use() == 'vista':
            style.configure('D.TFrame', background = '#F0F0F0')
            style.configure('TFrame', background = '#FFFFFF')
            style.configure('TLabel', background = '#FFFFFF')
            style.configure('TEntry', background = '#FFFFFF')
            style.configure('TCheckbutton', background = '#FFFFFF')
            style.configure('TSpinbox', background = '#FFFFFF')
            style.configure('Main.TButton', background = style.lookup('TButton', 'background'))
            style.configure('TButton', background = '#FFFFFF')
            style.configure('TOptionMenu', background = '#FFFFFF')
else:
    from tkinter.ttk import Notebook, Style, Combobox
    if ttkthemesimported:
        Style = ThemedStyle
    style = Style(root)
    for themename in eval(config0['General']['ttkthemefortk']):
        if themename in style.theme_names():
            style.theme_use(themename)
            break
if colorScheme == 2:
    darkStyle = config0['darkColorScheme']
    background = darkStyle['background']
    foreground = darkStyle['foreground']
    entries = darkStyle['entries']
    disabledEntries = darkStyle['disabledEntries']
    disabledForeground = darkStyle['disabledForeground']
    insertbackground = '#' + ''.join([('0' + hex(255 - int(entries[i:i+2], 16))[2:])[-2:] for i in range(1, len(entries), 2)])
    root['background'] = background
    def Tk(screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        window = tkinter.Tk(screenName, baseName, className, useTk, sync, use)
        window['background'] = background
        return window
    lkw = {'background': background, 'foreground': foreground, 'disabledforeground': disabledForeground}
    def Label(master=None, cnf={}, **kw):
        for arg in lkw:
            if arg not in kw:
                kw[arg] = lkw[arg]
        return tkinter.Label(master, cnf, **kw)
    bkw = {'background': background, 'foreground': foreground, 'activebackground': background, 'activeforeground': foreground, 'disabledforeground': disabledForeground}
    def Button(master=None, cnf={}, **kw):
        for arg in bkw:
            if arg not in kw:
                kw[arg] = bkw[arg]
        return tkinter.Button(master, cnf, **kw)
    class Frame(tkinter.Frame):
        def __init__(self, master=None, cnf={}, **kw):
            if 'background' not in kw:
                kw['background'] = background
            tkinter.Frame.__init__(self, master, cnf, **kw)
    style.configure('TNotebook', background = background)
    style.configure('TNotebook.Tab', background = background, foreground = foreground)
    ekw = {'background': entries, 'foreground': foreground, 'insertbackground': insertbackground, 'disabledbackground': disabledEntries, 'disabledforeground': disabledForeground}
    def Entry(master=None, cnf={}, **kw):
        for arg in ekw:
            if arg not in kw:
                kw[arg] = ekw[arg]
        return tkinter.Entry(master, cnf, **kw)
    cbkw = {'background': background, 'foreground': foreground, 'selectcolor': entries, 'activebackground': background, 'activeforeground': foreground}
    def Checkbutton(master=None, cnf={}, **kw):
        for arg in cbkw:
            if arg not in kw:
                kw[arg] = cbkw[arg]
        return tkinter.Checkbutton(master, cnf, **kw)
    def OptionMenu(master, variable, value, *values, **kwargs):
        optnMenu = tkinter.OptionMenu(master, variable, value, *values, **kwargs)
        optnMenu.config(highlightbackground = background, background = background, foreground = foreground, activebackground = background, activeforeground = foreground, disabledforeground = disabledForeground)
        optnMenu['menu'].config(background = background, foreground = foreground)
        return optnMenu
    sbkw = {'background': entries, 'buttonbackground': background, 'foreground': foreground, 'insertbackground': insertbackground, 'disabledbackground': disabledEntries, 'disabledforeground': disabledForeground}
    def Spinbox(master=None, cnf={}, **kw):
        for arg in sbkw:
            if arg not in kw:
                kw[arg] = sbkw[arg]
        return tkinter.Spinbox(master, cnf, **kw)
    def Canvas(master=None, cnf={}, **kw):
        if 'highlightbackground' not in kw:
            kw['highlightbackground'] = background
        return tkinter.Canvas(master, cnf, **kw)
    style.configure('TCombobox', background = background, fieldbackground = entries, foreground = foreground)


tabs = {}

_lan_game_client_settings_enabled = False

def enable_lan_game_client_settings():
    global _lan_game_client_settings_enabled
    if _lan_game_client_settings_enabled:
        return
    _lan_game_client_settings_enabled = True
    
    for tankid in tabs:
        ntbk.forget(tabs[tankid])
    local_tankn = lang['tankn']
    lang['tankn'] = lang['tank_lan']
    tab, widgets = makeTankTab(config0['LANGame']['tankid'])
    lang['tankn'] = local_tankn

    widgets['ai_label'].grid_forget()
    widgets['ai_menu'].grid_forget()
    widgets['remove_tank_button'].grid_forget()

    ntbk.tab(1, state = 'disabled')

    fieldWidthSB.configure(state = 'disabled')
    fieldHeightSB.configure(state = 'disabled')
    rspwnFtrDstrCheck.configure(state = 'disabled')
    damageFromWallsCheck.configure(state = 'disabled')
    addTankButton.configure(state = 'disabled')
    

def disable_lan_game_client_settings():
    global tabs, additionlTanks, _lan_game_client_settings_enabled
    if not _lan_game_client_settings_enabled:
        return
    _lan_game_client_settings_enabled = False
    
    tab = tabs.pop(config0['LANGame']['tankid'])
    ntbk.forget(tab)
    tabs_copy = tabs.copy()
    tabs = {}
    additionlTanks = {}
    for tankid in tabs_copy:
        makeTankTab(tankid)

    ntbk.tab(1, state = 'normal')

    fieldWidthSB.configure(state = 'normal')
    fieldHeightSB.configure(state = 'normal')
    rspwnFtrDstrCheck.configure(state = 'normal')
    damageFromWallsCheck.configure(state = 'normal')
    addTankButton.configure(state = 'normal')


class LANGameSettingsFrame(Frame):

    def _lan_game_switched(self):
        lan_game_enabled = bool(self._lan_game_enabled_var.get())
        config1['NetworkPlay']['enabled'] = str(lan_game_enabled)
        if lan_game_enabled:
            self._optionmenu_role.config(state = 'normal')
            self._role_callback()
            self._entry_port.config(state = 'normal')
        else:
            disable_lan_game_client_settings()
            self._optionmenu_role.config(state = 'disabled')
            self._entry_self_address.config(state = 'disabled')
            self._entry_server_address.config(state = 'disabled')
            self._entry_port.config(state = 'disabled')
        self._lan_game_enabled_last_value = lan_game_enabled

    def _role_callback(self, variable_name=None, index=None, mode=None):
        role = self._text_to_role[self._variable_role.get()]
        config1['NetworkPlay']['is_server'] = str(bool(role))
        if role:
            disable_lan_game_client_settings()
            self._entry_self_address.config(state = 'normal')
            self._entry_server_address.config(state = 'disabled')
        else:
            enable_lan_game_client_settings()
            self._entry_self_address.config(state = 'disabled')
            self._entry_server_address.config(state = 'normal')

    def _self_address_callback(self, variable_name, index, mode):
        config1['NetworkPlay']['self_ip'] = self._variable_self_address.get()

    def _server_address_callback(self, variable_name, index, mode):
        config1['NetworkPlay']['server_ip'] = self._variable_server_address.get()

    def _port_callback(self, variable_name, index, mode):
        config1['NetworkPlay']['port'] = self._variable_port.get()

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        current_row = 0
        gridpady = int(config0['General']['gridpady'])
        self._lan_game_enabled_last_value = False
        
        self._label_enabled = Label(master = self, text = lang['networkPlayText'])
        self._label_enabled.grid(row = current_row, column = 0, pady = gridpady)
        self._lan_game_enabled_var = tk.IntVar(self)
        self._lan_game_enabled_var.set(eval(config1['NetworkPlay']['enabled']))
        self._checkbox_enabled = Checkbutton(master = self, variable = self._lan_game_enabled_var, command = self._lan_game_switched)
        self._checkbox_enabled.grid(row = current_row, column = 1)
        current_row += 1

        self._label_role = Label(master = self, text = lang['compRole'])
        self._label_role.grid(row = current_row, column = 0, pady = gridpady)
        self._role_texts = (lang['client'], lang['server'])
        self._text_to_role = {self._role_texts[role]: role for role in range(len(self._role_texts))}
        self._variable_role = tk.StringVar(self, self._role_texts[eval(config1['NetworkPlay']['is_server'])])
        options = list(self._role_texts)
        if OptionMenu != tk.OptionMenu:
            options.insert(0, self._variable_role.get())
        self._optionmenu_role = OptionMenu(self, self._variable_role, *options)
        self._optionmenu_role.grid(row = current_row, column = 1)
        current_row += 1

        self._label_self_address = Label(master = self, text = lang['networkPlayIP1'])
        self._label_self_address.grid(row = current_row, column = 0, pady = gridpady)
        self._variable_self_address = tk.StringVar(self, config1['NetworkPlay']['self_ip'])
        self._variable_self_address.trace('w', self._self_address_callback)
        self._entry_self_address = Entry(self, width = 14, textvariable = self._variable_self_address)
        self._entry_self_address.grid(row = current_row, column = 1)
        current_row += 1

        self._label_server_address = Label(master = self, text = lang['networkPlayIP2'])
        self._label_server_address.grid(row = current_row, column = 0, pady = gridpady)
        self._variable_server_address = tk.StringVar(self, config1['NetworkPlay']['server_ip'])
        self._variable_server_address.trace('w', self._server_address_callback)
        self._entry_server_address = Entry(self, width = 14, textvariable = self._variable_server_address)
        self._entry_server_address.grid(row = current_row, column = 1)
        current_row += 1

        self._variable_role.trace('w', self._role_callback)

        self._label_port = Label(master = self, text = lang['port'])
        self._label_port.grid(row = current_row, column = 0, pady = gridpady)
        self._variable_port = tk.StringVar(self, config1['NetworkPlay']['port'])
        self._variable_port.trace('w', self._port_callback)
        self._entry_port = Entry(self, width = WIDTH, textvariable = self._variable_port)
        self._entry_port.grid(row = current_row, column = 1)
        current_row += 1


class AnimationEnabledCheckbox:

    def __init__(self, frame, row_n, name, animation_config, localization):
        self._name = name
        self._animation_config = animation_config
        self._current_animation_config = eval(animation_config[name])
        self._enabled_value = tk.IntVar(frame, self._current_animation_config['enabled'])
        self._label = Label(frame, text = localization['animation_{}'.format(name)])
        self._checkbox = Checkbutton(frame, variable = self._enabled_value, command = self._value_changed)
        self._label.grid(row = row_n, column = 0, padx = 3, pady = int(config0['General']['gridpady']))
        self._checkbox.grid(row = row_n, column = 1, padx = (0, 3))

    def _value_changed(self):
        value = self._enabled_value.get()
        self._current_animation_config['enabled'] = bool(value)
        self._animation_config[self._name] = self._current_animation_config.__repr__()


class AnimationsFrame(Frame):

    def __init__(self, master, animation_config, localization):
        super().__init__(master = master)
        self._animation_enabled_checkboxes = []
        for animation_name in animation_config:
            row_n = len(self._animation_enabled_checkboxes)
            animation_enabled_checkbox = AnimationEnabledCheckbox(self, row_n, animation_name, animation_config, localization)
            self._animation_enabled_checkboxes.append(animation_enabled_checkbox)


class AnimationsTab(Frame):

    def __init__(self, master, animation_config, localization):
        super().__init__(master = master)
        self._animations_frame = AnimationsFrame(self, animation_config, localization)
        self._animations_frame.grid(padx = 5, pady = 5)


rootFrame = Frame(root)
rootFrame.grid()
root.rowconfigure(index = 0, weight = 1)
root.columnconfigure(index = 0, weight = 1)

frame = Frame(rootFrame)
frame.pack()

if colorScheme == 3 and style.theme_use() == 'vista':
    rootFrame.config(style = 'D.TFrame')
    frame.config(style = 'D.TFrame')


ntbk = Notebook(frame)
ntbk.pack(fill='both', expand=True, padx = 7, pady = 7)
general = Frame(frame)
ntbk.add(general, text=lang['general'])
mapSettings = Frame(frame)
ntbk.add(mapSettings, text=lang['map'])
network = LANGameSettingsFrame(frame)
ntbk.add(network, text=lang['networkPlay'])

animations = AnimationsTab(frame, SectionProxy(config1, 'animations'), lang)
ntbk.add(animations, text = lang['animations_tab_title'])


rowg = 0

class inputWidgetPlaceholder:
    def set(self, **kw):
        pass
    def get(self):
        return None

class colorInputWidgetPlaceholder (inputWidgetPlaceholder):
    def get(self):
        return '#000000'

inputWidgets = {}

for section in config1:
    inputWidgets[section] = {}

gridpady = config0['General']['gridpady']

Label(general, text=lang['colorScheme']).grid(row = rowg, column = 0, pady = gridpady)
colorSchemes = [lang['classic'], lang['standard'], lang['dark'], lang['ttktheme']]
defaultColorScheme = StringVar(root)
if colorScheme == 1:
    defaultColorScheme.set(lang['standard'])
elif colorScheme == 2:
    defaultColorScheme.set(lang['dark'])
elif colorScheme == 3:
    defaultColorScheme.set(lang['ttktheme'])
else:
    defaultColorScheme.set(lang['classic'])
if colorScheme % 2 == 1: 
    OptionMenu(general, defaultColorScheme, *([defaultColorScheme.get()] + colorSchemes)).grid(row = rowg, column = 1, pady = gridpady)
else:
    OptionMenu(general, defaultColorScheme, *colorSchemes).grid(row = rowg, column = 1, pady = gridpady)
ttkThemeName = StringVar(root)
ttkThemeName.set(config1['General']['ttkthemename'])
ttkThemeMenu = OptionMenu(general, ttkThemeName, *([ttkThemeName.get()] + sorted(style.theme_names())))
rowg += 1

Label(general, text = lang['fieldsize']).grid(row = rowg, column = 0, pady = gridpady)
width = int(config1['General']['width'])
height = int(config1['General']['height'])
fieldWidth = StringVar(general)
fieldHeight = StringVar(general)
fszFrame = Frame(general)
fieldWidthSB = Spinbox(fszFrame, width = WIDTH // 2 - 2, from_ = 0, to = 1500, textvariable = fieldWidth)
fieldHeightSB = Spinbox(fszFrame, width = WIDTH // 2 - 2, from_ = 0, to = 1000, textvariable = fieldHeight)
fszFrame.grid(row = rowg, column = 1, pady = gridpady)
fieldWidthSB.grid(row = 0, column = 0)
Label(fszFrame, text = 'x').grid(row = 0, column = 1)
fieldHeightSB.grid(row = 0, column = 2)
rowg += 1

Label(general, text=lang['segSize']).grid(row = rowg, column = 0, pady = gridpady)
seg_size = StringVar(general)
segSizeSB = Spinbox(general, width = WIDTH - 2, from_ = 0, to = 1000, textvariable = seg_size)
seg_size.set(config1['General']['seg_size'])
segSizeSB.grid(row = rowg, column = 1, pady = gridpady)
rowg += 1

fieldSize = (width // int(seg_size.get()), height // int(seg_size.get()))
fieldWidth.set(str(fieldSize[0]))
fieldHeight.set(str(fieldSize[1]))
mappreviewsegsize = round(float(config0['General']['settingsmappreviewsegsizecoef']) * int(seg_size.get()))

Label(general, text=lang['useUnstdTex']).grid(row = rowg, column = 0, pady = gridpady)
useunstdtex = BooleanVar()
useunstdtex.set(bool(int(config1['General']['textures'])))
if UnStdTexLock:
    useunstdtex.set(False)
useunstdtexCheck = Checkbutton(general, var=useunstdtex)
useunstdtexCheck.grid(row = rowg, column = 1, pady = gridpady)
if UnStdTexLock:
    useunstdtexCheck.configure(state = 'disabled')
rowg += 1

mapSettingsFrame = Frame(mapSettings)
mapSettingsMenuFrame = Frame(mapSettings)
mapSettingsFrame.grid(row = 0, column = 0, sticky = 'nw', padx = 3, pady = 3)
mapSettingsMenuFrame.grid(row = 0, column = 1, sticky = 'nwse')
mapSettings.rowconfigure(index = 0, weight = 1)
mapSettings.columnconfigure(index = 1, weight = 1)
rowmsf = 0
rowmsmf = 0

backgroundImagePathList = detectTextures(config0['General']['mapTextures'], formats)
background_image = TextureMenu(mapSettingsMenuFrame, canvasWidth = int(fieldWidth.get()) * mappreviewsegsize, canvasHeight = int(fieldHeight.get()) * mappreviewsegsize, canvasBackground = '#000000', texturePathList = backgroundImagePathList, currentTexturePath = config1['General']['background_image'], colorEntry = colorInputWidgetPlaceholder(), text = lang['backgroundImage'])
background_image.pack(side = TOP, pady = gridpady)
rowmsmf += 1
Label(mapSettingsFrame, text=lang['backgrColor']).grid(row = rowmsf, column = 0, pady = gridpady)
background_color = ColorMenu(mapSettingsFrame)
background_color.set(config1['General']['background_color'])
background_color.grid(row = rowmsf, column = 1, pady = gridpady)
rowmsf += 1
background_image.canvas.config(background = background_color.get())
Label(mapSettingsFrame, text=lang['wallColor']).grid(row = rowmsf, column = 0, pady = gridpady)
wall_color = ColorMenu(mapSettingsFrame)
wall_color.set(config1['General']['wall_color'])
wall_color.grid(row = rowmsf, column = 1, pady = gridpady)
rowmsf += 1
mapPathList = detectTextures(config0['General']['mapfolder'], {'ptm': None})
map_name = MapMenu(mapSettingsMenuFrame, canvasWidth = int(fieldWidth.get()) * mappreviewsegsize, canvasHeight = int(fieldHeight.get()) * mappreviewsegsize, canvasBackground = background_color.get(), mapPathList = mapPathList, currentMapPath = config1['General']['map'], colorEntry = wall_color, segSize = mappreviewsegsize, text = lang['mapmenutext'])
map_name.pack(side = TOP, pady = gridpady)
rowmsmf += 1

Label(mapSettingsFrame, text = lang['walltexture']).grid(row = rowmsf, column = 0, pady = gridpady)
wallTexturePathList = detectTextures(config0['General']['wallTextures'], formats)
wallTexture = TextureMenu(mapSettingsFrame, canvasWidth = int(seg_size.get()) + 1, canvasHeight = int(seg_size.get()) + 1, canvasBackground = background_color.get(), texturePathList = wallTexturePathList, currentTexturePath = config1['General']['wall_texture'], colorEntry = wall_color)
wallTexture.grid(row = rowmsf, column = 1, pady = gridpady)
rowmsf += 1

Label(general, text=lang['imagetext']).grid(row = rowg, column = 0, pady = gridpady)
fs = StringVar(general)
fsInt = int(config1['General']['display_mode'])
fsv = [lang['inwindow'], lang['fullscreen']]
fs.set(fsv[fsInt])
if colorScheme % 2 == 1:
    fsMenu = OptionMenu(general, fs, *([fs.get()] + fsv))
else:
    fsMenu = OptionMenu(general, fs, *fsv)
fsMenu.grid(row = rowg, column = 1, pady = gridpady)
rowg += 1

Label(general, text=lang['language']).grid(row = rowg, column = 0, pady = gridpady)
lng = open(lngFileName, encoding = encoding)
cur = lng.readline()
while bool(cur) and '[description]' not in cur.rstrip('\n').strip(' '):
    cur = lng.readline()
lng.close()
defLng = StringVar(general)
defLng.set(cur.rstrip('\n').split('=')[1].strip('"'))
lngFiles = detectTextures(config0['General']['langfolder'], '.lng')
langsDescr = {}
langNames = []
for lngFileName in lngFiles:
    obi = lngFileName.find('[')
    cbi = lngFileName.find(']')
    if obi < cbi and obi != -1 and cbi != -1:
        enc = lngFileName[obi+1:cbi]
    else:
        enc = encoding
    lngFile = open(lngFileName, encoding = enc)
    for el in lngFile:
        l = el.split('=')
        if l[0] == '[description]':
            langNames.append(l[1].rstrip('\n').strip('"'))
            langsDescr[langNames[-1]] = lngFileName
            break
if colorScheme % 2 == 1:
    language = OptionMenu(general, defLng, defLng.get(), *langNames)
else:
    language = OptionMenu(general, defLng, *langNames)
language.grid(row = rowg, column = 1)
rowg += 1
Label(general, text=lang['respawnAfterDestruction']).grid(row = rowg, column = 0, pady = gridpady)
rspwnFtrDstr = BooleanVar()
rspwnFtrDstr.set(bool(int(config1['General']['respawnafterdestruction'])))
rspwnFtrDstrCheck = Checkbutton(general, var=rspwnFtrDstr)
rspwnFtrDstrCheck.grid(row = rowg, column = 1, pady = gridpady)
rowg += 1
Label(general, text=lang['damageFromWalls']).grid(row = rowg, column = 0, pady = gridpady)
damageFromWalls = BooleanVar()
damageFromWalls.set(bool(int(config1['General']['damagefromwalls'])))
damageFromWallsCheck = Checkbutton(general, var=damageFromWalls)
damageFromWallsCheck.grid(row = rowg, column = 1, pady = gridpady)
rowg += 1
Label(general, text=lang['rammingDamage'])#.grid(row = rowg, column = 0, pady = gridpady)
rammingDamage = BooleanVar()
rammingDamage.set(bool(int(config1['General']['rammingdamage'])))
rammingDamageCheck = Checkbutton(general, var=rammingDamage)
#rammingDamageCheck.grid(row = rowg, column = 1, pady = gridpady)
rowg += 1
ok = Button(frame, text=lang['okButton'], command = fok)
cancel = Button(frame, text=lang['cancelButton'], command = fcancel)
apply = Button(frame, text=lang['applyButton'], command = fapply)
if colorScheme == 3 and style.theme_use() == 'vista':
    for button in (ok, cancel, apply):
        button.configure(style = 'Main.TButton')
apply.pack(side=RIGHT, padx = (3, 7), pady = (0, 7))
cancel.pack(side=RIGHT, padx = 3, pady = (0, 7))
ok.pack(side=RIGHT, padx = (7, 3), pady = (0, 7))

Label(general, text = lang['hpbartype']).grid(row = rowg, column = 0, pady = gridpady)
hp_bar_types = [lang['hpbarstd'], lang['hpbarnew']]
hp_bar_type = StringVar()
hp_bar_type.set(hp_bar_types[eval(config1['General']['newhpbar'])])
if colorScheme % 2 == 1:
    hp_bar_type_menu = OptionMenu(general, hp_bar_type, hp_bar_type.get(), *hp_bar_types)
else:
    hp_bar_type_menu = OptionMenu(general, hp_bar_type, *hp_bar_types)
hp_bar_type_menu.grid(row = rowg, column = 1, pady = gridpady)
rowg += 1

tankTexturePathList = detectTextures(config0['General']['tankTextures'], formats)
bulletTexturePathList = detectTextures(config0['General']['bulletTextures'], formats)

additionlTanks = {}
tanklist = eval(config1['General']['tanklist'])
tankidfrmt = 'tank{}'

def addTank():
    global dec
    dec = False
    mn = 1
    for i in range(len(tanklist)):
        if tanklist[i][:len(tankidfrmt) - 2] == tankidfrmt[:-2] and tanklist[i][len(tankidfrmt) - 2:].isnumeric():
            n = int(tanklist[i][len(tankidfrmt) - 2:])
            if n <= mn:
                mn = max(mn, n + 1)
            else:
                tankid = tankidfrmt.format(mn)
                tanklist.insert(i, tankid)
                break
    else:
        tankid = tankidfrmt.format(mn)
        tanklist.append(tankid)
    if tankid not in inputWidgets:
        inputWidgets[tankid] = {}
    makeTankTab(tankid)
    dec = True

def removeTank(tankid):
    for i in range(len(tanklist) - 1, -1, -1):
        if tanklist[i] == tankid:
            tanklist.pop(i)
            break
    ntbk.forget(tabs[tankid])


ais = eval(config0['General']['ais'])
aiNames = [ais[ai] for ai in ais]
aiFromName = {}
for ai in ais:
    aiFromName[ais[ai]] = ai


def ai_changed_callback_template(aivar, widget_set, var, index, mode):
    if aiFromName[aivar.get()] == 'None':
        for widget in widget_set:
            widget.configure(state = 'normal')
    else:
        for widget in widget_set:
            widget.configure(state = 'disabled')


def reload_checkbutton_command(intvar, entry):
    if intvar.get():
        entry.configure(state = 'normal')
    else:
        entry.configure(state = 'disabled')


def makeTankTab(tankid):
    additionlTanks[tankid] = {}
    
    if tankid not in config1:
        config1.add_section(tankid)
        for key, value in config0.items('defaulttank'):
            config1.set(tankid, key, value)

    tank = SectionProxy(config1, tankid)
    rowt = 0
    tab = Frame(root)
    tabs[tankid] = tab
    
    text = lang['tankn'].format(number = len(additionlTanks))
    
    tab_n = ntbk.add(tab, text = text)

    frame1_ = Frame(tab)
    frame1 = Frame(frame1_)
    frame2 = Frame(tab)
    control_menu_frame = Frame(tab)
    frame1_.grid(row = 0, column = 0, padx = 3, pady = 3, sticky = 'nwse')
    control_menu_frame.grid(row = 0, column = 2)
    frame1.pack(side = TOP)
    frame2.grid(row = 0, column = 1, sticky = 'nwse')

    for i in range(1, 3):
        tab.columnconfigure(i, weight = 1)
        tab.rowconfigure(i, weight = 1)
    frame2.columnconfigure(0, weight = 1)
    
    Label(frame1, text=lang['tankArmorNS']).grid(row = rowt, column = 0, pady = gridpady)
    tankHpEntry = Entry(frame1, width = WIDTH)
    tankHpEntry.insert(0, tank['hp'])
    tankHpEntry.grid(row = rowt, column = 1, pady = gridpady)
    additionlTanks[tankid]['HP'] = tankHpEntry
    rowt += 1
    
    Label(frame1, text=lang['tankSpeedNS']).grid(row = rowt, column = 0, pady = gridpady)
    additionlTanks[tankid]['speed'] = IntVar()
    additionlTanks[tankid]['speed'].set(int(tank['speed']))
    tank_speed = Spinbox(frame1, from_=-2, to=2, width=WIDTH-2, textvariable=additionlTanks[tankid]['speed'])
    tank_speed.grid(row = rowt, column = 1, pady = gridpady)
    rowt += 1
    
    Label(frame1, text=lang['tankColorNS']).grid(row = rowt, column = 0, pady = gridpady)
    tank_color = ColorMenu(frame1)
    tank_color.set(tank['color'])
    tank_color.grid(row = rowt, column = 1, pady = gridpady)
    
    additionlTanks[tankid]['color'] = tank_color
    rowt += 1

    textureTankName = TextureMenu(frame2, canvasWidth = int(seg_size.get()) * 4 + 1, canvasHeight = int(seg_size.get()) * 3 + 1, canvasBackground = background_color.get(), texturePathList = tankTexturePathList, currentTexturePath = tank['texture'], colorEntry = tank_color, text = lang['tankTextureNS'])
    textureTankName.grid(row = 0, column = 0, pady = gridpady)
    additionlTanks[tankid]['texture'] = textureTankName
    
    textureBulletName = TextureMenu(frame2, canvasWidth = int(seg_size.get()) + 1, canvasHeight = int(seg_size.get()) + 1, canvasBackground = background_color.get(), texturePathList = bulletTexturePathList, currentTexturePath = tank['bulletTexture'], colorEntry = tank_color, text = lang['bulletTextureNS'])
    textureBulletName.grid(row = 1, column = 0, pady = gridpady)
    additionlTanks[tankid]['bulletTexture'] = textureBulletName

    inputWidgets[tankid][''] = None
    pass
    rowt += 1

    ai_label = Label(frame1, text = lang['ai']); ai_label.grid(row = rowt, column = 0, pady = gridpady)
    additionlTanks[tankid]['ai'] = StringVar()
    additionlTanks[tankid]['ai'].set(ais[tank['ai']])
    if colorScheme % 2 == 1:
        aiMemu = OptionMenu(frame1, additionlTanks[tankid]['ai'], additionlTanks[tankid]['ai'].get(), *aiNames)
    else:
        aiMemu = OptionMenu(frame1, additionlTanks[tankid]['ai'], *aiNames)
    aiMemu.grid(row = rowt, column = 1, pady = gridpady)
    rowt += 1

    title_lable = Label(control_menu_frame, text = lang['controls'])
    title_lable.grid(row = 0, column = 0, columnspan = 2)
    upcm = ControlMenu(control_menu_frame)
    downcm = ControlMenu(control_menu_frame)
    rightcm = ControlMenu(control_menu_frame)
    leftcm = ControlMenu(control_menu_frame)
    shootcm = ControlMenu(control_menu_frame)
    upcm.set(eval(tank['controls'])[0])
    downcm.set(eval(tank['controls'])[2])
    rightcm.set(eval(tank['controls'])[3])
    leftcm.set(eval(tank['controls'])[1])
    shootcm.set(eval(tank['controls'])[4])
    lbl1 = Label(control_menu_frame, text = lang['upcontrol']); lbl1.grid(row = 1, column = 0)
    lbl2 = Label(control_menu_frame, text = lang['downcontrol']); lbl2.grid(row = 2, column = 0)
    lbl3 = Label(control_menu_frame, text = lang['leftcontrol']); lbl3.grid(row = 3, column = 0)
    lbl4 = Label(control_menu_frame, text = lang['rightcontrol']); lbl4.grid(row = 4, column = 0)
    lbl5 = Label(control_menu_frame, text = lang['shootcontrol']); lbl5.grid(row = 5, column = 0)
    for i in range(5):
        (upcm, downcm, leftcm, rightcm, shootcm)[i].grid(row = i + 1, column = 1)
    
    additionlTanks[tankid]['controls'] = [upcm, leftcm, downcm, rightcm, shootcm]

    callback_fn = ft.partial(ai_changed_callback_template, additionlTanks[tankid]['ai'], {upcm, downcm, rightcm, leftcm, shootcm, title_lable, lbl1, lbl2, lbl3, lbl4, lbl5})
    additionlTanks[tankid]['ai'].trace_add('write', callback_fn)
    callback_fn(None, None, None)

    removeTankButton = Button(tab, text = lang['removetankbutton'], command = lambda: removeTank(tankid))
    removeTankButton.grid(row = 2, column = 0, sticky = 's')

    pm = PlacingMenu(tab, canvas_width = int(fieldWidth.get()) * mappreviewsegsize, canvas_height = int(fieldHeight.get()) * mappreviewsegsize, canvas_background = background_color.get(), map_menu = map_name, color_entry = tank_color, text = lang['rotatetank'])
    pm.grid(row = 1, column = 0, columnspan = 3, pady = gridpady)
    pm.set_tank_pos(eval(tank['initpos']))
    pm.set_hp_pos(eval(tank['hppos']))
    pm.set_tank_direction(tank['direction'])
    pm.update_()
    additionlTanks[tankid]['posmenu'] = pm

    Label(frame1, text = lang['team']).grid(row = rowt, column = 0, pady = gridpady)
    team_cb = Combobox(frame1, values = [str(el) for el in range(1, len(tanklist) + 1)], width = WIDTH - 2)
    team_cb.set(tank['team'])
    team_cb.grid(row = rowt, column = 1, pady = gridpady)
    additionlTanks[tankid]['team'] = team_cb
    rowt += 1

    Label(frame1, text = lang['reload']).grid(row = rowt, column = 0, pady = gridpady)
    reload_frame = Frame(frame1)
    reload_frame.grid(row = rowt, column = 1, pady = gridpady)
    reload_type = IntVar(frame1, value = eval(tank['reload']) != -1)
    reload_time = StringVar(frame1, value = str(max(eval(tank['reload']), 0)))
    reload_spinbox = Spinbox(reload_frame, from_ = 0, to = 3600, textvariable = reload_time, width = WIDTH - 5)
    reload_checkbutton = Checkbutton(reload_frame, var = reload_type)
    reload_checkbutton.configure(command = ft.partial(reload_checkbutton_command, reload_type, reload_spinbox))
    reload_checkbutton_command(reload_type, reload_spinbox)
    reload_checkbutton.pack(side = LEFT)
    reload_spinbox.pack(side = LEFT)
    additionlTanks[tankid]['reload_type'] = reload_type
    additionlTanks[tankid]['reload_time'] = reload_time
    rowt += 1

    widgets = {
        'main_frame': tab,
        'settings_lower_frame': frame1_,
        'settings_frame': frame1,
        'textures_frame': frame2,
        'control_menu_frame': control_menu_frame,
        # ...
        'ai_label': ai_label,
        'ai_menu': aiMemu,
        # ...
        'remove_tank_button': removeTankButton,
        # ...
        }

    return tab_n, widgets


for tankid in tanklist:
    makeTankTab(tankid)


addTankButton = Button(general, text = lang['addtankbutton'], command = addTank)
addTankButton.grid(row = rowg, column = 0, columnspan = 3, pady = gridpady)
rowg += 1


network._lan_game_switched()


dec = True
dynamicElementsControl()


pass


window = root
currentFont = font.nametofont('TkDefaultFont')

def adaptFonts():
    global frame_winfo_width, frame_winfo_height
    currentFont.configure(size = int(currentFont.actual('size') * min(window.winfo_width() / frame_winfo_width, window.winfo_height() / frame_winfo_height)))
    frame_winfo_width = window.winfo_width()
    frame_winfo_height = window.winfo_height()
    window.after(16, adaptFonts)


root.resizable(False, False)
window.update()
frame_winfo_width = window.winfo_width()
frame_winfo_height = window.winfo_height()
root.update()
#adaptFonts()
root.deiconify()
root.mainloop()
