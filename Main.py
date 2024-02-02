import pygame, sys, random
from pygame import *

from pygame._sdl2 import Window
from pygame import gfxdraw

pygame.init()
pygame.font.init()

import math as MATH
import time as TIME

clock = pygame.time.Clock()
playerFont = pygame.font.SysFont("bahnschrift", 30)
playerFont2 = pygame.font.SysFont("bahnschrift", 20)

#config
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

window_size = [600, 400]
main_game_surface = pygame.display.set_mode(window_size, pygame.NOFRAME)
game_title = pygame.display.set_caption("WindowKillRipoff")

game_surface = pygame.Surface(window_size)

windowX = 500 #int(monitor_size[0]/2)-int(window_size[0]/2)
windowY = 300 #int(monitor_size[1]/2)-int(window_size[1]/2)
saved_window_pos = [windowX, windowY]

window = Window.from_display_module()
window.position = (windowX, windowY)
window.opacity = 1

#Main
paused = False
maxShakeAmount = 60
shake_amount = maxShakeAmount

def renderSquares(squares, surface):
    for square in squares:
        square.render(surface)

def shake_screen():
    global windowX, windowY, shake_amount

    if shake_amount > 0:
        shake_amount -= 1
        window_shake_index_X = random.randint(0, 8)-4
        window_shake_index_Y = random.randint(0, 8)-4

        windowX = windowX+window_shake_index_X
        windowY = windowY+window_shake_index_Y

def removeBullets(list_of_list_of_bullets):
        for list_of_bullets in list_of_list_of_bullets:
            for bullet in list_of_bullets:
                if (bullet.rect.x>610 or bullet.rect.x<-20) or (bullet.rect.y>410 or bullet.rect.y<-20):
                    list_of_bullets.remove(bullet)

class Square:
    def __init__(self, position, size, rotation, movementVector, OGvertex1, OGvertex2, OGvertex3, OGvertex4):
        self.position = position
        self.size = size
        self.rotation = rotation
        self.movementVector = movementVector

        self.OGvertex1 = OGvertex1
        self.OGvertex2 = OGvertex2
        self.OGvertex3 = OGvertex3
        self.OGvertex4 = OGvertex4

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

    def rotateVerticies(self):
        self.rotation += 5
        self.position[0] += self.movementVector[0]
        self.position[1] += self.movementVector[1]

        self.vertex1 = self.OGvertex1.rotate(self.rotation)
        self.vertex2 = self.OGvertex2.rotate(self.rotation)
        self.vertex3 = self.OGvertex3.rotate(self.rotation)
        self.vertex4 = self.OGvertex4.rotate(self.rotation)

    def render(self, surface):
        if self.movementVector[0] == 0:
            self.movementVector[0] = random.randint(-5, 5)
        if self.movementVector[1] == 0:
            self.movementVector[1] = random.randint(-5, 5)

        self.createVerticies()
        self.rotateVerticies()

        pygame.gfxdraw.line(surface, int(self.vertex1[0]+self.position[0]), int(self.vertex1[1]+self.position[1]), int(self.vertex2[0]+self.position[0]), int(self.vertex2[1]+self.position[1]), (50, 150, 25))
        pygame.gfxdraw.line(surface, int(self.vertex2[0]+self.position[0]), int(self.vertex2[1]+self.position[1]), int(self.vertex4[0]+self.position[0]), int(self.vertex4[1]+self.position[1]), (50, 150, 25))
        pygame.gfxdraw.line(surface, int(self.vertex1[0]+self.position[0]), int(self.vertex1[1]+self.position[1]), int(self.vertex3[0]+self.position[0]), int(self.vertex3[1]+self.position[1]), (50, 150, 25))
        pygame.gfxdraw.line(surface, int(self.vertex3[0]+self.position[0]), int(self.vertex3[1]+self.position[1]), int(self.vertex4[0]+self.position[0]), int(self.vertex4[1]+self.position[1]), (50, 150, 25))

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



class EnemyBullet:
    def __init__(self, rect, movementPos, direction, damage):
        self.rect = rect
        self.movementPos = movementPos
        self.direction = direction
        self.damage = damage

    def render(self, surface, Spawnpos, radius, thickness):
        pos = [Spawnpos[0] + self.movementPos[0], Spawnpos[1] + self.movementPos[1]]
        bullet_rect = pygame.Rect(pos[0], pos[1], radius+7, radius+7)
        #pygame.draw.rect(surface, (255, 0, 0), bullet_rect)
        gfxdraw.aacircle(surface, int(bullet_rect.x+(bullet_rect.width/2)), int(bullet_rect.y+(bullet_rect.width/2)), radius, (255, 30, 140))

        return bullet_rect

    def move(self):
        self.movementPos[0] += self.direction[1]
        self.movementPos[1] += self.direction[0]



