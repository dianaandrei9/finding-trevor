from src.settings import *
from src.assets.parallax import ParallaxLayer
from src.assets.sprites import Sprite
from src.entities.player import Player

class Level:
    def __init__(self, tmx_map, surface):
        self.display_surface = surface
        
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
        pass
    
    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill('gray')
        self.all_sprites.draw(self.display_surface)