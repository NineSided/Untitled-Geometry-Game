import math as MATH

import pygame
pygame.init()

def renderEnemies(surface, enemies):
    for enemy in enemies:
        enemy.render(surface)

class SquareEnemy:
    def __init__(self, lives, position, size, rotation, damage, rotationMovement, rotationMovementMultiplier, movementVector, OGvertex1, OGvertex2, OGvertex3, OGvertex4, rotatedVerticies, colour, target):
        self.lives = lives

        self.position = position
        self.size = size
        self.rotation = rotation
        self.damage = damage
        self.rotationMovement = rotationMovement
        self.rotationMovementMultiplier = rotationMovementMultiplier
        self.movementVector = movementVector

        self.OGvertex1 = OGvertex1
        self.OGvertex2 = OGvertex2
        self.OGvertex3 = OGvertex3
        self.OGvertex4 = OGvertex4

        self.rotatedVerticies = rotatedVerticies

        self.colour = colour
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
        targetX, targetY = self.target.pos[0]+self.target.rect.height/2, self.target.pos[1]+self.target.rect.height/2
        rel_x, rel_y = targetX-self.position[0], targetY-self.position[1]

        angle = (180/MATH.pi)*MATH.atan2(rel_y, rel_x)

        moveX = MATH.cos(MATH.radians(angle))*self.rotationMovementMultiplier
        moveY = MATH.sin(MATH.radians(angle))*self.rotationMovementMultiplier

        self.rotationMovement = [moveX, moveY]
        self.rotation = angle

    def rotateVerticies(self):
        self.getRotationToTarget()

        self.vertex1 = self.OGvertex1.rotate(self.rotation)
        self.vertex2 = self.OGvertex2.rotate(self.rotation)
        self.vertex3 = self.OGvertex3.rotate(self.rotation)
        self.vertex4 = self.OGvertex4.rotate(self.rotation)

        self.rotatedVerticies = [self.vertex1, self.vertex2, self.vertex3, self.vertex4]

    def render(self, surface):
        self.createVerticies()
        self.rotateVerticies()

        self.position[0] += self.rotationMovement[0]
        self.position[1] += self.rotationMovement[1]
        self.rotationMovementMultiplier += 0.05

        pygame.gfxdraw.line(surface, int(self.vertex1[0]+self.position[0]), int(self.vertex1[1]+self.position[1]), int(self.vertex2[0]+self.position[0]), int(self.vertex2[1]+self.position[1]), self.colour)
        pygame.gfxdraw.line(surface, int(self.vertex2[0]+self.position[0]), int(self.vertex2[1]+self.position[1]), int(self.vertex4[0]+self.position[0]), int(self.vertex4[1]+self.position[1]), self.colour)
        pygame.gfxdraw.line(surface, int(self.vertex1[0]+self.position[0]), int(self.vertex1[1]+self.position[1]), int(self.vertex3[0]+self.position[0]), int(self.vertex3[1]+self.position[1]), self.colour)
        pygame.gfxdraw.line(surface, int(self.vertex3[0]+self.position[0]), int(self.vertex3[1]+self.position[1]), int(self.vertex4[0]+self.position[0]), int(self.vertex4[1]+self.position[1]), self.colour)

