PyTanksVersion = '1.15.0'

import sys
from ptlib import *
from configparser import ConfigParser, SectionProxy


enableCrachHandler = False
config0 = ConfigParser()

try:
    config0.read('settings.cfg', encoding = 'utf-8')
    enableCrachHandler = bool(int(config0['General']['enablecrachhandler']))
    sys.path.append(config0['General']['libdir'])
except KeyboardInterrupt:
    raise KeyboardInterrupt


if sys.stderr != None:
    stderr_write = sys.stderr.write
else:
    stderr_write = lambda s: 0


def error_write(s):
    tkmb.showerror('', s)
    return stderr_write(s)


if eval(config0.get('General', 'redirectstderr', fallback = 'True')):
    sys.stderr.write = error_write
    enableCrachHandler = False


if __name__ == '__main__' and enableCrachHandler:
    try:
        import crashhandler
        if crashhandler.main('pytanks.pyw'):
            sys.exit(0)
    except KeyboardInterrupt:
        raise KeyboardInterrupt

PTver = PyTanksVersion
encoding = 'utf-8'
COLOR = 'nocolor'

from tkinter import *
import sys
import os
import tkinter.messagebox as tkmb
import traceback
import socket as sckt
import threading as thrd
import time


if not hasattr(PhotoImage, 'transparency_get'):
    PhotoImage.transparency_get = PhotoImage_transparency_get
if not hasattr(PhotoImage, 'transparency_set'):
    PhotoImage.transparency_set = PhotoImage_transparency_set


formats = {'pgm': None, 'ppm': None, 'gif': None, 'png': None}
try:
    from PIL import Image, ImageTk
    import ptt
    formats['ptt'] = ptt
    formats['zip'] = ptt
except:
    pass

if os.name == 'nt':
    from os import startfile
else:
    def startfile(file):
        os.open(file, os.O_RDWR | os.O_CREAT)

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def MessageBox(code, title, text, style):
    icon = {0: tkmb.INFO, 16: tkmb.ERROR, 48: tkmb.WARNING, 64: tkmb.QUESTION}
    mbtype = [tkmb.OK, tkmb.OKCANCEL, tkmb.ABORTRETRYIGNORE, tkmb.YESNOCANCEL, tkmb.YESNO, tkmb.RETRYCANCEL, tkmb.ABORTRETRYIGNORE]
    reply = {tkmb.ABORT: 3, tkmb.RETRY: 4, tkmb.IGNORE: 5, tkmb.OK: 1, tkmb.CANCEL: 2, tkmb.YES: 6, tkmb.NO: 7}

    if style == 6:
        reply[tkmb.ABORT] = reply[tkmb.CANCEL]
        reply[tkmb.RETRY] = 10
        reply[tkmb.IGNORE] = 11
    
    return reply[tkmb._show(title, text, icon[code], mbtype[style])]

def terminate(master, code = 0):
    master.destroy()
    os._exit(code)

ver = [int(el) for el in sys.version.split()[0].split('.')[:2]]
if ver[0] * 100 + ver[1] < 307:
    from time import clock
else:
    from time import perf_counter
    clock = perf_counter


convertRGB = tkinter_color_to_rgb


def raiseFormatErrorAndExit():
    MessageBox(16, root.title(), lang['textureInvalidFormatErrorText'], 0)
    root.destroy()
    startfile(config['menu'])
    sys.exit(0)


def rgb_to_tk_color(color):
    tk_color = '#'
    for i in range(3):
        tk_color += ('0' + hex(color[i])[2:])[-2:]
    return tk_color


config0 = ConfigParser()
config0.read('settings.cfg', encoding = encoding)
config = SectionProxy(config0, 'General')
config1 = ConfigParser(allow_no_value = True, strict = False)
config1.read(config['config'], encoding = encoding)
config1.remove_section('RawData')

ns = 15
settings = open(config['config'], encoding = encoding)
for line in settings:
    if line.rstrip('\n').lower() == '[rawdata]':
        break
for i in range(ns):
    settings.readline()
lngFileName = settings.readline().rstrip('\n')
settings.close()


settings = open(config['config'], encoding = encoding)
for line in settings:
    if line.rstrip('\n').lower() == '[rawdata]':
        break
colorScheme = int(settings.readline())

if colorScheme % 2 == 1:
    from tkinter.ttk import *
    try:
        from ttkthemes import ThemedStyle as Style
    except ImportError:
        pass
