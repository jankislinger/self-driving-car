import cv2
import threading
import time

grab_delay = 0.03


class Vision(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.cam = cv2.VideoCapture(0)

    def run(self):
        while True:
            time.sleep(grab_delay)
            self.cam.grab()

    def snapshot(self):
        print 'getting snapshot'
        ret, image = self.cam.read()
        return image

    def terminate(self):
        cv2.destroyAllWindows()
        self.cam.release()
