import cv2

from face_detection import detect_face

i = 0
cam = cv2.VideoCapture(i)
print('trying slot {}'.format(i))

if not cam.isOpened():
    print('camera is not open')

ret, image = cam.read()

cv2.imshow('image', image)
cv2.waitKey(1)

# time.sleep(3)


while ret:
    ret, image = cam.read()
    image = detect_face(image)
    cv2.imshow('image', image)
    cv2.waitKey(1)

