import pygame

class MagicBurst(pygame.sprite.Sprite):
    def __init__(self, pos, radius, groups):
        super().__init__(groups)

        self.radius = radius
        self.lifetime = 1  # total duration (same unit as dt)
        self.elapsed = 0

        # base surface we'll fade over time
        self.base_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            self.base_surface,
            (200, 255, 220, 180),  # full alpha
            (radius, radius),
            radius,
            width=4
        )

        self.image = self.base_surface.copy()
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        # accumulate time
        self.elapsed += dt

        # clamp progress 0 → 1
        progress = max(0, min(1, self.elapsed / self.lifetime))

        # alpha: 255 → 0
        alpha = int(255 * (1 - progress))

        # apply fade
        self.image = self.base_surface.copy()
        self.image.set_alpha(alpha)

        # kill when done
        if self.elapsed >= self.lifetime:
            self.kill()