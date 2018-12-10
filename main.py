#Import necessary packages
import pygame
import random
from os import path

#Declare colour variables
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
FPS = 60

pygame.init() #Initialise pygame module
image_dir = path.join(path.dirname(__file__), 'images') #Add path to use the images folder, so files can be referenced
sound_dir = path.join(path.dirname(__file__), 'sound') #Add path to use sound folder 

#Load in sounds
pygame.mixer.music.load("music/background_music.wav")
falling_noise = pygame.mixer.Sound("music/falling_sound.wav")
jumping_noise = pygame.mixer.Sound("music/jump_sound.wav")
powerup_noise = pygame.mixer.Sound("music/powerup.wav")
pygame.mixer.pre_init(44100,16,2,4096) #initialises the pygame mixer module for loading and playing sound files and music
pygame.mixer.music.set_volume(0.5) #Set music volume
pygame.mixer.music.play(-1) #Play music

#Declare scoreboard variables
hs_file = "highscore.txt"
Font_Name="scoreboard"

class DoodleJump:
    def __init__(self):
        
        self.width=800 #Set game width
        self.height=600 #Set game height

        self.screen = pygame.display.set_mode((self.width, self.height)) #Initialize window
        pygame.display.set_caption("Next Hop!") #Set game window caption
        
        #Load images and convert them to the same pixel format as used by the screen.(optimizes performance)
        self.lily = pygame.image.load("images/lily_pad_sprite.png").convert_alpha() 
        self.playerstat = pygame.image.load("images/frog_sit_sprite.png").convert_alpha() 
        self.playerRight = pygame.image.load("images/jump_right.png").convert_alpha()
        self.playerLeft = pygame.image.load("images/jump_left.png").convert_alpha()
        self.fly = pygame.image.load("images/fly_sprite.png").convert_alpha()
        self.bird = pygame.image.load("images/bird_2.png").convert_alpha()
        
        #Set objects widths and heights
        self.playerwidth = self.playerstat.get_width()
        self.playerheight = self.playerstat.get_height()
        self.platformwidth = self.lily.get_width()
        self.platformheight = self.lily.get_height()
        self.birdwidth = self.bird.get_width()
        self.birdheight = self.bird.get_height()
        self.flywidth = self.fly.get_width()
        self.flyheight = self.fly.get_height()    
        
        pygame.font.init() #Initialize pygame font module
        self.font = pygame.font.SysFont("Arial", 25) #Declares the default font as Arial size 25
        self.font_name=pygame.font.match_font(Font_Name)
        
        self.clock = pygame.time.Clock() #Count time
    
        self.load_data() #Load previous high score   
        self.score = 0   #Set current highscore to zero
        
        self.direction = 0 #Direction of player - 0 for right, 1 for left
        self.playerx = self.width/2 #Left-most coordinate of player
        self.playery = self.height/3 #Top-most coordinate of player
        self.platforms = [[400, 500, 0, random.randint(0, 1)]] #Left and top coordinates of the lilypad platform, platform type, direction platform moves initially
        self.boosts = [[200, 300, random.randint(0, 1)]]
        self.enemies = [[200, 100, random.randint(0, 1)]]
        self.cameray = 0 #Used to move the view with the character as it jumps. Everything moves up by value of cameray.
        self.jump = 0 #Upwards speed
        self.gravity = 0 #Downwards speed
        self.xmovement = 0 #X-direction speed - -ve is left, +ve is right, 0 is stationary

    def load_data(self):
        #Load previous high score from file
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, hs_file), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
       
    def updatePlayer(self):
        if not self.jump:                   #If player is not jumping (jump=0) 
            self.playery += self.gravity    #Player moves down by gravity value
            self.gravity += 1               #Gravity increases until collision
        
        elif self.jump:                 #If player is jumping
            self.playery -= self.jump   #Player moves up by jump value
            self.jump -= 1              #Jump decreases to zero
        
        key = pygame.key.get_pressed()  #Return boolean values representing state of every key
        
        if key[pygame.K_RIGHT]:         #If the right key's pressed
            if self.xmovement < 10:
                self.xmovement += 1     #Increase speed to the right within limit
            self.direction = 0          #Set character direction to right so corresponding image is used
            
        elif key[pygame.K_LEFT]:        #If the left key's pressed 
            if self.xmovement > -10:
                self.xmovement -= 1     #Increase speed to the left within limit
            self.direction = 1          #Set character direction to left so corresponding image is used
            
        else:                           #If no key's pressed, slow character down (in X-direction)
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
                
        if self.playerx > self.width:   #If character goes over the right edge of screen 
            self.playerx = 0            #Move character to the left edge
        elif self.playerx < 0:          #If character goes over left edge of screen
            self.playerx = self.width   #Move character to the right edge
            
        self.playerx += self.xmovement #Execute character movement (in X-direction)
        
        if self.playery - self.cameray <= 200: #Defines the window view relative to the character. This value is distance between window and character allowed.
            if self.jump >15 :
                self.cameray -= 30   #Increment in which window moves. Must be larger when character moves faster.
            else:
                self.cameray -= 10   
            
        #Copy character image to screen
        if self.jump:
            if not self.direction:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))
        else:
                self.screen.blit(self.playerstat, (self.playerx, self.playery - self.cameray))
            

    def updateBoosts(self):
        for b in self.boosts:
            rect = pygame.Rect(b[0], b[1], self.flywidth, self.flyheight)
            player = pygame.Rect(self.playerx, self.playery, self.playerwidth, self.playerheight)
            
            if rect.colliderect(player):    #If the player and boost collide
                powerup_noise.play()        #Play power up sound      
                self.jump = 40          #Set jump (upwards speed) to 40
                self.gravity = 0        #Set gravity to 0 so the player moves upwards
                    
            if b[-1] == 1:      #If boost direction is left
                b[0] -= 5       #Move boost left
                if b[0] <= 0:   #If boost reaches the window's left edge
                    b[-1] = 0   #Change boost direction
            else:
                b[0] += 5       #Move boost right
                if b[0] >= self.width-self.flywidth: #If boost reaches the window's right edge
                    b[-1] = 1   #Change boost direction
                        
    def drawBoosts(self): 
        for b in self.boosts:
            check = self.boosts[0][1] - self.cameray 
            if check > self.height:          #If last boost is out of view
                self.boosts.append([random.randint(0, 700), self.boosts[-1][1] - 1000, random.randint(0, 1)]) #Adds new boost below previous one (space between is value 1000)
                self.boosts.pop(0)           #removes the 0th entry in boosts
            self.screen.blit(self.fly, (b[0], b[1] - self.cameray)) #Copy boost image to screen
           
           
    def updateEnemies(self):
        for e in self.enemies:
            rect = pygame.Rect(e[0], e[1], self.birdwidth, self.birdheight) #Creates a rectangle using the pygame function. References back to the top level of the class.
            player = pygame.Rect(self.playerx, self.playery, self.playerwidth, self.playerheight)#Creates a rectangle for the player.
            
            if rect.colliderect(player): #If the player hits an enemy game over.
                self.gameOverScreen()

            if e[-1] == 1:  #If the enemy direction is left move left. If it hits the edge then move right.
                e[0] -= 2
                if e[0] <= 0: 
                    e[-1] = 0
            else:
                e[0] += 2 #Start by moving right if it hits the edge then move left.
                if e[0] >= self.width-self.birdwidth:
                    e[-1] = 1
                
    def drawEnemies(self):
        for e in self.enemies:
            check = self.enemies[0][1] - self.cameray   #If the last enemy bird is out of view
            if check > self.height:                     #Define new bird
                self.enemies.append([random.randint(0, 700), self.enemies[-1][1] - 800, random.randint(0, 1)]) #Adds new bird below previous one (space between is value 800)
                self.enemies.pop(0)           #Removes the 0th entry in enemies
            self.screen.blit(self.bird, (e[0], e[1] - self.cameray))
                
            
    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.platformwidth, self.platformheight) #Rectangle (left,top,width,height) representing lilypad platform, uses picture dimensions
            player = pygame.Rect(self.playerx, self.playery, self.playerwidth, self.playerheight) #Rectangle representing player
            
            if rect.colliderect(player) and self.gravity: #If the character falls into platform from above it
                    self.jump = 15
                    self.gravity = 0
                    jumping_noise.play()
                    
            if p[2] == 1:           #Makes platform move
                if p[-1] == 1:      #Changes direction when gets to edge
                    p[0] += 5
                    if p[0] > self.width-self.platformwidth:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self): #Draw lilpad platforms
        for p in self.platforms:
            check = self.platforms[0][1] - self.cameray #If the last platform is out of view
            if check > self.height:                     #Define if new platform will be stationary or move
                platformtype = random.randint(0, 1000)
                if platformtype < 800:
                    platformtype = 0
                else:
                    platformtype = 1

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 80, platformtype, random.randint(0, 1)]) #Adds new platform below previous one (space between is value 80)
                self.platforms.pop(0)           #removes the 0th entry in platforms
                self.score += 100 #Add to player's score
            self.screen.blit(self.lily, (p[0], p[1] - self.cameray)) #Copy lilpad image to screen


    def generatePlatforms(self): #Generate all platforms for beginning of game
        on = self.height
        while on > -100:
            platformtype = random.randint(0, 1000)
            if platformtype < 800:
                platformtype = 0
            else:
                platformtype = 1

            self.platforms.append([random.randint(0,700), on, platformtype, random.randint(0, 1)])
            on -= 80


    def drawBackground(self):
        self.screen.fill(pygame.Color("light blue")) # Makes screen background light blue
       
    
    def run(self): #take that out and make into game loop
        
        clock = pygame.time.Clock() #creates a variable clock which is updated to track time
        self.generatePlatforms()
        
        pygame.mixer.music.play(loops=-1) # plays and loops background music when run method called
        
        while True:
            clock.tick(FPS) #updates clock while game is running
            
            e = pygame.event.poll() 
            if e.type == pygame.QUIT:
                pygame.quit() # gets single event from queue, if event is user quitting the game window then game quits

            if self.playery - self.cameray > self.height: #Restarts game when character falls off view
                # resets position of objects on screen
                self.cameray = 0  
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = self.width/2
                self.playery = self.width/2
                self.gameOverScreen() #displays game over screen if player dies
            
            #draws and updates the objects onto the screen
            self.drawBackground()
            self.drawPlatforms()
            self.drawBoosts()
            self.drawEnemies()
            self.updatePlayer()
            self.updatePlatforms()
            self.updateBoosts()
            self.updateEnemies()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip() 
            
    #gets the text message, font, colour and size and displays on screen    
    def messageToScreen(self, msg, size, colour, x, y):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(msg, True, colour)
        text_rect=text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)
    
    
    #creates a start screen and waits until key is pressed before running the game 
    def startScreen(self):
        self.drawBackground()
        self.messageToScreen("Next Hop!",75,white,self.width/2, self.height/ (3*4))
        self.messageToScreen("Use the arrow keys to move", 35, white, self.width / 2, self.height / 2)
        self.messageToScreen("Press any key to continue...", 25, white, self.width / 2, self.height / 4)
        self.messageToScreen("High Score: " + str(self.highscore), 25, white, self.width / 2, 35) #updates current highscore and displays on start screen
        pygame.display.update()
        self.waitForKeyPress()
        DoodleJump().run()


    def gameOverScreen(self):
        self.drawBackground()
        self.messageToScreen("OOPS!...GAME-OVER", 40, white, self.width / 2, self.height / (3*4))
        self.messageToScreen("Score : "+(str)(self.score), 40, white, self.width / 2, self.height / 2) #displays score
        self.messageToScreen("Press any key to play again...", 30, white, self.width / 2, self.height / 4)
        
        #if the new score is greater than the previous highscore stored in the highscore file then that score 
        #becomes new highscore and the highscore stored in the highscore file is overwritten
        if self.score > self.highscore:
            self.highscore = self.score
            self.messageToScreen("CONGRATULATIONS!!!  NEW HIGH SCORE!", 30, white, self.width / 2, self.height / 2 - 30)
            with open(path.join(self.dir, hs_file), 'w') as f: # writing the new highscore to the file
                f.write(str(self.score))
        else:
                self.messageToScreen("High Score: " + str(self.highscore), 30, white, self.width / 2, self.height / 2 - 30)
        
        pygame.display.update()
        self.waitForKeyPress()
        DoodleJump().__init__()
        DoodleJump().run()
   
    #function waits until a key is pressed before next action is executed such as updating the screen
    def waitForKeyPress(self):
        waiting=True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                if event.type==pygame.KEYUP:
                    waiting=False


#displays start screen when code file is run
DoodleJump().startScreen()