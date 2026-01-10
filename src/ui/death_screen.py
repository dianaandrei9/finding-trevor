from src.settings import *

class GameOverMenu:
    def __init__(self, screen):
        self.screen = screen

        # overlay
        self.overlay = pygame.Surface((BASE_WIDTH, BASE_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((50, 50, 50, 180))

        # text
        self.font = pygame.font.SysFont(None, 72)
        self.text = self.font.render("You Died", True, (255, 0, 0))
        self.text_rect = self.text.get_rect(center=(BASE_WIDTH//2, BASE_HEIGHT//2 - 50))

        # load button images
        self.button_restart = pygame.image.load("assets/ui/restart_button.png").convert_alpha()
        self.button_restart_hover = pygame.image.load("assets/ui/restart_button_touch.png").convert_alpha()

        scale = 3
        w, h = self.button_restart.get_size()
        self.button_restart = pygame.transform.scale(self.button_restart, (w*scale, h*scale))
        self.button_restart_hover = pygame.transform.scale(self.button_restart_hover, (w*scale, h*scale))

        # button rect
        self.restart_rect = self.button_restart.get_rect(center=(BASE_WIDTH//2, BASE_HEIGHT//2 + 50))

    def run(self):
        # mouse input
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # convert window mouse position -> internal screen coords
        win_w, win_h = pygame.display.get_surface().get_size()
        scale = min(win_w / BASE_WIDTH, win_h / BASE_HEIGHT)
        offset_x = (win_w - BASE_WIDTH * scale) / 2
        offset_y = (win_h - BASE_HEIGHT * scale) / 2
        mouse_x = (mouse_pos[0] - offset_x) / scale
        mouse_y = (mouse_pos[1] - offset_y) / scale
        mouse_scaled = (mouse_x, mouse_y)

        # draw background
        self.screen.blit(self.overlay, (0, 0))
        self.screen.blit(self.text, self.text_rect)

        # button hover and click
        if self.restart_rect.collidepoint(mouse_scaled):
            self.screen.blit(self.button_restart_hover, self.restart_rect)
            if mouse_click:
                return "restart"
        else:
            self.screen.blit(self.button_restart, self.restart_rect)

        return "game_over"
