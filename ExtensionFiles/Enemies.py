import math as MATH

import pygame
pygame.init()

class SquareEnemy:
    def __init__(self, position, size, rotation, rotationMovement, movementVector, OGvertex1, OGvertex2, OGvertex3, OGvertex4, target):
        self.position = position
        self.size = size
        self.rotation = rotation
        self.rotationMovement = rotationMovement
        self.movementVector = movementVector

        self.OGvertex1 = OGvertex1
        self.OGvertex2 = OGvertex2
        self.OGvertex3 = OGvertex3
        self.OGvertex4 = OGvertex4

        self.target = target

        self.vertex1 = None
        self.vertex2 = None
        self.vertex3 = None
        self.vertex4 = None

    def destroy(self):
        del self

    def createVerticies(self):
        self.OGvertex1 = pygame.Vector2(int((0-self.size/2)), int((0-self.size/2)))
        self.OGvertex2 = pygame.Vector2(int(self.OGvertex1[0]+self.size),  int(self.OGvertex1[1]))
        self.OGvertex3 = pygame.Vector2(int(self.OGvertex1[0]),            int(self.OGvertex1[1]+self.size))
        self.OGvertex4 = pygame.Vector2(int(self.OGvertex1[0]+self.size),  int(self.OGvertex1[1]+self.size))


    def getRotationToTarget(self):
        targetX, targetY = self.target.pos[0]+8, self.target.pos[1]+8
        rel_x, rel_y = targetX-self.position[0], targetY-self.position[1]

        angle = (180/MATH.pi)*MATH.atan2(rel_y, rel_x)

        moveX = MATH.cos(MATH.radians(angle))*2
        moveY = MATH.sin(MATH.radians(angle))*2

        self.rotationMovement = [moveX, moveY]
        self.rotation = angle

    def rotateVerticies(self):
        self.getRotationToTarget()

        self.vertex1 = self.OGvertex1.rotate(self.rotation)
        self.vertex2 = self.OGvertex2.rotate(self.rotation)
        self.vertex3 = self.OGvertex3.rotate(self.rotation)
        self.vertex4 = self.OGvertex4.rotate(self.rotation)

    def render(self, surface):
        self.createVerticies()
        self.rotateVerticies()

        self.position[0] += self.rotationMovement[0]
        self.position[1] += self.rotationMovement[1]

        pygame.gfxdraw.line(surface, int(self.vertex1[0]+self.position[0]), int(self.vertex1[1]+self.position[1]), int(self.vertex2[0]+self.position[0]), int(self.vertex2[1]+self.position[1]), (255,187,51))
        pygame.gfxdraw.line(surface, int(self.vertex2[0]+self.position[0]), int(self.vertex2[1]+self.position[1]), int(self.vertex4[0]+self.position[0]), int(self.vertex4[1]+self.position[1]), (255,187,51))
        pygame.gfxdraw.line(surface, int(self.vertex1[0]+self.position[0]), int(self.vertex1[1]+self.position[1]), int(self.vertex3[0]+self.position[0]), int(self.vertex3[1]+self.position[1]), (255,187,51))
        pygame.gfxdraw.line(surface, int(self.vertex3[0]+self.position[0]), int(self.vertex3[1]+self.position[1]), int(self.vertex4[0]+self.position[0]), int(self.vertex4[1]+self.position[1]), (255,187,51))

