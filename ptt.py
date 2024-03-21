PyTanksVersion = '1.15.0'

from PIL import Image, ImageTk
from zipfile import ZipFile
from configparser import ConfigParser
import os
from queue import Queue
separationSymbol = ','
imageMode = 'RGBA'
maskMode = 'RGB'
maxColorValue = 255

if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

class Texture:
    def __init__(self, unzipDirectory = None, textureConfig = None, textureConfigEncoding = None, textureStates = [], textureDirections = []):
        self.images = {}
        self.texture = {}
        self.tkTexture = {}
        self.unzipDirectory = unzipDirectory
        self.textureConfig = textureConfig
        self.textureStates = textureStates
        self.textureDirections = textureDirections

    def open(self, file):
        code = 0
        try:
            ZipFile(file).extractall(self.unzipDirectory)
        except:
            code = 1
        try:
            textureConfig = ConfigParser()
            textureConfig.read(os.path.join(self.unzipDirectory, self.textureConfig))
            for textureState in self.textureStates:
                self.images[textureState] = {}
                for textureDirection in self.textureDirections:
                    self.images[textureState][textureDirection] = [None, None]
                    self.images[textureState][textureDirection][0] = Image.open(os.path.join(self.unzipDirectory, textureConfig[textureState + separationSymbol + textureDirection]['image'])).convert(imageMode)
                    self.images[textureState][textureDirection][1] = Image.open(os.path.join(self.unzipDirectory, textureConfig[textureState + separationSymbol + textureDirection]['mask'])).convert(maskMode)
        except:
            code = 2
        queue = Queue()
        dirList = []
        queue.put(self.unzipDirectory)
        while not queue.empty():
            dirPath = queue.get()
            for item in os.listdir(dirPath):
                itemPath = os.path.join(dirPath, item)
                if os.path.isdir(itemPath):
                    queue.put(itemPath)
                    dirList.append(itemPath)
                else:
                    os.remove(itemPath)
        for item in dirList[::-1]:
            os.rmdir(item)
        return code

    def color(self, color, resizeX = 1, resizeY = 1):
        code = 0
        try:
            for textureState in self.textureStates:
                self.texture[textureState] = {}
                for textureDirection in self.textureDirections:
                    self.texture[textureState][textureDirection] = Image.new(imageMode, self.images[textureState][textureDirection][0].size)
                    size = self.texture[textureState][textureDirection].size
                    for x in range(size[0]):
                        for y in range(size[1]):
                            imagePixel = self.images[textureState][textureDirection][0].getpixel((x, y))
                            maskPixel = self.images[textureState][textureDirection][1].getpixel((x, y))
                            pixel = [None] * len(imagePixel)
                            for i in range(len(pixel) - 1):
                                if maskPixel[0] or maskPixel[1]:
                                    pixel[i] = (((color[i] * maskPixel[0] + imagePixel[i] * (maxColorValue - maskPixel[0])) // maxColorValue) * maskPixel[0] + (((maxColorValue - color[i]) * maskPixel[1] + imagePixel[i] * (maxColorValue - maskPixel[1])) // maxColorValue) * maskPixel[1]) // (maskPixel[0] + maskPixel[1])
                                else:
                                    pixel[i] = imagePixel[i]
                            i += 1
                            pixel[i] = (color[i] * maskPixel[0] + imagePixel[i] * (maxColorValue - maskPixel[0])) // maxColorValue
                            self.texture[textureState][textureDirection].putpixel((x, y), tuple(pixel))
                    self.texture[textureState][textureDirection] = self.texture[textureState][textureDirection].resize((round(size[0] * resizeX), round(size[1] * resizeY)), Image.ANTIALIAS)
        except:
            code = 1
        return code

    def tkImage(self, master = None):
        code = 0
        try:
            for textureState in self.textureStates:
                self.tkTexture[textureState] = {}
                for textureDirection in self.textureDirections:
                    self.tkTexture[textureState][textureDirection] = ImageTk.PhotoImage(master = master, image = self.texture[textureState][textureDirection])
        except:
            code = 1
        return code

    def __getitem__(self, key):
        try:
            return self.tkTexture[key]
        except:
            return None
