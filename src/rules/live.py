from src.rules.rule import *

class Live(Rule):
    def __init__(self):
        super().__init__()

    def execute(self, cell, simulation):
        numAlive = len(simulation.getAliveNeighbors(cell))
        if numAlive == 3:
            return self.actions['spawn']
        return self.actions['stay']