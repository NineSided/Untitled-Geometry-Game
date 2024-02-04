import pygame
from pygame import gfxdraw

pygame.init()

class Player:
    def __init__(self, pos, rect, health, respawnTime, dash_pixels):
        self.pos = pos
        self.rect = rect
        self.health = health
        self.respawnTime = respawnTime
        self.dash_pixels = dash_pixels

    def takeHealthAway(self, damager, list_of_damagers):
        if self.health > 0:
            self.health -= damager.damage
        list_of_damagers.remove(damager)

    def bullet_collision(self, bullets_main, rect, damageSquares):
        for bullets in bullets_main:
            for bullet in bullets:
                collide = pygame.Rect.colliderect(rect, bullet.rect)
                if collide == True:
                    square = Square([self.pos[0]+random.randint(0, 8), self.pos[1]+random.randint(0, 8)], 5, 0, [random.randint(-5, 5), random.randint(-5, 5)], None, None, None, None)
                    damageSquares.append(square)
                    self.takeHealthAway(bullet, bullets)

    def render(self, surface, rect):
        gfxdraw.aacircle(surface, int(rect.x+(rect.width/2)), int(rect.y+(rect.height/2)), 8, (0, 255, 0))
        #pygame.draw.rect(surface, (11, 147, 255), rect)

    def move(self, main_inputs, rect, pos, surface):
        speed = 3
        if main_inputs["w"] == True:
            pos[1] -= speed
        if main_inputs["s"] == True:
            pos[1] += speed
        if main_inputs["a"] == True:
            pos[0] -= speed
        if main_inputs["d"] == True:
            pos[0] += speed
        rect.x = player.pos[0]
        rect.y = player.pos[1]