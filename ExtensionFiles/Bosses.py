import random
import math as MATH

import Projectiles
CircleBossBullet = Projectiles.CircleBossBullet

import pygame
from pygame import gfxdraw

pygame.init()

class CircleBoss:
    def __init__(self, pos, boss_wave, chosenSequence, fireRate, maxFireRate, attackTypes, sequencing, sequencing_rotation, lookDirection):
        self.pos = pos
        self.boss_wave = boss_wave
        self.chosenSequence = chosenSequence
        self.fireRate = fireRate
        self.maxFireRate = maxFireRate
        self.attackTypes = attackTypes
        self.sequencing = sequencing
        self.sequencing_rotation = sequencing_rotation
        self.lookDirection = lookDirection

    def render(self, surface, pos, thickness):
        #pygame.draw.circle(surface, (255, 255, 255), pos, 30, thickness)
        gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), 30, (255, 255, 255))
        gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), 29, (255, 255, 255))
        #pygame.draw.circle(surface, (255, 0, 0), (pos[0]+self.lookDirection[0], pos[1]+self.lookDirection[1]), 15, 2)
        gfxdraw.aacircle(surface, int(pos[0]+self.lookDirection[0]), int(pos[1]+self.lookDirection[1]), 15, (255, 0, 0))
        gfxdraw.aacircle(surface, int(pos[0]+self.lookDirection[0]), int(pos[1]+self.lookDirection[1]), 14, (255, 0, 0))
        #pygame.draw.circle(surface, (200, 0, 0), (pos[0]+self.lookDirection[0], pos[1]+self.lookDirection[1]), 10, thickness)
        gfxdraw.aacircle(surface, int(pos[0]+self.lookDirection[0]), int(pos[1]+self.lookDirection[1]), 10, (200, 0, 0))
        gfxdraw.aacircle(surface, int(pos[0]+self.lookDirection[0]), int(pos[1]+self.lookDirection[1]), 9, (200, 0, 0))

    def create_bullets(self, amount, pattern):
        if pattern != None:
            if pattern not in self.attackTypes:
                raise ValueError(f"results: status must be one of {self.attackTypes}")

        if pattern == None:
            bullets = []
            return bullets

        if pattern == "random":
            bullets = []
            for i in range(0, amount):
                bossbullet = CircleBossBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [random.randint(-360, 360)/100, random.randint(-360, 360)/100], 5)
                bullets.append(bossbullet)

        if pattern == "bigRandom":
            bullets = []
            for i in range(0, 200):
                bossbullet = CircleBossBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [random.randint(-360, 360)/100, random.randint(-360, 360)/100], 5)
                bullets.append(bossbullet)

        if pattern == "sequenced1":
            self.maxFireRate = 10000
            bullets = []
            for i in range(0, int((360/(360/amount)))):
                angle = MATH.radians(int(((360/amount))*i))
                Vx = MATH.cos(angle)
                Vy = MATH.sin(angle)

                bossbullet = CircleBossBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                bullets.append(bossbullet)

        if pattern == "sequenced2":
            self.maxFireRate = 10000
            bullets = []
            for i in range(0, int((360/(360/10)))):
                angle = MATH.radians(int(((360/10))*i))
                Vx = MATH.cos(angle)
                Vy = MATH.sin(angle)

                bossbullet = CircleBossBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                bullets.append(bossbullet)

        if pattern == "sequenced3":
            self.sequencing = not self.sequencing
            if self.sequencing == True:
                self.maxFireRate = 10000
                bullets = []
                for i in range(0, int((360/(360/10)))):
                    angle = MATH.radians(int(((360/10))*i))
                    Vx = MATH.cos(angle)
                    Vy = MATH.sin(angle)

                    bossbullet = CircleBossBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                    bullets.append(bossbullet)
            if self.sequencing == False:
                self.maxFireRate = 5000
                bullets = []
                for i in range(0, int((360/(360/10)))):
                    angle = MATH.radians(int(((360/10))*i))
                    Vx = MATH.cos(angle)
                    Vy = MATH.sin(angle)

                    bossbullet = CircleBossBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                    bullets.append(bossbullet)

        if pattern == "sequenced4":
            self.maxFireRate = 10000
            bullets = []
            for i in range(0, 4):
                angle = MATH.radians(int(((360/4)*i))+self.sequencing_rotation)
                Vx = MATH.cos(angle)
                Vy = MATH.sin(angle)

                self.sequencing_rotation += 5
                bossbullet = CircleBossBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                bullets.append(bossbullet)

        if pattern == "sequenced5":
            self.maxFireRate = 20000
            bullets = []
            for i in range(0, 2):
                for j in range(0, 2):
                    angle = MATH.radians(int((360/2)*j)+self.sequencing_rotation)
                    Vx = MATH.cos(angle)
                    Vy = MATH.sin(angle)

                    self.sequencing_rotation += 5
                    enemybullet = EnemyBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                    bullets.append(enemybullet)

        self.boss_wave += 1
        if self.maxFireRate > 850:
            self.maxFireRate -= 0.5
        return bullets
    
    def render_bullets(self, bullets_main, pos, surface):
        for bullets in bullets_main:
            for bullet in bullets:
                bullet.move()
                bullet.rect = bullet.render(surface, pos, 10, 1)

    def look(self, focus_pos):
        rel_x, rel_y = focus_pos[0]-self.pos[0], focus_pos[1]-self.pos[1]
        
        angle = (180/MATH.pi)*MATH.atan2(rel_y, rel_x)


        lookX = MATH.cos(MATH.radians(angle)) * 10
        lookY = MATH.sin(MATH.radians(angle)) * 10

        self.lookDirection = [lookX, lookY]