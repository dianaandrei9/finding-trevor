from os import walk
from os.path import join
from src.settings import *

def import_folder(*path):
    frames = []
    for folder_path, subfolders, image_names in walk(join(*path)):
        for image_name in sorted(image_names, key = lambda name: int(name.split('-')[1].split('.')[0])):
            full_path = join(folder_path, image_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames

class Cutscene(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.frames = import_folder('assets', 'cutscene', 'start')
        self.frame_index = 0
        self.animation_speed = 2.7  # frames per second
        self.end = False
        self.waiting_for_input = False
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(0, 0))

        # text
        self.text = (
            "I haven't seen my pet familiar, Trevor, all morning "
            "but I'm pretty sure I know who has him. Let's get him back."
        )
        self.text_start_frame = 0
        self.text_end_frame = 17

        self.font = pygame.font.Font(None, 36)

    def update(self, dt):
        if not self.end and not self.waiting_for_input:
            self.frame_index += self.animation_speed * dt

            if self.frame_index >= len(self.frames):
                self.frame_index = len(self.frames) - 1

        # when text is fully on, stop and wait
        if self.frame_index >= self.text_end_frame:
            self.waiting_for_input = True

        self.image = self.frames[int(self.frame_index)]

    def check(self):
        if self.waiting_for_input:
            self.end = True

    def get_visible_text(self):
        if self.frame_index < self.text_start_frame:
            return ""

        if self.frame_index >= self.text_end_frame:
            return self.text

        total_frames = self.text_end_frame - self.text_start_frame
        total_chars = len(self.text)

        current_frame = int(self.frame_index) - self.text_start_frame
        chars_per_frame = total_chars / total_frames
        visible_chars = int(current_frame * chars_per_frame)

        return self.text[:visible_chars]
    
    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            width, _ = font.size(test_line)

            if width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.rstrip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.rstrip())

        return lines

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        
        # speech bubble
        bubble_rect = pygame.Rect(120, 340, 570, 140)
        pygame.draw.rect(self.screen, (10, 11, 23), bubble_rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), bubble_rect, 3, border_radius=8)

        # text
        text = self.get_visible_text()
        lines = self.wrap_text(text, self.font, max_width=bubble_rect.width - 40)
        lines = lines[:4]
        
        for i, line in enumerate(lines):
            line_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit( line_surf, (bubble_rect.x + 20, bubble_rect.y + 20 + i * 28))
