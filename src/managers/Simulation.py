from src.rules.rule import Rule
from src.rules.live import Live
from src.rules.die import Die

class Simulation:
    def __init__(self):
        self.speed = 10
        self.fixedDeltaTime = 1 / self.speed
        self.accumulator = 0
        self.run = False

        self.grid = {}
        self.rules : list[Rule] = [
            Live(),
            Die(),
        ]

        self.NextPlacing = set()
        self.NextDeleting = set()

    def Update(self, dt):
        if not self.run:
            return
        
        self.accumulator += dt
        while self.accumulator > self.fixedDeltaTime:
            self.UpdateSimulationStep()
            self.accumulator -= self.fixedDeltaTime


    def UpdateSimulationStep(self):
        activeCells = self.GetActiveCells()
        for cell in activeCells:
            for rule in self.rules:
                result = rule.execute(cell, self)
                if result == 0:
                    self.NextDeleting.add(cell)
                elif result == 1:
                    self.NextPlacing.add(cell)
        self.UpdatePlacementsDeletions()

    def UpdatePlacementsDeletions(self):
        for killedSquare in self.NextDeleting:
            self.DeleteSquare(killedSquare)
        for newSquare in self.NextPlacing:
            self.PlaceSquare(newSquare)

        self.NextDeleting.clear()
        self.NextPlacing.clear()
    
    
    def PlaceSquare(self, position : tuple):
        if position not in self.grid:
            self.grid[position] = 1

            return True
        
        if not self.grid[position]:
            self.grid[position] = 1

            return True
        
        return False
    
        
    def DeleteSquare(self, position : tuple):
        if position not in self.grid:
            return False
        
        if self.grid[position]:
            self.grid.pop(position)
            return True
        
        return False
        

    def FlipSquare(self, position : tuple):
        if self.PlaceSquare(position):
            return
        self.DeleteSquare(position)

    def GetActiveCells(self):
        activeCells = set()
        for cell, alive in self.grid.items():
            if not alive:
                continue
            activeCells.add(cell)
            for neighborCell in self.getCellNeighbors(cell):
                activeCells.add(neighborCell)
        return activeCells


    def getCellNeighbors(self, position):
        neighbors = [
            (position[0] - 1, position[1] - 1), # Topleft
            (position[0] + 1, position[1] + 1), # Bottomright
            (position[0] + 1, position[1] - 1), # Topright
            (position[0] - 1, position[1] + 1), # BottomLeft
            (position[0] - 1, position[1]), # Left
            (position[0] + 1, position[1]), # Right
            (position[0], position[1] - 1), # Top
            (position[0], position[1] + 1), # Bottom
            ]
        return neighbors
    
    def getAliveNeighbors(self, position):
        neighbors = self.getCellNeighbors(position)
        return [c for c in neighbors if self.isAlive(c)]
        

    def isAlive(self, position):
        if position in self.grid:
            return self.grid[position] != 0
        return False
        
    def changeSpeed(self, speed):
        if speed != self.speed:
            self.speed = speed
            self.fixedDeltaTime = 1 / self.speed

    def speedUp(self, value):
        self.changeSpeed(self.speed + value)

    def speedDown(self, value):
        self.changeSpeed(max(self.speed - value, 0.1))

    def Pause(self):
        self.run = False

    def Resume(self):
        self.run = True

    def isPaused(self):
        return self.run == False
    
"""
cells = {
(0, 1) : 0, (4, 1) : 1, (1, 1) : 1, (0, 2) : 1,
(0, 8) : 1, (8, 7) : 0, (14, 5) : 1, (0, 0) : 1
(1, 7) : 1, (9, 11) : 1, (0, 4) : 1, (3, 3) : 0
}
dyingGrid = {
(0, 1) : 0, (4, 1) : 3, (1, 1) : 3, (0, 2) : 3,
(0, 8) : 3, (8, 7) : 2, (14, 5) : 3, (0, 0) : 3
(1, 7) : 3, (9, 11) : 3, (0, 4) : 3, (3, 3) : 1
}


"""