class MiddleCircle:
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
                enemybullet = EnemyBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [random.randint(-360, 360)/100, random.randint(-360, 360)/100], 5)
                bullets.append(enemybullet)

        if pattern == "bigRandom":
            bullets = []
            for i in range(0, 200):
                enemybullet = EnemyBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [random.randint(-360, 360)/100, random.randint(-360, 360)/100], 5)
                bullets.append(enemybullet)

        if pattern == "sequenced1":
            self.maxFireRate = 10000
            bullets = []
            for i in range(0, int((360/(360/amount)))):
                angle = MATH.radians(int(((360/amount))*i))
                Vx = MATH.cos(angle)
                Vy = MATH.sin(angle)

                enemybullet = EnemyBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                bullets.append(enemybullet)

        if pattern == "sequenced2":
            self.maxFireRate = 10000
            bullets = []
            for i in range(0, int((360/(360/10)))):
                angle = MATH.radians(int(((360/10))*i))
                Vx = MATH.cos(angle)
                Vy = MATH.sin(angle)

                enemybullet = EnemyBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                bullets.append(enemybullet)

        if pattern == "sequenced3":
            self.sequencing = not self.sequencing
            if self.sequencing == True:
                self.maxFireRate = 10000
                bullets = []
                for i in range(0, int((360/(360/10)))):
                    angle = MATH.radians(int(((360/10))*i))
                    Vx = MATH.cos(angle)
                    Vy = MATH.sin(angle)

                    enemybullet = EnemyBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                    bullets.append(enemybullet)
            if self.sequencing == False:
                self.maxFireRate = 5000
                bullets = []
                for i in range(0, int((360/(360/10)))):
                    angle = MATH.radians(int(((360/10))*i))
                    Vx = MATH.cos(angle)
                    Vy = MATH.sin(angle)

                    enemybullet = EnemyBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                    bullets.append(enemybullet)

        if pattern == "sequenced4":
            self.maxFireRate = 10000
            bullets = []
            for i in range(0, 4):
                angle = MATH.radians(int(((360/4)*i))+self.sequencing_rotation)
                Vx = MATH.cos(angle)
                Vy = MATH.sin(angle)

                self.sequencing_rotation += 5
                enemybullet = EnemyBullet(pygame.Rect(0, 0, 0, 0), [0, 0], [Vx, Vy], 5)
                bullets.append(enemybullet)

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


main_inputs = {"w": False, "s": False, "a": False, "d": False}

middle_circle_thickness = 1
middle_circle_pos = [windowX-monitor_size[0], windowY-monitor_size[1]]
print(middle_circle_pos)

player = Player([200, 100], pygame.Rect(0, 0, 15, 15), 100, 500, [])
middleCircle = MiddleCircle(middle_circle_pos, 0, "sequenced1", 1000, 1000, ["random", "bigRandom", "sequenced1", "sequenced2", "sequenced3", "sequenced4", "sequenced5"], True, 0, [0, 0])

bossbullets = []
middleCircle.boss_wave = 1
bossbullets.append(middleCircle.create_bullets(middleCircle.boss_wave+4, None))

player_health_display = playerFont.render(str(player.health), False, (0, 0, 0))

damageSquares = []
while True:

    middle_circle_pos = [(monitor_size[0]/2)-windowX, (monitor_size[1]/2)-windowY]
    middleCircle.pos = middle_circle_pos

    game_surface.fill((11, 10, 18))
    window.position = (windowX, windowY)

    renderSquares(damageSquares, game_surface)

    if player.health > 0:
        player.move(main_inputs, player.rect, player.pos, game_surface)
        player.render(game_surface, player.rect)
        player.bullet_collision(bossbullets, player.rect, damageSquares)
        player_health_display = playerFont.render(f"HP: {player.health}", 1, (100, 255, 100))
        game_surface.blit(player_health_display, (10, 10))

    if player.health <= 0:
        bossbullets.append(middleCircle.create_bullets(middleCircle.boss_wave+4, None))
        bossbullets = []

        player.respawnTime -= 8.33333333
        game_over_display = playerFont.render("Game over", 1, (110, 30, 60))
        game_surface.blit(game_over_display, (225, 10))
        if player.respawnTime <= 0:
            game_over_display2 = playerFont2.render("Press any button to restart", 1, (80, 0, 30))
            game_surface.blit(game_over_display2, (178, 40))

    middleCircle.chosenSequence = "sequenced1"

    if middleCircle.fireRate > 0:
        middleCircle.fireRate -= middleCircle.maxFireRate/60
    if middleCircle.fireRate <= 0:
        middleCircle.fireRate = middleCircle.maxFireRate
        if middleCircle.chosenSequence != (middleCircle.attackTypes[0] or middleCircle.attackTypes[1]):
            if player.health > 0:
                bossbullets.append(middleCircle.create_bullets(middleCircle.boss_wave+4, middleCircle.chosenSequence))

    removeBullets(bossbullets)

    middleCircle.render(game_surface, middleCircle.pos, middle_circle_thickness)
    middleCircle.render_bullets(bossbullets, middle_circle_pos, game_surface)
    middleCircle.look(player.pos)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if player.respawnTime <= 0:
                if player.health <= 0:
                    player.respawnTime = 500
                    player.health = 100
                    player.pos = [10, 10]

            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_p:
                paused = not paused
            if event.key == K_w:
                main_inputs["w"] = True
            if event.key == K_s:
                main_inputs["s"] = True
            if event.key == K_a:
                main_inputs["a"] = True
            if event.key == K_d:
                main_inputs["d"] = True
        if event.type == KEYUP:
            if event.key == K_w:
                main_inputs["w"] = False
            if event.key == K_s:
                main_inputs["s"] = False
            if event.key == K_a:
                main_inputs["a"] = False
            if event.key == K_d:
                main_inputs["d"] = False

    surf = game_surface#pygame.transform.scale(game_surface, window_size)
    main_game_surface.blit(surf, (0, 0))

    clock.tick(60)
    pygame.display.update()

