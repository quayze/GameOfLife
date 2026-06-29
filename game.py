import pygame, sys, random
from src.utils.settings import *
from src.managers.Simulation import Simulation
from src.managers.MouseHandler import MouseHandler
from src.managers.InputHandler import InputHandler
from src.managers.ActionsManager import ActionsManager
from src.managers.Camera import Camera

class Game:

    def __init__(self):
        pygame.init()

        self.display = pygame.display.set_mode((1600, 900))
        self.screen  = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.clock   = pygame.time.Clock()
        self.mixer   = pygame.mixer
        self.FPS     = 300

        self.simulation = Simulation()
        self.mouseHandler = MouseHandler()
        self.inputHandler = InputHandler()
        self.actionsManager = ActionsManager(self.mouseHandler, self.inputHandler)
        self.camera = Camera(WIDTH, HEIGHT, self.simulation, 1, (0, 0), self.mouseHandler)
        




        
    def run(self):

        self.startTime = pygame.time.get_ticks()

        while True:
            self.clock.tick(self.FPS)
            self.deltaTime = (pygame.time.get_ticks() - self.startTime)/1000
            self.startTime = pygame.time.get_ticks()

            self.display.fill((0, 0, 0))
            self.screen.fill((0, 0, 0, 0))           

            window_width, window_height = self.display.get_size()
            window_height = (self.display.get_width()*HEIGHT)/ WIDTH

            scale_x, scale_y = WIDTH/window_width, HEIGHT/window_height

            self.actionsManager.clear()
            self.inputHandler.clear()
            self.mouseHandler.clear()
            self.mouseHandler.setPos(scale_x, scale_y, self.camera)
            for event in pygame.event.get():
                self.mouseHandler.handleEvents(event)
                self.inputHandler.handleEvents(event)

                if event.type == pygame.QUIT:
                    self.quit() 
                
            

            self.HandleActions()


            self.simulation.Update(self.deltaTime)
            self.camera.Update(self.deltaTime)
            self.camera.Render(self.screen)
                
                

        
            resized_screen = pygame.transform.scale(self.screen, (window_width, window_height))
            self.display.blit(resized_screen, (0, 0))
            pygame.display.set_caption(str(int(self.clock.get_fps())) + ' ' + 'SIM UPDATES : ' + str(self.simulation.speed) + ' ' + str(self.camera.zoom) + ' ' + str((self.camera.PosX, self.camera.PosY)))
            pygame.display.flip()




    def HandleActions(self):
        if self.actionsManager.getAction('FlipCell'):
            self.simulation.FlipSquare(self.mouseHandler.getGridPosition(self.camera.zoom, self.camera.zoom))

        if self.actionsManager.getAction('MultiFlipCell'):
            self.simulation.FlipSquare(self.mouseHandler.getGridPosition(self.camera.zoom, self.camera.zoom))

        if self.actionsManager.getAction('SpeedUp'):
            self.simulation.speedUp(1)

        if self.actionsManager.getAction('SpeedDown'):
            self.simulation.speedDown(1)

        if self.actionsManager.getAction('Pause'):
            if self.simulation.isPaused():
                self.simulation.Resume()
            else:
                self.simulation.Pause()

        scroll = self.mouseHandler.getScroll()
        if scroll > 0:  
            self.camera.Zoom(self.camera.getZoom() * 2 * scroll)
        elif scroll < 0:
            self.camera.AddZoom(self.camera.getZoom() / (2 * scroll))


        movX = 0
        movY = 0
        if self.actionsManager.getAction('Up'):
            movY -= 1
        if self.actionsManager.getAction('Left'):
            movX -= 1
        if self.actionsManager.getAction('Down'):
            movY += 1
        if self.actionsManager.getAction('Right'):
            movX += 1
        self.camera.Move((movX, movY), 1000)









    def get_fps(self):
        return self.clock.get_fps()




    def quit(self):
        pygame.quit()
        sys.exit()


        

if __name__ == '__main__':
    game = Game()
    game.run()


