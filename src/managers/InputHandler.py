from src.utils.librairies import *

class InputHandler:
    def __init__(self):
        self.held = set()
        self.pressed = set()
        self.released = set()

    def clear(self):
        self.pressed.clear()
        self.released.clear()

    def handleEvents(self, event : pygame.Event):
        if event.type == pygame.KEYDOWN:
            if event.key not in self.held:
                self.pressed.add(event.key) 
            self.held.add(event.key)

        if event.type == pygame.KEYUP:
            self.released.add(event.key)
            self.held.discard(event.key)


    def isPressed(self, key):
        return key in self.pressed

    def isHeld(self, key):
        return key in self.held
    
    def isReleased(self, key):
        return key in self.released
