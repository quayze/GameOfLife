from src.utils.functions import *

class InfoMenu:
    def __init__(self, simulation):
        self.sim = simulation


    def Draw(self, screen):
        drawText(screen, f'UPDATES PER SECOND : {self.sim.speed}', 20, (20, 20), alignment= 'topleft')
        drawText(screen, f'PAUSED : {not self.sim.run}', 20, (20, 40), alignment= 'topleft')
        drawText(screen, f'POPULATION : {len(self.sim.grid)}', 20, (20, 60), alignment= 'topleft')
        drawText(screen, f'SNAPSHOT POPULATION : {self.sim.population}', 20, (20, 80), alignment= 'topleft')
        drawText(screen, f'ESTIMATD CELLS : {self.sim.population * 10}', 20, (20, 100), alignment= 'topleft')
        drawText(screen, f'PROCESSED SQUARES : {self.sim.lastProcessed}', 20, (20, 120), alignment= 'topleft')
        drawText(screen, f'PROCESSED CELLS : {len(self.sim.processedCells)}', 20, (20, 140), alignment= 'topleft')