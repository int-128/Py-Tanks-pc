import pygame


default_button_resource = {
    'image': pg.image.fromstring(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffiii\xff\xff\xff\xe3\xe3\xe3\xe3\xe3\xe3\xa0\xa0\xa0iii\xff\xff\xff\xe3\xe3\xe3\xf0\xf0\xf0\xa0\xa0\xa0iii\xff\xff\xff\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0iiiiiiiiiiiiiiiiii', (5, 5), 'RGB'),
    'sizing_margins': (2, 2, 2, 2),
    'content_margins': (3, 4, 6, 7)
    }


class Button:

    def __init__(self, resource=default_button_resource):
        pass
