from src.settings import *
from os.path import join

class Health:
    def __init__(self, screen, health, max_health):
        self.health = health
        self.max_health = max_health
        self.screen = screen
        self.full_heart = pygame.image.load(join("assets", "graphics", "full_heart.png")).convert_alpha()
        self.empty_heart = pygame.image.load(join("assets", "graphics", "empty_heart.png")).convert_alpha()
    
    def set_health(self, health):
        self.health = max(0, min(health, self.max_health))
                 
    def empty_hearts(self):
        for heart in range(self.max_health):
            if heart < self.health:
                self.screen.blit(self.full_heart, (heart * 55 + 10, 30))
            else:
                self.screen.blit(self.empty_heart, (heart * 55 + 10, 30))
