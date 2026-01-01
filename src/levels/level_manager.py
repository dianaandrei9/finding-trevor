from pytmx.util_pygame import load_pygame
from os.path import join
from src.levels.level import Level

class LevelManager:
    def __init__(self, screen):
        self.screen = screen

        self.level_paths = [
            join("assets", "maps", "levels", "level_1.tmx"),
            join("assets", "maps", "levels", "level_2.tmx"),
            join("assets", "maps", "levels", "level_3.tmx"),
        ]

        self.current_index = 0
        self.current_level = self._load_level(self.current_index)

    def _load_level(self, index):
        tmx = load_pygame(self.level_paths[index])
        return Level(tmx, self.screen)

    def next_level(self):
        self.current_index += 1
        if self.current_index < len(self.level_paths):
            self.current_level = self._load_level(self.current_index)
        else:
            print("Game finished")

    def restart_level(self):
        self.current_level = self._load_level(self.current_index)

    def update(self, dt):
        self.current_level.update(dt)

    def draw(self, dt):
        self.current_level.run(dt)
