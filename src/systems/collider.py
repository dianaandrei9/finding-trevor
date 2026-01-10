from src.settings import *

# invisible collider sprite for handling collisions
class Collider(pygame.sprite.Sprite):
    def __init__(self, rect, groups):
        super().__init__(groups)
        self.rect = rect
        self.old_rect = self.rect.copy()
