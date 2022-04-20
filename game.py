import pygame as pg
from pygame.locals import *
from tkinter import *
import sys

pg.init()

vec = pg.math.Vector2
W = 700
H = 350
ACC = 0.3
FRIC = -0.1
FPS = pg.time.Clock()
COUNT = 0

displaysurface = pg.display.set_mode((W,H))
pg.display.set_caption("Game")
        
class EventHandler():
    def __init__(self):
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.battle = False
        self.mode = 1
    
    def stage_handler(self):
        self.root = Tk()
        self.root.geometry("250x300+820+370")
        
        def select():
            s = var.get()
            if s == 1:
                self.easy_mode()
            if s == 2:
                self.medium_mode()
            if var.get() == 3:            
                self.hard_mode()
        var = IntVar()
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
        self.img = pg.image.load("Player_Sprite_R.png")
        self.rect = self.img.get_rect()

        self.pos = vec((340, 240))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "R"
        self.jumping = False
    
    def move(self):
        #add gravity so that player can touch the ground
        #self.acc = vec(0, 0.5)
        #calculate velocity
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc #update positon
        self.rect.midbottom = self.pos #update rect

    def update(self):
        pass

    def attack(self):
        pass

    def jump(self):
        pass

    def gravity_check(self):
        hits = pg.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.bottom + 1
                    self.vel.y = 0
                    self.jumping = False

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

background = Background()
ground = Ground()
ground_group = pg.sprite.Group()
ground_group.add(ground)
player = Player()
handler = EventHandler()
handler.stage_handler()

while 1:
    player.gravity_check()
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
    player.move()
    displaysurface.blit(player.img, player.rect)

    pg.display.update()
    FPS.tick(60)
        