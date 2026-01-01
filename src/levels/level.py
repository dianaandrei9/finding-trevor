from src.settings import *
from src.core.parallax_att import ParallaxBackground
from src.assets.sprites import Sprite, MovingSprite
from src.entities.player import Player
from src.systems.collider import Collider

class Level:
    def __init__(self, tmx_map, surface):
        self.display_surface = surface
        
        self.parallax = ParallaxBackground( folder_path="assets/parallax", speeds=[0.02, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35, 0.5] )

        # groups
        self.moving_sprites = pygame.sprite.Group()
        self.all_sprites  = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # death zones        
        self.death_rects = []

        # end lvl
        self.level_complete = False
        self.level_end_rect = None
        
        self.setup(tmx_map)

    def setup(self, tmx_map):
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

        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'Tabitha':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            if obj.name == "end_lvl":
                self.level_end_rect = pygame.Rect( obj.x, obj.y, obj.width, obj.height)
                
        # trigger
        for obj in tmx_map.get_layer_by_name('block_movement'):
            if obj.name == "death":
                self.death_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.name == "block_map":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                Collider(rect, self.collision_sprites)
        
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
        
        # kill zone check
        for r in self.death_rects:
            if self.player.rect.colliderect(r):
                # respawn
                self.player.rect.topleft = self.player.pos
                self.player.direction.y = 0
        
        self.moving_sprites.update(dt)
        self.player.update(dt)
        if self.level_end_rect and self.player.rect.colliderect(self.level_end_rect):
            pygame.draw.rect(self.display_surface, (255, 0 ,0), self.level_end_rect, 2)
            self.level_complete = True
        
    def run(self, dt):
        self.parallax.draw(self.display_surface)
        self.all_sprites.draw(self.display_surface)