elif colorScheme == 2:
    import tkinter
    darkStyle = config0['darkColorScheme']
    background = darkStyle['background']; _background = background
    foreground = darkStyle['foreground']
    def Tk(screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        window = tkinter.Tk(screenName, baseName, className, useTk, sync, use)
        window['background'] = _background
        return window
    def Toplevel(master=None, cnf={}, **kw):
        if 'background' not in kw:
            kw['background'] = _background
        return tkinter.Toplevel(master, cnf, **kw)
    lkw = {'background': background, 'foreground': foreground}
    def Label(master=None, cnf={}, **kw):
        for arg in lkw:
            if arg not in kw:
                kw[arg] = lkw[arg]
        return tkinter.Label(master, cnf, **kw)
    bkw = {'background': background, 'foreground': foreground, 'activebackground': background, 'activeforeground': foreground}
    def Button(master=None, cnf={}, **kw):
        for arg in bkw:
            if arg not in kw:
                kw[arg] = bkw[arg]
        return tkinter.Button(master, cnf, **kw)
    class Frame(tkinter.Frame):
        def __init__(self, master=None, cnf={}, **kw):
            if 'background' not in kw:
                kw['background'] = _background
            tkinter.Frame.__init__(self, master, cnf, **kw)

root = Tk()
root.withdraw()


def close():
    global config
    startfile(config['menu'])
    terminate(root)


if colorScheme == 3:
    style = Style(root)
    style.theme_use(config1['General']['ttkthemename'])

settings.readline()
WIDTH, HEIGHT = map(int, settings.readline().split())
SEG_SIZE = int(settings.readline())
WIDTH -= WIDTH % SEG_SIZE
HEIGHT -= HEIGHT % SEG_SIZE
UseUnstdTex = bool(int(settings.readline()))
for _ in range(6): settings.readline()
backgroundImageFileName = settings.readline().rstrip('\n')
background = settings.readline().rstrip('\n')
WALL_COLOR = settings.readline().rstrip('\n')
mapName = settings.readline().rstrip('\n')
settings.readline()
settings.readline()
settings.readline()
settings.readline()
settings.readline()
settings.readline()
walltextureFile = settings.readline().rstrip('\n')
displayMode = bool(int(settings.readline().rstrip('\n')))
settings.readline()
settings.close()

IN_GAME = True
b1 = b2 = True
wait = 0.5
timeLastBump1 = timeLastBump2 = clock()
pause = False
texture_redraw_options = eval(config0['General']['textureredrawoptions'])

lang = readLngFile(config['fallbacklng'], 'Py Tanks')
lang.update(readLngFile(lngFileName, 'Py Tanks'))

root.title(lang['title'])

def rotate_image(img, direction):
    w, h = img.width(), img.height()
    if direction in [90, 270]:
        newimg = PhotoImage(width=h + 1, height=w + 1)
    elif direction == 180: # 180 degree
        newimg = PhotoImage(width=w + 1, height=h + 1)
    for x in range(w):
        for y in range(h):
            rgb = '#%02x%02x%02x' % img.get(x, y)
            transparency = img.transparency_get(x, y)
            if (direction % 360) == 90: # 90 degrees
                newimg.put(rgb, (h-y,x))
                if transparency:
                    try:
                        newimg.transparency_set(h - y, x, True)
                    except:
                        pass
            elif (direction % 360) == 270: # -90 or 270 degrees
                newimg.put(rgb, (y,w-x))
                if transparency:
                    try:
                        newimg.transparency_set(y, w - x, True)
                    except:
                        pass
            else: # 180 degrees
                newimg.put(rgb, (w-x,h-y))
                if transparency:
                    try:
                        newimg.transparency_set(w - x, h - y, True)
                    except:
                        pass
    return newimg

def rotateImageNew(tkImage, direction):
    image = ImageTk.getimage(tkImage)
    rotatedImage = Image.Image.rotate(image, (360 - direction) % 360, expand = True)
    return ImageTk.PhotoImage(master = root, image = rotatedImage)

rotateImageDefault = rotate_image

def rotateImageSelector(image, direction):
    try:
        return rotateImageNew(image, direction)
    except:
        return rotateImageDefault(image, direction)

rotate_image = rotateImageSelector

def checkTanksArmor():
    aliveTeams = set()
    for i in range(len(tanks)):
        if tanks[i][0].hp > 0:
            aliveTeams.add(tanks[i][0].team)
        else:
            tanks[i][0].mapping = {}
            tanks[i][0].fireMapping = set()
    global IN_GAME
    if len(aliveTeams) == 1:
        aliveTeam = aliveTeams.pop()
        teamColor = [0, 0, 0]
        teamSize = 0
        for i in range(len(tanks)):
            if tanks[i][0].team == aliveTeam and tanks[i][0].color[0] == '#':
                for j in range(len(teamColor)):
                    teamColor[j] += int(tanks[i][0].color[1 + 2 * j:3 + 2 * j], 16)
                teamSize += 1
        for i in range(len(teamColor)):
            teamColor[i] //= teamSize
        tkTeamColor = '#'
        for i in range(len(teamColor)):
            tkTeamColor += f"{('0' + hex(teamColor[i])[2:])[-2:]}"
        c.create_text(WIDTH / 2, HEIGHT / 2, text = lang['teamwon'].format(name = aliveTeam), font = config0['General']['canvasfont'] + ' ' + str(SEG_SIZE), fill = tkTeamColor)
        IN_GAME = False
    elif len(aliveTeams) == 0:
        pass
        IN_GAME = False


class Texture:    
    def __init__(self, image, sizeX, sizeY, color, rotate = True):
        self.image = {}
        self.pttimage = None
        self.sizeX = sizeX
        self.sizeY = sizeY
        if type(image) == PhotoImage:
            w, h = image.width(), image.height()
            for x in range(w):
                for y in range(h):
                    clr = '#%02x%02x%02x' % image.get(x, y)
                    if clr == COLOR:
                        image.put(color, (x, y))
            self.image[(1, 0)] = image
            if rotate:
                self.image[(-1, 0)] = rotate_image(image, 180)
                self.image[(0, 1)] = rotate_image(image, 90)
                self.image[(0, -1)] = rotate_image(image, 270)
        else:
            resize = image[1]
            image = image[0]
            image.color(convertRGB(color), resize[0], resize[1])
            image.tkImage(root)
            self.image[(1, 0)] = image['Normal']['Right']
            self.image[(-1, 0)] = image['Normal']['Left']
            self.image[(0, 1)] = image['Normal']['Down']
            self.image[(0, -1)] = image['Normal']['Up']
            self.pttimage = image
        self.img = None
        return

    def spawn(self, x, y, d):
        if self.img != None:
            c.delete(self.img)
        self.img = c.create_image(x, y, anchor='nw',image=self.image[d])
        self.x = x
        self.y = y
        self.d = d

    def despawn(self):
        if self.img != None:
            c.delete(self.img)
        self.img = None

    def respawn(self):
        self.spawn(self.x, self.y, self.d)

    def spawnCopy(self, x, y, d, canvas = None):
        global c
        if canvas == None:
            canvas = c
        return canvas.create_image(x, y, anchor = 'nw', image = self.image[d])


class _Animation:

    def __init__(self, master, canvas, animation_update_delay, textureFilesMask, textureFileCount, size, scaling = None, rotate_textures = True):
        self.master = master
        self.canvas = canvas
        self.animationContinueRate = animation_update_delay
        self.textureList = []
        for i in range(textureFileCount):
            image = PhotoImage(master = root, file = eval("f'" + textureFilesMask + "'"))
            if scaling == None:
                tempSize = (image.width(), image.height())
                tempImg = image.zoom(SEG_SIZE * size[0] + 1, SEG_SIZE * size[1] + 1)
                image = tempImg.subsample(tempSize[0], tempSize[1])
            else:
                image = image.zoom(scaling[0], scaling[1])
            self.textureList.append(Texture(image, image.width(), image.height(), None, rotate_textures))
        self.textureMap = {}
        self.textureMapI = 0

    def start(self, posx, posy, direction=(1, 0), cycle=False):
        self.textureMap[self.textureMapI] = self.textureList[0].spawnCopy(posx, posy, direction, self.canvas)
        self.textureMapI += 1
        self.master.after(self.animationContinueRate, self._continue, posx, posy, direction, self.textureMapI - 1, 0, cycle)

    def _continue(self, posx, posy, direction, textureMapI, i=0, cycle=False):
        if pause:
            self.master.after(self.animationContinueRate, self._continue, posx, posy, direction, textureMapI, i, cycle)
            return
        self.canvas.delete(self.textureMap[textureMapI])
        i += 1
        if i >= len(self.textureList):
            if not cycle:
                self.textureMap.pop(textureMapI)
                return
            else:
                i = 0
        self.textureMap[textureMapI] = self.textureList[i].spawnCopy(posx, posy, direction, self.canvas)
        self.master.after(self.animationContinueRate, self._continue, posx, posy, direction, textureMapI, i, cycle)


class Animation(_Animation):

    def __init__(self, textureFilesMask, textureFileCount, size):
        super().__init__(root, c, int(config0['General']['animationcontinuerate']), textureFilesMask, textureFileCount, size)


class DisabledAnimation:

    def __init__(self, textureFilesMask, textureFileCount, size):
        pass

    def start(self, posx, posy, direction=(1, 0)):
        pass

    def _continue(self, posx, posy, direction, textureMapI, i=0):
        pass


def create_block(tank, posx, posy, direction, color):
    if tank.b:
        tank.b = False
        if not UseUnstdTex:
            block = c.create_oval(posx, posy, posx + SEG_SIZE, posy + SEG_SIZE, fill=color)
        else:
            block = c.create_oval(posx, posy, posx + SEG_SIZE, posy + SEG_SIZE, outline='')
            color.spawn(posx, posy, direction)
            startShootAnimation(posx + SEG_SIZE * direction[0], posy + SEG_SIZE * direction[1], direction)
        move_block(tank, block, posx, posy, direction, color)

def move_block(tank, block, posx, posy, direction, texture = None):
    global lang, pause
    if pause:
        root.after(50, move_block, tank, block, posx, posy, direction, texture)
        return
    if UseUnstdTex:
        textureBlock = texture
    if -SEG_SIZE <= posx <= WIDTH + SEG_SIZE and -SEG_SIZE <= posy <= HEIGHT + SEG_SIZE:
        global WALLS
        x1, y1, x2, y2 = c.coords(block)
        x2, y2 = x1 - direction[0] * SEG_SIZE * 3, y1 - direction[1] * SEG_SIZE * 3
        index = int(posx) // SEG_SIZE
        jndex = int(posy) // SEG_SIZE
        if index < WIDTH // SEG_SIZE and jndex < HEIGHT // SEG_SIZE:
            for i in range(3):
                if WALLS[jndex + i * direction[1]][index + i * direction[0]]:
                    x3, y3, x4, y4 = WIDTH, HEIGHT, WIDTH + SEG_SIZE, HEIGHT + SEG_SIZE
                    c.coords(block, x3 + direction[0] * SEG_SIZE * 3, y3 + direction[1] * SEG_SIZE * 3, x4 + direction[0] * SEG_SIZE * 3, y4 + direction[1] * SEG_SIZE * 3)
                    if UseUnstdTex:
                        textureBlock.despawn()
                        startDamageAnimation((index + i * direction[0]) * SEG_SIZE, (jndex + i * direction[1]) * SEG_SIZE)
                    tank.b = True
                    return
        for i in range(len(tanks)):
            if tanks[i][0].team != tank.team:
                for index in range(len(tanks[i][0].segments)):
                    x3, y3, x4, y4 = c.coords(tanks[i][0].segments[index].instance)
                    if (x1 <= x3 <= x2 or x2 <= x3 <= x1) and (y1 <= y3 <= y2 or y2 <= y3 <= y1):
                        global IN_GAME
                        tanks[i][0].hp -= 1
                        if int(config1['General']['respawnafterdestruction']):
                            tanks[i][0].respawn()
                        else:
                            tanks[i][0].respawn(False)
                        if IN_GAME:
                            c.itemconfig(tanks[i][1], text = tanks[i][0].hp)
                        x3, y3, x4, y4 = WIDTH, HEIGHT, WIDTH + SEG_SIZE, HEIGHT + SEG_SIZE
                        c.coords(block, x3 + direction[0] * SEG_SIZE * 3, y3 + direction[1] * SEG_SIZE * 3, x4 + direction[0] * SEG_SIZE * 3, y4 + direction[1] * SEG_SIZE * 3)
                        if UseUnstdTex:
                            texture.despawn()
                            startDamageAnimation(x1, y1)
                        tank.b = True
                        checkTanksArmor()
                        return
        x1, y1, x2, y2 = c.coords(block)
        c.coords(block, x1 + direction[0] * SEG_SIZE * 3, y1 + direction[1] * SEG_SIZE * 3, x2 + direction[0] * SEG_SIZE * 3, y2 + direction[1] * SEG_SIZE * 3)
        if UseUnstdTex:
            texture.despawned = False
            texture.despawn()
            _moveBlockTexture(block, posx, posy, direction, texture, *texture_redraw_options)
        posx += direction[0] * SEG_SIZE * 3
        posy += direction[1] * SEG_SIZE * 3
        root.after(50, move_block, tank, block, posx, posy, direction, texture)
    else:
        if UseUnstdTex:
            texture.despawned = False
            textureBlock.despawn()
        tank.b = True
        return

def _moveBlockTexture(block, posx, posy, direction, texture, n, d, i=0, texture_canvas_id = None):
    c.delete(texture_canvas_id)
    if i >= n or texture.despawned:
        return
    x, y = posx, posy
    x, y = ((x, y)[j] - direction[j] * 3 * SEG_SIZE * (n - i - 1) / n for j in range(len((x, y))))
    texture_canvas_id = texture.spawnCopy(x, y, direction)
    root.after(d, _moveBlockTexture, block, posx, posy, direction, texture, n, d, i + 1, texture_canvas_id)


class Segment(object):
    def __init__(self, c, x, y, color):
        self.instance = c.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, fill=color)


