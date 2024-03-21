PyTanksVersion = '1.15.0'

import sys
import traceback
import tkinter.messagebox
import os.path

def displayError(traceBack):
    tkinter.messagebox.showerror('Traceback', traceBack)       

def main(pythonProgramFileName):

    if not os.path.exists(pythonProgramFileName):
        return False

    traceBack = traceback.format_exc()
        
    try:
        __import__(pythonProgramFileName)
    except SystemExit:
        if int(sys.exc_info()[1].__str__()) != 0:
            traceBack = traceback.format_exc()
    except Exception:
        traceBack = traceback.format_exc()
        
    if traceBack != traceback.format_exc():
        index1 = traceBack.find('\n') + 1
        index2 = traceBack.find('\n', index1) + 1
        index3 = traceBack.find('\n', index2) + 1
        traceBack = traceBack[:index1] + traceBack[index3:]
        traceBack = traceBack.replace('<string>', os.path.abspath(pythonProgramFileName))
        displayError(traceBack)

    return True
