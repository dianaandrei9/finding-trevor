from src.settings import *
from src.core.parallax_att import ParallaxBackground
from src.assets.sprites import Sprite, MovingSprite
from src.entities.player import Player
from src.systems.collider import Collider
from src.systems.health import Health
from src.systems.inventory import ItemType, DroppedItem, Key
from src.systems.gate import Gate
from src.ui.death_screen import GameOverMenu
from os.path import join

class Level:
    def __init__(self, tmx_map, surface, health):
        self.display_surface = surface
        self.game_over_menu = GameOverMenu(self.display_surface)
        self.tmx_map = tmx_map
        self.parallax = ParallaxBackground( folder_path="assets/parallax", speeds=[0.02, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35, 0.5] )
        
        # groups
        self.moving_sprites = pygame.sprite.Group()
        self.all_sprites  = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.gate = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # death zone
        self.death_rects = []
        self.start_health = health
        
        # end lvl
        self.level_complete = False
        self.level_end_rect = None
        self.game_over = False
        self.restart = False
        
        self.setup(tmx_map)

    def setup(self, tmx_map):
        # clear 
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.moving_sprites.empty()
        self.items.empty()
        self.gate.empty()
        self.death_rects.clear()
        
        # tiles
        for layer in tmx_map.layers:
            if hasattr(layer, 'name') and layer.name.startswith("terrain"):
                tint_hex = layer.properties.get('tint')
                tint_color = pygame.Color(tint_hex) if tint_hex else None
                                
                for x,y,surf in layer.tiles():
                    if tint_color:
                        image = surf.copy()
                        tint = pygame.Surface(image.get_size(), pygame.SRCALPHA)
                        tint.fill(tint_color)
                        image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    else: 
                        image = surf
                    if layer.properties.get('collidable') == True:
                        Sprite((x * TILE_SIZE , y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))
                    else:
                        Sprite((x * TILE_SIZE , y * TILE_SIZE), image, (self.all_sprites))

        key_type = Key.key
        key_type.load_icon()
        
        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'Tabitha':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.start_health, self.enemies)
            if obj.name == 'Trevor':
                self.trevor = Sprite((obj.x, obj.y), pygame.image.load(join("assets", "graphics", "Trev_64x64.png")), (self.all_sprites, self.collision_sprites))
            if obj.name == "end_lvl":
                self.level_end_rect = pygame.Rect( obj.x, obj.y, obj.width, obj.height)
            if obj.name == "Key":
                amount = obj.properties.get("amount", 1)
                DroppedItem( pos=(obj.x + obj.width // 2, obj.y + obj.height // 2), item_type=key_type, amount=amount, groups=(self.all_sprites, self.items))                
        self.health = Health(self.display_surface, self.player.health, self.player.max_health)

        # trigger
        for obj in tmx_map.get_layer_by_name('block_movement'):
            if obj.name == "death":
                self.death_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.name == "block_map":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                Collider(rect, self.collision_sprites)
            if obj.name == "gate":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                gate = Gate(rect, key_type, pygame.image.load("assets/graphics/gate_closed.png").convert_alpha())
                self.gate.add(gate)
                self.all_sprites.add(gate)
                gate.collider = Collider(rect, self.collision_sprites)
        
        # moving objects (platforms)
        if 'moving_platforms' in tmx_map.layernames:
            for obj in tmx_map.get_layer_by_name('moving_platforms'): 
                if obj.properties.get('platform') is True:
                    if obj.name == 'platform1':
                        # horizontal
                        move_dir = 'x'
                        start_pos = (obj.x, obj.y + obj.height / 2)
                        end_pos = (obj.x + obj.width, obj.y + obj.height / 2) 
                        speed = obj.properties['speed']
                        MovingSprite((self.all_sprites, self.collision_sprites, self.moving_sprites), start_pos, end_pos, move_dir, speed, 1)
                        
                    if obj.name == 'platform2':
                        # horizontal
                        move_dir = 'x'
                        start_pos = (obj.x + obj.width, obj.y + obj.height / 2) 
                        end_pos = (obj.x, obj.y + obj.height / 2)
                        speed = obj.properties['speed']
                        MovingSprite((self.all_sprites, self.collision_sprites, self.moving_sprites), start_pos, end_pos, move_dir, speed, 2)
                        
                    if obj.name == 'platform3':
                        # horizontal
                        move_dir = 'x'
                        start_pos = (obj.x, obj.y + obj.height / 2)
                        end_pos = (obj.x + obj.width, obj.y + obj.height / 2) 
                        speed = obj.properties['speed']
                        MovingSprite((self.all_sprites, self.collision_sprites, self.moving_sprites), start_pos, end_pos, move_dir, speed, 3)
                    
                
    def update(self, dt: float):   
        player = next((s for s in self.all_sprites if isinstance(s, Player)), None)
        if player:
            camera_dx = player.actual_dx
        else:
            camera_dx = 0 
        self.parallax.update(camera_dx)
        
        # inventory check
        hits = pygame.sprite.spritecollide(self.player, self.items, dokill=True)
        for item in hits:
           self.player.inventory.add(item.item_type, item.amount)
        
        # open gate
        for gate in self.gate: 
            gate.update(self.player)
        
        # kill zone check
        for r in self.death_rects:
            if self.player.hitbox_rect.colliderect(r):
                if self.player.health > 1:
                    # small respawn
                    self.player.health -= 1
                    self.player.rect.topleft = self.player.pos
                    self.player.hitbox_rect = self.player.rect.inflate(-5, 0)
                    self.player.direction.y = 0
                else:
                    # big respawn == death => menu screen
                    self.player.health = 0
                    self.game_over = True
                    return
        
        self.moving_sprites.update(dt)
        self.player.update(dt)
        self.health.set_health(self.player.health)
        if self.level_end_rect and self.player.rect.colliderect(self.level_end_rect):
            pygame.draw.rect(self.display_surface, (255, 0 ,0), self.level_end_rect, 2)
            self.level_complete = True
        
    def run(self, dt):
        self.parallax.draw(self.display_surface)
        self.all_sprites.draw(self.display_surface)
        self.health.empty_hearts()
        self.player.inventory.draw(self.display_surface)
        
        if self.game_over:
            result = self.game_over_menu.run()
            if result == "restart":
                self.game_over = False
                self.restart = True
        return
