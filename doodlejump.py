import pygame
import sys
import random

class DoodleJump:
    def __init__(self):
        width=800
        height=600
        self.screen = pygame.display.set_mode((width, height)) #Initialize window
        self.green = pygame.image.load("assets/green.png").convert_alpha() #Loads image and converts it to the same pixel format as used by the screen so that it isn't converted everytime it's copied (optimizes performance). Also makes it transparent?
        pygame.font.init() #Initialize pygame font module
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 25)
        self.blue = pygame.image.load("assets/blue.png").convert_alpha()
        self.red = pygame.image.load("assets/red.png").convert_alpha()
        self.red_1 = pygame.image.load("assets/red_1.png").convert_alpha()
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha() #different images used for jumping/falling
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()
        self.spring = pygame.image.load("assets/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("assets/spring_1.png").convert_alpha()
        self.direction = 0 #direction - 0 for right, 1 for left
        self.playerx = 400 #left-most coordinate of player
        self.playery = 400 #top-most coordinate of player
        self.platforms = [[400, 500, 0, 0]] #left and top coordinates of the platform
        self.springs = []
        self.cameray = 0
        self.jump = 0 #Upwards speed
        self.gravity = 0 #Downwards speed
        self.xmovement = 0 # x direction speed - -ve is left, +ve is right, 0 is stationary
    
    def updatePlayer(self):
        if not self.jump:               #if jump is 0   
            self.playery += self.gravity#Player moves down by gravity value (gravity increases until collision)
            self.gravity += 1
        elif self.jump:                 #if jump isn't 0
            self.playery -= self.jump   #Player moves up by jump value (jump will decrease to 0)
            self.jump -= 1          
        
        key = pygame.key.get_pressed()  #returns boolean values representing state of every key
        
        if key[pygame.K_RIGHT]:         #If the right key's pressed
            if self.xmovement < 10:
                self.xmovement += 1     #Increase speed to the right within limit
            self.direction = 0
        elif key[pygame.K_LEFT]:        #If the left key's pressed 
            if self.xmovement > -10:
                self.xmovement -= 1     #Increase speed to the left within limit
            self.direction = 1          
        else:                           #slow character down (x direction only)
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
                
        if self.playerx > 850:  #If character goes over the edge of the screen (screen width+ just over half of character width)
            self.playerx = -50  #Move character to the otherside (just over half character width)
        elif self.playerx < -50: 
            self.playerx = 850
            
        self.playerx += self.xmovement #Execute character movement
        
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
            
        #COPIES THE CHARACTER IMAGE TO THE SCREEN
        if not self.direction:  
            if self.jump:       
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))

    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height()) #rectangle (left,top,width,height) representing platform, uses picture dimensions
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10, self.playerRight.get_height()) #Rectangle representing player
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100
            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.red, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.red_1, (p[0], p[1] - self.cameray))
    
        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(), self.playerRight.get_height())):
                self.jump = 50
                self.cameray -= 50

    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0,700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222,222,222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(self.screen, (222,222,222), (0, x * 12), (800, x * 12))
    
    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill((255,255,255))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if self.playery - self.cameray > 700:
                self.cameray = 0
                self.score = 0
                self.springs = []
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = 400
                self.playery = 400
            self.drawGrid()
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip() 


DoodleJump().run()
