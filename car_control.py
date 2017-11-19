import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BOARD)

MOTOR_FWD_PIN  = 7
MOTOR_BWD_PIN  = 11
SERVO_PIN      = 18
SERVO_FREQ     = 50
SERVO_DC_RANGE = [5, 10]

FORWARD  =  1
BACKWARD = -1
STOPPED  =  0
LEFT     = -1
RIGHT    =  1
STRAIGHT =  0


class Car:

    def __init__(self):
        self.motor = Motor(MOTOR_FWD_PIN, MOTOR_BWD_PIN)
        self.servo = Servo(SERVO_PIN, SERVO_FREQ, SERVO_DC_RANGE)

    def forward(self):
        self.motor.forward()

    def backward(self):
        self.motor.backward()

    def stop(self):
        self.motor.stop()

    def left(self):
        self.servo.left()

    def right(self):
        self.servo.right()

    def straight(self):
        self.servo.straight()

    def get_status(self):
        return {'motor': self.motor.status,
                'servo': self.servo.status}


class Motor:

    def __init__(self, forward_pin, backward_pin):
        GPIO.setup(forward_pin, GPIO.OUT)
        GPIO.setup(backward_pin, GPIO.OUT)
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        self.status = STOPPED

    def forward(self):
        GPIO.output(self.backward_pin, False)
        GPIO.output(self.forward_pin, True)
        self.status = FORWARD

    def backward(self):
        GPIO.output(self.forward_pin, False)
        GPIO.output(self.backward_pin, True)
        self.status = BACKWARD

    def stop(self):
        GPIO.output(self.forward_pin, False)
        GPIO.output(self.backward_pin, False)
        self.status = STOPPED


class Servo:

    def __init__(self, pin, frequency, dc_interval):
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, frequency)
        self.pwm.start(np.mean(dc_interval))
        self.dc = dc_interval
        self.dc_width = np.diff(dc_interval)[0]
        self.status = STRAIGHT

    def left(self):
        self.pwm.ChangeDutyCycle(self.dc[0])
        self.status = LEFT

    def right(self):
        self.pwm.ChangeDutyCycle(self.dc[1])
        self.status = RIGHT

    def straight(self):
        self.pwm.ChangeDutyCycle(np.mean(self.dc))
        self.status = STRAIGHT
