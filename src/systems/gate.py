from src.settings import *

#  represents a locked gate that needs a key to be opened
class Gate(pygame.sprite.Sprite):
    def __init__(self, rect, key_type, image_closed):
        super().__init__()
        self.collider = None
        self.image_closed = image_closed
        self.key_type = key_type
        self.image_open = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.image = image_closed
        self.rect = self.image.get_rect(topleft=rect.topleft)
        self.hitbox = rect
        self.opened = False

    def update(self, player):
        if self.opened:
            return

        # check if the player collided and has key
        if self.rect.colliderect(player.rect):
            if player.inventory.has(self.key_type):
                self.open(player)

    # open gate
    def open(self, player):
        self.opened = True
        self.image = self.image_open

        # remove collider so player can pass through
        if hasattr(self, "collider"):
            self.collider.kill()
        player.inventory.remove(1)

    # reset gate to closed state (for level restart)
    def reset(self, collision_sprites):
        self.opened = False
        self.image = self.image_closed
        if self.collider:
            collision_sprites.add(self.collider)
