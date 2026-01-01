from src.settings import *
from src.systems.timer import Timer
from src.systems.collision import Collision
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("assets/sprites/Tabitha-fixed.png").convert_alpha()

        # rect
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        # movement
        self.pos = pos
        self.direction = vector()
        self.speed = 400
        self.gravity = 1000
        self.actual_dx = 0
        self.actual_dy = 0
        self.jump = False
        self.jump_height = 600

        # collision
        self.collision_sprites = Collision(collision_sprites)
        self.on_surface = {'floor': False, 'left': False, 'right': False}

        # timer
        self.timers = {
            'wall jump': Timer(300),
            'jump wait': Timer(50)
        }
        # animations
        self.animations = {
            'idle': [],
            'walk': [],
            'walk_back': []
        }

        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 10  # adjust if too fast/slow

        # load frames
        self.animations['idle'] = self.load_frames('assets/sprites/tabitha_standing_animation')
        self.animations['walk'] = self.load_frames('assets/sprites/tabitha_running_animation')
        self.animations['walk_back'] = self.load_frames('assets/sprites/tabitha_running_back_animation')

        # start with first idle frame
        self.image = self.animations['idle'][0]


    def load_frames(self, path):
        frames = []
        for filename in sorted(os.listdir(path)):
            img = pygame.image.load(path + '/' + filename).convert_alpha()
            frames.append(img)
        return frames

    def get_status(self):
        if self.direction.x > 0:
            self.status = 'walk'
        elif self.direction.x < 0:
            self.status = 'walk_back'
        else:
            self.status = 'idle'


    def animate(self, dt):
        frames = self.animations[self.status]

        # different speeds per animation
        if self.status == 'idle':
            speed = 2      # slow
        elif self.status in ('walk', 'walk_back'):
            speed = 10     # normal
        else:
            speed = 10

        self.frame_index += speed * dt

        if self.frame_index >= len(frames):
            self.frame_index = 0

        # rect update
        self.image = frames[int(self.frame_index)]


    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        if not self.timers['wall jump'].active:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                input_vector.x += 1
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                input_vector.x -= 1

            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE]:
            self.jump = True

    def move(self, dt):
        # horizontal
        old_x = self.rect.x
        self.rect.x += self.direction.x * self.speed * dt
        self.collision_sprites.resolve(self.rect, self.old_rect, 'horizontal')
        self.actual_dx = self.rect.x - old_x

        # vertical
        old_y = self.rect.y
        self.direction.y += self.gravity * dt
        # sliding on walls yeah
        if (not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and self.direction.y > 0):
            self.direction.y = min(self.direction.y, self.gravity * 0.1)
        self.rect.y += self.direction.y * dt


        hit_vertical = self.collision_sprites.resolve(self.rect, self.old_rect, 'vertical')
        if hit_vertical:
            self.direction.y = 0
        self.actual_dy = self.rect.y - old_y


    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.on_surface = self.collision_sprites.check_contact(self.rect)
        self.get_status()
        self.animate(dt)

        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['jump wait'].activate()
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['jump wait'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False

