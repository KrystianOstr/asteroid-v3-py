import pygame as py
import sys


py.init()

clock = py.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

display_surface = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#text
font = py.font.Font('assets/graphics/subatomic.ttf',50)
text_surf = font.render("Universe", True, (255,255,255))
text_rect = text_surf.get_rect(center=(WINDOW_WIDTH//2,600))

#images
ship_surf = py.image.load('assets/graphics/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(midtop = (WINDOW_WIDTH//2,WINDOW_HEIGHT- 80))
# ship_reversed_surface = py.transform.flip(ship_surf, False,True)
# ship_rotated = py.transform.rotate(ship_surf, 45)


laser_surf = py.image.load('assets/graphics/laser.png').convert_alpha()
laser_list = []


#background
background_surf = py.image.load('assets/graphics/background.png').convert_alpha()

# draw
test_rect = py.Rect(100,200,400,500)



while True:

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                py.quit()
                sys.exit()
        if event.type == py.MOUSEBUTTONDOWN:
            laser_rect = laser_surf.get_rect(midbottom = (ship_rect.midtop))
            laser_list.append(laser_rect)

                


    # FPS
    dt = clock.tick(60) / 1000

    ship_rect.center = py.mouse.get_pos()


    display_surface.fill((200,200,200))
    display_surface.blit(background_surf,(0,0)) 

    display_surface.blit(text_surf, text_rect)
    py.draw.rect(display_surface, (255,255,255), text_rect.inflate(30,30), width=8, border_radius= 5)
    
    for laser in laser_list:
        display_surface.blit(laser_surf, laser)
        laser.y -= round(200 * dt)


    display_surface.blit(ship_surf, ship_rect)
  

    py.display.update()

