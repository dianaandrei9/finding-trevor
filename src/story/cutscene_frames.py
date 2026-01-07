import pygame
from os import walk
from os.path import join

START_FRAMES = None
END_FRAMES   = None

def import_folder(*path):
    frames = []
    for folder_path, _, image_names in walk(join(*path)):
        for image_name in sorted(
            image_names,
            key=lambda name: int(name.split('-')[1].split('.')[0])
        ):
            full_path = join(folder_path, image_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames


def load_cutscene_frames():
    global START_FRAMES, END_FRAMES
    START_FRAMES = import_folder('assets', 'cutscene', 'start')
    END_FRAMES   = import_folder('assets', 'cutscene', 'end')
