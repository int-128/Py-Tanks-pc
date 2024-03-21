PyTanksVersion = '1.14.1'


from aiinterface import *
from queue import Queue
from random import randint


class AI1(AIClass):

    def _init(self):
        self.actionQueue = Queue()

    def findShootableDirection(self):
        x, y = self.getPosition()
        mnx = x - self.segmentSize
        mny = y - self.segmentSize
        mxx = x + self.segmentSize
        mxy = y + self.segmentSize
        for tank in self.tankSet:
            if self.tank.team == tank.team:
                continue
            if tank.hp <= 0:
                self.tankSet.remove(tank)
                continue
            xi, yi = self.getPosition(tank)
            if mnx <= xi <= mxx:
                if y < yi:
                    for yw in self.wallsX[x]:
                        if y < yw < yi:
                            return None
                    return DOWN
                else:
                    for yw in self.wallsX[x]:
                        if yi < yw < y:
                            return None
                    return UP
            if mny <= yi <= mxy:
                if x < xi:
                    for xw in self.wallsY[y]:
                        if x < xw < xi:
                            return None
                    return RIGHT
                else:
                    for xw in self.wallsY[y]:
                        if xi < xw < x:
                            return None
                    return LEFT
        return None

    def _findPath(self, x, y, ex, ey):
        if x == ex and y == ey:
            self.path = self._path[1:]
            return True
        if x < 1 or y < 1 or x >= self.fieldSize[0] - 1 or y >= self.fieldSize[0] - 1:
            return False
        for wx in (x - 2, x, x + 2):
            for wy in (y - 2, y, y + 2):
                if self.walls[wy][wx]:
                    return False
        _directions = self._directions
        self._directions = [el[1] for el in sorted([[x - ex, LEFT], [ex - x, RIGHT], [y - ey, UP], [ey - y, DOWN]], reverse = True)]
        for direction in self._directions:
            if direction[0] == -self._path[-1][0] and direction[1] == -self._path[-1][1]:
                continue
            self._path.append(direction)
            if self._findPath(x + direction[0], y + direction[1], ex, ey):
                return True
            self._path.pop()
        self._directions = _directions

    def findPath(self, enemyTank):
        sx, sy = [el // self.segmentSize for el in self.getPosition()]
        ex, ey = [el // self.segmentSize for el in self.getPosition(enemyTank)]
        self._directions = [el[1] for el in sorted([[sx - ex, LEFT], [ex - sx, RIGHT], [sy - ey, UP], [ey - sy, DOWN]], reverse = True)]
        self.path = []
        self._path = [(0, 0)]
        self._findPath(sx, sy, ex, ey)

    def doAction(self):
        shootableDirection = self.findShootableDirection()
        if shootableDirection:
            self.actionQueue.queue.clear()
            if self.getDirection() != shootableDirection:
                self.actionQueue.put(shootableDirection)
            self.actionQueue.put(SHOOT)

        if not self.actionQueue.empty():
            self.move(self.actionQueue.get())
            return

        enemyTank = self.tank
        while True:
            if enemyTank.team != self.tank.team:
                if enemyTank.hp <= 0:
                    self.tankSet.remove(enemyTank)
                else:
                    break
            enemyTank = list(self.tankSet)[randint(0, len(self.tankSet) - 1)]
        self.findPath(enemyTank)
        for el in self.path:
            self.actionQueue.put(el)

        if not self.actionQueue.empty():
            self.move(self.actionQueue.get())

    def destruction(self):
        self.actionQueue.queue.clear()