class Bar:

    def __init__(self, canvas, width, hp_bar_height, reload_bar_height, border_width, posx, posy, background_color, hp_bar_color, reload_bar_color, max_hp, max_reload, tank = None):
        self.canvas = canvas
        self.tank = tank
        self.width = width
        self.hp_bar_height = hp_bar_height
        self.reload_bar_height = reload_bar_height
        self.border_width = border_width
        self.posx = posx
        self.posy = posy
        self.background_color = background_color
        self.hp_bar_color = hp_bar_color
        self.reload_bar_color = reload_bar_color
        self.max_hp = max_hp
        self.max_reload = max_reload
        self.bar = None
        self.hp_bar = None
        self.reload_bar = None

    def assign_tank(self, tank):
        self.tank = tank
        tank_color = convertRGB(tank.color)
        self.hp_bar_current_color = rgb_to_tk_color([round((self.hp_bar_color[i] * self.hp_bar_color[3] + tank_color[i] * (255 - self.hp_bar_color[3])) / 255) for i in range(3)])
        self.reload_bar_current_color = rgb_to_tk_color([round((self.reload_bar_color[i] * self.reload_bar_color[3] + tank_color[i] * (255 - self.reload_bar_color[3])) / 255) for i in range(3)])

    def update(self, x = None, y = None):
        if x == None or y == None:
            x, y = self.canvas.coords(self.tank.segments[0].instance)[:2]
        if self.bar != None:
            self.canvas.delete(self.bar)
        if self.hp_bar != None:
            self.canvas.delete(self.hp_bar)
        if self.reload_bar != None:
            self.canvas.delete(self.reload_bar)
        if self.tank.vector == (1, 0):
            x -= SEG_SIZE // 2
        if self.tank.vector == (-1, 0):
            x -= SEG_SIZE // 2
        elif self.tank.vector == (0, -1):
            y = y - SEG_SIZE
        if self.tank.vector[0] == 0:
            x = x - SEG_SIZE // 2
        x += self.posx
        y += self.posy
        max_width = self.width - 2 * self.border_width
        self.bar = self.canvas.create_rectangle(x, y, x + self.width, y + 3 * self.border_width + self.hp_bar_height + self.reload_bar_height, fill = self.background_color, outline = '')
        self.hp_bar = self.canvas.create_rectangle(x + self.border_width, y + self.border_width, x + self.border_width + round(max_width * self.tank.hp / self.max_hp), y + self.border_width + self.hp_bar_height, fill = self.hp_bar_current_color, outline = '')
        if self.tank.reload == -1:
            ln = self.tank.b / self.max_reload
        else:
            ln = min((clock() - self.tank.last_shoot_time) / self.tank.reload, 1)
        self.reload_bar = self.canvas.create_rectangle(x + self.border_width, y + 2 * self.border_width + self.hp_bar_height, x + self.border_width + round(max_width * ln), y + 2 * self.border_width + self.hp_bar_height + self.reload_bar_height, fill = self.reload_bar_current_color, outline = '')


