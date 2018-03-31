import RPi.GPIO as GPIO
import threading
from sensor.vision import Vision
from utils.saver import Saver
import utils.utils as utils
import time

GPIO.setmode(GPIO.BOARD)

RT_FWD_PIN = 7   # red     IN4
RT_BWD_PIN = 11  # orange  IN3
LT_FWD_PIN = 13  # yellow  IN2
LT_BWD_PIN = 15  # green   IN1

RECORD_PIN = 12

FORWARD  =  1
BACKWARD = -1
STOPPED  =  0

startup_time = 10.0

GPIO.setup(RECORD_PIN, GPIO.OUT)
GPIO.output(RECORD_PIN, False)


class Tank:

    status = {'fwd': False, 'bwd': False, 'lt': False, 'rt': False}

    def __init__(self):
        self.session_key = utils.random_key()
        self.screen_id = 0
        self.recording = False

        self.right_track = Motor(RT_FWD_PIN, RT_BWD_PIN)
        self.left_track = Motor(LT_FWD_PIN, LT_BWD_PIN)
        self.vision = Vision()
        self.saver = Saver('data', self.session_key)

        self.vision.start()
        self.saver.start()
        threading.Timer(startup_time - 0.1, self.switch_recording).start()
        threading.Timer(startup_time, self.save_status).start()

    def save_status(self):
        timer = threading.Timer(1.0, self.save_status)
        timer.daemon = True
        timer.start()

        image_name = self.session_key + '-' + str(self.screen_id).zfill(5)
        image = self.vision.snapshot()

        status = self.status.copy()
        status.update({'time': time.time(), 'image_name': image_name, 'screen_key': self.screen_id})

        self.saver.put({'type': 'status', 'status': status})
        self.saver.put({'type': 'image', 'image': image, 'name': image_name})

        self.screen_id += 1

    def button_action(self, button, action):
        if button in self.status.keys() and type(action) == bool:
            self.status[button] = action
            print 'status changed', self.status
            self.update_drive()

    def switch_recording(self):
        self.recording = not self.recording
        GPIO.output(RECORD_PIN, self.recording)

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
