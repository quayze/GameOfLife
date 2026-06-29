from src.utils.librairies import *

class MouseHandler:
    def __init__(self):
        self.pos = (0, 0)
        self.delta = (0, 0)          
        self.pressed = set()    
        self.released = set()   
        self.held = set()            
        self.scroll = 0


    def clear(self):
        self.pressed.clear()
        self.released.clear()
        self.delta = (0, 0)
        self.scroll = 0
    

    def setPos(self, window_scale_x, window_scale_y, camera):
        mouse_pos_x, mouse_pos_y  = pygame.mouse.get_pos()
        self.pos = (
            mouse_pos_x * window_scale_x + camera.PosX,
            mouse_pos_y * window_scale_y + camera.PosY
        )


    def handleEvents(self, event : pygame.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pressed.add(event.button)
            self.held.add(event.button)

        if event.type == pygame.MOUSEBUTTONUP:
            self.released.add(event.button)
            self.held.discard(event.button)

        if event.type == pygame.MOUSEWHEEL:
            self.scroll = event.y

        if event.type == pygame.MOUSEMOTION:
            self.delta = event.rel

    def isClicked(self, button):
        return button in self.pressed
    
    def isHeld(self, button):
        return button in self.held
    
    def isReleased(self, button):
        return button in self.released
    
    def getScroll(self):
        return self.scroll
    
    def getPosition(self):
        return self.pos
    
    def getGridPosition(self, cellWidth, cellHeight):
        return int(self.pos[0] // cellWidth), int(self.pos[1] // cellHeight)