class Tank:
    def __init__(self, segments, mapping, fireMapping, vector, team, hp, hpWidget, speed, texture = None, bulletTexture = '', color = '#000000', bar = None, reload = -1):
        self.segments = segments
        self.respawnCoords = []
        for segment in segments:
            self.respawnCoords.append(c.coords(segment.instance))
        self.mapping = mapping
        self.fireMapping = fireMapping
        self.vector = vector
        self.respawnVector = vector
        self.team = team
        self.hp = hp
        self.hpWidget = hpWidget
        self.speed = speed
        self.timeLastBump = clock()
        self.texture = texture
        self.bulletTexture = bulletTexture
        self.b = True
        self.ai = None
        self.color = color
        self.bar = bar
        self.bar.assign_tank(self)
        self.b2 = False
        self.reload = reload
        self.last_shoot_time = clock() - reload

    def move(self, event):
        global lang
        if event in self.mapping:
            last_direction = self.vector
            self.vector = self.mapping[event]
            bl = False
            lastCoords = []
            for index in range(len(self.segments)):
                x1, y1, x2, y2 = c.coords(self.segments[index].instance)
                lastCoords.append((x1, y1, x2, y2))
                segment = self.segments[index].instance
                c.coords(segment, x1 + self.vector[0] * SEG_SIZE * self.speed, y1 + self.vector[1] * SEG_SIZE * self.speed, x2 + self.vector[0] * SEG_SIZE * self.speed, y2 + self.vector[1] * SEG_SIZE * self.speed)
                x1, y1, x2, y2 = c.coords(self.segments[index].instance)
                if WALLS[int(y1) // SEG_SIZE][int(x1) // SEG_SIZE]:
                    bl = True
            move_of_front = (last_direction[0] - self.vector[0], last_direction[1] - self.vector[1])
            x1, y1, x2, y2 = c.coords(self.segments[6].instance)
            segment = self.segments[6].instance
            c.coords(segment, x1 - move_of_front[0] * SEG_SIZE * 2, y1 - move_of_front[1] * SEG_SIZE * 2, x2 - move_of_front[0] * SEG_SIZE * 2, y2 - move_of_front[1] * SEG_SIZE * 2)
            x1, y1, x2, y2 = c.coords(self.segments[6].instance)
            global IN_GAME, wait
            bv1 = bv2 = bv3 = True
            if bl or WALLS[int(y1) // SEG_SIZE][int(x1) // SEG_SIZE]:
                bv1 = False
                now = clock()
                timeLastBump = self.timeLastBump
                if now - timeLastBump > wait and int(config1['General']['damagefromwalls']):
                    self.hp -= 1
                    checkTanksArmor()
                self.timeLastBump = now
                if int(config1['General']['respawnafterdestruction']) and int(config1['General']['damagefromwalls']):
                    self.respawn()
                else:
                    self.vector = last_direction
                    for index in range(len(self.segments)):
                        c.coords(self.segments[index].instance, *lastCoords[index])
                    self.respawn(False)
                if IN_GAME:
                    c.itemconfig(self.hpWidget, text=self.hp)
            if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
                bv2 = False
                now = clock()
                timeLastBump = self.timeLastBump
                if now - timeLastBump > wait and int(config1['General']['damagefromwalls']):
                    self.hp -= 1
                    checkTanksArmor()
                self.timeLastBump = now
                if int(config1['General']['respawnafterdestruction']) and int(config1['General']['damagefromwalls']):
                    self.respawn()
                else:
                    self.vector = last_direction
                    for index in range(len(self.segments)):
                        c.coords(self.segments[index].instance, *lastCoords[index])
                    self.respawn(False)
                if IN_GAME:
                    c.itemconfig(self.hpWidget, text=self.hp)
            if int(config1['General']['rammingdamage']):
                for index in range(len(self.segments)):
                    segments = []
                    for jndex in range(len(segments)):
                        if c.coords(self.segments[index].instance) == c.coords(segments[jndex].instance):
                            bv3 = False
                            self.hp -= 1
                            if int(config1['General']['respawnafterdestruction']):
                                self.respawn()
                            return
            if UseUnstdTex and bv1 and bv2 and bv3:
                self.b2 = True
                self._moveTexture(*texture_redraw_options)
                    
        elif event in self.fireMapping:
            if self.reload != -1:
                if clock() - self.last_shoot_time >= self.reload:
                    self.b = True
                    self.last_shoot_time = clock()
                else:
                    self.b = False
            create_block(self, c.coords(self.segments[6].instance)[0], c.coords(self.segments[6].instance)[1], self.vector, self.bulletTexture)

        if not UseUnstdTex or not self.b2:
            self.bar.update()


    def _moveTexture(self, n, d, i=0):
        if i >= n or not self.segments:
            self.b2 = False
            return
        texture = self.texture
        x, y = c.coords(self.segments[0].instance)[:2]
        x, y = ((x, y)[j] - self.vector[j] * SEG_SIZE * (n - i - 1) / n for j in range(len((x, y))))
        self.bar.update(x, y)
        if self.vector == (-1, 0):
            texture.spawn(x - SEG_SIZE, y, self.vector)
        elif self.vector == (0, -1):
            texture.spawn(x, y - SEG_SIZE, self.vector)
        else:
            texture.spawn(x, y, self.vector)
        root.after(d, self._moveTexture, n, d, i + 1)

    def _respawn(self):
        self.vector = self.respawnVector
        for i in range(len(self.segments)):
            c.coords(self.segments[i].instance, *self.respawnCoords[i])
        if UseUnstdTex:
            if self.respawnVector == (-1, 0):
                self.texture.spawn(self.respawnCoords[6][0], self.respawnCoords[0][1], self.respawnVector)
            elif self.respawnVector == (0, -1):
                self.texture.spawn(self.respawnCoords[0][0], self.respawnCoords[6][1], self.respawnVector)
            else:
                self.texture.spawn(self.respawnCoords[0][0], self.respawnCoords[0][1], self.respawnVector)
        if self.ai:
            self.ai.destruction()
        self.bar.update()

    def respawn(self, __respawn = True):
        if self.hp > 0:
            if __respawn:
                self._respawn()
        else:
            self.bar.update()
            if UseUnstdTex:
                try:
                    self.texture.image[(1, 0)] = self.texture.pttimage['Destroyed']['Right']
                    self.texture.image[(-1, 0)] = self.texture.pttimage['Destroyed']['Left']
                    self.texture.image[(0, 1)] = self.texture.pttimage['Destroyed']['Down']
                    self.texture.image[(0, -1)] = self.texture.pttimage['Destroyed']['Up']
                    self.texture.respawn()
                except:
                    pass
                startDestructionAnimation(*c.coords(self.segments[0].instance)[:2])
            self.segments = []

    def spawn(self, x, y, vector):
        _respawnVector = self.respawnVector
        self.respawnVector = vector
        _respawnCoords = self.respawnCoords
        spawn_coords = [None] * 9
        _respawnCoords = spawn_coords
        for i in range(3):
            for j in range(3):
                segments[i * 3 + j] = ((x + i) * SEG_SIZE, (y + j) * SEG_SIZE, (x + i) * SEG_SIZE + SEG_SIZE, (y + j) * SEG_SIZE + SEG_SIZE)
        spawn_coords.insert(6, None)
        if vector == (-1, 0):
            segments[6] = ((x - 1) * SEG_SIZE, (y + 1) * SEG_SIZE, (x - 1) * SEG_SIZE + SEG_SIZE, (y + 1) * SEG_SIZE + SEG_SIZE)
        elif vector == (1, 0):
            segments[6] = ((x + 3) * SEG_SIZE, (y + 1) * SEG_SIZE, (x + 3) * SEG_SIZE + SEG_SIZE, (y + 1) * SEG_SIZE + SEG_SIZE)
        elif vector == (0, -1):
            segments[6] = ((x + 1) * SEG_SIZE, (y - 1) * SEG_SIZE, (x + 1) * SEG_SIZE + SEG_SIZE, (y - 1) * SEG_SIZE + SEG_SIZE)
        elif vector == (0, 1):
            segments[6] = ((x + 1) * SEG_SIZE, (y + 3) * SEG_SIZE, (x + 1) * SEG_SIZE + SEG_SIZE, (y + 3) * SEG_SIZE + SEG_SIZE)
        self._respawn()
        self.respawnVector = _respawnVector
        self.respawnCoords = _respawnCoords


class F10Menu():

    def __init__(self, canvas = None, window = None):
        self.canvas = canvas
        self.window = window
        self.frame = Frame(canvas.master)
        self.label = Label(self.frame, text = lang['pausetitle'])
        self.continueButton = Button(self.frame, text = lang['continuebutton'], command = self._continue)
        self.exitButton = Button(self.frame, text = lang['exitbutton'], command = self._exit)
        self.label.grid(row = 0, column = 0, columnspan = 2, padx = 7, pady = (7, 3))
        self.continueButton.grid(row = 1, column = 0, padx = (7, 3), pady = (3, 7))
        self.exitButton.grid(row = 1, column = 1, padx = (3, 7), pady = (3, 7))
        try:
            img = Image.new(mode = 'RGBA', size = (int(canvas['width']), int(canvas['height'])), color = eval(config0['General']['pausecolor']))
            self.image = ImageTk.PhotoImage(image = img)
        except NameError:
            self.image = None
        self.imgCnvF = False

    def display(self):
        self.imgCnvF = True
        self.imgCnv = self.canvas.create_image(0, 0, anchor = 'nw', image = self.image)
        self.frame.place(relx = 0.5, rely = 0.5, anchor = 'center')
        self.window.after(100, self._updateImg)

    def _updateImg(self):
        if self.imgCnvF:
            self.canvas.delete(self.imgCnv)
        self.imgCnvF = True
        self.imgCnv = self.canvas.create_image(0, 0, anchor = 'nw', image = self.image)

    def close(self):
        self.frame.place_forget()
        if self.imgCnvF:
            self.canvas.delete(self.imgCnv)

    def _continue(self):
        global pause
        self.close()
        if pause:
            pause = False

    def _exit(self):
        close()


#====================NG==============================================================================================================================================================
def gen_tank_move_str(tankid, action):
    return '{}_{}'.format(tankid, action)


def keysym(event):
    if ord('A') <= event.keycode <= ord('Z'):
        return chr(event.keycode)
    else:
        return event.keysym


class RemoteEventController:

    def rec_init(self, tankid_to_index, default_action):
        self.tank_actions = {}
        self.tank_shoot = {}
        for tankid in tankid_to_index:
            self.tank_actions[tankid] = default_action
            self.tank_shoot[tankid] = False

    def update_tank_list(self, tank_list, eventsf):
        for tankid in self.tank_actions:
            if tankid not in tankid_to_index:
                continue
            tank_list[tankid_to_index[tankid]][1] = gen_tank_move_str(tankid, self.tank_actions[tankid])
            if self.tank_shoot[tankid]:
                eventsf.add(gen_tank_move_str(tankid, 'Shoot'))
            else:
                try:
                    eventsf.remove(gen_tank_move_str(tankid, 'Shoot'))
                except:
                    pass

    def kpc_(self, keysym):
        pass

    def krc_(self, keysym):
        pass

    def kpc(self, event):
        KeyPressController(event)
        self.kpc_(keysym(event))

    def krc(self, event):
        KeyReleaseController(event)
        self.krc_(keysym(event))


class ConnectionAnimationWindow:

    def __init__(self, master, config0, config1, lang):
        self.window = Toplevel(master)
        self.window.withdraw()
        self.window.title(lang['CAWtitle'])
        if os.name == 'nt':
            root.iconbitmap(config0['General']['icon'])
        texture_files_mask = os.path.join(config0['General']['сonnectionTextures'], '{i}.' + config0['General']['сonnectionTexturesType'])
        image = PhotoImage(master = self.window, file = texture_files_mask.format(i = 0))
        zoom = eval(config0['General']['сonnectionTexturesZoom'])
        canvas = Canvas(self.window, highlightthickness = 0, width = image.width() * zoom[0], height = image.height() * zoom[1])
        self.animation = _Animation(self.window, canvas, round(float(config0['General']['сonnectionUpdateDelay']) * 1000), texture_files_mask, int(config0['General']['сonnectionTexturesCount']), (0, 0), zoom, False)
        canvas.grid(row = 0, column = 1)
        self.frame = Frame(self.window)
        self.frame.grid(row = 0, column = 0)
        self.window.protocol('WM_DELETE_WINDOW', lambda: close())
        
    def start(self):
        self.window.deiconify()
        self.animation.start(0, 0, cycle = True)

    def update(self):
        self.window.update()

    def destroy(self):
        self.window.destroy()


class DataTransmitter:

    def __init__(self, connection, pkg_size):
        self.connection = connection
        self.pkg_size = pkg_size
        self.size_field_size = 2
        self.buffer = [0] * pkg_size

    def _send(self, byte_array):
        ba_i = 0
        while True:
            buf_i = self.size_field_size
            while buf_i < self.pkg_size and ba_i < len(byte_array):
                self.buffer[buf_i] = byte_array[ba_i]
                ba_i += 1
                buf_i += 1
            self.buffer[0] = buf_i >> 8
            self.buffer[1] = buf_i - (self.buffer[0] << 8)
            self.connection.send(bytes(self.buffer))
            if buf_i < self.pkg_size:
                break

    def send_python_value(self, value):
        byte_array = value.__repr__().encode(encoding = 'utf-8')
        self._send(byte_array)

    pass


class DataReceiver:

    def __init__(self, connection, pkg_size):
        self.connection = connection
        self.pkg_size = pkg_size
        self.size_field_size = 2

    def _recv(self):
        byte_array = []
        while True:
            buffer = self.connection.recv(self.pkg_size)
            size = (buffer[0] << 8) + buffer[1]
            for buf_i in range(self.size_field_size, size):
                byte_array.append(buffer[buf_i])
            if size < self.pkg_size:
                break
        return byte_array

    def recv_python_value(self):
        byte_array = bytes(self._recv())
        return eval(byte_array.decode(encoding = 'utf-8'))

    pass


package_size = int(config0['LANGame']['package_size'])
udp_package_size = int(config0['LANGame']['udp_pkg_size'])
tank_settings = ('team', 'hp', 'speed', 'color', 'initpos', 'hppos', 'direction', 'reload')


def version_to_tuple(version):
    return tuple((int(n) for n in version.split('.')))


def calc_checksum(file_name, mod):
    checksum = 0
    file = open(file_name, 'br')
    while True:
        n = file.read(1)
        if not n:
            break
        checksum = (checksum + n[0]) % mod
    file.close()
    return checksum


checksum_mod = config0['LANGame']['checksum_mod']


dta = {(0, -1): 'Up', (0, 1): 'Down', (-1, 0): 'Left', (1, 0): 'Right'}
atd = {}
for d in dta:
    atd[dta[d]] = d


class PTServer(RemoteEventController):

    def __init__(self, ip_address, port):
        self.socket = sckt.socket()
        self.ip_address = ip_address
        self.port = port
        self.socket.bind((ip_address, port))
        self.caw = ConnectionAnimationWindow(root, config0, config1, lang)
        self.udp_socket = sckt.socket(sckt.AF_INET, sckt.SOCK_DGRAM)
        self.tank_shoot_keysym = {}

    def set_number_of_clients(self, number_of_clients):
        self.socket.listen(len(number_of_clients))
        self.number_of_clients = number_of_clients.copy()

    def _accept_connection(self, result):
        result[0] = self.socket.accept()
        result[1] = True

    def accept_connection(self):
        result = [None, False]
        thread = thrd.Thread(target = self._accept_connection, args = [result])
        thread.start()
        return result

    def accept_connections(self):
        connection_list = []
        for i in range(len(self.number_of_clients)):
            connection_list.append(self.accept_connection())
        self.caw.start()
        while True:
            v = True
            for connection in connection_list:
                v = v and connection[1]
            if v:
                break
            self.caw.update()
        self.connections = {}
        self.connection_list_2 = []
        for connection_list_el in connection_list:
            connection = connection_list_el[0][0]
            self.connection_list_2.append([connection, DataTransmitter(connection, package_size), DataReceiver(connection, package_size), None])

    def _get_settings_from_client(self, i, result):
        result[1] = False
        settings = {}
        result[0] = settings
        settings_list = ['py_tanks_version', 'team', 'hp', 'speed', 'color', 'initpos', 'hppos', 'direction', 'reload']
        settings_list_i = 0
        while settings_list_i < len(settings_list):
            self.connection_list_2[i][1].send_python_value(settings_list[settings_list_i])
            settings[settings_list[settings_list_i]] = self.connection_list_2[i][2].recv_python_value()
            pass
            settings_list_i += 1
        self.connection_list_2[i][1].send_python_value('sync_done')
        result[1] = True

    def _send_settings_to_client(self, tankid, result):
        result[0] = False
        while True:
            msg = self.clients[tankid][2].recv_python_value()
            if msg == 'sync_done':
                break
            elif msg == 'tank_s':
                t_id, s = self.clients[tankid][2].recv_python_value()
                self.clients[tankid][1].send_python_value(config1[t_id][s])
            elif msg == 'field_size':
                self.clients[tankid][1].send_python_value((WIDTH // SEG_SIZE, HEIGHT // SEG_SIZE))
            elif msg == 'are_textures_enabled':
                self.clients[tankid][1].send_python_value(UseUnstdTex)
            elif msg == 'map_file_name':
                self.clients[tankid][1].send_python_value(mapName)
            elif msg == 'bg_color':
                self.clients[tankid][1].send_python_value(background)
            elif msg == 'wall_color':
                self.clients[tankid][1].send_python_value(WALL_COLOR)
            elif msg == 'r.a.d.':
                self.clients[tankid][1].send_python_value(config1['General']['respawnafterdestruction'])
            elif msg == 'd.f.w.':
                self.clients[tankid][1].send_python_value(config1['General']['damagefromwalls'])
            elif msg == 'tank_list':
                self.clients[tankid][1].send_python_value(config1['General']['tanklist'])
            elif msg == 'id':
                self.clients[tankid][1].send_python_value(tankid)
        result[0] = True

    def synchronize_settings(self):
        for i in range(len(self.connection_list_2)):
            self.connection_list_2[i][3] = [None, False]
            thread = thrd.Thread(target = self._get_settings_from_client, args = (i, self.connection_list_2[i][3]))
            thread.start()
        while True:
            v = True
            for i in range(len(self.connection_list_2)):
                v = v and self.connection_list_2[i][3][1]
            if v:
                break
            self.caw.update()
        self.clients = {}
        for i in range(len(self.connection_list_2)):
            tankid = self.number_of_clients[i]
            self.clients[tankid] = [self.connection_list_2[i][3][0], self.connection_list_2[i][1], self.connection_list_2[i][2]]
        for tankid in self.clients:
            for key in tank_settings:
                config1[tankid][key] = self.clients[tankid][0][key]
        sync_done_list = {}
        for tankid in self.clients:
            sync_done_list[tankid] = [False]
            thread = thrd.Thread(target = self._send_settings_to_client, args = (tankid, sync_done_list[tankid]))
            thread.start()
        while True:
            v = True
            for tankid in sync_done_list:
                v = v and sync_done_list[tankid][0]
            if v:
                break
            self.caw.update()
        self.caw.window.withdraw()
        pass

    def _get_ready_packet(self, client, is_ready):
        while self.clients[client][2].recv_python_value() != 'Ready':
            pass
        is_ready[client] = True

    def wait_clients(self):
        self.caw.window.deiconify()
        is_ready = {}
        for client in self.clients:
            is_ready[client] = False
            thread = thrd.Thread(target = self._get_ready_packet, args = (client, is_ready))
            thread.start()
        while True:
            v = True
            for client in is_ready:
                v = v and is_ready[client]
            if v:
                break
            self.caw.update()
        self.caw.destroy()

    def _action_getter(self):
        while True:
            self._get_action()

    def _get_action(self):
        data, addr = self.udp_socket.recvfrom(udp_package_size)
        tankid, action = data.decode('utf-8').split(';')
        self.udp_addresses[tankid] = addr
        if action in {'None', 'Up', 'Down', 'Left', 'Right'}:
            self.tank_actions[tankid] = action
        elif action == 'Shoot':
            self.tank_shoot[tankid] = True
        elif action == '-Shoot':
            self.tank_shoot[tankid] = False
        self._send_action_to_clients(tankid, action)

    def _send_action_to_clients(self, tankid, action):
        enc_msg_type = 'A'.encode('utf-8')
        enc_tank_id = tankid.encode('utf-8')
        enc_action = action.encode('utf-8')
        etidl = len(enc_tank_id)
        eal = len(enc_action)
        msg = enc_msg_type + bytes([etidl]) + enc_tank_id + bytes([eal]) + enc_action
        for client in self.udp_addresses:
            self.udp_socket.sendto(msg, self.udp_addresses[client])

    def _make_s_pkg(self, tankid):
        enc_msg_type = 'S'.encode('utf-8')
        sync_list = []
        tank = tankList[tankid_to_index[tankid]][0]
        x, y = [el // SEG_SIZE for el in c.coords(tank.segments[0].instance)[:2]]
        sync_list.append((x, y))
        sync_list.append(tank.vector)
        sync_list.append(tank.hp)
        enc_tank_id = tankid.encode('utf-8')
        enc_sl = str(sync_list).encode('utf-8')
        etidl = len(enc_tank_id)
        esll = len(enc_sl)
        msg = enc_msg_type + bytes([etidl]) + enc_tank_id + bytes([esll]) + enc_sl
        return msg

    def _sync_game(self):
        for tankid in tankList:
            msg = self._make_s_pkg(tankid)
            for client in self.udp_addresses:
                self.udp_socket.sendto(msg, self.udp_addresses[client])

    def _start_sync(self):
        sync_delay = int(config0['LANGame']['sync_delay'])
        while True:
            sync_start_time = round(clock() * 1000)
            self._sync_game()
            sync_end_time = round(clock() * 1000)
            time.sleep(max(0, (sync_delay - (sync_end_time - sync_start_time)) / 1000))

    def kpc_(self, keysym):
        for i in range(len(tankList)):
            tank = tankList[i][0]
            if keysym in tank.mapping:
                self.tank_actions[tank.id] = dta[tank.mapping[keysym]]
                self._send_action_to_clients(tank.id, self.tank_actions[tank.id])
            if keysym in tank.fireMapping:
                self.tank_shoot[tank.id] = True
                self.tank_shoot_keysym[tank.id] = keysym
                self._send_action_to_clients(tank.id, 'Shoot')

    def krc_(self, keysym):
        for i in range(len(tankList)):
            tank = tankList[i][0]
            if keysym in tank.mapping and self.tank_actions[tank.id] == dta[tank.mapping[keysym]]:
                self.tank_actions[tank.id] = 'None'
                self._send_action_to_clients(tank.id, self.tank_actions[tank.id])
            if keysym in tank.fireMapping and tank.id in self.tank_shoot_keysym and self.tank_shoot_keysym[tank.id] == keysym:
                self.tank_shoot[tank.id] = False
                self.tank_shoot_keysym[tank.id] = None
                self._send_action_to_clients(tank.id, '-Shoot')

    def start_game_data_exchange(self):
        for client in self.clients:
            self.clients[client][1].send_python_value('Start')
        self.socket.close()
        self.udp_socket.bind((self.ip_address, self.port))
        self.udp_addresses = {}
        ag_thread = thrd.Thread(target = self._action_getter, args = [])
        ag_thread.start()
        s_thread = thrd.Thread(target = self._start_sync, args = [])
        s_thread.start()

    pass


class PTClient(RemoteEventController):

    def __init__(self, ip_address, port):
        self.socket = sckt.socket()
        self.ip_address = ip_address
        self.port = port
        self.caw = ConnectionAnimationWindow(root, config0, config1, lang)
        self.udp_socket = sckt.socket(sckt.AF_INET, sckt.SOCK_DGRAM)

    def _connect(self, result):
        while True:
            result[0] = self.socket.connect_ex((self.ip_address, self.port))
            if result[0] != 10060:
                break
        result[1] = True

    def connect(self):
        result = [None, False]
        thread = thrd.Thread(target = self._connect, args = [result])
        thread.start()
        self.caw.start()
        while True:
            if result[1]:
                break
            self.caw.update()
        self.data_transmitter = DataTransmitter(self.socket, package_size)
        self.data_receiver = DataReceiver(self.socket, package_size)
        s1 = 'laddr='
        i = self.socket.__repr__().find(s1)
        s2 = client.socket.__repr__()[i + len(s1): client.socket.__repr__().find(')', i) + 1]
        self.self_ip_addr = eval(s2)[0]
        if result[0] == 0:
            pass
        return result[0]

    def _send_settings_to_server(self, result):
        result[0] = False
        tankid = config0['LANGame']['tankid']
        settings = {'py_tanks_version': version_to_tuple(PyTanksVersion)}
        s_lst = tank_settings
        for s in s_lst:
            settings[s] = config1[tankid][s]
        while True:
            msg = self.data_receiver.recv_python_value()
            if msg == 'sync_done':
                break
            else:
                self.data_transmitter.send_python_value(settings[msg])
        result[0] = True

    def _get_settings_from_server(self, result):
        global WIDTH, HEIGHT, UseUnstdTex, background, WALL_COLOR, mapName, backgroundImageFileName, walltextureFile
        result[1] = False
        settings = {}
        result[0] = settings
        settings_list = ('field_size', 'are_textures_enabled', 'map_file_name', 'bg_color', 'wall_color', 'r.a.d.', 'd.f.w.', 'tank_list', 'id')
        for s in settings_list:
            self.data_transmitter.send_python_value(s)
            settings[s] = self.data_receiver.recv_python_value()
        WIDTH = settings['field_size'][0] * SEG_SIZE
        HEIGHT = settings['field_size'][1] * SEG_SIZE
        UseUnstdTex = UseUnstdTex and settings['are_textures_enabled']
        mapName = settings['map_file_name']
        background = settings['bg_color']
        WALL_COLOR = settings['wall_color']
        pass
        config1['General']['respawnafterdestruction'] = settings['r.a.d.']
        config1['General']['damagefromwalls'] = settings['d.f.w.']
        config1['General']['tanklist'] = settings['tank_list']
        selfid = settings['id']
        for tankid in eval(config1['General']['tanklist']):
            if tankid != selfid:
                config1[tankid]['is_remote'] = 'True'
                config1[tankid]['ai'] = 'None'
                for ts in tank_settings:
                    self.data_transmitter.send_python_value('tank_s')
                    self.data_transmitter.send_python_value((tankid, ts))
                    config1[tankid][ts] = self.data_receiver.recv_python_value()
            else:
                config1[tankid] = config1[config0['LANGame']['tankid']]
        self.data_transmitter.send_python_value('sync_done')
        self.id = selfid
        result[1] = True

    def synchronize_settings(self):
        sync_done = [False]
        thread = thrd.Thread(target = self._send_settings_to_server, args = [sync_done])
        thread.start()
        while True:
            if sync_done[0]:
                break
            self.caw.update()
        sync_done = [None, False]
        thread = thrd.Thread(target = self._get_settings_from_server, args = [sync_done])
        thread.start()
        while True:
            if sync_done[1]:
                break
            self.caw.update()
        self.caw.window.withdraw()
        pass

    def ready(self):
        self.data_transmitter.send_python_value('Ready')

    _action_getter = PTServer._action_getter

    def _get_action(self):
        data, addr = self.udp_socket.recvfrom(udp_package_size)
        i = 0
        msgt = bytes([data[i]]).decode('utf-8')
        if msgt == 'A':
            i += 1
            etidl = data[i]
            i += 1
            enc_tank_id = data[i:i+etidl]
            i += etidl
            eal = data[i]
            i += 1
            enc_action = data[i:i+eal]
            i += eal
            tankid = enc_tank_id.decode('utf-8')
            action = enc_action.decode('utf-8')
            if action in {'None', 'Up', 'Down', 'Left', 'Right'}:
                self.tank_actions[tankid] = action
            elif action == 'Shoot':
                self.tank_shoot[tankid] = True
            elif action == '-Shoot':
                self.tank_shoot[tankid] = False
        pass

    def _send_action_to_server(self, action):
        msg = ('{tankid};{action}'.format(tankid = self.id, action = action)).encode('utf-8')
        self.udp_socket.sendto(msg, (self.ip_address, self.port))

    def start_game_data_exchange(self):
        while self.data_receiver.recv_python_value() != 'Start':
            self.caw.update()
        self.caw.destroy()
        self.socket.close()
        self.udp_socket.bind((self.self_ip_addr, self.port))
        thread = thrd.Thread(target = self._action_getter, args = [])
        thread.start()
        self._send_action_to_server('None')

    pass

        
if eval(config1['NetworkPlay']['enabled']):

    if eval(config1['NetworkPlay']['is_server']):
        server = PTServer(config1['NetworkPlay']['self_ip'], eval(config1['NetworkPlay']['port']))
        rec = server

    else:
        client = PTClient(config1['NetworkPlay']['server_ip'], eval(config1['NetworkPlay']['port']))
        rec = client

else:
    rec = None
#=========================================================================================================


tankList = []


def KeyController():
    global eventsf, tankList, pause, rec

    if pause:
        root.after(50, KeyController)
        return

    if eval(config1['NetworkPlay']['enabled']):
        rec.update_tank_list(tankList, eventsf)

    for tank, event in tankList:
        if event == 'AI':
            if IN_GAME:
                try:
                    tank.doAction()
                except:
                    pass
            continue
        tank.move(event)
        for eventf in eventsf:
            tank.move(eventf)
    root.after(50, KeyController)


def log_event(event):
    global event2
    event2 = event
    if not eval(config0['Debug']['keylogging']):
        return
    keyloggingfilename = config0['Debug']['keyloggingfile']
    if keyloggingfilename == 'stdout':
        keyloggingfile = sys.stdout
    else:
        keyloggingfile = open(config0['Debug']['keyloggingfile'], 'a')
    event_type = event.type.__repr__()[event.type.__repr__().find('.')+1:event.type.__repr__().find(':')]
    if len(event_type) < 10:
        event_type += '\t'
    print(f'type: {event_type}\tSerial: {event.serial}\tkeycode: {event.keycode}\tchar: "{event.char}"\tkeysym: {event.keysym}\tkeysym_num: {event.keysym_num}', file = keyloggingfile)
    if keyloggingfilename != 'stdout':
        keyloggingfile.close()


def KeyPressController(event):
    global pause

    log_event(event)

    keysym = event.keysym
    if ord('A') <= event.keycode <= ord('Z'):
        keysym = chr(event.keycode)
    
    if keysym == 'Escape' and eval(config0['General']['exitonesc']):
        close()
    
    if keysym == 'F11':
        global root
        if root.attributes('-fullscreen'):
            root.attributes('-fullscreen', False)
        else:
            root.attributes('-fullscreen', True)
    if keysym == 'R':
        restart()

    if keysym == 'F10':
        global c
        pause = not pause
        if pause:
            f10m.display()
        else:
            f10m.close()

    global tankList
    eventkeysym = keysym

    for i in range(len(tankList)):
        if eventkeysym in tankList[i][0].mapping:
            tankList[i][1] = eventkeysym
        if eventkeysym in tankList[i][0].fireMapping:
            eventsf.add(eventkeysym)


def KeyReleaseController(event):
    global tankList

    log_event(event)
    
    if ord('A') <= event.keycode <= ord('Z'):
        eventkeysym = chr(event.keycode)
    else:
        eventkeysym = event.keysym
    
    for i in range(len(tankList)):
        if eventkeysym == tankList[i][1]:
            tankList[i][1] = ''
    if eventkeysym in eventsf:
        eventsf.remove(eventkeysym)


class TransparentSegment:
    def __init__(self, c, x, y, color):
        self.instance = c.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, outline='')


texture = Texture


def restart():
    global config
    startfile(config['pytanks'])
    terminate(root)

root.protocol("WM_DELETE_WINDOW", close)

if os.name == 'nt':
    root.iconbitmap(config['icon'])

pbwindow = Toplevel(root)
pbwindow.withdraw()
if os.name == 'nt':
    pbwindow.iconbitmap(config['icon'])
pbwindow.title(lang['loadingTitle'])
pblen = int(config['progressbarLength'])
if colorScheme % 2 == 0:
    from tkinter.ttk import Progressbar, Style
    style = Style(root)
    if 'winnative' in style.theme_names():
        style.theme_use('winnative')
    else:
        style.theme_use('default')
    if colorScheme == 2:
        style.configure('dark.Horizontal.TProgressbar', troughcolor = '#3F3F3F')
        def Progressbar(master=None, **kw):
            if 'style' not in kw:
                kw['style'] = 'dark.Horizontal.TProgressbar'
            return tkinter.ttk.Progressbar(master, **kw)


#======================================NG============================================
if eval(config1['NetworkPlay']['enabled']):

    if eval(config1['NetworkPlay']['is_server']):
        number_of_clients = []
        for tank in eval(config1['General']['tanklist']):
            if eval(config1[tank]['is_remote']):
                number_of_clients.append(tank)
        server.set_number_of_clients(number_of_clients)
        server.accept_connections()
        server.synchronize_settings()
        pass

    else:
        client.connect()
        client.synchronize_settings()
        pass
#====================================================================================


pb = Progressbar(pbwindow, length = pblen)
pb.pack()
pbwindow.deiconify()
pbwindow.update()


frame = Frame(root)
frame.grid(sticky = 'nwse')
root.rowconfigure(index = 0, weight = 1)
root.columnconfigure(index = 0, weight = 1)


c = Canvas(frame, width=WIDTH, height=HEIGHT, bg=background)
if backgroundImageFileName:
    try:
        bgimage = Image.open(backgroundImageFileName)
        rbgimage = bgimage.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        backgroundImage = ImageTk.PhotoImage(master = root, image = rbgimage)
    except:
        backgroundImage = PhotoImage(file = backgroundImageFileName)
else:
    backgroundImage = None
c.create_image(0, 0, anchor="nw", image=backgroundImage)
c.place(relx = 0.5, rely = 0.5, anchor = CENTER)

if not UseUnstdTex:
    WallSegment = Segment
else:
    WallSegment = TransparentSegment
    file = walltextureFile
    frmt = os.path.splitext(file)[1][1:]
    if frmt not in formats:
        raiseFormatErrorAndExit()
    texlib = formats[frmt]
    if texlib == None:
        WallImg = PhotoImage(file = file)
        w, h = WallImg.width(), WallImg.height()
        for x in range(w):
            for y in range(h):
                clr = '#%02x%02x%02x' % WallImg.get(x, y)
                if clr == COLOR:
                    WallImg.put(WALL_COLOR, (x, y))
        tempSize = (WallImg.width(), WallImg.height())
        tempImg = WallImg.zoom(SEG_SIZE + 1, SEG_SIZE + 1)
        WallImg = tempImg.subsample(tempSize[0], tempSize[1])
    else:
        WallImgF = [None] * 2
        WallImgF[0] = texlib.Texture(unzipDirectory = os.path.abspath(config['tempDir']), textureConfig = config['textureconfig'], textureConfigEncoding = config['textureconfigencoding'], textureStates = eval(config0['General']['walltexturestates']), textureDirections = config['walltexturedirections'].split(','))
        WallImgF[0].open(os.path.abspath(file))
        WallImgF[1] = list(WallImgF[0].images['Normal']['Std'][0].size)
        WallImgF[1][0] = (SEG_SIZE + 1) / WallImgF[1][0]
        WallImgF[1][1] = (SEG_SIZE + 1) / WallImgF[1][1]
        resize = WallImgF[1]
        WallImgF0 = WallImgF[0]
        WallImgF0.color(convertRGB(WALL_COLOR), resize[0], resize[1])
        WallImgF0.tkImage(root)
        WallImg = WallImgF0['Normal']['Std']


cnv = c


mbppbp = 88235
pr = 1

if not UseUnstdTex:
    WallImg = None
WALLS = readPtmFile(mapName, SEG_SIZE, c, WallSegment, WALL_COLOR, UseUnstdTex, WallImg, pbwindow, pb, mbppbp, pr)


if not int(config['canvasBorder']):
    c.config(highlightthickness = 0)
c.focus_set()
WIDTH2 = WIDTH // 2
HEIGHT2 = HEIGHT // 2
if UseUnstdTex:
    Segment = TransparentSegment
    textureBlock1 = textureBlock2 = None


sys.path.append(config0['General']['aisfolder'])


tanks = []
tanklist = eval(config1['General']['tanklist'])


action_list = ['Up', 'Down', 'Left', 'Right', 'Shoot']


tankid_to_index = {}


for tank in tanklist:
    x, y = map(int, config1[tank]['initpos'].replace(' ', '').split(','))
    segments = [None] * 9
    for i in range(3):
        for j in range(3):
            segments[i * 3 + j] = Segment(cnv, (x + i) * SEG_SIZE, (y + j) * SEG_SIZE, config1[tank]['color'])
    segments.insert(6, None)
    vector = None
    if config1[tank]['direction'] == 'left':
        segments[6] = Segment(cnv, (x - 1) * SEG_SIZE, (y + 1) * SEG_SIZE, config1[tank]['color'])
        vector = (-1, 0)
    elif config1[tank]['direction'] == 'right':
        segments[6] = Segment(cnv, (x + 3) * SEG_SIZE, (y + 1) * SEG_SIZE, config1[tank]['color'])
        vector = (1, 0)
    elif config1[tank]['direction'] == 'up':
        segments[6] = Segment(cnv, (x + 1) * SEG_SIZE, (y - 1) * SEG_SIZE, config1[tank]['color'])
        vector = (0, -1)
    elif config1[tank]['direction'] == 'down':
        segments[6] = Segment(cnv, (x + 1) * SEG_SIZE, (y + 3) * SEG_SIZE, config1[tank]['color'])
        vector = (0, 1)

    if UseUnstdTex:
        file = config1[tank]['texture']
        frmt = os.path.splitext(file)[1][1:]
        if frmt not in formats:
            raiseFormatErrorAndExit()
        texlib = formats[frmt]
        if texlib == None:
            TankImg = PhotoImage(file = file)
            tempSize = (TankImg.width(), TankImg.height())
            tempImg = TankImg.zoom(SEG_SIZE * 4 + 1, SEG_SIZE * 3 + 1)
            TankImg = tempImg.subsample(tempSize[0], tempSize[1])
        else:
            TankImg = [None] * 2
            TankImg[0] = texlib.Texture(unzipDirectory = os.path.abspath(config['tempDir']), textureConfig = config['textureconfig'], textureConfigEncoding = config['textureconfigencoding'], textureStates = config['texturestates'].split(','), textureDirections = config['texturedirections'].split(','))
            TankImg[0].open(os.path.abspath(file))
            TankImg[1] = list(TankImg[0].images['Normal']['Right'][0].size)
            TankImg[1][0] = (SEG_SIZE * 4 + 1) / TankImg[1][0]
            TankImg[1][1] = (SEG_SIZE * 3 + 1) / TankImg[1][1]
        pb['value'] += 7
        pbwindow.update()

        file = config1[tank]['bulletTexture']
        frmt = os.path.splitext(file)[1][1:]
        if frmt not in formats:
            raiseFormatErrorAndExit()
        texlib = formats[frmt]
        if texlib == None:
            BulletImg = PhotoImage(file = file)
            tempSize = (BulletImg.width(), BulletImg.height())
            tempImg = BulletImg.zoom(SEG_SIZE + 1, SEG_SIZE + 1)
            BulletImg = tempImg.subsample(tempSize[0], tempSize[1])
        else:
            BulletImg = [None] * 2
            BulletImg[0] = texlib.Texture(unzipDirectory = os.path.abspath(config['tempDir']), textureConfig = config['textureconfig'], textureConfigEncoding = config['textureconfigencoding'], textureStates = eval(config0['General']['bullettexturestates']), textureDirections = config['texturedirections'].split(','))
            BulletImg[0].open(os.path.abspath(file))
            BulletImg[1] = list(BulletImg[0].images['Normal']['Right'][0].size)
            BulletImg[1][0] = (SEG_SIZE + 1) / BulletImg[1][0]
            BulletImg[1][1] = (SEG_SIZE + 1) / BulletImg[1][1]
        pb['value'] += 6
        pbwindow.update()

        tankTexture = texture(TankImg, SEG_SIZE * 4, SEG_SIZE * 3, config1[tank]['color'])
        bulletTexture = texture(BulletImg, SEG_SIZE * 4, SEG_SIZE * 3, config1[tank]['color'])
    else:
        tankTexture = None
        bulletTexture = config1[tank]['color']
    
    tankControls = {}
    tankShootControls = set()

    is_remote = eval(config1['NetworkPlay']['enabled']) and eval(config1[tank]['is_remote'])
    
    if not is_remote:
        controlList = eval(config1[tank]['controls'])
    else:
        controlList = [[], [], [], [], []]
    
    for i in range(len(controlList)):
        for j in range(len(controlList[i])):
            if i == 0:
                tankControls[controlList[i][j]] = (0, -1)
                tankControls[controlList[i][j].lower()] = (0, -1)
                tankControls[controlList[i][j].upper()] = (0, -1)
            elif i == 1:
                tankControls[controlList[i][j]] = (-1, 0)
                tankControls[controlList[i][j].lower()] = (-1, 0)
                tankControls[controlList[i][j].upper()] = (-1, 0)
            elif i == 2:
                tankControls[controlList[i][j]] = (0, 1)
                tankControls[controlList[i][j].lower()] = (0, 1)
                tankControls[controlList[i][j].upper()] = (0, 1)
            elif i == 3:
                tankControls[controlList[i][j]] = (1, 0)
                tankControls[controlList[i][j].lower()] = (1, 0)
                tankControls[controlList[i][j].upper()] = (1, 0)
            elif i == 4:
                tankShootControls.add(controlList[i][j])
                tankShootControls.add(controlList[i][j].lower())
                tankShootControls.add(controlList[i][j].upper())

    if is_remote:
        for i in range(len(action_list)):
            if i == 0:
                tankControls[gen_tank_move_str(tank, action_list[i])] = (0, -1)
            elif i == 1:
                tankControls[gen_tank_move_str(tank, action_list[i])] = (0, 1)
            elif i == 2:
                tankControls[gen_tank_move_str(tank, action_list[i])] = (-1, 0)
            elif i == 3:
                tankControls[gen_tank_move_str(tank, action_list[i])] = (1, 0)
            elif i == 4:
                tankShootControls.add(gen_tank_move_str(tank, action_list[i]))

    if not eval(config1['General']['newhpbar']):
        hpWidget = c.create_text(*[int(el) * SEG_SIZE for el in config1[tank]['hppos'].replace(' ', '').split(',')], text=int(config1[tank]['hp']), font='Arial ' + str(SEG_SIZE), fill=config1[tank]['color'])
    else:
        hpWidget = None

    bar = Bar(c, eval(config0['General']['barwidth']), eval(config0['General']['hpbarheight']), eval(config0['General']['reloadbarheight']), eval(config0['General']['barborderwidth']), *eval(config0['General']['barpos']), eval(config0['General']['barbackgroundcolor']), eval(config0['General']['hpbarcolor']), eval(config0['General']['reloadbarcolor']), int(config1[tank]['hp']), 1)
    if not eval(config1['General']['newhpbar']):
        bar.update = lambda x = None, y = None: None

    reload = eval(config1[tank]['reload'])

    tankObject = Tank(segments, tankControls, tankShootControls, vector, config1[tank]['team'], int(config1[tank]['hp']), hpWidget, int(config1[tank]['speed']), tankTexture, bulletTexture, config1[tank]['color'], bar, reload)
    tankObject.respawn()

    tankObject.id = tank
    
    tankList.append([tankObject, ''])
    if is_remote:
        tankid_to_index[tank] = len(tankList) - 1
    
    tanks.append([tankObject, hpWidget])

    aiName = config1[tank]['ai']
    if aiName != 'None':
        ai_lib_name, ai_class_name = aiName.split('.')
        ai_lib = __import__(ai_lib_name)
        AI = eval(f'ai_lib.{ai_class_name}')
        ai = AI(tankObject, c, SEG_SIZE, (WIDTH // SEG_SIZE, HEIGHT // SEG_SIZE), WALLS, {tanks[i][0] for i in range(len(tanks))})
        tankList[-1] = [ai, 'AI']


if eval(config1['NetworkPlay']['enabled']):
    rec.rec_init(tankid_to_index, 'Nothing')


tankSet = {tanks[i][0] for i in range(len(tanks))}
for i in range(len(tankList)):
    if tankList[i][1] == 'AI':
        tankList[i][0].tankSet = tankSet.copy()
        tankList[i][0].tankSet.remove(tankList[i][0].tank)

f10m = F10Menu(c, root)

if not eval(config1['General']['animations']):
    Animation = DisabledAnimation

shootAnimation = Animation(config0['General']['shootanimationtextures'], int(config0['General']['shootanimationtexturecount']), eval(config0['General']['shootanimationtexturesegsize']))
startShootAnimation = shootAnimation.start
damageAnimation = Animation(config0['General']['damageanimationtextures'], int(config0['General']['damageanimationtexturecount']), eval(config0['General']['damageanimationtexturesegsize']))
startDamageAnimation = damageAnimation.start
destructionAnimation = Animation(config0['General']['destructionanimationtextures'], int(config0['General']['destructionanimationtexturecount']), eval(config0['General']['destructionanimationtexturesegsize']))
startDestructionAnimation = destructionAnimation.start

lastevent = ''
event1 = ''
event2 = ''
eventsf = set()


if not int(config['bindToWindow']):
    bind_to = c     
else:
    bind_to = root

if eval(config1['NetworkPlay']['enabled']):
    kpc = rec.kpc
    krc = rec.krc
else:
    kpc = KeyPressController
    krc = KeyReleaseController

bind_to.bind('<KeyPress>', kpc)
bind_to.bind('<KeyRelease>', krc)


try:
    root.state('zoomed')
except:
    root.attributes('-zoomed', True)
if displayMode:
    root.attributes('-fullscreen', True)

root.withdraw()


pbwindow.destroy()


#=========================================================================
if eval(config1['NetworkPlay']['enabled']):

    if eval(config1['NetworkPlay']['is_server']):
        server.wait_clients()
        server.start_game_data_exchange()

    else:
        client.ready()
        client.start_game_data_exchange()
#=========================================================================


root.deiconify()
KeyController()
root.mainloop()
