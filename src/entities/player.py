from src.settings import *
from src.systems.timer import Timer
from src.systems.collision import Collision

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("assets/sprites/tabitha.png").convert_alpha()

        # rect
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        # movement
        self.direction = vector()
        self.speed = 300
        self.gravity = 350
        self.actual_dx = 0
        self.actual_dy = 0
        self.jump = False
        self.jump_height = 500

        # collision
        self.collision_sprites = Collision(collision_sprites)
        self.on_surface = {'floor': False, 'left': False, 'right': False}

        # timer
        self.timers = {
            'wall jump': Timer(300),
            'jump wait': Timer(250)
        }

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

        self.actual_dx = self.rect.x - old_x
        self.collision_sprites.resolve(self.rect, self.old_rect, 'horizontal')

        # vertical
        old_y = self.rect.y
        # sliding on walls yeah
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['jump wait'].active:
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt

        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['jump wait'].activate()
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['jump wait'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False

        self.actual_dy = self.rect.y - old_y
        hit_vertical = self.collision_sprites.resolve(self.rect, self.old_rect, 'vertical')
        if hit_vertical:
            self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.on_surface = self.collision_sprites.check_contact(self.rect)
