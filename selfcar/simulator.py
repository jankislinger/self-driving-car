import cv2

from selfcar.common import Vehicle


class Simulator(Vehicle):

    def __init__(self, file_name):
        super().__init__()
        self.video = cv2.VideoCapture(file_name)

    def get_data(self):
        data = super().get_data()
        ret, data['frame'] = self.video.read()
        if not ret:
            self.driver.active = False
        return data
