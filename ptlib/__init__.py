import sys
from configparser import ConfigParser, SectionProxy
import os
import subprocess as sp
from .py_tanks_version import *
from .tkinter_text_colors import *


PyTanksVersion = '.'.join((str(n) for n in PY_TANKS_VERSION))
tkinter_text_colors = TKINTER_TEXT_COLORS


def readPtmFile(mapName, SEG_SIZE = 0, c = None, WallSegment = None, WALL_COLOR = '', UseUnstdTex = False, WallImg = None, pbwindow = None, pb = None, mbppbp = 0, pr = 0, fastread = False):
    WALLS = []
    Map = open(mapName)
    index = 0
    cnv = c
    for string in Map:
        jndex = 0
        WALLS.append([])
        for char in string:
            if char == 'X':
                WALLS[-1].append(True)
                x = jndex * SEG_SIZE
                y = index * SEG_SIZE
                if WallSegment != None:
                    WallSegment(cnv, x, y, WALL_COLOR)
                if UseUnstdTex:
                    c.create_image(x, y, anchor='nw',image=WallImg)
            else:
                WALLS[-1].append(False)
            jndex += 1
        if fastread:
            jndex = 2000
        while jndex < 2000:
            WALLS[-1].append(False)
            jndex += 1
        if pb != None:
            if index * 2000 + jndex >= pr * mbppbp:
                pb['value'] += 1
                pbwindow.update()
                pr += 1
        index += 1
    if fastread:
        index = 1500
    while index < 1500:
        jndex = 0
        WALLS.append([])
        while jndex < 2000:
            WALLS[-1].append(False)
            jndex += 1
        if pb != None:
            if index * 2000 + jndex >= pr * mbppbp:
                pb['value'] += 1
                pbwindow.update()
                pr += 1
        index += 1
    Map.close()
    return WALLS


def readLngFile(lngFileName, moduleName):
    obi = lngFileName.find('[')
    cbi = lngFileName.find(']')
    if obi < cbi and obi != -1 and cbi != -1:
        enc = lngFileName[obi+1:cbi]
    else:
        enc = 'utf-8'

    lng = open(lngFileName, encoding = enc)
    cur = lng.readline()
    while bool(cur) and cur.rstrip('\n').strip(' ') != f'[{moduleName}]':
        cur = lng.readline()
    cur = lng.readline()
    lang = {}
    while bool(cur) and cur.strip(' ')[0] != '[':
        if cur.rstrip('\n').strip(' '):
            pair = cur.rstrip('\n').strip(' ').split('=')
            lang[pair[0]] = pair[1].strip('"')
        cur = lng.readline()
    lng.close()
    return lang


def PhotoImage_transparency_get(self, x, y):
    """Return True if the pixel at x,y is transparent."""
    return self.tk.getboolean(self.tk.call(self.name, 'transparency', 'get', x, y))

def PhotoImage_transparency_set(self, x, y, boolean):
    """Set the transparency of the pixel at x,y."""
    self.tk.call(self.name, 'transparency', 'set', x, y, boolean)


def tkinter_color_to_rgb(color):
    if color == '':
        return (0, 0, 0, 0)
    if color in tkinter_text_colors:
        return (*tkinter_text_colors[color], 255)
    try:
        if len(color) == 4:
            return (*[int(color[i + 1] * 2, 16) for i in range(3)], 255)
        elif len(color) == 7:
            return (*[int(color[i * 2 + 1 : i * 2 + 3], 16) for i in range(3)], 255)
        elif len(color) == 10:
            return (*[int(color[i * 3 + 1 : i * 3 + 3], 16) for i in range(3)], 255)
    except:
        pass
    raise ValueError(f'"{color}" is not a valid color')


def update_config_for_app(config, section_name_format):
    for section in config:
        app_section = section_name_format.format(section)
        if app_section in config:
            for key in config[app_section]:
                config[section][key] = config[app_section][key]


def _run_python_file(interpreter, file_path):
    return sp.run((interpreter, file_path))

if os.name == 'nt':
    def run_python_file(file_path):
        return _run_python_file('pythonw', file_path)
else:
    def run_python_file(file_path):
        return _run_python_file('python3', file_path)
