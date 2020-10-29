import pygame
import sys


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 656))  # put this floor at the left side of the screen
    screen.blit(floor_surface, (floor_x_pos + 576, 656))  # put another floor at the right side of the screen


pygame.init()  # initialize all imported pygame modules
screen = pygame.display.set_mode(size=(576, 780))  # initialize a display surface of 576 px x 780 px
clock = pygame.time.Clock()  # create an object to help track time

# import images
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)  # double the size of the surface

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# game loop
while True:
    for event in pygame.event.get():  # get events from the queue (e.g. user moving mouse, timer ending, etc.)
        if event.type == pygame.QUIT:
            pygame.quit()  # uninitialize all pygame modules
            sys.exit()
    screen.blit(bg_surface, (0, 0))  # position the background image at the origin point of the screen
    floor_x_pos -= 1  # make the floor move to the left
    draw_floor()
    if floor_x_pos <= -576:  # ensure a continuously moving floor
        floor_x_pos = 0  # reset to the left side of the screen

    pygame.display.update()
    clock.tick(120)  # limit frame rate to 120 frames per second
