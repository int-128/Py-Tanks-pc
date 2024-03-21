PyTanksVersion = '1.14.1'


from aiinterface import *
from queue import Queue
from random import randint
ai1 = __import__('ai1')
AI1 = ai1.AI1


class AI2(AIClass):

    def _init(self):
        # state list
        self.findingTarget = 0
        self.movingToTarget = 1
        self.shooting = 2
        self.evading = 3
        #
        self.state = self.findingTarget
        self.pathUpdateRate = 15
        self.evadingMoveCnt = 3
        self.evasionDirection = None

    findShootableDirection = AI1.findShootableDirection

    _findPath = AI1._findPath

    findPath = AI1.findPath

    def _findingTargetAction(self):
        self.state = self.findingTarget
        if self.findShootableDirection():
            return self._shootingAction()
        enemyTank = self.tank
        while True:
            if enemyTank.team != self.tank.team:
                if enemyTank.hp <= 0:
                    self.tankSet.remove(enemyTank)
                else:
                    break
            enemyTank = list(self.tankSet)[randint(0, len(self.tankSet) - 1)]
        self.findPath(enemyTank)
        self.pathi = 0
        return self._movingToTargetAction()

    def _movingToTargetAction(self):
        self.state = self.movingToTarget
        if self.findShootableDirection():
            return self._shootingAction()
        if self.pathi < self.pathUpdateRate:
            self.pathi += 1
            return self.path[self.pathi - 1]
        else:
            return self._findingTargetAction()

    def _shootingAction(self):
        self.state = self.shooting
        shootableDirection = self.findShootableDirection()
        if self.getDirection() != shootableDirection:
            return shootableDirection
        self.state = self.evading
        self.cEvadingMoveCnt = self.evadingMoveCnt
        return SHOOT

    def _evadingAction(self):
        self.state = self.evading
        if self.cEvadingMoveCnt <= 0:
            self.evasionDirection = None
            return self._findingTargetAction()
        self.cEvadingMoveCnt -= 1
        if self.evasionDirection != None:
            return self.evasionDirection
        if self.getDirection() in {UP, DOWN}:
            self.evasionDirection = [RIGHT, LEFT][randint(0, 1)]
            return self.evasionDirection
        elif self.getDirection() in {RIGHT, LEFT}:
            self.evasionDirection = [UP, DOWN][randint(0, 1)]
            return self.evasionDirection
        else:
            return self._findingTargetAction()

    def doAction(self):
        if self.state == self.findingTarget:
            action = self._findingTargetAction()
        elif self.state == self.movingToTarget:
            action = self._movingToTargetAction()
        elif self.state == self.shooting:
            action = self._shootingAction()
        elif self.state == self.evading:
            action = self._evadingAction()
        else:
            action = self._findingTargetAction()
        self.move(action)

    def destruction(self):
        self.state = self.findingTarget
