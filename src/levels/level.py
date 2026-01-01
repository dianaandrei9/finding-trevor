from src.settings import *
from src.core.parallax_att import ParallaxBackground
from src.assets.sprites import Sprite
from src.entities.player import Player
from src.systems.collider import Collider

class Level:
    def __init__(self, tmx_map, surface):
        self.display_surface = surface
        
        self.parallax = ParallaxBackground( folder_path="assets/parallax", speeds=[0.02, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35, 0.5, 0.8] )

        # groups
        self.all_sprites  = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # death zones        
        self.death_rects = []

        self.setup(tmx_map)
        
    def setup(self, tmx_map):
        # tiles
        for x,y,surf in tmx_map.get_layer_by_name('terrain').tiles():
            Sprite((x * TILE_SIZE , y * TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))
        
        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'Tabitha':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
        
        # trigger
        for obj in tmx_map.get_layer_by_name('block_movement'):
            if obj.name == "death":
                self.death_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.name == "block_map":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                Collider(rect, self.collision_sprites)
        
        # moving objects (platforms)
        for obj in tmx_map.get_layer_by_name('moving_platforms'):
            pass
        
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
                
    
    def run(self, dt):
        self.parallax.draw(self.display_surface)
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)