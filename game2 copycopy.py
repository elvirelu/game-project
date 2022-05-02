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

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect(topleft=position)
        self.position = position
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.direction = True
        self._layer = 1

    def update(self, delta_time):
        self.move()
        self.rect.center = (round(self.position.x), round(self.position.y))

    def move(self):
        self.acceleration = Vector2(0, GRAV)
        # taken from https://coderslegacy.com/python/pygame-gravity-and-jumping/
        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        # Accelerates the player in the direction of the key press
        if pressed_keys[K_RIGHT]:
            self.acceleration.x = 0.3
        if pressed_keys[K_LEFT]:
            self.acceleration.x = -0.3
        if pressed_keys[K_SPACE]:
            self.acceleration.y = -1
        
        self.velocity += self.acceleration
        self.velocity.x *= 1 - FRIC

        hits = pygame.sprite.spritecollide(self, game.current_scene.ground, False)
        # check if touch the ground, then stop
        if self.velocity.y > 0:
            if hits:
                if self.rect.bottom > hits[0].rect.top:
                    self.position.y = hits[0].rect.top - self.rect.height / 2
                    self.velocity.y = 0

        self.position += self.velocity
        if self.direction:
            self.image = pygame.image.load("Player_Sprite_R.png")
        else:
            self.image = pygame.image.load("Player_Sprite_L.png")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect(topleft=position)

    def update(self, delta_time):
        self.rect.y += 1

class Ground(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("Ground.png")
        self.rect = self.image.get_rect(center=position)

class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.LayeredUpdates()
        self.display = pygame.display.set_mode((W, H))
        self.framebuffer = self.display.copy()
        self.ui_manager = pygame_gui.UIManager((W, H))
        self.current_scene = None

    def run(self):
        self.shake = False
        self.current_scene = TitleScene()
        self.offset = (0, 0)
        while self.running:
            self.tick()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.ui_manager.process_events(event)
            self.current_scene.process_events(event)

    def tick(self):
        delta_time = self.clock.tick(FPS)/1000.0
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
FPS = 120
FRIC = 0.05
GRAV = 0.5

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

if __name__ == '__main__':
    game = Game()
    game.run()