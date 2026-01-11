import pygame
import os

class ParallaxLayer:
    def __init__(self, image_path, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.speed = speed

        self.x1 = 0
        self.x2 = self.image.get_width()

    def update(self, camera_dx):
        # move layer relative to camera movement
        self.x1 -= camera_dx * self.speed
        self.x2 -= camera_dx * self.speed

        w = self.image.get_width()
        # wrap left
        if self.x1 <= -w:
            self.x1 = self.x2 + w
        if self.x2 <= -w:
            self.x2 = self.x1 + w

        # wrap right
        if self.x1 >= w:
            self.x1 = self.x2 - w
        if self.x2 >= w:
            self.x2 = self.x1 - w

    def draw(self, surface):
        surface.blit(self.image, (self.x1, 0))
        surface.blit(self.image, (self.x2, 0))


class ParallaxBackground:
    def __init__(self, folder_path, speeds):
        self.layers = []

        for i, speed in enumerate(speeds, start=1):
            img_path = os.path.join(folder_path, f"{i}.png")
            self.layers.append(ParallaxLayer(img_path, speed))

    def update(self, camera_dx):
        for layer in self.layers:
            layer.update(camera_dx)

    def draw(self, surface):
        for layer in self.layers:
            layer.draw(surface)
