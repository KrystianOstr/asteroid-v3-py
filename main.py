import pygame as py
import sys


py.init()

clock = py.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

display_surface = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#text
font = py.font.Font('assets/graphics/subatomic.ttf',50)
text_surf = font.render("dsdsadsa", True, (255,255,255))

#images
ship_surf = py.image.load('assets/graphics/ship.png').convert_alpha()
# ship_rect = ship_surf.get_rect(center = (640,360))
ship_rect = ship_surf.get_rect(midright = (WINDOW_WIDTH, WINDOW_HEIGHT//2))


#background
background_surf = py.image.load('assets/graphics/background.png').convert_alpha()



while True:

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                py.quit()
                sys.exit()


    # FPS
    clock.tick(120)

    display_surface.fill((200,200,200))
    display_surface.blit(background_surf,(0,0))
    display_surface.blit(ship_surf, ship_rect)
    display_surface.blit(text_surf, (WINDOW_WIDTH//2 - text_surf.get_width() //2, 600))

    py.display.update()

