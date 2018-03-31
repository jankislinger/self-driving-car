import threading
import Queue
import time
import cv2
import json


class Saver(threading.Thread):

    def __init__(self, folder, key):
        threading.Thread.__init__(self)
        self.daemon = True
        self.folder = folder
        self.queue = Queue.Queue()
        self.text_file = open('{0}/{1}.txt'.format(folder, key), 'w')

    def run(self):
        while True:
            if not self.queue.empty():
                self.save(self.queue.get_nowait())
            else:
                time.sleep(0.05)

    def save(self, x):
        data_type = x['type']
        print 'trying to save object of type', type
        if data_type == 'image':
            self.save_image(x['image'], x['name'])
        elif data_type == 'status':
            self.save_status(x['status'])

    def save_image(self, image, name):
        filename = self.folder + '/' + name + '.png'
        cv2.imwrite(filename, image)

    def save_status(self, status):
        json.dump(status, self.text_file)
        self.text_file.write('\n')

    def put(self, item):
        self.queue.put_nowait(item)
