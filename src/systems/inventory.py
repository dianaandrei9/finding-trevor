from src.settings import *
from os.path import join


# represents a type of item (KEY)
class ItemType:
    def __init__(self, name, icon_path):
        self.name = name
        self.icon = None
        self.icon_path = icon_path

    def load_icon(self):
        if not self.icon:
            self.icon = pygame.image.load(join("assets", "graphics", self.icon_path)).convert_alpha()

class ItemSlot:
    def __init__(self):
        self.type = None
        self.amount = 0

    def empty(self):
        return self.type is None

    def clear(self):
        self.type = None
        self.amount = 0

class Inventory:
    # player inventory, currently ne slot
    def __init__(self):
        self.slot = ItemSlot()
        self.slot_bg = pygame.image.load(join("assets", "graphics", "inventory_slot.png")).convert_alpha()

    # check if slot has a specific item type
    def has(self, item_type):
        return self.slot.type == item_type

    # add item to slot if empty
    def add(self, item_type, amount=1):
        if self.slot.empty():
            self.slot.type = item_type
            self.slot.amount = amount
            return True

    # removes an amount of the certain itemtype
    def remove(self, amount=1):
        if self.slot.empty():
            return False

        self.slot.amount -= amount
        if self.slot.amount <= 0:
            # clear the slot if no more items left
            self.slot.clear()

        return True

    def draw(self, surface):
        sw, sh = surface.get_size()

        slot_rect = self.slot_bg.get_rect(topright=(sw - 55, 30))

        # draw slot frame
        surface.blit(self.slot_bg, slot_rect)

        # draw item icon ON TOP
        if self.slot.type:
            icon = self.slot.type.icon
            icon_rect = icon.get_rect(center=slot_rect.center)
            surface.blit(icon, icon_rect)

class DroppedItem(pygame.sprite.Sprite):
    def __init__(self, pos, item_type, amount, groups):
        super().__init__(groups)
        self.item_type = item_type
        self.amount = amount
        self.image = item_type.icon
        self.rect = self.image.get_rect(center=pos)

class Key:
    key = ItemType("Key", "key.png")
