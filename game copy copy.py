"""
class Menu:
    start_menu()
    gameover_menu()
    gamewin_menu()

class Game:
    start_game()
    event_handle()
    menu()
    update_scene()

class Player:
    set_pos()
    move()
    attack()
    health_check()
    update()

class Enemy:
    move()
    hit()
    update()
"""

import pygame
from pygame import *
from tkinter import *

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("background.png")
        self.rect = self.image.get_rect(topleft=(0, 0))

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ground.png")
        self.rect = self.image.get_rect(center=(350, 350))

class HealthBar(pygame.sprite.Sprite):
    # health bar animation
    health_ani = [pygame.image.load("heart0.png"), pygame.image.load("heart.png"),
                pygame.image.load("heart2.png"), pygame.image.load("heart3.png"),
                pygame.image.load("heart4.png"), pygame.image.load("heart5.png")]
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("heart5.png")
        self.rect = self.image.get_rect(topleft=(10, 10))

class Player(pygame.sprite.Sprite):
    # taken from https://coderslegacy.com/python/pygame-rpg-movement-animations/
    # move animation for the right
    move_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Sprite2_R.png"),
                pygame.image.load("Player_Sprite3_R.png"), pygame.image.load("Player_Sprite4_R.png"),
                pygame.image.load("Player_Sprite5_R.png"), pygame.image.load("Player_Sprite6_R.png"),
                pygame.image.load("Player_Sprite_R.png")]

    # move animation for the left
    move_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Sprite2_L.png"),
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

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect(topleft=(W/2, 265))
        self.position = Vector2(W/2, 265)
        self.velocity = Vector2(0, 0)
        self.direction = True
        self.moving = True
        self.attacking = False
        self.move_frame = 0
        self.attack_frame = 0
        self.health = 5
        self.hitpause = False

    def get_pos(self):
        self.acceleration = Vector2(0, 0)
        self.pressed_keys = pygame.key.get_pressed()

        # Accelerates the player in the direction of the key press
        if self.pressed_keys[K_RIGHT]:
            self.acceleration.x = 0.2
        elif self.pressed_keys[K_LEFT]:
            self.acceleration.x = -0.2

        # calculate the velocity
        self.velocity += self.acceleration
        self.velocity.x *= 0.95

        self.position += self.velocity
        self.rect.topleft = self.position

        # keep player inside the screen
        if self.position.x > W:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = W

    def move(self):
        # reset move frame
        if self.move_frame > 6:
            self.move_frame = 0
            
        # move player to next frame
        if self.velocity.x > 0.2:
            self.image = self.move_ani_R[self.move_frame]
            self.direction = True
            self.move_frame += 1
        elif self.velocity.x < -0.2:
            self.image = self.move_ani_L[self.move_frame]
            self.direction = False
            self.move_frame += 1
        else:
            if self.direction:
                self.image = self.move_ani_R[0]
            else:
                self.image = self.move_ani_L[0]

    def attack(self):
        # taken from https://coderslegacy.com/python/pygame-rpg-attack-animations/
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
        # check direction for good display
        if self.direction:
            self.image = self.attack_ani_R[self.attack_frame]
        else:
            self.image = self.attack_ani_L[self.attack_frame]
        self.attack_frame += 1

    def hit(self):
        # taken from https://coderslegacy.com/python/pygame-rpg-health-bar/
        #to avoid hit continually, set pausehit switch, allow detect hit after 1 second
        if self.hitpause == False:
            self.hitpause = True
            self.health -= 1
            pygame.time.set_timer(game.hitpause_event, 1000)

        if self.health <= 0:
            self.kill()
            menu.gameover_menu()
       
    def update(self):
        self.get_pos()
        self.move()
        if self.attacking == True:
            self.attack()

    def respawn(self):
        game.sprites.add(self)
        game.playergroup.add(self)
        self.health = 5
        for sprite in game.sprites:
            if type(sprite) is Enemy:
                sprite.kill() 

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect(topleft=(W-30, 255))
        self.position = Vector2(W-30, 255)
        self.velocity = Vector2(3, 0)
        self.direction = True

    def move(self):
        #verify if position is out of range
        if self.position.x < 0:
            self.position.x = 0
            self.direction = False
        elif self.position.x > W-30:
            self.position.x = W-30
            self.direction = True

        if self.direction:
            self.position.x -= self.velocity.x
        else:
            self.position.x += self.velocity.x
        self.rect.topleft = self.position
    
    def hit(self):
        hit = pygame.sprite.spritecollide(self, game.playergroup, False)
        if hit and game.player.attacking == True:
            self.kill()
            game.dead_enemy_count += 1
        if game.dead_enemy_count == game.enemy_num:
            menu.gamewin_menu()
        if hit and game.player.attacking == False:
            game.player.hit()

    def update(self):
        self.move()
        self.hit()

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((W, H))
        self.sprites = pygame.sprite.LayeredUpdates()
        self.player = Player()
        self.playergroup = pygame.sprite.GroupSingle(self.player)
        self.ground = Ground()
        self.groundgroup = pygame.sprite.GroupSingle(self.ground)
        self.healthbar = HealthBar()
        self.background = Background()
        self.sprites.add(self.background, self.ground, self.player, self.healthbar)
        self.run_game = True
        self.enemycreate_event = pygame.USEREVENT + 1
        self.hitpause_event = pygame.USEREVENT + 2
    
    def start_game(self):
        while self.run_game:
            self.update_scene()

    def update_scene(self):
        self.clock.tick(60)
        self.healthbar.image = self.healthbar.health_ani[self.player.health]

        self.event_handle()
        self.sprites.draw(self.surface)
        self.sprites.update()
        pygame.display.update()

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_game = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_a:
                    if not self.player.attacking:
                        self.player.attack()
                        self.player.attacking = True 
            if event.type == self.enemycreate_event:
                if self.enemy_count < self.enemy_num:
                    self.sprites.add(Enemy())
                    self.enemy_count += 1
            if event.type == self.hitpause_event:
                self.player.hitpause = False

    def level1(self):
        menu.root.destroy()        
        pygame.time.set_timer(self.enemycreate_event, 1200)
        self.background.image = pygame.image.load("background.png")
        self.ground.image = pygame.image.load("ground.png")
        self.level = 1
        self.enemy_num = 5
        self.enemy_count = 0
        self.dead_enemy_count = 0

    def level2(self):
        menu.root.destroy()
        pygame.time.set_timer(self.enemycreate_event, 1000)
        self.background.image = pygame.image.load("desert.jpg")
        self.ground.image = pygame.image.load("desert_ground.png")
        self.level = 2
        self.enemy_num = 8
        self.enemy_count = 0
        self.dead_enemy_count = 0

    def level3(self):
        menu.root.destroy()
        pygame.time.set_timer(self.enemycreate_event, 800)
        self.background.image = pygame.image.load("dark.png")
        self.ground.image = pygame.image.load("darkground.png")
        self.level = 3
        self.enemy_num = 12
        self.enemy_count = 0
        self.dead_enemy_count = 0

