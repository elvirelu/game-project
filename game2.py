from abc import ABC, abstractmethod
import random
import pygame
import pygame_gui

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
        game.sprites.add(Enemy((0, 0)))
        game.background = pygame.transform.scale(pygame.image.load("background.png"), (W, H))

    def update(self, delta_time):
        pass

    def process_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    print("gamescene")
                    game.current_scene = GameScene()
                    self.cleanup()
                elif event.ui_element == self.shake_button:
                    game.shake = not game.shake
                elif event.ui_element == self.exit_button:
                    game.running = False

    def cleanup(self):
        super().cleanup()
        self.start_button.kill()
        self.shake_button.kill()
        self.exit_button.kill()

class GameScene(Scene):
    def __init__(self):
        game.sprites.add(Player())
        pass
    def update(self, delta_time):
        pass
    def process_events(self, event):
        pass
    def cleanup(self):
        pass

class Enemy(pygame.sprite.DirtySprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect(topleft=position)

    def update(self, delta_time):
        self.rect.y += 1
        self.dirty = 1

class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.LayeredDirty()
        self.display = pygame.display.set_mode((W, H), pygame.SCALED)
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

        rects = self.sprites.draw(self.framebuffer, self.background)
        self.display.blit(self.framebuffer, self.offset)
        self.ui_manager.draw_ui(self.display)
        pygame.display.update(rects)

W = 700
H = 350
FPS = 120

if __name__ == '__main__':
    game = Game()
    game.run()