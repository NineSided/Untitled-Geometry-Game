import pygame
from pygame import gfxdraw

pygame.init()

class CircleBossBullet:
    def __init__(self, lives, rect, movementPos, direction, damage, colour):
        self.lives = lives

        self.rect = rect
        self.movementPos = movementPos
        self.direction = direction
        self.damage = damage

        self.colour = colour

    def destroy(self):
        del self

    def render(self, surface, Spawnpos, radius, thickness):
        pos = [Spawnpos[0] + self.movementPos[0], Spawnpos[1] + self.movementPos[1]]
        bullet_rect = pygame.Rect(pos[0], pos[1], radius+7, radius+7)
        #pygame.draw.rect(surface, (255, 0, 0), bullet_rect)
        gfxdraw.aacircle(surface, int(bullet_rect.x+(bullet_rect.width/2)), int(bullet_rect.y+(bullet_rect.width/2)), radius, self.colour)

        return bullet_rect

    def move(self):
        self.movementPos[0] += self.direction[1]
        self.movementPos[1] += self.direction[0]