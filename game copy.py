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
        self._layer = -1

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ground.png")
        self.rect = self.image.get_rect(center=(350, 350))

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((W, H))
        self.sprites = pygame.sprite.LayeredUpdates()
        self.sprites.add(Background(), Ground())
        self.running = True

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def start_game(self):
        while self.running:
            self.tick()

    def tick(self):
        self.event_handle()
        self.sprites.draw(self.surface)
        pygame.display.update()

W = 700
H = 350
game = Game()
game.start_game()