from src.settings import *
from os.path import join

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups = None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        
class MovingSprite(Sprite):
    def __init__(self, groups, start_pos, end_pos, move_dir, speed, nr):
        surf =  pygame.image.load(join("assets", "graphics", f"platform{nr}.png"))
        super().__init__(start_pos, surf, groups)
        if move_dir == 'x':
            self.rect.midleft = start_pos
        
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        self.moving = True
        self.speed = speed
        if nr == 2:
            self.direction = vector(-1, 0) if move_dir == 'x' else vector(0, 1)
        else:
            self.direction = vector(1, 0) if move_dir == 'x' else vector(0, 1)
        self.move_dir = move_dir

    def check_border(self):
        if self.move_dir == 'x':
            left_bound  = min(self.start_pos[0], self.end_pos[0])
            right_bound = max(self.start_pos[0], self.end_pos[0])

            if self.rect.centerx >= right_bound and self.direction.x == 1:
                self.direction.x = -1
                self.rect.centerx = right_bound

            if self.rect.centerx <= left_bound and self.direction.x == -1:
                self.direction.x = 1
                self.rect.centerx = left_bound
                
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.check_border()
        