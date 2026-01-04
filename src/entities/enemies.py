from src.settings import *
from random import choice
from os import walk
from os.path import join

def import_folder(*path):
    frames = []
    for folder_path, subfolders, image_names in walk(join(*path)):
        for image_name in sorted(image_names, key = lambda name: int(name.split('-')[1].split('.')[0])):
            full_path = join(folder_path, image_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames

class Runner(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.frames, self.frame_index = import_folder('assets', 'sprites','enemies', 'runner', 'run'), 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = vector(self.rect.topleft)
        self.damage = 1

        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 200
        self.snap_to_ground()
        
        self.frames_right = self.frames
        self.frames_left = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        
        self.max_health = 2 # 2 hits and it dead i think it ok
        self.health = self.max_health
        self.is_dead = False

        # flashing
        self.original_frames = self.frames
        self.original_frames_left = self.frames_left
        self.original_frames_right = self.frames_right

        self.hit_flash_time = 0

        # invincibility after hit
        self.invincible = False
        self.invincible_time = 300  # ms
        self.invincible_timer = 0


    def snap_to_ground(self):
        while True:
            self.rect.y += 1
            if self.rect.collidelist(self.collision_rects) != -1:
                self.rect.y -= 1
                break

    def take_damage(self, amount):
        if self.is_dead or self.invincible:
            return

        self.health -= amount
        self.hit_flash_time = 120  # flash white
        self.invincible = True
        self.invincible_timer = self.invincible_time

        if self.health <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.kill()   # remove from game

    def update(self, dt):
        # animate
        self.frame_index += ANIMATION_SPEED * dt
        frames = self.frames_left if self.direction < 0 else self.frames_right
        self.image = frames[int(self.frame_index) % len(frames)]
        
        if self.invincible:
            self.invincible_timer -= dt * 1000
            if self.invincible_timer <= 0:
                self.invincible = False

        # hit flash
        if self.hit_flash_time > 0:
            self.hit_flash_time -= dt * 1000  # dt is seconds → convert to ms
            # flash white
            base_image = frames[int(self.frame_index) % len(frames)]
            self.image = base_image.copy()

            flash = pygame.Surface(self.image.get_size())
            flash.fill((255, 255, 255))
            flash.set_alpha(150)
            self.image.blit(flash, (0, 0))
        else:
            # restore original frames if needed
            self.image = frames[int(self.frame_index) % len(frames)]

        # move
        self.pos.x += self.direction * self.speed * dt
        self.rect.x = round(self.pos.x)

        # reverse direction (at the end of a cliff)
        floor_rect_right = pygame.Rect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.Rect(self.rect.bottomleft, (-1, 1))

        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0:
           self.direction = -1
        if floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0:
           self.direction = 1 
        
        
class Shooter(pygame.sprite.Sprite):
     def __init__(self, pos, groups, collision_sprites):
        pass
#         super().__init__(groups)
#         # self.frames, self.frame_index = frames, 0
#         # self.image = self.frames[self.frame_index] 
#         # self.rect = self.image.get_rect(topleft = pos)