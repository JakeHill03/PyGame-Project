import pygame
import random


white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
FPS = 60

power_up_boost = -40
power_up_spawn_freq = 7

enemy_freq = 5000
hs_file = "highscore.txt"
Font_Name="scoreboard"

class DoodleJump:
    def __init__(self):
        
        self.width=800
        self.height=600

        self.screen = pygame.display.set_mode((self.width, self.height)) #Initialize window
        self.green = pygame.image.load("images/sprite_images/lily_pad_sprite.png").convert_alpha() #Loads image and converts it to the same pixel format as used by the screen so that it isn't converted everytime it's copied (optimizes performance). Also makes it transparent?
        self.blue = pygame.image.load("images/sprite_images/lily_pad_sprite.png").convert_alpha()
        self.playerfall = pygame.image.load("images/sprite_images/frog_sit_sprite.png").convert_alpha() #different images used for jumping/falling
        self.playerRight = pygame.image.load("images/sprite_images/jump_right.png").convert_alpha()
        self.playerLeft = pygame.image.load("images/sprite_images/jump_left.png").convert_alpha()
        self.fly = pygame.image.load("images/sprite_images/fly_sprite.png").convert_alpha()
        self.bird = pygame.image.load("images/sprite_images/bird_2.png").convert_alpha()
        pygame.font.init() #Initialize pygame font module
        pygame.display.set_caption("Next Hop!")
        self.font = pygame.font.SysFont("Arial", 25)
        self.font_name=pygame.font.match_font(Font_Name)
        self.clock = pygame.time.Clock()
        self.gameOver = False
    
        self.playerwidth = self.playerfall.get_width()
        self.playerheight = self.playerfall.get_height()
        self.platformwidth = self.green.get_width()
        self.platformheight = self.green.get_height()
        self.birdwidth = self.bird.get_width()
        self.birdheight = self.bird.get_height()
        self.flywidth = self.fly.get_width()
        self.flyheight = self.fly.get_height()
        
        
        self.score = 0        
        self.direction = 0 #direction - 0 for right, 1 for left
        self.playerx = self.width/2 #left-most coordinate of player
        self.playery = self.height/3 #top-most coordinate of player
        self.platforms = [[400, 500, 0, random.randint(0, 1)]] #left and top coordinates of the platform, platform type, direction platform moves initially
        self.boosts = [[200, 100, 0, random.randint(0, 1)]]
        self.enemies = [[200, 100, 0, random.randint(0, 1)]]
        self.cameray = 0 #Used to move the view with the character as it jumps. Everything moves up by value of cameray.
        self.jump = 0 #Upwards speed
        self.gravity = 0 #Downwards speed
        self.xmovement = 0 # x direction speed - -ve is left, +ve is right, 0 is stationary
        self.gameExit = False
    
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
                
        if self.playerx > self.width:   #If character goes over the edge of the screen 
            self.playerx = 0            #Move character to the otherside
        elif self.playerx < 0: 
            self.playerx = self.width
            
        self.playerx += self.xmovement #Execute character movement
        
        if self.playery - self.cameray <= 200: #Defines the window view relative to the character. This value is distance between window and character allowed.
            self.cameray -= 10   #increment of window moving upward (smaller = smoother, larger= moves up in stages)
            
        #COPIES THE CHARACTER IMAGE TO THE SCREEN
        if not self.direction:  
            if self.jump:       
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerfall, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerfall, (self.playerx, self.playery - self.cameray))
#"""NEW UP TO HERE"""      
    def updateBoosts(self):
        for b in self.boosts:
            rect = pygame.Rect(b[0], b[1], self.flywidth, self.flyheight)
            player = pygame.Rect(self.playerx, self.playery, self.playerwidth, self.playerheight)
            
            if rect.colliderect(player) and self.gravity:
                if b[2] != 2: #indexes list of self.boosts and says if boost type is 0 does not equal 2
                    self.jump = 80 #sets new jump height/range to 30 if collision with boost detected
                    self.gravity = 0 #and new gravity to 0 so the object (player) moves upwards by 30 pixels
                    
            if b[2] == 1:
                if b[-1] == 1:
                    b[0] += 5
                    if b[0] > self.width - self.flywidth:
                        b[-1] = 1
                        
                else:
                    b[0] -= 5
                    if b[0] <= 0:
                        b[-1] = 1
                        
    def drawBoosts(self):
        for b in self.boosts:
            check = self.boosts[-1][1] - self.cameray
            if check > self.height:
                boosttype = random.randint(0, 1000) #declares a random spawning position between 0 and 1000
                if boosttype < 800: #if the position of the spawn is less than 800 then the boost spawns in from the left to right
                    boosttype = 0
                else:
                    boosttype = 1 #else the postion of the spawn is greater than the width of the window and so the boost spawns in from right to left 
                
                self.boosts.append([random.randint(0, 700), self.boosts[-1][1] - 800, boosttype, random.randint(0, 1)]) #Adds new platform below previous one (space between is value 50)
                self.boosts.pop(0)           #removes the 0th entry in boosts
                
                #self.score += 100       
            
            #COPIES THE PLATFORM IMAGE TO SCREEN
            if b[2] == 0:
                self.screen.blit(self.fly, (b[0], b[1] - self.cameray))
            elif b[2] == 1:
                self.screen.blit(self.fly, (b[0], b[1] - self.cameray))
                
    def generateBoosts(self):
        on = 600
        while on > -100:
            x = random.randint(0,700)
            boosttype = random.randint(0, 1000)
            if boosttype < 800:
                boosttype = 0
            elif boosttype < 900:
                boosttype = 1
            else:
                boosttype = 2
            self.boosts.append([x, on, boosttype, 0])
            on -= 50
