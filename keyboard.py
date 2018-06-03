import pygame
from RPi import GPIO
from tank_old import Tank

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


try:
    while running:
        clock.tick(20)

        for event in pygame.event.get():
            process_event(event)

finally:
    tank.saver.text_file.close()
    pygame.quit()
    GPIO.cleanup()
