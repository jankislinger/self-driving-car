import GPIO
import numpy as np

GPIO.setup(GPIO.BOARD)


class Car:

    motor = Motor(7, 11)
    servo = Servo(0, 50, [0.1, 0.2])

    def forward(self):
        print('Forward')
        self.motor.forward()

    def backward(self):
        print('Backward')
        self.motor.backward()

    def stop(self):
        print('Stopped')
        self.motor.stop()

    def left(self):
        print('Left')
        self.servo.left()

    def right(self):
        print('Right')
        self.servo.right()

    def straight(self):
        print('Straight')
        self.servo.straight()


class Motor:

    def __init__(self, forward_pin, backward_pin):
        GPIO.setup(forward_pin, GPIO.OUT)
        GPIO.setup(backward_pin, GPIO.OUT)
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin

    def forward(self):
        GPIO.output(self.backward_pin, False)
        GPIO.output(self.forward_pin, True)

    def backward(self):
        GPIO.output(self.forward_pin, False)
        GPIO.output(self.backward_pin, True)

    def stop(self):
        GPIO.output(self.forward_pin, False)
        GPIO.output(self.backward_pin, False)


class Servo:

    def __init__(self, pin, frequency, dc_interval):
        self.pwm = GPIO.PWM(pin, frequency)
        self.pwm.start(np.mean(dc_interval))
        self.dc = dc_interval
        self.dc_width = np.diff(dc_interval)[0]

    def left(self):
        self.pwm.ChangeDutyCycle(self.dc[0])

    def right(self):
        self.pwm.ChangeDutyCycle(self.dc[1])

    def straight(self):
        self.pwm.ChangeDutyCycle(np.mean(self.dc))

    def turn(self, direction):
        new_dc = self.dc[0] + (direction + 1) / 2 * self.dc_width
        self.pwm.ChangeDutyCycle(new_dc)
