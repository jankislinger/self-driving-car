class Vehicle:

    def __init__(self):
        self.status = {'steer': 0, 'power': 0}
        self.driver = None

    def drive(self, power, steer):
        self.power(power, False)
        self.steer(steer, False)
        self.update_driving()

    def start(self):
        print('Vehicle started.')

    def stop(self):
        self.drive(power=0, steer=0)
        self.driver.active = False
        print('Vehicle stopped.')

    def steer(self, direction, update=True):
        self.status['steer'] = direction
        if update:
            self.update_driving()

    def steer_right(self):
        self.steer(1)

    def steer_left(self):
        self.steer(-1)

    def steer_straight(self):
        self.steer(0)

    def power(self, power, update=True):
        self.status['power'] = power
        if update:
            self.update_driving()

    def power_forward(self):
        self.power(1)

    def power_backward(self):
        self.power(-1)

    def power_stop(self):
        self.power(0)

    def update_driving(self):
        print('Vehicle is updating driving.')
        pass

    def get_data(self):
        print('Getting data from Vehicle.')
        return {'status': self.status}


class Driver:

    def __init__(self):
        self.active = False
        self.last_data = None
        self.vehicle = None

    def drive(self, vehicle):
        print('Driver is driving a vehicle.')
        self.vehicle = vehicle
        self.vehicle.driver = self
        self.vehicle.start()
        self.active = True

    def process_data(self, data):
        print('Driver is processing data.')
        self.last_data = data
