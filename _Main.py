# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 13:09:19 2018
PlayerActive class
@author: Stephen
"""
import pygame
import os
import random

WIDTH = 600
HEIGHT = 800
FPS = 30

pygame.init()
pygame.mixer.init()
GameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Next Hop")
clock = pygame.time.Clock()

#Colours
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)

#set up assets folder
#game_folder = os.path.dirname(__file__)
#img_folder = os.path.join(game_folder, "img")



class PlayerActive(pygame.sprite.Sprite):
    #sprite for player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((30, 60)) #sets dimensions of player image surface
        self.image.fill(green)
        """self.playerImage = pygame.image.load(os.path.join(img_folder, "frog_sit_sprite.png")).convert() #loads in player image and converts to format that can be used by pygame
        self.playerJump = pygame.image.load(os.path.join(img_folder, "frog_jump_sprite.png")).convert()
        self.playerLeft = pygame.image.load(os.path.join(img_folder, "jump_left.png")).convert()
        self. playerRight = pygame.image.load(os.path.join(img_folder, "jump_right.png")).convert()"""
        self.image.set_colorkey(blue) #makes background of 
        self.rect = self.image.get_rect() #defines a rectangular area where the player image is defined - makes locating image easier
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 1
    
        self.speed = 0
        
    def move(self, xdir, ydir):
        self.speed = 0
        activeKey = pygame.key.get_pressed()
        if activeKey[pygame.K_RIGHT]:
            player.move(1, 0)
        if activeKey[pygame.K_LEFT]:
            player.move(-1, 0)
        if activeKey[pygame.K_UP]:
            player.move(-1, 0)
    
        self.rect.x += xdir*self.speed
        self.rect.y += ydir*self.speed
        
        if self.rect.left > WIDTH:
            self.rect.right = 0 
        
        if self.rect.right < 0 :
            self.rect.right = 0  # contrains character image to the surface


class PlatformActive(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 5))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width) #ensures that platforms spawn in at random x coordinates between the width of the gameWindow and the width of the platform
        self.rect.y = random.randrange(-100, -40) #randomises the y postion of spawning platforms
        self.speedx = random.randrange(1, 6)
        
    def update(self):
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width) 
            self.rect.y = random.randrange(-100, -40) 
            self.speedx = random.randrange(1, 6)



class FlyActive(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(5, 5)
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width) #ensures that platforms spawn in at random x coordinates between the width of the gameWindow and the width of the platform
        self.rect.y = random.randrange(-100, -40) #randomises the y postion of spawning platforms
        self.speedx = random.randrange(1, 3)



all_sprites = pygame.sprite.Group() 
player = PlayerActive()
all_sprites.add(player)       
platforms = pygame.sprite.Group()
for i in range(8):
    p = PlatformActive()
    all_sprites.add(p)
    platforms.add(p)


#Game loop
gameActive = True
while gameActive:
    clock.tick(FPS)
    #Event tracking
    for event in pygame.event.get():
        #prints event
        if event.type == pygame.QUIT:
            gameActive = False
            

    
    # UPDATE    
    all_sprites.update()
    #drawing
    GameWindow.fill(blue)
    all_sprites.draw(GameWindow)
    #after drawing everything 'flip' display
    pygame.display.flip()
    
pygame.quit()
