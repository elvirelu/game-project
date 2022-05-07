"""
class Menu:
    start_menu()
    gameover_menu()
    gamewin_menu()

class Game:
    start_game()
    level1()
    level2()
    level3()
    event_handle()
    update_scene()
    respawn()

class Player:
    set_pos()
    move()
    attack()
    health_check()
    update()

class Enemy:
    move()
    collide()
    update()

class Healthbar
class Background
"""

import random
import pygame
from pygame import *
from tkinter import *

# create class Background
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("background/background.jpg")
        self.rect = self.image.get_rect(topleft=(0, 0))

# create class HealthBar
class HealthBar(pygame.sprite.Sprite):
    # line 49 to 51 taken from https://coderslegacy.com/python/pygame-rpg-health-bar/
    # health bar animation
    health_ani = [pygame.image.load("healthbar/heart0.png"), pygame.image.load("healthbar/heart.png"),
                pygame.image.load("healthbar/heart2.png"), pygame.image.load("healthbar/heart3.png"),
                pygame.image.load("healthbar/heart4.png"), pygame.image.load("healthbar/heart5.png")]

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("healthbar/heart5.png")
        self.rect = self.image.get_rect(topleft=(10, 10))

    def update(self):
        self.image = self.health_ani[menu.game.player.health]

# class Player
class Player(pygame.sprite.Sprite):
    # taken from https://coderslegacy.com/python/pygame-rpg-movement-animations/
    # line 66 to 80 taken close to litteraly
    # modifed logic afterwards so that ....
    # move animation for the right
    move_ani_R = [pygame.image.load("player/Player_Sprite_R.png"), pygame.image.load("player/Player_Sprite2_R.png"),
                pygame.image.load("player/Player_Sprite3_R.png"), pygame.image.load("player/Player_Sprite4_R.png"),
                pygame.image.load("player/Player_Sprite5_R.png"), pygame.image.load("player/Player_Sprite6_R.png"),
                pygame.image.load("player/Player_Sprite_R.png")]
    # move animation for the left
    move_ani_L = [pygame.image.load("player/Player_Sprite_L.png"), pygame.image.load("player/Player_Sprite2_L.png"),
                pygame.image.load("player/Player_Sprite3_L.png"), pygame.image.load("player/Player_Sprite4_L.png"),
                pygame.image.load("player/Player_Sprite5_L.png"), pygame.image.load("player/Player_Sprite6_L.png"),
                pygame.image.load("player/Player_Sprite_L.png")]
    # Attack animation for the RIGHT
    attack_ani_R = [pygame.image.load("player/Player_Sprite_R.png"), pygame.image.load("player/Player_Attack_R.png"),
                    pygame.image.load("player/Player_Attack2_R.png"), pygame.image.load("player/Player_Attack2_R.png"),
                    pygame.image.load("player/Player_Attack3_R.png"), pygame.image.load("player/Player_Attack3_R.png"),
                    pygame.image.load("player/Player_Attack4_R.png"), pygame.image.load("player/Player_Attack4_R.png"),
                    pygame.image.load("player/Player_Attack5_R.png"), pygame.image.load("player/Player_Attack5_R.png"),
                    pygame.image.load("player/Player_Sprite_R.png")]
    # Attack animation for the LEFT
    attack_ani_L = [pygame.image.load("player/Player_Sprite_L.png"), pygame.image.load("player/Player_Attack_L.png"),
                    pygame.image.load("player/Player_Attack2_L.png"), pygame.image.load("player/Player_Attack2_L.png"),
                    pygame.image.load("player/Player_Attack3_L.png"), pygame.image.load("player/Player_Attack3_L.png"),
                    pygame.image.load("player/Player_Attack4_L.png"), pygame.image.load("player/Player_Attack4_L.png"),
                    pygame.image.load("player/Player_Attack5_L.png"), pygame.image.load("player/Player_Attack5_L.png"),
                    pygame.image.load("player/Player_Sprite_L.png")]

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player/Player_Sprite_R.png")
        self.rect = self.image.get_rect(topleft=(W/2, 310))
        self.position = Vector2(W/2, 310)
        self.velocity = Vector2(0, 0)
        self.direction = True
        self.moving = True
        self.attacking = False
        self.move_frame = 0
        self.attack_frame = 0
        self.health = 5
        self.collidepause = False

    def get_pos(self):
        # calculate the velocity
        self.velocity.x *= 0.9
        self.position += self.velocity
        self.rect.topleft = self.position

        # keep player inside the screen
        if self.position.x > W-40:
            self.position.x = W-40
        elif self.position.x < 0:
            self.position.x = 0

    def move(self):
        # if move_frame out of range, restart it from 0
        if self.move_frame > 6:
            self.move_frame = 0
            
        # if player has some extent velocity, change the image as running images
        if self.velocity.x > 1:
            self.image = self.move_ani_R[self.move_frame]
            self.direction = True
            self.move_frame += 1
        elif self.velocity.x < -1:
            self.image = self.move_ani_L[self.move_frame]
            self.direction = False
            self.move_frame += 1
        else:
            if self.direction:
                self.image = self.move_ani_R[0]
            else:
                self.image = self.move_ani_L[0]

    def attack(self):
        # restart the attack_frame number if it is out of range
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
        # check direction for right display
        if self.direction:
            self.image = self.attack_ani_R[self.attack_frame]
        else:
            self.image = self.attack_ani_L[self.attack_frame]
        self.attack_frame += 1
    
    def collide_check(self, g): 
        # line 151 to 154 taken from https://coderslegacy.com/python/pygame-rpg-collision-detection/
        # to avoid collide continually, set pausecollide switch, allow detect collide after 1 second
        if self.collidepause == False:
            self.collidepause = True
            self.health -= 1
            pygame.time.set_timer(g.collidepause_event, 1000)

        # after losing all the health, kill the player, redraw game sprites, 
        # update dispaly, wait 2s then call the gameover menu
        if self.health < 0:
            self.kill()
            g.sprites.draw(g.surface)
            pygame.display.update()
            menu.gameover_menu()
        
    # update position, movement and attack
    def update(self):
        self.get_pos()
        self.move()
        if self.attacking == True:
            self.attack()

# enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()        
        self.image = pygame.image.load("enemy/Enemy.png")
        self.rect = self.image.get_rect()
        self.velocity = Vector2(random.randint(1, 2), 0)
        self.direction = random.randint(0, 1)
        if self.direction:
            self.position = Vector2(W-30, 300)
        else:
            self.position = Vector2(0, 300)

    def move(self):
        # calculate the position according to the direction
        if self.direction:
            self.position.x -= self.velocity.x
        else:
            self.position.x += self.velocity.x
        self.rect.topleft = self.position

        # when position is out of border, change direction
        if self.position.x <= 0:
            self.direction = 0
        elif self.position.x >= W-30:
            self.direction = 1
    
    def collide_check(self, g):

        # check if collide
        collide = pygame.sprite.collide_rect(self, g.player)
        if collide :
        # when player is attacking and collide, kill enemy, otherwise decrease player's health
            if g.player.attacking == True:
                self.kill()
                g.dead_enemy_count += 1
            else:
                g.player.collide_check(g)

        # if all the enemies are dead, call gamewin menu
        if g.dead_enemy_count == g.enemy_num:
            g.sprites.draw(g.surface)
            pygame.display.update()
            menu.gamewin_menu()

    def update(self):
        self.collide_check(menu.game)
        self.move()

# class Game, to handle all the sprites instances and events, set 3 levels and update all
class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()        
        self.sprites = pygame.sprite.LayeredUpdates()
        self.player = Player()
        self.playergroup = pygame.sprite.GroupSingle(self.player)
        self.healthbar = HealthBar()
        self.background = Background()
        self.sprites.add(self.background, self.player, self.healthbar)
        self.run_game = True
        self.enemycreate_event = pygame.USEREVENT + 1
        self.collidepause_event = pygame.USEREVENT + 2
    
    # initial the game window and keep running the scene updates
    def start_game(self):
        self.surface = pygame.display.set_mode((W, H))
        while self.run_game:
            self.update_scene()

    # draw the sprites, call all the sprites update methods, update events handle
    def update_scene(self):
        self.clock.tick(60)
        self.event_handle()
        self.sprites.draw(self.surface)
        self.sprites.update()
        pygame.display.update()

    def event_handle(self):
        # get pygame events
        for event in pygame.event.get():
            # press window close button, quit game
            if event.type == pygame.QUIT:
                self.run_game = False
            if event.type == KEYDOWN:

                # line 259 to 262 taken from https://coderslegacy.com/python/pygame-rpg-attack-animations/
                # press key A to perform player attack
                if event.key == pygame.K_a:
                    if not self.player.attacking:
                        self.player.attack()
                        self.player.attacking = True

                if event.key == pygame.K_RIGHT:
                    self.player.velocity.x = 3
                elif event.key == pygame.K_LEFT:
                    self.player.velocity.x = -3

            # in every second check enemycreate event, then instanciate enemy
            if event.type == self.enemycreate_event:
                if self.enemy_count < self.enemy_num:
                    self.sprites.add(Enemy())
                    self.enemy_count += 1

            # avoid collide continually
            if event.type == self.collidepause_event:
                self.player.collidepause = False
    
    # have to kill all the sprites in the precedent level, then add sprites for next level, also reset healthbar
    def respawn(self):
        for sprite in self.sprites:
            if type(sprite) is Enemy:
                sprite.kill() 
        self.sprites.add(self.player)
        self.playergroup.add(self.player)
        self.player.health = 5

    # when called, destroy tkinter menu, set enemycreate interval, set level 1 initial values
    def level1(self):
        menu.root.destroy()        
        pygame.time.set_timer(self.enemycreate_event, 1000)
        self.background.image = pygame.image.load("background/background.jpg")
        self.level = 1
        self.enemy_num = 8
        self.enemy_count = 0
        self.dead_enemy_count = 0

    # when called, destroy tkinter menu, set enemycreate interval, set level 2 initial values
    def level2(self):
        menu.root.destroy()
        pygame.time.set_timer(self.enemycreate_event, 800)
        self.background.image = pygame.image.load("background/desert.jpg")
        self.level = 2
        self.enemy_num = 12
        self.enemy_count = 0
        self.dead_enemy_count = 0

    # when called, destroy tkinter menu, set enemycreate interval, set level 2 initial values
    def level3(self):
        menu.root.destroy()
        pygame.time.set_timer(self.enemycreate_event, 600)
        self.background.image = pygame.image.load("background/dark.jpg")
        self.level = 3
        self.enemy_num = 18
        self.enemy_count = 0
        self.dead_enemy_count = 0

