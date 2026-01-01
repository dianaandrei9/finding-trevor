from src.settings import *
from src.levels.level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

class Game:
    def __init__(self):
        pygame.init()

        # resizable window
        self.window = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Finding Trevor")

        # internal surf
        self.screen = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        # TMX
        self.tmx_maps = {0: load_pygame(join("assets", "maps", "levels", "level_1.tmx"))}
        self.current_stage = Level(self.tmx_maps[0], self.screen)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            self.handle_events()
            # camera stuff not yet
            self.current_stage.update(dt)
            
            self.screen.fill((53, 58, 26))
            self.current_stage.run(dt)

            self.present()
            pygame.display.update()
            
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:
                # recreate window with new dim
                self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self._last_scaled_size = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def present(self):
        win_w, win_h = self.window.get_size()

        # keep aspect ratio
        scale = min(win_w / BASE_WIDTH, win_h / BASE_HEIGHT)
        new_w = int(BASE_WIDTH * scale)
        new_h = int(BASE_HEIGHT * scale)

        scaled = pygame.transform.smoothscale(self.screen, (new_w, new_h))
        
        x = (win_w - new_w) // 2
        y = (win_h - new_h) // 2

        self.window.fill((53, 58, 26))
        self.window.blit(scaled, (x, y))
