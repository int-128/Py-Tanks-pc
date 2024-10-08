version = '1.0.1'
py_tanks_version = '1.15.0'


import aiinterface as aii
import random as rnd
ai2 = __import__('ai2')


def random_move():
    return [aii.UP, aii.DOWN, aii.LEFT, aii.RIGHT][rnd.randint(0, 3)]


class AI2_1(ai2.AI2):

    def _init(self):
        super()._init()
        self.pathUpdateRate = 25
        self._moved = True
        self._coords = self.getPosition()

    def doAction(self):
        coords = self.getPosition()
        if coords == self._coords:
            if self._moved:
                self._moved = False
            else:
                self.move(random_move())
                return
        else:
            self._moved = True
        self._coords = coords
        super().doAction()
