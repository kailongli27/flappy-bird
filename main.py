import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 656))  # put this floor at the left side of the screen
    screen.blit(floor_surface, (floor_x_pos + 576, 656))  # put another floor at the right side of the screen


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)  # choose a random height from the list of possible heights
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))  # create a rectangle and place it at a given position
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))  # create another rectangle and place it higher
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5  # move each pipe in the list to the left
    return pipes  # return the new list of pipe rectangles


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 780:  # bottom pipe
            screen.blit(pipe_surface, pipe)  # draw all pipes in the list on the screen
        else:  # top pipe
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


pygame.init()  # initialize all imported pygame modules
screen = pygame.display.set_mode(size=(576, 780))  # initialize a display surface of 576 px x 780 px
clock = pygame.time.Clock()  # create an object to help track time

# game variables
gravity = 0.25
bird_movement = 0

# import images
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)  # double the size of the surface

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(100, 390))  # create a rectangle with the width and height of the
# bird_surface and center it at a given position

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT  # an event to create a new pipe
pygame.time.set_timer(SPAWNPIPE, 1200)  # the event will be triggered every 1200 ms
pipe_height = [400, 600, 800]  # all of the possible heights for a pipe

# game loop
while True:
    for event in pygame.event.get():  # get events from the queue (e.g. user moving mouse, timer ending, etc.)
        if event.type == pygame.QUIT:
            pygame.quit()  # uninitialize all pygame modules
            sys.exit()
        if event.type == pygame.KEYDOWN:  # detect if a key is physically pressed down
            if event.key == pygame.K_SPACE:  # spacebar
                bird_movement = 0  # disable the effect of gravity
                bird_movement -= 12  # make the bird go up after the player presses the spacebar
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())  # add a new pipe to the list
            print(pipe_list)

    screen.blit(bg_surface, (0, 0))  # position the background image at the origin point of the screen

    # bird
    bird_movement += gravity
    bird_rect.centery += bird_movement  # make the bird fall down
    screen.blit(bird_surface, bird_rect)  # draw the bird_surface onto the bird_rect, at the bird_rect's position

    # pipes
    pipe_list = move_pipes(pipe_list)  # move pipes to the left and overwrite existing list
    draw_pipes(pipe_list)

    # floor
    floor_x_pos -= 1  # make the floor move to the left
    draw_floor()
    if floor_x_pos <= -576:  # ensure a continuously moving floor
        floor_x_pos = 0  # reset to the left side of the screen

    pygame.display.update()
    clock.tick(120)  # limit frame rate to 120 frames per second
