import pygame
import sys

pygame.init()  # initialize all imported pygame modules
screen = pygame.display.set_mode(size=(576, 1024))  # initialize a display surface of 576 px x 1024 px

# game loop
while True:
    for event in pygame.event.get():  # get events from the queue (e.g. user moving mouse, timer ending, etc.)
        if event.type == pygame.QUIT:
            pygame.quit()  # uninitialize all pygame modules
            sys.exit()
    pygame.display.update()
