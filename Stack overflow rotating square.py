import pygame, sys, random
from pygame import *

from pygame import gfxdraw
pygame.init()

import math as MATH

#config

window_size=[600, 400]
main_game_surface = pygame.display.set_mode(window_size)

#square

class Square:
    def __init__(self, pos, rot, size, line1, line2, line3, line4): #initialises square
        self.pos = pos #position
        self.rot = rot #rotation amount in degrees
        self.size = size #distance between verticies

        self.line1 = line1 #line 1
        self.line2 = line2 #line 2
        self.line3 = line3 #line 3
        self.line4 = line4 #line 4

    def render(self, surface): #renders square
        x=self.pos[0]
        y=self.pos[1]

        topleft     = pygame.math.Vector2(int(0+self.pos[0]), int(0+self.pos[1]))
        topright    = pygame.math.Vector2(topleft[0]+self.size, topleft[1])
        bottomleft  = pygame.math.Vector2(topleft[0], topleft[1]+self.size)
        bottomright = pygame.math.Vector2(topleft[0]+self.size, topleft[1]+self.size)

        topleft.rotate_ip(self.rot)
        topright.rotate_ip(self.rot)
        bottomleft.rotate_ip(self.rot)
        bottomright.rotate_ip(self.rot)

        pygame.gfxdraw.line(surface, int(topleft[0]),    int(topleft[1]),       int(topright[0]),          int(topright[1]),     (150, 0, 0))
        pygame.gfxdraw.line(surface, int(topright[0]),   int(topright[1]),     int(bottomright[0]),     int(bottomright[1]),     (150, 0, 0))
        pygame.gfxdraw.line(surface, int(topleft[0]),    int(topleft[1]),       int(bottomleft[0]),        int(bottomleft[1]),     (150, 0, 0))
        pygame.gfxdraw.line(surface, int(bottomleft[0]), int(bottomleft[1]), int(bottomright[0]), int(bottomright[1]),     (150, 0, 0))

        self.line1 = pygame.gfxdraw.line(surface, int(topleft[0]),    int(topleft[1]),    int(topright[0]),    int(topright[1]),      (0, 0, 150))
        self.line2 = pygame.gfxdraw.line(surface, int(topright[0]),   int(topright[1]),   int(bottomright[0]), int(bottomright[1]), (0, 0, 150))
        self.line3 = pygame.gfxdraw.line(surface, int(topleft[0]),    int(topleft[1]),    int(bottomleft[0]),  int(bottomleft[1]),  (0, 0, 150))
        self.line4 = pygame.gfxdraw.line(surface, int(bottomleft[0]), int(bottomleft[1]), int(bottomright[0]), int(bottomright[1]), (0, 0, 150))



square = Square([300, 200], 0, 5, None, None, None, None)

#main

while True:
	main_game_surface.fill((0, 0, 0))

	square.rot = 1
	square.render(main_game_surface)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.update()

