from selfcar.common import Vehicle
from selfcar.gpio_parts import Motor


class Tank(Vehicle):

    def __init__(self, track_channels):
        self.Vehicle.__init__()
        self.right_track = Motor(track_channels['right'])
        self.left_track = Motor(track_channels['right'])

    def __update_driving(self):
        if self.status['power'] > 0:
            if self.status['steer'] > 0:
                self.__forward_right()
            elif self.status['steer'] < 0:
                self.__forward_left()
            else:
                self.__forward()
        elif self.status['power'] < 0:
            if self.status['steer'] > 0:
                self.__backward_right()
            elif self.status['steer'] < 0:
                self.__backward_left()
            else:
                self.__backward()
        else:
            if self.status['steer'] > 0:
                self.__right()
            elif self.status['steer'] < 0:
                self.__left()
            else:
                self.__stop()

    def __forward(self):
        self.right_track.forward()
        self.left_track.forward()

    def __backward(self):
        self.right_track.backward()
        self.left_track.backward()

    def __forward_right(self):
        self.right_track.stop()
        self.left_track.forward()

    def __backward_right(self):
        self.right_track.stop()
        self.left_track.backward()

    def __forward_left(self):
        self.right_track.forward()
        self.left_track.stop()

    def __backward_left(self):
        self.right_track.backward()
        self.left_track.stop()

    def __stop(self):
        self.right_track.stop()
        self.left_track.stop()

    def __right(self):
        self.right_track.backward()
        self.left_track.forward()

    def __left(self):
        self.right_track.forward()
        self.left_track.backward()
