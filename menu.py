from ptlib import *

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
        if crashhandler.main('menu.pyw'):
            sys.exit(0)
    except KeyboardInterrupt:
        raise KeyboardInterrupt


PTver = PyTanksVersion
encoding = 'utf-8'
from tkinter import *
from tkinter import font
import os
import ptlib as ptl


try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


cnfprsr = ConfigParser()
config0 = cnfprsr
cnfprsr.read('settings.cfg', encoding = encoding)
config1 = ConfigParser()
config1.read(config0['General']['config'], encoding = encoding)

app_config_section_format = eval(config0[config1['General']['pytanks_application']]['config_section_format'])
ptl.update_config_for_app(config0, app_config_section_format)
ptl.update_config_for_app(config1, app_config_section_format)

config = SectionProxy(cnfprsr, 'General')


colorScheme = int(config1['General']['theme'])


if colorScheme % 2 == 1:
    from tkinter.ttk import *
    try:
        from ttkthemes import ThemedStyle as Style
    except ImportError:
        pass
elif colorScheme == 2:
    import tkinter
    darkStyle = config0['darkColorScheme']
    background = darkStyle['background']
    foreground = darkStyle['foreground']
    def Tk(screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        window = tkinter.Tk(screenName, baseName, className, useTk, sync, use)
        window['background'] = background
        return window
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
                kw['background'] = background
            tkinter.Frame.__init__(self, master, cnf, **kw)


def fplay():
    window.withdraw()
    ptl.run_python_file(config['pytanks'])
    window.deiconify()

def fsettings():
    window.destroy()
    ptl.run_python_file(config0['General']['settings'])
    ptl.run_python_file(config0['General']['menu'], True)
    sys.exit(0)

def fexit():
    window.destroy()
    sys.exit(0)


lngFileName = config1['General']['localization_file']

lang = readLngFile(config['fallbacklng'], 'Menu')
lang.update(readLngFile(lngFileName, 'Menu'))


window = Tk()
window.withdraw()
frame = Frame(master = window)
frame.pack()

currentFont = font.nametofont('TkDefaultFont')

def adaptFonts():
    global frame_winfo_width, frame_winfo_height
    currentFont.configure(size = int(currentFont.actual('size') * min(window.winfo_width() / frame_winfo_width, window.winfo_height() / frame_winfo_height)))
    frame_winfo_width = frame.winfo_width()
    frame_winfo_height = frame.winfo_height()
    window.after(16, adaptFonts)

if colorScheme == 3:
    root = frame
    style = Style(root)
    style.theme_use(config1['General']['ttkthemename'])
    del root

if os.name == 'nt':
    window.iconbitmap(config['icon'])
window.title(lang['title'])
Label(master = frame, text = f'Py Tanks {PyTanksVersion}').grid(row = 0, column = 0, columnspan = 3, padx = 7, pady = (7, 3))
settings = Button(master = frame, text=lang['settingsButton'], command = fsettings)
play = Button(master = frame, text=lang['playButton'], command = fplay)
exitbt = Button(master = frame, text=lang['exitButton'], command = fexit)
settings.grid(row = 1, column = 0, padx = [7, 3], pady = [3, 7])
play.grid(row = 1, column = 1, padx = 3, pady = [3, 7])
exitbt.grid(row = 1, column = 2, padx = [3, 7], pady = [3, 7])
if os.name != 'nt':
    window.resizable(False, False)
window.update()
frame_winfo_width = frame.winfo_width()
frame_winfo_height = frame.winfo_height()
if os.name == 'nt':
    adaptFonts()
window.deiconify()
window.mainloop()
