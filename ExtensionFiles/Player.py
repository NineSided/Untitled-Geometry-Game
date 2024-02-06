import random
import math as MATH

import pygame
from pygame import gfxdraw

pygame.init()

class Player:
    def __init__(self, pos, rect, health, respawnTime, diameter):
        self.pos = pos
        self.rect = rect
        self.health = health
        self.respawnTime = respawnTime

        self.diameter = diameter
        self.radius = diameter/2

    def takeHealthAway(self, damager, list_of_damagers):
        if self.health > 0:
            self.health -= damager.damage
        list_of_damagers.remove(damager)

    def bullet_collision(self, bullets_main, rect, damageSquares, squareClass):
        for bullets in bullets_main:
            for bullet in bullets:
                collide = pygame.Rect.colliderect(rect, bullet.rect)
                if collide == True:
                    square = squareClass([self.pos[0]+random.randint(0, 8), self.pos[1]+random.randint(0, 8)], 5, 0, [random.randint(-5, 5), random.randint(-5, 5)], None, None, None, None)
                    damageSquares.append(square)
                    self.takeHealthAway(bullet, bullets)

    def enemyCollision(self, surface, enemy):
        collidepoints = []
        rect = self.rect
        for i in range(len(enemy.rotatedVerticies)):
            point = ((int(enemy.rotatedVerticies[0][0]), 
                      int(enemy.rotatedVerticies[0][1])))
            enemyMiddle = (int((enemy.vertex4[0]+enemy.position[0])), 
                           int((enemy.vertex4[1]+enemy.position[1])))
            playerMiddle = (int(rect.x+(rect.width/2)), 
                            int(rect.y+(rect.height/2)))
            distance = MATH.hypot(abs(enemyMiddle[0]-playerMiddle[0]), abs(enemyMiddle[1]-playerMiddle[0]))
            pygame.gfxdraw.pixel(surface, enemyMiddle[0], enemyMiddle[1], (255, 255, 255))
            pygame.gfxdraw.pixel(surface, playerMiddle[0], playerMiddle[1], (255, 255, 255))
            if distance <= self.radius:
                collidepoints = "collide"
            else:
                collidepoints = "no collision"

        return collidepoints

    def render(self, surface, rect):
        gfxdraw.aacircle(surface, int(rect.x+(rect.width/2)), int(rect.y+(rect.height/2)), self.diameter, (0, 255, 0))
        #pygame.draw.rect(surface, (11, 147, 255), rect)

    def move(self, main_inputs, rect, pos, surface):
        rect.x = self.pos[0]
        rect.y = self.pos[1]
        speed = 3
        if main_inputs["w"] == True:
            pos[1] -= speed
            rect.x = self.pos[0]
            rect.y = self.pos[1]
        if main_inputs["s"] == True:
            pos[1] += speed
            rect.x = self.pos[0]
            rect.y = self.pos[1]
        if main_inputs["a"] == True:
            pos[0] -= speed
            rect.x = self.pos[0]
            rect.y = self.pos[1]
        if main_inputs["d"] == True:
            pos[0] += speed
            rect.x = self.pos[0]
            rect.y = self.pos[1]

