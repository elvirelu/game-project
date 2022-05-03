"""
class Game:
    show_gamewindow()
    start_game()
    event_handle()
    menu()
    update_scene()

class Player:
    move()
    run()
    attack()
    health_check()
    update()

class Enemy:
    move()
    update()
"""

import pygame
from pygame import *

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

class Player(pygame.sprite.Sprite):
    # taken from https://coderslegacy.com/python/pygame-rpg-movement-animations/
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

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect(topleft=(350, 0))
        self.position = (350, 0)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.direction = True
        self.attacking = False
        self.move_frame = 0
        self.attack_frame = 0
        
    def move(self):
        self.acceleration = Vector2(0, 0.5)

        # Returns the current key presses
        self.pressed_keys = pygame.key.get_pressed()

        # Accelerates the player in the direction of the key press
        if self.pressed_keys[K_RIGHT]:
            self.acceleration.x = 0.2
        elif self.pressed_keys[K_LEFT]:
            self.acceleration.x = -0.2

        # calculate the velocity
        self.velocity += self.acceleration
        self.velocity.x *= 0.95

        hits = pygame.sprite.spritecollide(self, game.ground, False)
        # check if touch the ground, if touch, disable the velocity of direction y
        if self.velocity.y > 0:
            if hits:
                if self.rect.bottom > hits[0].rect.top:
                    self.position.y = hits[0].rect.top - self.rect.height / 2
                    self.velocity.y = 0

        self.position += self.velocity
        self.rect.center = (round(self.position.x), round(self.position.y))

        # keep player inside the screen
        if self.position.x > W:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = W

    def run(self):
        # reset move frame
        if self.move_frame > 6:
            self.move_frame = 0

        # move player to next frame
        if self.velocity.x > 0.2:
            self.image = self.run_ani_R[self.move_frame]
            self.direction = True
        elif self.velocity.x < -0.2:
            self.image = self.run_ani_L[self.move_frame]
            self.direction = False
        else:
            if self.direction:
                self.image = self.run_ani_R[0]
            else:
                self.image = self.run_ani_L[0]
        self.move_frame += 1
        
    def attack(self):
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
        # check direction for good display
        if self.direction:
            self.image = self.attack_ani_R[self.attack_frame]
        else:
            self.image = self.attack_ani_L[self.attack_frame]
        self.attack_frame += 1
        
    def update(self):
        self.move()
        self.run()
        if self.attacking == True:
            self.attack()

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((W, H))
        self.sprites = pygame.sprite.LayeredUpdates()
        self.player = Player()
        self.ground = pygame.sprite.GroupSingle(Ground())
        self.sprites.add(Background(), self.ground, self.player)
        self.running = True

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_a:
                    if not self.player.attacking:
                        self.player.attack()
                        self.player.attacking = True 
    
    def start_game(self):
        while self.running:
            self.tick()

    def tick(self):
        self.clock.tick(60)
        self.event_handle()
        self.sprites.draw(self.surface)
        self.sprites.update()
        pygame.display.update()

W = 700
H = 350
game = Game()
game.start_game()