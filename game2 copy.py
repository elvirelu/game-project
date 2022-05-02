import random
import pygame
import pygame_gui

class TitleScene():
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
        #game.sprites.add(Enemy((0, 0)))
        game.sprites.add(Player((0, 0)))
        game.sprites.add(Ground((350, 350)))
        game.sprites.add(Background())

    def update(self):
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

class GameScene():
    def __init__(self):
        game.sprites.add(Player())
        pass
    def update(self, delta_time):
        pass
    def process_events(self, event):
        pass
    def cleanup(self):
        pass

class Player(pygame.sprite.DirtySprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_L.png")
        self.rect = self.image.get_rect(topleft=position)

    def update(self):
        self.rect.y += 1
        self.dirty = 1

class Enemy(pygame.sprite.DirtySprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect(topleft=position)

    def update(self):
        self.rect.y += 1
        self.dirty = 1

class Background(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("Background.png")

class Ground(pygame.sprite.DirtySprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("Ground.png")
        self.rect = self.image.get_rect(center=position)

class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.LayeredDirty()
        self.display = pygame.display.set_mode((W, H))
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
        self.handle_events()
        self.ui_manager.update()
        self.sprites.update()
        self.current_scene.update()
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