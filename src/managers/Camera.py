from src.utils.librairies import *
from src.utils.settings import *

class Camera:
    def __init__(self, 
                 width,
                 height,
                 simulation, 
                 zoom, 
                 position, 
                 mouseHandler):

        self.PosX, self.PosY = position
        self.halfWidth = width / 2
        self.halfHeight = height / 2
        self.velX = 0
        self.velY = 0
        self.zoom = zoom
        self.sim = simulation
        self.mouse = mouseHandler
    

    def Render(self, screen):
        for cell, alive in self.sim.grid.items():
            if alive:
                pygame.draw.polygon(
                    screen,
                    (255, 255, 255),
                    [
                        (cell[0] * self.zoom - self.PosX, 
                        cell[1] * self.zoom  - self.PosY),             # Topleft

                        (cell[0] * self.zoom + self.zoom  - self.PosX, 
                        cell[1] * self.zoom  - self.PosY),             # Topright

                        (cell[0] * self.zoom + self.zoom - self.PosX, 
                        cell[1] * self.zoom + self.zoom  - self.PosY), # Bottomright

                        (cell[0] * self.zoom - self.PosX, 
                        cell[1] * self.zoom + self.zoom - self.PosY)  # Bottomleft
                    ]
                )
        self.DrawMouse(screen)
        
    def DrawMouse(self, screen):
        mouseCellPos = self.mouse.getGridPosition(self.zoom, self.zoom)
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (mouseCellPos[0] * self.zoom - self.PosX, 
            mouseCellPos[1] * self.zoom - GRID_OFFSET * self.zoom - self.PosY), # Topleft
            (mouseCellPos[0] * self.zoom - self.PosX, 
            mouseCellPos[1] * self.zoom + (GRID_OFFSET + 1) * self.zoom - self.PosY), # Bottomleft
            4
        )
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (mouseCellPos[0] * self.zoom + self.zoom - self.PosX, 
            mouseCellPos[1] * self.zoom - GRID_OFFSET * self.zoom - self.PosY), # Topright
            (mouseCellPos[0] * self.zoom + self.zoom - self.PosX, 
            mouseCellPos[1] * self.zoom + (GRID_OFFSET + 1) * self.zoom - self.PosY), # Bottomright
            4
        )
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (mouseCellPos[0] * self.zoom - GRID_OFFSET * self.zoom - self.PosX, 
            mouseCellPos[1] * self.zoom - self.PosY), # Topleft
            (mouseCellPos[0] * self.zoom + (GRID_OFFSET + 1) * self.zoom - self.PosX, 
            mouseCellPos[1] * self.zoom - self.PosY), # Topright
            4 
        )
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (mouseCellPos[0] * self.zoom - GRID_OFFSET * self.zoom - self.PosX, 
            mouseCellPos[1] * self.zoom + self.zoom - self.PosY), # Bottomleft
            (mouseCellPos[0] * self.zoom + (GRID_OFFSET + 1) * self.zoom - self.PosX, 
            mouseCellPos[1] * self.zoom + self.zoom - self.PosY), # Bottomright
            4
        )

    def Update(self, dt):
        if self.velX:
            self.PosX += self.velX * dt
            self.velX = 0

        if self.velY:
            self.PosY += self.velY * dt
            self.velY = 0
    
    def Move(self, direction : tuple | V2, speed : float):
        vector = V2(direction)
        if vector.length() != 0: vector.normalize()
        self.velX = vector.x * speed
        self.velY = vector.y * speed

    def Zoom(self, newZoom):
        if newZoom < CameraSettings.MINZOOM or newZoom > CameraSettings.MAXZOOM: 
            return
        diff = newZoom - self.zoom
        if diff == 0:
            return
        self.PosX += (self.PosX + self.halfWidth) / (self.zoom * (1/diff))
        self.PosY += (self.PosY + self.halfHeight) / (self.zoom * (1/diff))
        self.zoom = newZoom

    def getZoom(self):
        return self.zoom

    def AddZoom(self, value):
        self.Zoom(self.zoom + value)

    def getCenter(self):
        return self.PosX + self.halfWidth, self.PosY + self.halfHeight
