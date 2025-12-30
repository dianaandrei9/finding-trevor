from src.settings import *
from src.core.parallax_att import ParallaxBackground
from src.assets.sprites import Sprite
from src.entities.player import Player

class Level:
    def __init__(self, tmx_map, surface):
        self.display_surface = surface
        
        from src.core.parallax_att import ParallaxBackground 
        self.parallax = ParallaxBackground( folder_path="assets/parallax", speeds=[0.02, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35, 0.5, 0.8] )

        # groups
        self.all_sprites  = pygame.sprite.Group()
        
        self.setup(tmx_map)
        
    def setup(self, tmx_map):
        for x,y,surf in tmx_map.get_layer_by_name('platforms').tiles():
            Sprite((x * TILE_SIZE , y * TILE_SIZE), surf, self.all_sprites)
        
        for obj in tmx_map.get_layer_by_name('Player'):
            if obj.name == 'Tabitha':
                Player((obj.x, obj.y), self.all_sprites)
            
    def update(self, dt: float):
        player = next((s for s in self.all_sprites if isinstance(s, Player)), None)
        if player:
            camera_dx = player.direction.x * player.speed * dt 
        else:
            camera_dx = 0 
        self.parallax.update(camera_dx)
    
    def run(self, dt):
        self.all_sprites.update(dt)
        self.parallax.draw(self.display_surface)
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)