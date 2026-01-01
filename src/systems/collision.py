from src.settings import *

class Collision:
    def __init__(self, collision_sprites):
        self.collision_sprites = collision_sprites
        self.platform = None

    def check_contact(self, rect: pygame.Rect):
        floor_rect = pygame.Rect(rect.bottomleft, (rect.width, 2))
        right_rect = pygame.Rect(rect.topright + vector(0, rect.height / 4), (2, rect.height / 2))
        left_rect = pygame.Rect(rect.topleft + vector(-2, rect.height / 4), (2 , rect.height / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        
        self.platform = None
        for sprite in [sprite for sprite in self.collision_sprites.sprites() if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
            
        # collisions
        return {
            "floor": floor_rect.collidelist(collide_rects) >= 0,
            "right": right_rect.collidelist(collide_rects) >= 0,
            "left": left_rect.collidelist(collide_rects) >= 0
        }, self.platform
        
            
    def resolve(self, rect: pygame.Rect, old_rect: pygame.Rect, axis: str):
        collided = False
        
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(rect):
                collided = True

                if axis == 'horizontal':
                    # left
                    if rect.left <= sprite.rect.right and old_rect.left >= sprite.old_rect.right:
                        rect.left = sprite.rect.right
                    
                    # right
                    if rect.right >= sprite.rect.left and old_rect.right <= sprite.old_rect.left:
                        rect.right = sprite.rect.left
                    
                else: # vertical
                    # top
                    if rect.top <= sprite.rect.bottom and old_rect.top >= sprite.old_rect.bottom:
                        rect.top = sprite.rect.bottom
                    
                    # bottom
                    if rect.bottom >= sprite.rect.top and old_rect.bottom <= sprite.old_rect.top:
                        rect.bottom = sprite.rect.top
        return collided
    