class Menu:
    def __init__(self):
        self.tk_init()        

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
                game.level1()
            if s == 2:
                game.level2()
            if s == 3:
                game.level3()
            game.start_game()
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
        pygame.time.set_timer(game.enemycreate_event, 0)
        self.tk_init()
        def select():
            game.player.respawn()
            if game.level == 1:
                game.level1()
            if game.level == 2:
                game.level2()
            if game.level == 3:
                game.level3()
        # create gameover label and restart game button
        label1 = Label(self.root, text=" Game Over ", font=("Arial", 25))
        bouton1 = Button(self.root, text="Restart", font=("Arial", 15), background="light blue", width=10,
                        command=select)
        bouton2 = Button(self.root, text="Quit", font=("Arial", 15), background="light blue", width=10, command=exit)
        label1.pack()
        bouton1.place(x=65, y=100)
        bouton2.place(x=65, y=175)
        self.root.mainloop()

    def gamewin_menu(self):
        pygame.time.set_timer(game.enemycreate_event, 0)
        self.tk_init()
        if game.level == 3:
            game.player.respawn()
            def handle():
                self.root.destroy()
                self.tk_init()
                self.start_menu()
            label1 = Label(self.root, text="You won the game", font=("Arial", 25))
            bouton1 = Button(self.root, text="Main menu", font=("Arial", 15), background="light blue", width=10,
                            command=handle)               
        elif game.level == 1:
            def handle():
                game.level2()
                game.player.respawn()
            label1 = Label(self.root, text="You won level 1", font=("Arial", 25))
        
            bouton1 = Button(self.root, text="Level 2", font=("Arial", 15), background="light blue", width=10,
                            command=handle) 
        elif game.level == 2:
            def handle():
                game.level3()
                game.player.respawn()
            label1 = Label(self.root, text="You won level 2", font=("Arial", 25))
            bouton1 = Button(self.root, text="Level 3", font=("Arial", 15), background="light blue", width=10,
                            command=handle) 
        bouton2 = Button(self.root, text="Quit", font=("Arial", 15), background="light blue", width=10,
                            command=exit)
        label1.pack()
        bouton1.place(x=65, y=100)
        bouton2.place(x=65, y=175)

        self.root.mainloop()

W = 700
H = 350

game = Game()
menu = Menu()
menu.start_menu()