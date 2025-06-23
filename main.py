from random import randint, uniform
import pygame as py
import sys


def laser_update(laser_list, speed=300):
    for rect in laser_list:
        rect.y -= round(speed * dt)
        if rect.bottom < 0:
            laser_list.remove(rect)


def meteor_update(meteor_list, speed=300):
    for meteor_tuple in meteor_list:
        direction = meteor_tuple[1]
        meteor_rect = meteor_tuple[0]
        meteor_rect.center += direction * speed * dt
        if meteor_rect.top > WINDOW_HEIGHT:
            meteor_list.remove(meteor_tuple)


def display_score():
    score_text = f"Score: {py.time.get_ticks()//1000}"
    text_surf = font.render(score_text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80))
    display_surface.blit(text_surf, text_rect)
    py.draw.rect(
        display_surface,
        (255, 255, 255),
        text_rect.inflate(30, 30),
        width=8,
        border_radius=5,
    )


def laser_timer(can_shoot, duration=500):
    if not can_shoot:
        current_time = py.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot


py.init()

clock = py.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

display_surface = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# text
font = py.font.Font("assets/graphics/subatomic.ttf", 50)

# images

# background
background_surf = py.image.load("assets/graphics/background.png").convert_alpha()

# ship
ship_surf = py.image.load("assets/graphics/ship.png").convert_alpha()
ship_rect = ship_surf.get_rect(midtop=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80))

# laser
laser_surf = py.image.load("assets/graphics/laser.png").convert_alpha()
laser_list = []

# meteor
meteor_surf = py.image.load("assets/graphics/meteor.png").convert_alpha()
meteor_list = []

# laser timer
can_shoot = True
shoot_time = None

# meteor timer
meteor_timer = py.event.custom_type()
py.time.set_timer(meteor_timer, 500)

# import sound
laser_sound = py.mixer.Sound("assets/sounds/laser.ogg")
explosion_sound = py.mixer.Sound("assets/sounds/explosion.wav")
ship_explosion_sound = py.mixer.Sound("assets/sounds/explosion.mp3")
background_music = py.mixer.Sound("assets/sounds/music.wav")
background_music.play(-1)

running = True
game_over = False

while running:

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                py.quit()
                sys.exit()
        if event.type == py.MOUSEBUTTONDOWN and can_shoot:
            laser_rect = laser_surf.get_rect(midbottom=(ship_rect.midtop))
            laser_list.append(laser_rect)
            laser_sound.play()

            can_shoot = False
            shoot_time = py.time.get_ticks()
        if event.type == meteor_timer:

            # random pos
            x_pos = randint(-100, WINDOW_WIDTH + 100)
            y_pos = randint(-100, -50)

            meteor_rect = meteor_surf.get_rect(midbottom=(x_pos, y_pos))

            # random direction
            direction = py.math.Vector2(uniform(-0.5, 0.5), 1)

            meteor_list.append((meteor_rect, direction))

    # FPS
    dt = clock.tick(60) / 1000

    ship_rect.center = py.mouse.get_pos()

    laser_update(laser_list)
    can_shoot = laser_timer(can_shoot, 400)

    # meteor ship collision
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect) and not game_over:
            ship_explosion_sound.play()
            game_over = True
            # py.quit()
            # sys.exit()

    # laser meteor collision
    for laser_rect in laser_list:
        for meteor_tuple in meteor_list:
            meteor_rect = meteor_tuple[0]
            if laser_rect.colliderect(meteor_rect):
                laser_list.remove(laser_rect)
                meteor_list.remove(meteor_tuple)
                explosion_sound.play()

    meteor_update(meteor_list)

    display_surface.fill((200, 200, 200))
    display_surface.blit(background_surf, (0, 0))

    display_score()

    for laser in laser_list:
        display_surface.blit(laser_surf, laser)

    for meteor_tuple in meteor_list:
        display_surface.blit(meteor_surf, meteor_tuple[0])

    display_surface.blit(ship_surf, ship_rect)

    if game_over == True:
        background_music.stop()
        display_surface.fill("Teal")
        game_over_text = font.render(
            f"Game over, press ESC to exit", True, (255, 255, 255)
        )
        game_over_text_rect = game_over_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        display_surface.blit(game_over_text, game_over_text_rect)

    py.display.update()
