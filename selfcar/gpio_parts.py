import RPi.GPIO as GPIO

from selfcar.common import Tank, Motor


def gpio_start():
    print('initializing GPIO')
    GPIO.setmode(GPIO.BOARD)


def gpio_stop():
    print('ending GPIO')
    GPIO.cleanup()


class GpioTank(Tank):

    def __init__(self, track_channels):
        super().__init__(track_channels)
        self.right_track = GpioMotor(track_channels['right'])
        self.left_track = GpioMotor(track_channels['right'])


class GpioMotor(Motor):

    def __init__(self, channels, pwm_frequency=50):
        super().__init__(channels, pwm_frequency)
        GPIO.setup(channels['forward'], GPIO.OUT)
        GPIO.setup(channels['backward'], GPIO.OUT)
        self.forward_pin = GPIO.PWM(channels['forward'], pwm_frequency)
        self.backward_pin = GPIO.PWM(channels['backward'], pwm_frequency)
