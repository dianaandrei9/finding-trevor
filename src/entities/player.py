from src.settings import *
from src.systems.timer import Timer
from src.systems.collision import Collision
from src.systems.inventory import Inventory
from src.systems.magic_burst import MagicBurst
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, health, enemy_group):
        super().__init__(groups)
        self.image = pygame.image.load("assets/sprites/Tabitha-fixed.png").convert_alpha()
        
        # rect
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox_rect = self.rect.inflate(-5, 0)
        self.old_rect = self.rect.copy()

        # health
        self.health = health
        self.max_health = 3

        # attack
        self.attack = False
        self.attack_radius = 64 * 3

        # enemies
        self.enemy_group = enemy_group

        # inventory
        self.inventory = Inventory() 

        # movement
        self.pos = pos
        self.direction = vector()
        self.speed = 300
        self.gravity = 1050
        self.actual_dx = 0
        self.actual_dy = 0
        self.jump = False
        self.did_jump = False
        self.jump_height = 600
        self.platform = None

        self.hit_flash_time = 0
        self.hit_flash_duration = 60

        # invincibility - idk if necessary
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_time = 0.8
        
        # collision
        self.collision_sprites = Collision(collision_sprites)
        self.on_surface = {'floor': False, 'left': False, 'right': False}
 
        # timer
        self.timers = {
            'wall jump': Timer(300),
            'jump wait': Timer(50),
            'fall_delay': Timer(50),
            'land': Timer(120),
            'attack_cooldown': Timer(1500)
        }
        
        # animations
        self.animations = {
            'idle': [],
            'walk': [],
            'walk_back': [],
            'jump_right': [],
            'jump_left': [],
            'fall_right': [],
            'fall_left': []
        }

        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 10  # adjust if too fast/slow

        # load frames
        self.animations['idle'] = self.load_frames('assets/sprites/tabitha_standing_animation')
        self.animations['walk'] = self.load_frames('assets/sprites/tabitha_running_animation')
        self.animations['walk_back'] = self.load_frames('assets/sprites/tabitha_running_back_animation')
        self.animations['jump_right'] = self.load_frames("assets/sprites/tabitha_jump_animation")
        self.animations['jump_left'] = self.load_frames("assets/sprites/tabitha_jump_back_animation")
        self.animations['fall_right'] = self.load_frames("assets/sprites/tabitha_fall_animation")
        self.animations['fall_left'] = self.load_frames("assets/sprites/tabitha_fall_back_animation")
        self.animations["land"] = self.load_frames("assets/sprites/tabitha_land_animation")

        # start with first idle frame
        self.image = self.animations['idle'][0]


    def load_frames(self, path):
        frames = []
        for filename in sorted(os.listdir(path)):
            img = pygame.image.load(path + '/' + filename).convert_alpha()
            frames.append(img)
        return frames

    def get_status(self):

        # Landing - overwrites all
        if self.timers["land"].active:
            self.status = "land"
            return

        if self.direction.y < 0:
            self.status = "jump_left" if self.direction.x < 0 else "jump_right"
            return

        if not self.on_surface['floor'] and (self.on_surface['left'] or self.on_surface['right']):
            self.status = "idle"   # or a wall-slide animation later
            return

        if not self.on_surface['floor'] and self.direction.y > 0 and self.timers["fall_delay"].active:
            self.status = "jump_left" if self.direction.x < 0 else "jump_right"
            return

        if not self.on_surface['floor'] and self.direction.y > 0:
            self.status = "fall_left" if self.direction.x < 0 else "fall_right"
            return

        # Running on ground
        if self.direction.x > 0:
            self.status = "walk"
        elif self.direction.x < 0:
            self.status = "walk_back"
        else:
            self.status = "idle"


    def animate(self, dt):

        if self.status == "land":
            frames = self.animations["land"]
            speed = 3  # fast snap landing

            self.frame_index += speed * dt

            # stop at last frame (do NOT loop)
            if self.frame_index >= len(frames):
                self.frame_index = len(frames) - 1

            self.image = frames[int(self.frame_index)]
            return 

        frames = self.animations[self.status]

        # different speeds per animation
        if self.status == 'idle':
            speed = 2      # slow
        elif self.status in ('walk', 'walk_back'):
            speed = 10     # normal
        elif self.status in ('jump_right', 'jump_left'):
            speed = 4
        elif self.status in ('fall_right', 'fall_left'):
            speed = 6
        else:
            speed = 10

        self.frame_index += speed * dt

        if self.status in ('jump_right', 'jump_left'):
            max_jump_frames = 5  # frames 0,1,2,3,4

            if self.frame_index >= max_jump_frames:
                self.frame_index = max_jump_frames - 1  # freeze on frame 4

            self.image = frames[int(self.frame_index)]
            return

        # rect update
        if self.frame_index >= len(frames):
            self.frame_index = 0
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
        
        if keys[pygame.K_x]:
            self.attack = True

            
    def move(self, dt):
        # horizontal
        old_x = self.hitbox_rect.x
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision_sprites.resolve(self.hitbox_rect, self.old_rect, 'horizontal')
        self.actual_dx = self.hitbox_rect.x - old_x

        # vertical
        old_y = self.hitbox_rect.y
        self.direction.y += self.gravity * dt
        # sliding on walls yeah
        if (not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and self.direction.y > 0):
            self.direction.y = min(self.direction.y, self.gravity * 0.1)
        self.hitbox_rect.y += self.direction.y * dt


        hit_vertical = self.collision_sprites.resolve(self.hitbox_rect, self.old_rect, 'vertical')
        if hit_vertical:
            self.direction.y = 0
        self.actual_dy = self.hitbox_rect.y - old_y
        self.rect.center = self.hitbox_rect.center

    def platform_move(self):
        if self.platform and self.on_surface['floor']:
            dx = self.platform.rect.x - self.platform.old_rect.x
            dy = self.platform.rect.y - self.platform.old_rect.y
            self.hitbox_rect.x += dx
            self.hitbox_rect.y += dy
            self.rect.center = self.hitbox_rect.center

    def start_attack(self):
        self.timers['attack_cooldown'].activate()

        # spawn visual effect
        MagicBurst(self.hitbox_rect.center, self.attack_radius, self.groups())

        # apply damage
        self.apply_attack_damage()
        
    def take_damage(self, damage):
        if self.invincible:
            return
        self.health -= damage
        self.hit_flash_time = self.hit_flash_duration

        self.invincible = True
        self.invincible_timer = self.invincible_time

        if self.health <= 0:
            # death logic here
            pass

        
    def apply_attack_damage(self):
        cx, cy = self.hitbox_rect.center
        radius = self.attack_radius

        for enemy in self.enemy_group:   # we’ll set this up later
            ex, ey = enemy.rect.center
            if (cx - ex)**2 + (cy - ey)**2 <= radius * radius:
                enemy.take_damage(1)

    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)

        self.on_surface, self.platform = self.collision_sprites.check_contact(self.hitbox_rect)
        self.platform_move()

        if not self.on_surface['floor'] and self.direction.y > 0 and not self.jump:
            self.did_jump = False

        self.collision_sprites.resolve(self.hitbox_rect, self.old_rect, 'horizontal')
        self.collision_sprites.resolve(self.hitbox_rect, self.old_rect, 'vertical')

        self.rect.center = self.hitbox_rect.center
        
        if self.did_jump and self.direction.y > 0 and not self.on_surface['floor']:
            if not self.timers["fall_delay"].active:
                self.timers["fall_delay"].activate()
        else:
            self.timers["fall_delay"].deactivate()


        just_landed = (
            self.on_surface['floor'] and
            self.direction.y == 0 and
            self.old_rect.y < self.hitbox_rect.y and
            not self.timers["land"].active
        )

        if just_landed:
            self.timers["land"].activate()
            self.status = "land"
            self.frame_index = 0
            self.did_jump = False

        self.get_status()
        self.animate(dt)

        if self.hit_flash_time > 0:
            self.hit_flash_time -= dt * 1000  # convert to ms

            base_image = self.animations[self.status][int(self.frame_index)]
            self.image = base_image.copy()

            flash = pygame.Surface(self.image.get_size())
            flash.fill((255, 255, 255))
            flash.set_alpha(150)
            self.image.blit(flash, (0, 0))
        else:
            self.image = self.animations[self.status][int(self.frame_index)]

        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['jump wait'].activate()
                self.did_jump = True
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['jump wait'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False

        if self.attack and not self.timers['attack_cooldown'].active:
            if self.on_surface['floor']:   # ⭐ only attack on ground
                self.start_attack()
        self.attack = False

        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

