import pygame
from pygame.locals import *
from tkinter import *
import sys
import random

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

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Attack_R.png"),
                pygame.image.load("Player_Attack2_R.png"),pygame.image.load("Player_Attack2_R.png"),
                pygame.image.load("Player_Attack3_R.png"),pygame.image.load("Player_Attack3_R.png"),
                pygame.image.load("Player_Attack4_R.png"),pygame.image.load("Player_Attack4_R.png"),
                pygame.image.load("Player_Attack5_R.png"),pygame.image.load("Player_Attack5_R.png"),
                pygame.image.load("Player_Sprite_R.png")]
 
# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Attack_L.png"),
                pygame.image.load("Player_Attack2_L.png"),pygame.image.load("Player_Attack2_L.png"),
                pygame.image.load("Player_Attack3_L.png"),pygame.image.load("Player_Attack3_L.png"),
                pygame.image.load("Player_Attack4_L.png"),pygame.image.load("Player_Attack4_L.png"),
                pygame.image.load("Player_Attack5_L.png"),pygame.image.load("Player_Attack5_L.png"),
                pygame.image.load("Player_Sprite_L.png")]

class EventHandler():
    def __init__(self):
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 2

    #create main menu
    def level_handler(self):
        self.root = Tk()
        self.root.geometry("250x300+820+370")
        
        #get value from radio button (level1, level2 and level3)
        def select():
            s = var.get()
            if s == 1:
                self.level1()
            if s == 2:
                self.level2()
            if s == 3:            
                self.level3()
        var = IntVar()
        #create label, radio button and game start quit button
        label1 = Label(self.root, text=" Dungeon Game ", font=("Arial", 25))
        label2 = Label(self.root, text="Select Game Level", font=("Arial", 15))
        rbouton1 = Radiobutton(self.root, text="Level 1", font=("Arial", 12), value=1, variable=var, indicatoron=0, width=20)
        rbouton2 = Radiobutton(self.root, text="Level 2",font=("Arial", 12), value=2, variable=var, indicatoron=0, width=20)
        rbouton3 = Radiobutton(self.root, text="Level 3", font=("Arial", 12), value=3, variable=var, indicatoron=0, width=20)
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
            
    def level1(self):
        self.root.destroy()
        pygame.time.set_timer(self.enemy_generation, 2000)
        self.level = 1
        self.level_enemies = 6
        self.enemy_count = 0

    def level2(self):
        self.root.destroy()
        pygame.time.set_timer(self.enemy_generation, 2000)
        self.level = 2
        self.level_enemies = 12
        self.enemy_count = 0

    def level3(self):
        self.root.destroy()
        pygame.time.set_timer(self.enemy_generation, 2000)
        self.level = 3
        self.level_enemies = 20
        self.enemy_count = 0

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

        #position and direction
        self.pos = vec((340, 240))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "R"

        #movement
        self.jumping = False
        self.running = False
        self.move_frame = 0

        #combat
        self.attacking = False
        self.attack_frame = 0
        self.cooldown = False
    
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
        #reset move frame
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
        #return to base frame
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
        #check direction for good display
        if self.direction == "R":
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "L":
            self.correction()
            self.image = attack_ani_L[self.attack_frame]
        self.attack_frame += 1

    #correct 2 pics positions
    def correction(self):
        if self.attack_frame == 1:
            self.pos.x -= 20
        if self.attack_frame == 10:
            self.pos.x += 20

    def jump(self):
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12
    
    #check if touch the ground, then stop
    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                if self.rect.bottom > hits[0].rect.top:
                    self.rect.y = hits[0].rect.top + 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
    
    def player_hit(self):
        if self.cooldown == False:
            self.cooldown = True
            pygame.time.set_timer(hit_cooldown, 1000)
            pygame.display.update()
    
    def render(self):
        displaysurface.blit(self.image, self.rect)

#create enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.direction = random.randint(0, 1)
        self.vel.x = random.randint(1, 5) / 2

        #sets the initial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235
    
    def move(self):
        #when reach the border of screen, turn the direction
        if self.pos.x >= (W - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0

        #update position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
        self.rect.topleft = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(self, player_group, False)
        #check if collision with player
        if hits and player.attacking == True:
            self.kill()
        elif hits and player.attacking == False:
            player.player_hit()

    def render(self):
        #display enemy on screen
        displaysurface.blit(self.image, self.rect)

handler = EventHandler()
handler.level_handler()

background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

enemy = Enemy()
enemy_group = pygame.sprite.Group()

hit_cooldown = pygame.USEREVENT + 1

while 1:
    player.gravity_check()
    for event in pygame.event.get():
        # quit when the close window button is clicked
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #generate enemy
        if event.type == handler.enemy_generation:
            if handler.enemy_count < handler.level_enemies:
                enemy = Enemy()
                enemy_group.add(enemy)
                handler.enemy_count += 1
        
        # event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_a:
                if player.attacking == False:
                    player.attack()
                    player.attacking = True
        
        #resets the cooldown
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)
        
    background.render()
    ground.render()

    player.update()
    if player.attacking == True:
        player.attack()
    player.move()
    player.render()
    
    for entity in enemy_group:
        enemy.update()
        enemy.move()
        enemy.render()

    pygame.display.update()
    FPS.tick(60)
        