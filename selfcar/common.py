class Vehicle:

    status = None
    driver = None

    def __init__(self):
        self.status = {'steer': 0, 'power': 0}

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


class Tank(Vehicle):

    def __init__(self, track_channels):
        super().__init__()
        self.right_track = Motor(track_channels['right'])
        self.left_track = Motor(track_channels['right'])

    def update_driving(self):
        if self.status['power'] > 0:
            if self.status['steer'] > 0:
                self.forward_right()
            elif self.status['steer'] < 0:
                self.forward_left()
            else:
                self.forward()
        elif self.status['power'] < 0:
            if self.status['steer'] > 0:
                self.backward_right()
            elif self.status['steer'] < 0:
                self.backward_left()
            else:
                self.backward()
        else:
            if self.status['steer'] > 0:
                self.right()
            elif self.status['steer'] < 0:
                self.left()
            else:
                self.stop()

    def forward(self):
        self.right_track.forward()
        self.left_track.forward()

    def backward(self):
        self.right_track.backward()
        self.left_track.backward()

    def forward_right(self):
        self.right_track.stop()
        self.left_track.forward()

    def backward_right(self):
        self.right_track.stop()
        self.left_track.backward()

    def forward_left(self):
        self.right_track.forward()
        self.left_track.stop()

    def backward_left(self):
        self.right_track.backward()
        self.left_track.stop()

    def stop(self):
        self.right_track.stop()
        self.left_track.stop()

    def right(self):
        self.right_track.backward()
        self.left_track.forward()

    def left(self):
        self.right_track.forward()
        self.left_track.backward()


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


class Motor:

    def __init__(self, channels, pwm_frequency):
        self.channels = channels
        self.pwm_frequency = pwm_frequency
        self.status = 0
        self.forward_pin = PwmPin()
        self.backward_pin = PwmPin()

    def forward(self, power=1):
        self.status = power
        self.backward_pin.stop()
        self.forward_pin.start(power * 100)

    def backward(self, power=1):
        self.status = -power
        self.forward_pin.stop()
        self.backward_pin.start(power * 100)

    def stop(self):
        self.status = 0
        self.backward_pin.stop()
        self.forward_pin.stop()


class PwmPin:

    def __init__(self):
        pass

    def start(self, dc):
        pass

    def stop(self):
        pass
