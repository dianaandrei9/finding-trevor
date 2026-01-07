from src.settings import *
from src.levels.level import Level
from src.levels.level_manager import LevelManager
from pytmx.util_pygame import load_pygame
from os.path import join
from src.ui.menu import MainMenu
from src.story.cutscene_start import StartCutscene
from src.story.cutscene_end import EndCutscene
from src.story.cutscene_frames import load_cutscene_frames
from src.story.end_credits import EndCredits, CREDITS

class Game:
    def __init__(self):
        pygame.init()

        # resizable window
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Finding Trevor")
        
        # cutscenes
        load_cutscene_frames()
        self.credits = None
               
        # set window icon
        icon = pygame.image.load(join("assets", "graphics", "Trev_32x32.png")).convert_alpha()
        pygame.display.set_icon(icon)
        
        # internal surf
        self.screen = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = "menu"
        self.cutscene = StartCutscene(self.screen)

        # MENU
        self.menu = MainMenu(self.screen)
        
        # TMX    
        self.level_manager = LevelManager(self.screen)


    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()

            self.screen.fill((53, 58, 26))

            # MENU STATE
            if self.state == "menu":
                result = self.menu.run()

                if result == "start_game":
                    self.state = "cutscene"
                    continue  # skip drawing the menu frame

            # CUTSCENE STATE
            if self.state == "cutscene":
                self.cutscene.update(dt)

                # draw cutscene frame
                self.cutscene.draw()

                # move on when cutscene ends
                if self.cutscene.end:
                    self.state = "game"

                self.present()
                pygame.display.update()
                continue 

            # END CUTSCENE STATE
            if self.state == "end_cutscene":
                self.cutscene.update(dt)
                self.cutscene.draw()

                # when end cutscene finishes → quit game
                if self.cutscene.end:
                    self.credits = EndCredits(self.screen, CREDITS)
                    self.state = "credits"

                self.present()
                pygame.display.update()
                continue
            
            # END CREDITS
            if self.state == "credits":
                self.credits.update(dt)
                self.credits.draw()

                if self.credits.finished():
                    pygame.quit()
                    sys.exit()

                self.present()
                pygame.display.update()
                continue

            # GAME STATE
            if self.state == "game":
                result = self.level_manager.update(dt)
                self.level_manager.draw(dt)
                if result == "game_over":
                    self.state = "menu"
                    continue
                if result == "end_cutscene":
                    self.cutscene = EndCutscene(self.screen)
                    self.state = "end_cutscene"
                    continue

            self.present()
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def start_credits(self):
        self.credits = EndCredits(self.screen, CREDITS)
        self.state = "credits"


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # skip cutscene
                if event.key == pygame.K_SPACE:
                    if self.state == "cutscene":
                        self.cutscene.check(True)
                    elif self.state == "end_cutscene":
                        self.cutscene.check(True)
                        self.start_credits()

                # END OR START CUTSCENE
                if self.state in ("cutscene", "end_cutscene"):
                    self.cutscene.check(False)

                # END CUTSCENE
                if event.key == pygame.K_SPACE and self.state == "end_cutscene":
                    self.start_credits()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state in ("cutscene", "end_cutscene"):
                    self.cutscene.check(False)
                if self.state == "end_cutscene":
                    self.start_credits()
                elif self.state == "credits":
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
