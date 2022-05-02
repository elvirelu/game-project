import pygame
from pygame.locals import *
from tkinter import *
import sys
import random

class EventHandler():
    def __init__(self):
        self.enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 2
        self.dead_enemy_count = 0
        self.windowWidth = 250
        self.windowHeight = 300

    def tk_init(self):
        self.root = Tk()
        self.topleft_x = int(self.root.winfo_screenwidth()/2 - self.windowWidth/2)
        self.topleft_y = int(self.root.winfo_screenheight()/2 - self.windowHeight/2)
        self.root.geometry(f"{self.windowWidth}x{self.windowHeight}+{self.topleft_x}+{self.topleft_y}")

    # create main menu
    def level_handler(self):
        self.tk_init()
        # get value from radio button (level1, level2 and level3)
        def select():
            s = var.get()
            if s == 1:
                self.level1()
            if s == 2:
                self.level2()
            if s == 3:
                self.level3()

        var = IntVar()
        # create label, radio button and game start quit button
        label1 = Label(self.root, text=" Dungeon Game ", font=("Arial", 25))
        label2 = Label(self.root, text="Select Game Level", font=("Arial", 15))
        rbouton1 = Radiobutton(self.root, text="Level 1", font=("Arial", 12), value=1, variable=var, indicatoron=0,
                               width=20)
        rbouton2 = Radiobutton(self.root, text="Level 2", font=("Arial", 12), value=2, variable=var, indicatoron=0,
                               width=20)
        rbouton3 = Radiobutton(self.root, text="Level 3", font=("Arial", 12), value=3, variable=var, indicatoron=0,
                               width=20)
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
        background.bgimage = pygame.image.load("background.png")
        ground.gimage = pygame.image.load("ground.png")
        self.level = 1
        self.level_enemies = 3
        self.enemy_count = 0
        self.dead_enemy_count = 0

    def level2(self):
        self.root.destroy()
        pygame.time.set_timer(self.enemy_generation, 1800)
        background.bgimage = pygame.image.load("desert.jpg")
        ground.gimage = pygame.image.load("desert_ground.png")
        self.level = 2
        self.level_enemies = 5
        self.enemy_count = 0
        self.dead_enemy_count = 0


    def level3(self):
        self.root.destroy()
        pygame.time.set_timer(self.enemy_generation, 1500)
        background.bgimage = pygame.image.load("dark.png")
        ground.gimage = pygame.image.load("darkground.png")
        self.level = 3
        self.level_enemies = 8
        self.enemy_count = 0
        self.dead_enemy_count = 0

    def gameover_handler(self):
        pygame.time.set_timer(self.enemy_generation, 0)
        self.tk_init()
        # create gameover label and restart game button
        label1 = Label(self.root, text=" Game Over ", font=("Arial", 25))

        def select():
            player.respawn()
            if self.level == 1:
                self.level1()
            if self.level == 2:
                self.level2()
            if self.level == 3:
                self.level3()

        bouton1 = Button(self.root, text="Restart", font=("Arial", 15), background="light blue", width=10,
                         command=select)
        bouton2 = Button(self.root, text="Quit", font=("Arial", 15), background="light blue", width=10, command=quit)

        label1.pack()
        bouton1.place(x=65, y=100)
        bouton2.place(x=65, y=175)
        self.root.mainloop()

    def gamewin_handler(self):
        pygame.time.set_timer(self.enemy_generation, 0)
        self.tk_init()
        if self.level == 3:
            player.respawn()
            def tk_handle():
                self.root.destroy()
                self.level_handler()
            label1 = Label(self.root, text="You won the game", font=("Arial", 25))
            bouton1 = Button(self.root, text="Main menu", font=("Arial", 15), background="light blue", width=10,
                             command=tk_handle)
            
        elif self.level == 1:
            label1 = Label(self.root, text="You won level 1", font=("Arial", 25))
        
            bouton1 = Button(self.root, text="Level 2", font=("Arial", 15), background="light blue", width=10,
                             command=self.level2) 
        elif self.level == 2:
            label1 = Label(self.root, text="You won level 2", font=("Arial", 25))
            bouton1 = Button(self.root, text="Level 3", font=("Arial", 15), background="light blue", width=10,
                             command=self.level3) 
        bouton2 = Button(self.root, text="Quit", font=("Arial", 15), background="light blue", width=10,
                             command=quit)
        label1.pack()
        bouton1.place(x=65, y=100)
        bouton2.place(x=65, y=175)

        self.root.mainloop()

    def update(self):
        if self.dead_enemy_count == self.level_enemies:
            self.gamewin_handler()

# create background
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("Background.png")

    def render(self):
        displaysurface.blit(self.bgimage, (0, 0))


# create ground
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gimage = pygame.image.load("Ground.png")
        self.rect = self.gimage.get_rect(center=(350, 350))

    def render(self):
        displaysurface.blit(self.gimage, (self.rect.x, self.rect.y))


