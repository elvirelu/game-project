from operator import truediv
from pickle import FALSE, TRUE
import pygame
pygame.init()


#game windows
screen_width = 800
screen_height= 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')


#Background image
background_img = pygame.image.load('img/Background/Background.png').convert_alpha()


#function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))

run = TRUE
while run:
    #draw background
    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = FALSE

    pygame.display.update()        

pygame.quit()            
