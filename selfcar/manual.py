import pygame

from selfcar.common import Driver

key_types = [pygame.KEYDOWN, pygame.KEYUP]
arrows = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]


class ManualDriver(Driver):

    def __init__(self):
        super(ManualDriver, self).__init__()
        self.key_status = {a: False for a in arrows}
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

    def drive(self, vehicle):
        super(ManualDriver, self).drive(vehicle)
        while self.active:
            data = self.vehicle.get_data()
            self.process_data(data)
            self.process_events()
            self.clock.tick(2)
        self.vehicle.stop()

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
        self.print_event(event)
        if self.is_stop_event(event):
            self.active = False
        elif event.type in key_types and event.key in arrows:
            self.key_status[event.key] = event.type == pygame.KEYDOWN

    def get_key_diff(self, key_x, key_y):
        x = int(self.key_status[key_x])
        y = int(self.key_status[key_y])
        return x - y

    @staticmethod
    def is_stop_event(event):
        return event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)

    @staticmethod
    def print_event(event):
        ev_type = {pygame.QUIT: 'QUIT', pygame.KEYDOWN: 'KEYDOWN', pygame.KEYUP: 'KEYUP'}[event.type]
        if event.type in key_types:
            print('Processing event of type {} and key {}'.format(ev_type, event.key))
        else:
            print('Processing event of type {}'.format(ev_type))