# create player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        # position and direction
        self.pos = vec((340, 240))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "R"

        # movement
        self.jumping = False
        self.running = False
        self.move_frame = 0

        # combat
        self.attacking = False
        self.attack_frame = 0
        self.cooldown = False

        # health
        self.health = 5

    def move(self):
        # add gravity so that player can touch the ground
        self.acc = vec(0, 0.5)

        # set running to False if the player has slowed down
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        # Accelerates the player in the direction of the key press
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        # calculate velocity
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  # update positon
        self.rect.midbottom = self.pos  # update rect

        # keep player inside the screen
        if self.pos.x > W:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = W

        self.rect.midbottom = self.pos  # update rect

    def update(self):
        # reset move frame
        if self.move_frame > 6:
            self.move_frame = 0

        # move player to next frame
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.direction = "R"
            else:
                self.image = run_ani_L[self.move_frame]
                self.direction = "L"
            self.move_frame += 1

        # return to base frame
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "R":
                self.image = run_ani_R[self.move_frame]
            if self.direction == "L":
                self.image = run_ani_L[self.move_frame]

    def attack(self):
        # return to base frame
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
        # check direction for good display
        if self.direction == "R":
            self.correctionr()
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "L":
            self.correctionl()
            self.image = attack_ani_L[self.attack_frame]
        self.attack_frame += 1

    # correct 2 pics positions
    def correctionr(self):
        if self.attack_frame == 1:
            self.pos.x += 20
        elif self.attack_frame == 10:
            self.pos.x -= 20
        self.rect.midbottom = self.pos  # update rect
        
    # correct 2 pics positions
    def correctionl(self):
        if self.attack_frame == 1:
            self.pos.x -= 20
        elif self.attack_frame == 10:
            self.pos.x += 20
        self.rect.midbottom = self.pos  # update rect

    def jump(self):
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

    # check if touch the ground, then stop
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

            self.health -= 1

            # if lose all the health, game over
            if self.health <= 0:
                handler.gameover_handler()

    def render(self):
        displaysurface.blit(self.image, self.rect)

    def respawn(self):
        self.health = 5
        for sprite in enemy_group:
            sprite.kill()

# create enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.direction = random.randint(0, 1)
        self.vel.x = random.randint(2, 6) / 2

        # sets the initial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235

    def move(self):
        # when reach the border of screen, turn the direction
        if self.pos.x >= (W - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0

        # update position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
        self.rect.topleft = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(self, player_group, False)
        # check if collision with player
        if hits and player.attacking == True:
            self.kill()
            pygame.display.update()
            handler.dead_enemy_count += 1
        elif hits and player.attacking == False:
            player.player_hit()

    def render(self):
        # display enemy on screen
        displaysurface.blit(self.image, self.rect)


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("heart5.png")

    def render(self):
        displaysurface.blit(self.image, (10, 10))


pygame.init()

vec = pygame.math.Vector2
W = 700
H = 350
ACC = 0.3
FRIC = -0.1
FPS = pygame.time.Clock()
COUNT = 0

# create game windows
displaysurface = pygame.display.set_mode((W, H))
pygame.display.set_caption("Game")

# run animation for the right
run_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Sprite2_R.png"),
             pygame.image.load("Player_Sprite3_R.png"), pygame.image.load("Player_Sprite4_R.png"),
             pygame.image.load("Player_Sprite5_R.png"), pygame.image.load("Player_Sprite6_R.png"),
             pygame.image.load("Player_Sprite_R.png")]

# run animation for the left
run_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Sprite2_L.png"),
             pygame.image.load("Player_Sprite3_L.png"), pygame.image.load("Player_Sprite4_L.png"),
             pygame.image.load("Player_Sprite5_L.png"), pygame.image.load("Player_Sprite6_L.png"),
             pygame.image.load("Player_Sprite_L.png")]

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Attack_R.png"),
                pygame.image.load("Player_Attack2_R.png"), pygame.image.load("Player_Attack2_R.png"),
                pygame.image.load("Player_Attack3_R.png"), pygame.image.load("Player_Attack3_R.png"),
                pygame.image.load("Player_Attack4_R.png"), pygame.image.load("Player_Attack4_R.png"),
                pygame.image.load("Player_Attack5_R.png"), pygame.image.load("Player_Attack5_R.png"),
                pygame.image.load("Player_Sprite_R.png")]

# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Attack_L.png"),
                pygame.image.load("Player_Attack2_L.png"), pygame.image.load("Player_Attack2_L.png"),
                pygame.image.load("Player_Attack3_L.png"), pygame.image.load("Player_Attack3_L.png"),
                pygame.image.load("Player_Attack4_L.png"), pygame.image.load("Player_Attack4_L.png"),
                pygame.image.load("Player_Attack5_L.png"), pygame.image.load("Player_Attack5_L.png"),
                pygame.image.load("Player_Sprite_L.png")]

# health bar animation
health_ani = [pygame.image.load("heart0.png"), pygame.image.load("heart.png"),
              pygame.image.load("heart2.png"), pygame.image.load("heart3.png"),
              pygame.image.load("heart4.png"), pygame.image.load("heart5.png")]

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

health = HealthBar()

handler = EventHandler()
handler.level_handler()

while 1:
    player.gravity_check()

    for event in pygame.event.get():
        # resets the cooldown
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)

        # quit when the close window button is clicked
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # generate enemy
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

    background.render()
    ground.render()

    player.update()
    if player.attacking == True:
        player.attack()
    player.move()
    if player.health > 0:
        player.render()
    health.render()

    for entity in enemy_group:
        entity.update()
        entity.move()
        entity.render()

    health.image = health_ani[player.health]
    handler.update()

    pygame.display.update()
    FPS.tick(60)
