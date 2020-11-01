import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))  # put this floor at the left side of the screen
    screen.blit(floor_surface, (floor_x_pos + 576, 900))  # put another floor at the right side of the screen


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)  # choose a random height from the list of possible heights
    bottom_pipe = pipe_surface.get_rect(
        midtop=(700, random_pipe_pos))  # create a rectangle and place it at a given position
    top_pipe = pipe_surface.get_rect(
        midbottom=(700, random_pipe_pos - 300))  # create another rectangle and place it higher
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5  # move each pipe in the list to the left
    return pipes  # return the new list of pipe rectangles


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:  # bottom pipe
            screen.blit(pipe_surface, pipe)  # draw all pipes in the list on the screen
        else:  # top pipe
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):  # check if the bird collides with any of the pipes
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:  # the game is over if the bird hits the floor or flies too high
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)  # use bird_movement as the angle of rotation
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))  # use the centery of the previous bird
    # rectangle to avoid changing the bird's position
    return new_bird, new_bird_rect


pygame.init()  # initialize all imported pygame modules
screen = pygame.display.set_mode(size=(576, 1024))  # initialize a display surface of 576 px x 1024 px
clock = pygame.time.Clock()  # create an object to help track time

# game variables
gravity = 0.25
bird_movement = 0
game_active = True

# import and scale images to fit screen size
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)  # double the size of the surface

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]  # put all three surfaces into a list
bird_index = 0
bird_surface = bird_frames[bird_index]  # pick a bird surface from the list
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1  # event to animate the bird's wings
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT  # event to create a new pipe
pygame.time.set_timer(SPAWNPIPE, 1200)  # the event will be triggered every 1200 ms
pipe_height = [400, 600, 800]  # all of the possible heights for a pipe

# game loop
while True:
    for event in pygame.event.get():  # get events from the queue (e.g. user moving mouse, timer ending, etc.)
        if event.type == pygame.QUIT:
            pygame.quit()  # uninitialize all pygame modules
            sys.exit()
        if event.type == pygame.KEYDOWN:  # detect if a key is physically pressed down
            if event.key == pygame.K_SPACE and game_active:  # spacebar
                bird_movement = 0  # disable the effect of gravity
                bird_movement -= 10  # make the bird go up after the player presses the spacebar
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()  # despawn all existing pipes
                bird_rect.center = (100, 512)  # reset the bird's position
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())  # add a new pipe to the list

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1  # choose a different wing animation from bird_frames
            else:
                bird_index = 0  # reset the index to the beginning of the list

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))  # position the background image at the origin point of the screen

    if game_active:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement  # make the bird fall down
        screen.blit(rotated_bird, bird_rect)  # draw the bird onto the bird_rect
        game_active = check_collision(pipe_list)  # check if the bird has collided with any pipes

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
