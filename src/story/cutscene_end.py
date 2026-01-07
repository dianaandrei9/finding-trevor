from os import walk
from os.path import join
from src.settings import *
import src.story.cutscene_frames as cutscene_frames

class StartCutscene(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.frames = cutscene_frames.START_FRAMES

        if self.frames is None:
            raise RuntimeError("Cutscene frames not loaded. Call load_cutscene_frames() first.")

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(0, 0))

class EndCutscene(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.frames = cutscene_frames.END_FRAMES
        self.frame_index = 0
        self.animation_speed = 2.3
        self.end = False
        self.waiting_for_input = False

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.font = pygame.font.Font(None, 36)

        # --- MULTI-SPEAKER DIALOGUE SETUP ---
        self.dialogue = [
            {
                "speaker": "Tabitha",
                "text": "Trevor! I'm so glad you're fine... I had to fight a damn bug to get you!",
                "start": 1,
                "end": 22
            },
            {
                "speaker": "Trevor",
                "text": "Kid... I did not get kidnapped. I went with Skeleton myself! Told him to save me from your awful cookin'... Sorry.",
                "start": 24,
                "end": 58
            }
        ]

        self.current_dialogue = None

    def update(self, dt):
        if not self.end and not self.waiting_for_input:
            self.frame_index += self.animation_speed * dt

            if self.frame_index >= len(self.frames):
                self.frame_index = len(self.frames) - 1

        # update image
        self.image = self.frames[int(self.frame_index)]

        # update which dialogue segment we're in
        self.current_dialogue = self.get_current_dialogue()

        # stop animation when text finishes
        if self.current_dialogue and self.frame_index >= self.current_dialogue["end"]:
            self.waiting_for_input = True

    def get_current_dialogue(self):
        for segment in self.dialogue:
            if segment["start"] <= self.frame_index < segment["end"]:
                return segment
        return None

    def get_visible_text(self):
        if not self.current_dialogue:
            return ""

        text = self.current_dialogue["text"]
        start = self.current_dialogue["start"]
        end = self.current_dialogue["end"]

        if self.frame_index < start:
            return ""

        if self.frame_index >= end:
            return text

        total_frames = end - start
        total_chars = len(text)

        current_frame = int(self.frame_index) - start
        chars_per_frame = total_chars / total_frames
        visible_chars = min(
            len(text),
            round((current_frame + 1) * chars_per_frame)
        )

        return text[:visible_chars]

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

        if not self.current_dialogue:
            return

        # speech bubble
        screen_rect = self.screen.get_rect()
        bubble_rect = pygame.Rect(0, 0, 570, 140)
        bubble_rect.midbottom = screen_rect.midbottom
        bubble_rect.y -= 40

        pygame.draw.rect(self.screen, (10, 11, 23), bubble_rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), bubble_rect, 3, border_radius=8)

        # speaker name (optional)
        speaker = self.current_dialogue["speaker"]
        speaker_surf = self.font.render(speaker, True, (200, 200, 255))
        self.screen.blit(speaker_surf, (bubble_rect.x + 20, bubble_rect.y - 30))

        # text
        text = self.get_visible_text()
        lines = self.wrap_text(text, self.font, max_width=bubble_rect.width - 40)
        lines = lines[:4]

        for i, line in enumerate(lines):
            line_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(line_surf, (bubble_rect.x + 20, bubble_rect.y + 20 + i * 28))
            
    def check(self, force):
        if self.waiting_for_input or force:
            self.end = True
