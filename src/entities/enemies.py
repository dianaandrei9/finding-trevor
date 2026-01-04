from os import walk
from os.path import join
from src.settings import *
from random import choice
from src.systems.timer import Timer
from src.entities.player import Player

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

    def update(self, dt, player=None):
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

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, orbs_group, player_group,display_surf):
        super().__init__(groups)
        self.player_group = player_group
        self.display_surface = display_surf
        self.all_sprites = groups[0]
        self.orbs_group = orbs_group
        self.frames, self.frame_index = import_folder('assets', 'sprites','enemies', 'boss', 'boss'), 0
        self.original_frames = self.frames.copy() 
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = vector(self.rect.topleft)
        self.damage = 2
        
        # throws
        self.max_attacks = 3    # max throws before getting tired
        self.attack_count = 0
        self.tired_timer = Timer(5000)  # Boss rests 5 seconds after being tired
        self.tired_timer.active = False
        self.is_tired = False

        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.snap_to_ground()

        self.max_health = 6 # 4 hits and it dead i think it ok
        self.health = self.max_health
        self.is_dead = False

        # sky orbs
        self.sky_orbs_timer = Timer(3000)  # every 2 seconds
        self.sky_orbs_timer.activate()
        
        # attack
        self.attack_timer = Timer(2000)  # every 2 seconds
        self.attack_timer.activate()

        # flashing
        self.original_frames = self.frames
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
    
    # boss starts shooting when player in range 
    def player_in_range(self, player):
        boss_pos = vector(self.rect.center)
        player_pos = vector(player.rect.center)
        return boss_pos.distance_to(player_pos) <= 700


    def update(self, dt, player):
        # animate
        self.sky_orbs_timer.update()
        self.attack_timer.update()
        self.frame_index += ANIMATION_SPEED * dt
        frames = self.frames
        self.image = frames[int(self.frame_index) % len(frames)]

        if self.invincible:
            self.invincible_timer -= dt * 1000
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # sky orbs
        # if player and self.player_in_range(player):
        #     if not self.sky_orbs_timer.active:
        #         self.summon_sky_orbs()
        #         self.sky_orbs_timer.activate()

        # attack
        # if player and self.player_in_range(player) and not self.is_tired:
        #     if not self.attack_timer.active:
        #         self.summon_orbs()
        #         self.attack_timer.activate()
        #         self.attack_count += 1
        #         if self.attack_count >= self.max_attacks:
        #             self.is_tired = True
        #             self.tired_timer.activate()

        # handle tired
        if self.is_tired:
            self.tired_timer.update()
            if not self.tired_timer.active:
                self.is_tired = False
                self.attack_count = 0

        # boss tired UGLY HELP
        if self.is_tired:
            frame = self.original_frames[int(self.frame_index) % len(self.original_frames)]
            self.image = frame.copy()  # copy original
            gray_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            gray_surf.fill((100, 100, 100, 80))
            self.image.blit(gray_surf, (0, 0))
        else:
            self.image = self.original_frames[int(self.frame_index) % len(self.original_frames)]

        # hit flash
        if self.hit_flash_time > 0:
            self.hit_flash_time -= dt * 1000  # dt is seconds → convert to ms
            # flash white
            flash = pygame.Surface(self.image.get_size())
            flash.fill((255, 255, 255))
            flash.set_alpha(150)
            self.image.blit(flash, (0, 0))
        else:
            # restore original frames if needed
            self.frames = self.original_frames

    def summon_orbs(self):
        directions = [
            vector(-1, -1),  # top-left
            vector(1, -1),   # top-right
            vector(-1, 1),   # bottom-left
            vector(1, 1),    # bottom-right
            vector(0, -1),    # up
            vector(1, 0),    # right
            vector(-1, 0)    # left
        ]

        for dir in directions:
            Orb(self.rect.center, (self.all_sprites, self.orbs_group), dir, 300, self.player_group)
    
    def summon_sky_orbs(self):
        screen_width = self.display_surface.get_width()
        num_orbs = 5
        spacing = screen_width / (num_orbs - 1)
        for i in range(num_orbs):
            pos = vector(i * spacing, 0)
            Orb(pos, (self.all_sprites, self.orbs_group), vector(0, 1), 200, self.player_group)

class Orb(pygame.sprite.Sprite):
    def __init__(self, pos, groups, direction, speed, player_group):
        super().__init__(groups)
        self.image = pygame.image.load(join("assets", "sprites", "enemies", "boss", "orb", "orb.png")).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = vector(self.rect.center)
        self.player = player_group
        
        self.direction = direction.normalize()
        self.speed = speed
        self.damage = 1

        self.timer = Timer(5000)
        self.timer.activate()

    def update(self, dt):
        self.timer.update()
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

        # check collision with player
        if self.player:
            hits = pygame.sprite.spritecollide(self, self.player, False)
            for sprite in hits:
                if isinstance(sprite, Player):
                    sprite.take_damage(self.damage)
                    self.kill()
                    break
        
        if not self.timer.active:
            self.kill()
