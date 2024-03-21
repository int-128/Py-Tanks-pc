PyTanksVersion = '1.14.1'


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
SHOOT = True

aiTankMapping = {UP: UP, DOWN: DOWN, LEFT: LEFT, RIGHT: RIGHT}
aiTankFireMapping = {SHOOT}

class AIClass:

    def __init__(self, tank, canvas, segmentSize, fieldSize, walls, tankSet):
        tank.ai = self
        
        self.tank = tank
        self.canvas = canvas
        self.segmentSize = segmentSize
        self.fieldSize = fieldSize
        tankSet.remove(tank)
        self.walls = walls
        self.tankSet = tankSet

        self.wallsY = {}
        for i in range(len(walls)):
            self.wallsY[i * self.segmentSize] = []
            for j in range(len(walls[i])):
                if walls[i][j]:
                    self.wallsY[i * self.segmentSize].append(j * self.segmentSize)

        self.wallsX = {}
        for j in range(len(walls[i])):
            self.wallsX[j * self.segmentSize] = []
            for i in range(len(walls)):
                if walls[i][j]:
                    self.wallsX[j * self.segmentSize].append(i * self.segmentSize)
        
        self.tank.mapping = aiTankMapping
        self.tank.fireMapping = aiTankFireMapping

        self._init()

        self.mapping = {}
        self.fireMapping = {}

    def _init(self): pass

    def getPosition(self, tank=None):
        # Returns position of the central segment
        if tank == None:
            tank = self.tank
        return [int(el) for el in self.canvas.coords(tank.segments[4].instance)[:2]]

    def getDirection(self, tank=None):
        if tank == None:
            tank = self.tank
        return tank.vector

    def _move(self, direction):
        self.tank.move(direction)

    def move(self, direction = None):
        if not direction:
            direction = self.getDirection()
        self._move(direction)

    def shoot(self):
        self._move(SHOOT)

    def moveUp(self):
        self._move(UP)

    def moveDown(self):
        self._move(DOWN)

    def moveLeft(self):
        self._move(LEFT)

    def moveRight(self):
        self._move(RIGHT)

    def doAction(self): pass
