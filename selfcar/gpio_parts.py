import RPi.GPIO as GPIO


def gpio_start():
    print('initializing GPIO')
    GPIO.setmode(GPIO.BOARD)


def gpio_stop():
    print('ending GPIO')
    GPIO.cleanup()


class Motor:

    def __init__(self, channels, pwm_frequency=50):
        GPIO.setup(channels['forward'], GPIO.OUT)
        GPIO.setup(channels['backward'], GPIO.OUT)
        self.forward_pin = GPIO.PWM(channels['forward'], pwm_frequency)
        self.backward_pin = GPIO.PWM(channels['backward'], pwm_frequency)

    def forward(self, power=1):
        self.backward_pin.stop()
        self.forward_pin.start(power)

    def backward(self, power=1):
        self.forward_pin.stop()
        self.backward_pin.start(power)

    def stop(self):
        self.backward_pin.stop()
        self.forward_pin.stop()
