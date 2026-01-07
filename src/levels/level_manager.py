from pytmx.util_pygame import load_pygame
from src.settings import *
from os.path import join
from src.levels.level import Level

class LevelManager:
    def __init__(self, screen):
        self.screen = screen
        self.current_health = 3
        self.inv_data = None
        self.level_paths = [
            join("assets", "maps", "levels", "level_1.tmx"),
            join("assets", "maps", "levels", "level_2.tmx"),
            join("assets", "maps", "levels", "level_3.tmx"),
        ]

        self.current_index = 0
        self.current_level = self._load_level(self.current_index)

    def _load_level(self, index):
        tmx = load_pygame(self.level_paths[index])
        level = Level(tmx, self.screen, self.current_health)
        if self.inv_data:
            level.player.inventory.slot.type = self.inv_data["type"]
            level.player.inventory.slot.amount = self.inv_data["amount"]
        return level
    
    def cutscene(self):
        return "end_cutscene"  

    def next_level(self):
        self.current_index += 1
        slot = self.current_level.player.inventory.slot
        if slot.type:
            self.inv_data = {
                "type": slot.type,
                "amount": slot.amount
            }
        else:
            self.inv_data = None
        
        self.current_health = self.current_level.player.health
        if self.current_index < len(self.level_paths):
            self.current_level = self._load_level(self.current_index)
        else:
            print("Game finished")

    def restart_level(self):
        self.current_level = self._load_level(self.current_index)

    def go_to_first_level(self):
        self.current_health = 3
        self.current_index = 0
        self.inv_data = None
        for gate in self.current_level.gate:
            gate.reset(self.current_level.collision_sprites)
        self.current_level = self._load_level(self.current_index)

    def update(self, dt):
        self.current_level.update(dt)
        self.current_level.run(dt)
        if getattr(self.current_level, "game_over", False):
            return
        if getattr(self.current_level, "restart", False):
            self.go_to_first_level()
            return
        if self.current_level.level_complete:
            self.next_level()
            return
        if self.current_level.met_trev:
            return self.cutscene()
        return None
            
        
    def draw(self, dt):
        self.current_level.run(dt)
