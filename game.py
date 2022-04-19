import pygame as pg
from pygame.locals import *
import tkinter as tk
import sys

pg.init()
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.1
FPS = pg.time.Clock()
COUNT = 0

displaysurface = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Game")

class Background(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimg = pg.image.load("Background.png")
    
    def render(self):
        displaysurface.blit(self.bgimg, (0, 0))

class Ground(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gimg = pg.image.load("Ground.png")
        self.rect = self.gimg.get_rect(center = (350, 350))

    def render(self):
        displaysurface.blit(self.gimg, (self.rect.x, self.rect.y))

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

background = Background()
ground = Ground()



while 1:
    for event in pg.event.get():
        # quit when the close window button is clicked
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        
        # event handling for a range of different key presses
        if event.type == pg.KEYDOWN:
            pass
    
    background.render()
    ground.render()

    pg.display.update()
    FPS.tick(60)
        