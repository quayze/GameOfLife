from src.rules.rule import *

class Die(Rule):
    def __init__(self):
        super().__init__()

    def execute(self, cell, simulation):
        numAlive = len(simulation.getAliveNeighbors(cell))
        if numAlive < 2 or numAlive > 3:
            return self.actions['kill']
        return self.actions['stay']