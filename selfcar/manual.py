import pygame
import numpy as np

from selfcar.common import Driver

key_types = [pygame.KEYDOWN, pygame.KEYUP]
arrows = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]


class ManualDriver(Driver):

    def __init__(self):
        super().__init__()
        self.key_status = {a: False for a in arrows}
        pygame.init()
        self.screen = pygame.display.set_mode((640, 360))
        self.clock = pygame.time.Clock()

    def drive(self, vehicle):
        super(ManualDriver, self).drive(vehicle)
        while self.active:
            data = self.vehicle.get_data()
            self.process_data(data)
            self.process_events()
            self.clock.tick(30)
        self.vehicle.stop()

    def process_data(self, data):
        if 'frame' in data and data['frame'] is not None:
            surface = frame_as_surface(data['frame'])
            self.screen.blit(surface, (0, 0))
        if 'status' in data:
            status = data['status']
            draw_polygon(self.screen, False, True,  status['power'] > 0)
            draw_polygon(self.screen, False, False, status['power'] < 0)
            draw_polygon(self.screen, True,  False, status['steer'] > 0)
            draw_polygon(self.screen, True,  True,  status['steer'] < 0)
        pygame.display.update()

    def process_events(self):
        events = pygame.event.get(key_types + [pygame.QUIT])
        for event in events:
            self.process_event(event)
            if not self.active:
                return
        if len(events) > 0:
            power = self.get_key_diff(pygame.K_UP, pygame.K_DOWN)
            steer = self.get_key_diff(pygame.K_RIGHT, pygame.K_LEFT)
            self.vehicle.drive(power, steer)

    def process_event(self, event):
        print_event(event)
        if is_stop_event(event):
            self.active = False
        elif event.type in key_types and event.key in arrows:
            self.key_status[event.key] = event.type == pygame.KEYDOWN

    def get_key_diff(self, key_x, key_y):
        x = int(self.key_status[key_x])
        y = int(self.key_status[key_y])
        return x - y


def is_stop_event(event):
    return event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)


def print_event(event):
    ev_type = {pygame.QUIT: 'QUIT', pygame.KEYDOWN: 'KEYDOWN', pygame.KEYUP: 'KEYUP'}[event.type]
    if event.type in key_types:
        print('Processing event of type {} and key {}'.format(ev_type, event.key))
    else:
        print('Processing event of type {}'.format(ev_type))


def frame_as_surface(frame):
    frame = np.rot90(np.flip(frame, 1))
    return pygame.surfarray.make_surface(frame)


def arrow_points(horizontal, flipped):
    d = 15
    center = [580, 300]
    offset = [[d, -10], [5+d, 0], [d, 10], [25+d, 0]]
    if not horizontal:
        offset = [list(reversed(point)) for point in offset]
    if flipped:
        offset = [[-x for x in point] for point in offset]
    return [[c + x for x, c in zip(point, center)] for point in offset]


def draw_polygon(screen, horizontal, flipped, active):
    width = 3
    color = (0, 0, 0)
    pygame.draw.polygon(screen, color, arrow_points(horizontal, flipped), 0 if active else width)
