# TESTS IGNORE 
import pygame, sys

pygame.init()

BASE_W, BASE_H = 1920, 1080
WIN_W, WIN_H = 1280, 720
WORLD_W = 5000

window = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
pygame.display.set_caption("Parallax - Proper Resize (Letterbox)")
clock = pygame.time.Clock()

screen = pygame.Surface((BASE_W, BASE_H))

layer_files = [f"assets/parallax/{i}.png" for i in range(1, 10)]
layers = [pygame.image.load(f).convert_alpha() for f in layer_files]
factors = [0.0, 0.0, 0.10, 0.20, 0.30, 0.45, 0.60, 0.80, 1.00]

player_img = pygame.image.load("assets/sprites/tabitha.png").convert_alpha()
player_x_world = 200.0
player_y = 800.0
player_speed = 900.0

camera_x = 0.0
PLAYER_SCREEN_X_RATIO = 0.2

scaled_frame = None
last_scale_size = None

move_left = False
move_right = False

font = pygame.font.SysFont(None, 36)

def draw_parallax_layer(target, img, cam_x, factor):
    w = img.get_width()
    offset = (cam_x * factor) % w
    x = -offset
    while x < BASE_W:
        target.blit(img, (int(x), 0))
        x += w

def scale_to_window(frame, win_w, win_h):
    global scaled_frame, last_scale_size
    scale = min(win_w / BASE_W, win_h / BASE_H)
    new_w = int(BASE_W * scale)
    new_h = int(BASE_H * scale)

    if last_scale_size != (new_w, new_h):
        scaled_frame = pygame.transform.smoothscale(frame, (new_w, new_h))
        last_scale_size = (new_w, new_h)

    x = (win_w - new_w) // 2
    y = (win_h - new_h) // 2
    return scaled_frame, x, y

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WIN_W, WIN_H = event.w, event.h
            window = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
            last_scale_size = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False

    # movement
    if move_right:
        player_x_world += player_speed * dt
    if move_left:
        player_x_world -= player_speed * dt

    # clamp player
    player_x_world = max(0, min(player_x_world, WORLD_W))

    # camera follow
    camera_x = player_x_world - BASE_W * PLAYER_SCREEN_X_RATIO
    camera_x = max(0, min(camera_x, WORLD_W - BASE_W))

    # draw internal
    screen.fill((0, 0, 0))
    for img, f in zip(layers, factors):
        draw_parallax_layer(screen, img, camera_x, f)

    player_screen_x = player_x_world - camera_x
    screen.blit(player_img, (int(player_screen_x), int(player_y)))

    # indicator: focus + input state (on-screen, no terminal)
    focused = pygame.key.get_focused()
    status_text = f"FOCUS: {focused} | L:{move_left} R:{move_right}"
    txt = font.render(status_text, True, (255, 255, 255))
    screen.blit(txt, (20, 20))

    # scale to window
    window.fill((0, 0, 0))
    scaled, x, y = scale_to_window(screen, WIN_W, WIN_H)
    window.blit(scaled, (x, y))

    pygame.display.flip()

pygame.quit()
sys.exit()