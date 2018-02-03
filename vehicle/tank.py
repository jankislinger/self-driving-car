import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

RT_FWD_PIN = 7
RT_BWD_PIN = 11
LT_FWD_PIN = 13
LT_BWD_PIN = 15

FORWARD  =  1
BACKWARD = -1
STOPPED  =  0


class Tank:

    status = {'fwd': False, 'bwd': False, 'lt': False, 'rt': False}

    def __init__(self):
        self.right_track = Motor(RT_FWD_PIN, RT_BWD_PIN)
        self.left_track = Motor(LT_FWD_PIN, LT_BWD_PIN)

    def button_action(self, button, action):
        self.status[button] = action
        self.update_drive()

    def update_drive(self):
        if self.status['fwd'] and not self.status['bwd']:
            if self.status['rt'] and not self.status['lt']:
                self.forward_right()
            elif self.status['lt'] and not self.status['rt']:
                self.forward_left()
            else:
                self.forward()
        elif self.status['bwd'] and not self.status['fwd']:
            if self.status['rt'] and not self.status['lt']:
                self.backward_right()
            elif self.status['lt'] and not self.status['rt']:
                self.backward_left()
            else:
                self.backward()
        else:
            if self.status['rt'] and not self.status['lt']:
                self.right()
            elif self.status['lt'] and not self.status['rt']:
                self.left()
            else:
                self.stop()

    def forward(self):
        self.right_track.backward()
        self.left_track.backward()

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

    def left(self):
        self.servo.left()

    def right(self):
        self.servo.right()

    def get_status(self):
        return {'right_track': self.right_track.status,
                'left_track': self.left_track.status}


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
