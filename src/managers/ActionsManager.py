from src.utils.librairies import *

class ActionsManager:
    def __init__(self, MouseHandler, InputHandler):
        self.MouseHandler = MouseHandler
        self.InputHandler = InputHandler

        self.Actions = {
            'FlipCell'      : ('m', 'pressed', 1),
            'MultiFlipCell' : ('m', 'held', 3),
            'Up'            : ('k', 'held', pygame.K_z),
            'Down'          : ('k', 'held', pygame.K_s),
            'Left'          : ('k', 'held', pygame.K_q),
            'Right'         : ('k', 'held', pygame.K_d),
            'Pause'         : ('k', 'pressed', pygame.K_SPACE),
            'Step'          : ('k', 'pressed', pygame.K_RIGHT),
            'SpeedUp'       : ('k', 'pressed', pygame.K_UP),
            'SpeedDown'     : ('k', 'pressed', pygame.K_DOWN)
        }
        self.currentActions = {}

    def getAction(self, action):
        if action in self.Actions:
            
            if action not in self.currentActions:
                act = self.checkAction(action)
                self.currentActions[action] = act
                return act
            
            else:
                return self.currentActions[action]
            
        return False
    
    def checkAction(self, action):
        if action in self.Actions:
            device, type, input = self.Actions[action]
            if device == 'm':
                if type == 'pressed':
                    return self.MouseHandler.isClicked(input)
                elif type == 'held':
                    return self.MouseHandler.isHeld(input)
                elif type == 'released':
                    return self.MouseHandler.isReleased(input)

            elif device == 'k':
                if type == 'pressed':
                    return self.InputHandler.isPressed(input)
                elif type == 'held':
                    return self.InputHandler.isHeld(input)
                elif type == 'released':
                    return self.InputHandler.isReleased(input)
        return False
    
    def clear(self):
        self.currentActions.clear()
    

    
    def changeMapping(self, action, device, inputType, input):
        if action not in self.Actions:
            return
        if device not in ('k', 'm'):
            return
        if inputType not in ('held', 'pressed', 'released'):
            return
        
        self.Actions[action] = (device, inputType, input)