#"""NEW UP TO HERE"""
                    
    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.platformwidth, self.platformheight) #rectangle (left,top,width,height) representing platform, uses picture dimensions
            player = pygame.Rect(self.playerx, self.playery, self.playerwidth, self.playerheight) #Rectangle representing player
            
            if rect.colliderect(player) and self.gravity: #If the character falls into platform from above it
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                    
            if p[2] == 1:           #Makes platform move
                if p[-1] == 1:      #Changes direction when gets to edge
                    p[0] += 5
                    if p[0] > self.width-self.platformwidth:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self): #platforms use stephens example
        for p in self.platforms:
            check = self.platforms[0][1] - self.cameray #If the last platform is out of view
            if check > self.height:                     #Define new platform
                platformtype = random.randint(0, 1000)
                if platformtype < 800:
                    platformtype = 0
                else:
                    platformtype = 1

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platformtype, random.randint(0, 1)]) #Adds new platform below previous one (space between is value 50)
                self.platforms.pop(0)           #removes the 0th entry in platforms
                
                self.score += 100       
            
            #COPIES THE PLATFORM IMAGE TO SCREEN
            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cameray))

    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0,700)
            platformtype = random.randint(0, 1000)
            if platformtype < 800:
                platformtype = 0
            elif platformtype < 900:
                platformtype = 1
            else:
                platformtype = 2
            self.platforms.append([x, on, platformtype, 0])
            on -= 50

    def drawBackground(self):
        self.screen.fill(pygame.Color("light blue"))       
        
    def run(self): #take that out and make into game loop
        
        clock = pygame.time.Clock()
        self.generatePlatforms()
        
        while True:
            self.screen.fill((255,255,255))
            clock.tick(60)
            e = pygame.event.poll()
            if e.type == pygame.QUIT:
                pygame.quit()

            if self.playery - self.cameray > 700: #Restarts when character falls off view
                self.cameray = 0
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = self.width/2
                self.playery = self.width/3
                self.gameOver == True
                self.gameOverScreen()
            self.drawBackground()
            self.drawPlatforms()
            self.drawBoosts()
            self.updatePlayer()
            self.updatePlatforms()
            self.updateBoosts()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip() 
            
#"NEW FROM HERE"""         
    def messageToScreen(self,msg,size, color, x, y):
        font=pygame.font.Font(self.font_name,size)
        text_surface=font.render(msg,True,color)
        text_rect=text_surface.get_rect()
        text_rect.midtop=(x,y)
        self.screen.blit(text_surface,text_rect)
    
    
    def startScreen(self):
        self.screen.fill(pygame.Color ("light blue"))
        self.messageToScreen("Next Hop!",40,white,self.width/2,self.height/2)
        self.messageToScreen("Press any key to continue...", 25, white, self.width / 2 + 50, self.height / 2 + 50)
        #self.messageToScreen("High Score: " + str(self.highscore), 25, white, self.width / 2, 35)
        pygame.display.update()
        self.waitForKeyPress()
        DoodleJump().run()


    def gameOverScreen(self):
        self.screen.fill(pygame.Color("light blue"))
        self.messageToScreen("OOPS!...GAME-OVER", 40, white, self.width / 2, 180)
        self.messageToScreen("Score : "+(str)(self.score), 40, white, self.width / 2, self.height / 2-100)
        self.messageToScreen("Press any key to play again...", 30, white, self.width / 2 + 50, self.height / 2 + 50)
        pygame.display.update()
        self.waitForKeyPress()
        DoodleJump().__init__()
        DoodleJump().run()
   
    def waitForKeyPress(self):
        waiting=True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    waiting=False
                    self.gameExit=True
                if event.type==pygame.KEYUP:
                    waiting=False
                    self.gameOver=False
                    self.gameExit=False

#"""NEW UP TO HERE"""  
DoodleJump().startScreen()