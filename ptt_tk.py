import tkinter as tk
import zipfile as zf
import configparser as cp
import os
import math


class FakeImage:

    def __init__(self, image):
        self.size = (image.width(), image.height())


def hex_color(color):
    hex_color_ = '#'
    for i in range(3):
        hex_color_ += ('0' + hex(color[i])[2:])[-2:]
    return hex_color_


def color_image(master, image, mask, color):
    width = image.width()
    height = image.height()
    colored_image = tk.PhotoImage(master = master, width = width, height = height)
    for x in range(width):
        for y in range(height):
            pixel = image.get(x, y)
            mask_pixel = mask.get(x, y)
            colored_pixel = [0] * len(pixel)
            colored_pixel_transparency = False
            for i in range(len(pixel)):
                if mask_pixel[0] or mask_pixel[1]:
                    colored_pixel[i] = (((color[i] * mask_pixel[0] + pixel[i] * (255 - mask_pixel[0])) // 255) * mask_pixel[0] + (((255 - color[i]) * mask_pixel[1] + pixel[i] * (255 - mask_pixel[1])) // 255) * mask_pixel[1]) // (mask_pixel[0] + mask_pixel[1])
                else:
                    colored_pixel[i] = pixel[i]
                    colored_pixel_transparency = image.transparency_get(x, y)
            colored_image.put(hex_color(colored_pixel), (x, y))
            colored_image.transparency_set(x, y, colored_pixel_transparency)
    return colored_image


def resize_image(image, resize_x, resize_y):
    subsample_args = [image.width(), image.height()]
    zoom_args = [round(image.width() * resize_x), round(image.height() * resize_y)]
    for i in range(2):
        d = math.gcd(zoom_args[i], subsample_args[i])
        zoom_args[i] //= d
        subsample_args[i] //= d
    zoomed_image = image.zoom(*zoom_args)
    resized_image = zoomed_image.subsample(*subsample_args)
    return resized_image


class Texture:

    _init_done = False
    _default_master = None

    def _init_class(self):
        if self._init_done:
            return
        self._init_done = True
        self._default_master = tk.Tk()
        self._default_master.withdraw()
    
    def __init__(self, unzipDirectory=None, textureConfig=None, textureConfigEncoding=None, textureStates=[], textureDirections=[], separation_symbol=','):
        self._init_class()
        self._images = {}
        self.images = {}
        self.tkTexture = {}
        self.unzip_directory = unzipDirectory
        self.texture_config_file_path = textureConfig
        self._texture_config_file_encoding = textureConfigEncoding
        self.texture_states = textureStates
        self.texture_directions = textureDirections
        self.separation_symbol = separation_symbol
        self.image_names = ['image', 'mask']
        self._master = self._default_master
        self._color_args = {}

    @property
    def textureDirections(self):
        return self.texture_directions

    @textureDirections.setter
    def textureDirections(self, texture_directions):
        self.texture_directions = texture_directions

    def _open(self, file):
        zip_file = zf.ZipFile(file)
        zip_file.extractall(self.unzip_directory)
        
        texture_config = cp.ConfigParser()
        texture_config.read(os.path.join(self.unzip_directory, self.texture_config_file_path), encoding = self._texture_config_file_encoding)
        
        for texture_state in self.texture_states:
            self._images[texture_state] = {}
            self.images[texture_state] = {}
            for texture_direction in self.texture_directions:
                self._images[texture_state][texture_direction] = [None, None]
                self.images[texture_state][texture_direction] = [None, None]
                for image_name_i in range(len(self.image_names)):
                    image_name = self.image_names[image_name_i]
                    image_file_path = os.path.join(self.unzip_directory, texture_config[self.separation_symbol.join((texture_state, texture_direction))][image_name])
                    self._images[texture_state][texture_direction][image_name_i] = tk.PhotoImage(master = self._master, file = image_file_path)
                    self.images[texture_state][texture_direction][image_name_i] = FakeImage(self._images[texture_state][texture_direction][image_name_i])
        
        for root_dir, dir_names, file_names in os.walk(self.unzip_directory, topdown = False):
            for file_name in file_names:
                file_path = os.path.join(root_dir, file_name)
                os.remove(file_path)
            for dir_name in dir_names:
                dir_path = os.path.join(root_dir, dir_name)
                os.rmdir(dir_path)

    def open(self, file):
        try:
            self._open(file)
            return 0
        except:
            import traceback
            print(traceback.format_exc())
            return 1

    def _color(self, color, resizeX=1, resizeY=1):
        for texture_state in self.texture_states:
            self.tkTexture[texture_state] = {}
            for texture_direction in self.texture_directions:
                colored_image = color_image(self._master, self._images[texture_state][texture_direction][0], self._images[texture_state][texture_direction][1], color)
                resized_colored_image = resize_image(colored_image, resizeX, resizeY)
                self.tkTexture[texture_state][texture_direction] = resized_colored_image

    def color(self, color, resizeX=1, resizeY=1):
        self._color_args = {'color': color, 'resizeX': resizeX, 'resizeY': resizeY}

    def tkImage(self, master=None):
        self._master = master
        self._color(**self._color_args)

    def __getitem__(self, key):
        try:
            return self.tkTexture[key]
        except:
            return None