class Menu:
    def __init__(self):
        self.tk_init() 
        self.game = Game()   

    # set tkinter menu in the center of screen
    def tk_init(self):
        self.windowWidth = 250
        self.windowHeight = 300
        self.root = Tk()
        self.topleft_x = int(self.root.winfo_screenwidth()/2 - self.windowWidth/2)
        self.topleft_y = int(self.root.winfo_screenheight()/2 - self.windowHeight/2)
        self.root.geometry(f"{self.windowWidth}x{self.windowHeight}+{self.topleft_x}+{self.topleft_y}")

    def start_menu(self): 
        # get value from radio button (level1, level2 and level3)
        def select():           
            s = var.get()
            if s == 1:
                self.game.level1()
            if s == 2:
                self.game.level2()
            if s == 3:
                self.game.level3()
            self.game.start_game()
        var = IntVar()
        # create label, radio button and game start quit button
        label1 = Label(self.root, text=" Dungeon Game ", font=("Arial", 25))
        label2 = Label(self.root, text="Select Game Level", font=("Arial", 15))
        rbouton1 = Radiobutton(self.root, text="Level 1", font=("Arial", 12), value=1, variable=var, indicatoron=0, width=20)
        rbouton2 = Radiobutton(self.root, text="Level 2", font=("Arial", 12), value=2, variable=var, indicatoron=0, width=20)
        rbouton3 = Radiobutton(self.root, text="Level 3", font=("Arial", 12), value=3, variable=var, indicatoron=0, width=20)
        label3 = Label(self.root, text="")
        bouton1 = Button(self.root, text="Start", font=("Arial", 15), background="light blue", width=10, command=select)
        bouton2 = Button(self.root, text="Quit", font=("Arial", 15), background="light blue", width=10, command=exit)
        label1.pack()
        label2.pack(pady=20)
        rbouton1.pack(ipady=5)
        rbouton2.pack(ipady=5)
        rbouton3.pack(ipady=5)
        label3.pack(pady=5)
        bouton1.pack(side=LEFT)
        bouton2.pack(side=RIGHT)
        self.root.mainloop()

    def gameover_menu(self):
        # in waiting time, pause the enemy create event to avoid create enemy before menu selection
        pygame.time.set_timer(self.game.enemycreate_event, 0)
        self.tk_init()
        def select():
            self.game.respawn()
            if self.game.level == 1:
                self.game.level1()
            if self.game.level == 2:
                self.game.level2()
            if self.game.level == 3:
                self.game.level3()
        # create gameover label and restart game button
        label1 = Label(self.root, text=" Game Over ", font=("Arial", 25))
        bouton1 = Button(self.root, text="Restart", font=("Arial", 15), background="light blue", width=10, command=select)
        bouton2 = Button(self.root, text="Quit", font=("Arial", 15), background="light blue", width=10, command=exit)
        label1.pack()
        bouton1.place(x=65, y=100)
        bouton2.place(x=65, y=175)
        self.root.mainloop()

    def gamewin_menu(self):
        # in waiting time, pause the enemy create event to avoid create enemy before menu selection
        pygame.time.set_timer(self.game.enemycreate_event, 0)
        self.tk_init()
        if self.game.level == 3:
            self.game.respawn()
            # destroy previous menu, reinitialize start menu
            def handle():
                self.root.destroy()
                self.tk_init()
                self.start_menu()
            label1 = Label(self.root, text="You won the game", font=("Arial", 25))
            bouton1 = Button(self.root, text="Main menu", font=("Arial", 15), background="light blue", width=10, command=handle)               
        elif self.game.level == 1:
            # go to next level, redraw the sprites
            def handle():
                self.game.level2()
                self.game.respawn()
            label1 = Label(self.root, text="You won level 1", font=("Arial", 25))        
            bouton1 = Button(self.root, text="Level 2", font=("Arial", 15), background="light blue", width=10, command=handle) 
        elif self.game.level == 2:
            # go to next level, redraw the sprites
            def handle():
                self.game.level3()
                self.game.respawn()
            label1 = Label(self.root, text="You won level 2", font=("Arial", 25))
            bouton1 = Button(self.root, text="Level 3", font=("Arial", 15), background="light blue", width=10, command=handle) 
        bouton2 = Button(self.root, text="Quit", font=("Arial", 15), background="light blue", width=10, command=exit)
        label1.pack()
        bouton1.place(x=65, y=100)
        bouton2.place(x=65, y=175)
        self.root.mainloop()

W = 700
H = 400

menu = Menu()
menu.start_menu()
