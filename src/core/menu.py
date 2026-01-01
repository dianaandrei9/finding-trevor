import pygame
from src.settings import BASE_WIDTH, BASE_HEIGHT

class MainMenu:
    def __init__(self, screen):
        self.screen = screen

        # load background
        self.bg = pygame.image.load("assets/ui/menu_background.png").convert()

        # load button images
        self.button_start = pygame.image.load("assets/ui/start_button.png").convert_alpha()
        self.button_start_hover = pygame.image.load("assets/ui/start_button_touch.png").convert_alpha()

        scale = 5
        w, h = self.button_start.get_size()
        self.button_start = pygame.transform.scale(self.button_start, (w*scale, h*scale))
        self.button_start_hover = pygame.transform.scale(self.button_start_hover, (w*scale, h*scale))


        # button rect
        self.start_rect = self.button_start.get_rect(midleft=(120, self.screen.get_height() // 2))

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # convert window mouse position → internal screen coords
        win_w, win_h = pygame.display.get_surface().get_size()
        scale = min(win_w / BASE_WIDTH, win_h / BASE_HEIGHT)

        offset_x = (win_w - BASE_WIDTH * scale) / 2
        offset_y = (win_h - BASE_HEIGHT * scale) / 2

        mouse_x = (mouse_pos[0] - offset_x) / scale
        mouse_y = (mouse_pos[1] - offset_y) / scale
        mouse_scaled = (mouse_x, mouse_y)

        # draw background
        self.screen.blit(self.bg, (0, 0))

        # hover + click detection using scaled coords
        if self.start_rect.collidepoint(mouse_scaled):
            self.screen.blit(self.button_start_hover, self.start_rect)
            if mouse_click:
                return "start_game"
        else:
            self.screen.blit(self.button_start, self.start_rect)

        return "menu"