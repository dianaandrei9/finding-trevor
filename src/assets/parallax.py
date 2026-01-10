class ParallaxLayer:
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed

    def draw(self, surface, camera_x):
        # calculate horizontal offset based on camera position
        x = -camera_x * self.speed
        width = self.image.get_width()

        # infinite repetitionn
        x = x % width

        surface.blit(self.image, (x - width, 0))
        surface.blit(self.image, (x, 0))
