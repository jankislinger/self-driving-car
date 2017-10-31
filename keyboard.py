import pygame
from car_control import *

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

car = Car()

try:
    while running:
        clock.tick(20)

        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, [x, y], 40)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    going_left = True
                    going_right = False
                    car.left()
                elif event.key == pygame.K_RIGHT:
                    going_right = True
                    going_left = False
                    car.left()
                elif event.key == pygame.K_UP:
                    going_up = True
                    going_down = False
                    car.forward()
                elif event.key == pygame.K_DOWN:
                    going_down = True
                    going_up = False
                    car.backward()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    going_left = False
                    car.straight()
                elif event.key == pygame.K_RIGHT:
                    going_right = False
                    car.straight()
                elif event.key == pygame.K_UP:
                    going_up = False
                    car.stop()
                elif event.key == pygame.K_DOWN:
                    going_down = False
                    car.stop()
            elif event.type == pygame.QUIT:
                running = False

        if going_left:
            x -= 1
        elif going_right:
            x += 1

        if going_up:
            y -= 1
        elif going_down:
            y += 1

        pygame.display.flip()

finally:
    pygame.quit()
