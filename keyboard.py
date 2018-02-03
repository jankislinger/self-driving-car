import pygame
from vehicle.tank import Tank

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((640, 480))

WHITE = (255, 255, 255)
RED   = (255,   0,   0)

x = 60
y = 250

going_left = False
going_right = False
going_up = False
going_down = False

running = True

tank = Tank()


def process_event(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        global running
        running = False
    elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        action = event.type == pygame.KEYDOWN
        if event.key == pygame.K_LEFT:
            button = 'lt'
        elif event.key == pygame.K_RIGHT:
            button = 'rt'
        elif event.key == pygame.K_UP:
            button = 'fwd'
        elif event.key == pygame.K_DOWN:
            button = 'bwd'
        tank.button_action(button, action)
    elif event.type == pygame.QUIT:
        global running
        running = False

try:
    while running:
        clock.tick(20)

        for event in pygame.event.get():
            process_event(event)

finally:
    pygame.quit()
    GPIO.cleanup()
