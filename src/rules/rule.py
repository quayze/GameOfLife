class Rule:
    def __init__(self):
        self.actions = {
            'kill' : 0,
            'spawn' : 1,
            'stay' : 100
        }

    def execute(self, cell, simulation) -> bool:
        return False