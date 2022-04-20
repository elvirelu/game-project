import pygame
from pygame.locals import *
from tkinter import *
import sys

pygame.init()

vec = pygame.math.Vector2
W = 700
H = 350
ACC = 0.3
FRIC = -0.1
FPS = pygame.time.Clock()
COUNT = 0

#create game windows
displaysurface = pygame.display.set_mode((W,H))
pygame.display.set_caption("Game")
        
#run animation for the right
run_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Sprite2_R.png"),
             pygame.image.load("Player_Sprite3_R.png"),pygame.image.load("Player_Sprite4_R.png"),
             pygame.image.load("Player_Sprite5_R.png"),pygame.image.load("Player_Sprite6_R.png"),
             pygame.image.load("Player_Sprite_R.png")]

#run animation for the left
run_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Sprite2_L.png"),
             pygame.image.load("Player_Sprite3_L.png"),pygame.image.load("Player_Sprite4_L.png"),
             pygame.image.load("Player_Sprite5_L.png"),pygame.image.load("Player_Sprite6_L.png"),
             pygame.image.load("Player_Sprite_L.png")]

class EventHandler():
    def __init__(self):
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.battle = False

    #create main menu
    def stage_handler(self):
        self.root = Tk()
        self.root.geometry("250x300+820+370")
        
        #get value from radio button (easy, medium and hard mode)
        def select():
            s = var.get()
            if s == 1:
                self.easy_mode()
            if s == 2:
                self.medium_mode()
            if s == 3:            
                self.hard_mode()
        var = IntVar()
        #create label, radio button and game start quit button
        label1 = Label(self.root, text=" Dungeon Game ", font=("Arial", 25))
        label2 = Label(self.root, text="Select Game Mode", font=("Arial", 15))
        rbouton1 = Radiobutton(self.root, text="Easy", font=("Arial", 12), value=1, variable=var, indicatoron=0, width=20)
        rbouton2 = Radiobutton(self.root, text="Medium",font=("Arial", 12), value=2, variable=var, indicatoron=0, width=20)
        rbouton3 = Radiobutton(self.root, text="Hard", font=("Arial", 12), value=3, variable=var, indicatoron=0, width=20)
        label3 = Label(self.root, text="")
        bouton1 = Button(self.root, text="Start", font=("Arial", 15), background="light blue", width=10, command=select)
        bouton2 = Button(self.root, text="Quit", font=("Arial", 15), background="light blue", width=10, command=quit)
        label1.pack()
        label2.pack(pady=20)
        rbouton1.pack(ipady=5)
        rbouton2.pack(ipady=5)
        rbouton3.pack(ipady=5)
        label3.pack(pady=5)
        bouton1.pack(side=LEFT)
        bouton2.pack(side=RIGHT)

        self.root.mainloop()
            
    def easy_mode(self):
        self.root.destroy()

    def medium_mode(self):
        self.root.destroy()

    def hard_mode(self):
        self.root.destroy()

#create background
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimg = pygame.image.load("Background.png")
    
    def render(self):
        displaysurface.blit(self.bgimg, (0, 0))

#create ground
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gimg = pygame.image.load("Ground.png")
        self.rect = self.gimg.get_rect(center = (350, 350))

    def render(self):
        displaysurface.blit(self.gimg, (self.rect.x, self.rect.y))

#create player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        self.pos = vec((340, 240))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "R"
        self.jumping = False
        self.running = False
        self.move_frame = 0
    
    def move(self):
        #add gravity so that player can touch the ground
        self.acc = vec(0, 0.5)

        #set running to False if the player has slowed down
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        #Accelerates the player in the direction of the key press
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        #calculate velocity
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc #update positon
        self.rect.midbottom = self.pos #update rect

        #keep player inside the screen
        if self.pos.x > W:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = W
        
        self.rect.midbottom = self.pos #update rect

    def update(self):
        if self.move_frame > 6:
            self.move_frame = 0

        #move player to next frame
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.direction = "R"
            else:
                self.image = run_ani_L[self.move_frame]
                self.direction = "L"
            self.move_frame += 1
        
        #return to base frame
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "R":
                self.image = run_ani_R[self.move_frame]
            if self.direction == "L":
                self.image = run_ani_L[self.move_frame]

    def attack(self):
        pass

    def jump(self):
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12


    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                if self.rect.bottom > hits[0].rect.top:
                    self.rect.y = hits[0].rect.top + 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

#create enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player()
handler = EventHandler()
handler.stage_handler()

while 1:
    player.gravity_check()
    for event in pygame.event.get():
        # quit when the close window button is clicked
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        # event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    
    background.render()
    ground.render()
    player.update()
    player.move()
    displaysurface.blit(player.image, player.rect)

    pygame.display.update()
    FPS.tick(60)
        