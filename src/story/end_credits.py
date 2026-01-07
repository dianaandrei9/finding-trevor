import pygame

CREDITS = [
            "",
            "You got Trevor back! Seems like he didnt need saving... But anyway!",
            "You got some harsh feedback... dont take it to heart...maybe do...fix your cooking",
            "",
            "",
            "?FINDING TREVOR",
            "",
            "A game made with love by",
            "cata & di",
            "",
            "",
            "#CAST",
            "",
            "Tabitha .......... The Hero?",
            "Trevor .......... The Familiar",
            "Bug .......... The Bug",
            "Skeleton Lord .......... Innocent Man",
            "",
            "",
            "#CREW",
            "",
            "WRITERS .......... ANDREI Diana, FASUI Catalina-Andreea",
            "ARTWORK & ANIMATION .......... FASUI Catalina-Andreea",
            "LEVEL DESIGN .......... ANDREI Diana",
            "PRODUCERS .......... ANDREI Diana, FASUI Catalina-Andreea",
            "",
            "",
            "#THANKS",
            "",
            "All creators of youtube tutorials for python, pygame and tiled, especially Clear Code",
            "",
            "",
            "We hope you enjoyed our little project! It took us enough time to get attached to it,", 
            "well maybe cause we also built it brick by brick, pixel by pixel. Please give us a good grade",
            "",
            "#THANK YOU FOR PLAYING!",
            "",
        ]

class EndCredits:
    def __init__(self, screen, lines, speed=80):
        self.screen = screen
        self.lines = lines
        self.speed = speed

        self.font_big_title = pygame.font.Font(None, 100)
        self.font_title = pygame.font.Font(None, 70)
        self.font_text = pygame.font.Font(None, 40)

        self.surfaces = []
        self.positions = []

        self._prepare_text()

    def _prepare_text(self):
        screen_h = self.screen.get_height()
        y = screen_h + 40

        for line in self.lines:
            if line.startswith("?"):
                surf = self.font_title.render(line[1:], True, (76, 166, 101))
            else:
                if line.startswith("#"):
                    surf = self.font_title.render(line[1:], True, (153, 0, 255))
                else:
                    surf = self.font_text.render(line, True, (255, 255, 255))

            rect = surf.get_rect(centerx=self.screen.get_width() // 2)
            rect.y = y

            self.surfaces.append(surf)
            self.positions.append(rect)
            y += rect.height + 30

        self.end_y = y

    def update(self, dt):
        for rect in self.positions:
            rect.y -= self.speed * dt

    def draw(self):
        self.screen.fill((0, 0, 0))
        for surf, rect in zip(self.surfaces, self.positions):
            self.screen.blit(surf, rect)

    def finished(self):
        return self.positions[-1].bottom < 0
