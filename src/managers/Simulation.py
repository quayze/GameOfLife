from src.rules.rule import Rule
from src.rules.live import Live
from src.rules.die import Die
from src.utils.librairies import *

class Simulation:
    def __init__(self):
        self.speed = 1
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

        self.processedCells = set()
        self.StartNextStep()
        
    
    def StartNextStep(self):
        self.UpdatePlacementsDeletions()
        self.lastProcessed = -1
        self.population = len(self.grid)
        self.gridList = list(self.grid.keys())
        self.processedCells.clear()

    def Update(self, dt):
        if not self.run:
            return
        
        diff = self.fixedDeltaTime - self.accumulator
        if dt < diff:
            percentage = dt/diff
            updates = int((self.population - self.lastProcessed) * percentage) + 1
            self.UpdatePartialStep(min(self.population - 1, self.lastProcessed + updates))

        self.accumulator += dt
        while self.accumulator > self.fixedDeltaTime:
            self.UpdatePartialStep(self.population - 1)
            self.StartNextStep()
            self.accumulator -= self.fixedDeltaTime

    def UpdatePartialStep(self, end):
        if end <= self.lastProcessed:
            return
        i = self.lastProcessed
        while i < end:
            i = i + 1
            cx, cy = self.gridList[i]
            for x in range(cx - 1, cx + 2):
                for y in range(cy - 1, cy + 2):
                    self.processCell((x, y))

        self.lastProcessed = i

    def processCell(self, cell):
        if cell in self.processedCells:
            return
        
        self.processedCells.add(cell)
        for rule in self.rules:
            result = rule.execute(cell, self)
            if result == 0:
                self.NextDeleting.add(cell)
            elif result == 1:
                self.NextPlacing.add(cell)

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
        if position not in self.grid : #or not self.grid[position]:
            self.grid[position] = 1
            return True
        
        return False
    
        
    def DeleteSquare(self, position : tuple):
        if position not in self.grid:
            return False
        
        self.grid.pop(position)
        return True
        

    def FlipSquare(self, position : tuple):
        if self.PlaceSquare(position):
            return
        self.DeleteSquare(position)

    def GetActiveCells(self):
        activeCells = set()
        for cell in self.grid.keys():
            activeCells.add(cell)
            for neighborCell in self.getCellNeighbors(cell):
                activeCells.add(neighborCell)
        return activeCells


    def getCellNeighbors(self, position):
        return (
            (position[0] - 1, position[1] - 1), # Topleft
            (position[0] + 1, position[1] + 1), # Bottomright
            (position[0] + 1, position[1] - 1), # Topright
            (position[0] - 1, position[1] + 1), # BottomLeft
            (position[0] - 1, position[1]), # Left
            (position[0] + 1, position[1]), # Right
            (position[0], position[1] - 1), # Top
            (position[0], position[1] + 1), # Bottom
        )
    
    def getAliveNeighbors(self, position):
        neighbors = self.getCellNeighbors(position)
        return [c for c in neighbors if self.isAlive(c)]
    
    def countAliveNeighbors(self, position):
        neighbors = self.getCellNeighbors(position)
        return sum(self.isAlive(c) for c in neighbors)    

    def isAlive(self, position):
        return position in self.grid
        
    def changeSpeed(self, speed):
        if speed != self.speed:
            self.speed = speed
            self.fixedDeltaTime = 1 / self.speed

    def speedUp(self, value):
        self.changeSpeed(self.speed + value)

    def speedDown(self, value):
        self.changeSpeed(max(self.speed - value, 0.01))

    def Pause(self):
        self.run = False

    def Resume(self):
        self.run = True

    def isPaused(self):
        return self.run == False
    
    


