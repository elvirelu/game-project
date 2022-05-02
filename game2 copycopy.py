from abc import ABC, abstractmethod
import random
import pygame
import pygame_gui
from pygame import *

class Scene(ABC):
    @abstractmethod
    def update(self, delta_time):
        pass

    @abstractmethod
    def process_events(self, event):
        pass

    @abstractmethod
    def cleanup(self):
        game.sprites.empty()

class TitleScene(Scene):
    def __init__(self):
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Start Game',
                                             manager=game.ui_manager)
        self.shake_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 275), (100, 50)),
                                             text='Shake',
                                             manager=game.ui_manager)
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 275), (100, 50)),
                                             text='Exit Game',
                                             manager=game.ui_manager)

        game.sprites.add(Background())

    def update(self, delta_time):
        pass

    def process_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    self.cleanup()
                    game.current_scene = GameScene()
                elif event.ui_element == self.shake_button:
                    game.shake = not game.shake
                elif event.ui_element == self.exit_button:
                    game.running = False

    def cleanup(self):
        super().cleanup()
        self.start_button.kill()
        self.shake_button.kill()
        self.exit_button.kill()
        pygame.display.update()

class GameScene(Scene):
    def __init__(self):
        self.ground = pygame.sprite.GroupSingle(Ground((350, 350)))
        game.sprites.add(Player((W/2, 0)), self.ground, Background())

    def update(self, delta_time):
        pass
    def process_events(self, event):
        pass
    def cleanup(self):
        pass

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("background.png"), (W, H))
        self.rect = self.image.get_rect(topleft=(0, 0))
        self._layer=-1


class Ground(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("Ground.png")
        self.rect = self.image.get_rect(center=position)


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

    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect(topleft=position)
        self.position = position
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.direction = True
        self.attacking = False
        self.move_frame = 0
        self.attack_fram = 0
        self._layer = 1

    def update(self, delta_time):
        self.move()
        self.run()
        
    def move(self):
        self.acceleration = Vector2(0, 0.5)

        # Returns the current key presses
        self.pressed_keys = pygame.key.get_pressed()

        # Accelerates the player in the direction of the key press
        if self.pressed_keys[K_RIGHT]:
            self.acceleration.x = 0.3
        elif self.pressed_keys[K_LEFT]:
            self.acceleration.x = -0.3

        # calculate the velocity
        self.velocity += self.acceleration
        self.velocity.x *= 0.95

        hits = pygame.sprite.spritecollide(self, game.current_scene.ground, False)
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
        if self.velocity.x > 0.3:
            self.image = self.run_ani_R[self.move_frame]
            self.direction = True
        elif self.velocity.x < -0.3:
            self.image = self.run_ani_L[self.move_frame]
            self.direction = False
        else:
            if self.direction:
                self.image = self.run_ani_R[0]
            else:
                self.image = self.run_ani_L[0]
        self.move_frame += 1
        
    def attack(self):
        # return to base frame
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
        # check direction for good display
        if self.direction:
            self.image = self.attack_ani_R[self.attack_frame]
        else:
            self.image = self.attack_ani_L[self.attack_frame]
        self.attack_frame += 1
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect(topleft=position)

    def update(self, delta_time):
        self.rect.y += 1

class Game():

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.LayeredUpdates()
        self.display = pygame.display.set_mode((W, H))
        self.framebuffer = self.display.copy()
        self.ui_manager = pygame_gui.UIManager((W, H))
        self.current_scene = None

    def start(self):
        self.shake = False
        self.current_scene = TitleScene()
        self.offset = (0, 0)
        while True:
            self.tick()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_a:
                    pass
                    
            self.ui_manager.process_events(event)
            self.current_scene.process_events(event)

    def tick(self):
        delta_time = self.clock.tick(120)/1000
        self.handle_events()
        self.ui_manager.update(delta_time)
        self.sprites.update(delta_time)
        self.current_scene.update(delta_time)

        if self.shake:
            self.offset = (random.randrange(-5, 5), random.randrange(-5, 5))
        else:
            self.offset = (0, 0)

        self.framebuffer.fill(Color(0,0,0,0))
        self.sprites.draw(self.framebuffer)
        self.display.blit(self.framebuffer, self.offset)
        self.ui_manager.draw_ui(self.display)
        pygame.display.flip()
    
W = 700
H = 350

if __name__ == '__main__':
    game = Game()
    game.start()