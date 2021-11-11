import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

print("Camera feed is up! Try pressing any button in the feed to take a new picture.")

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()

    classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # perform face detection
    bboxes = classifier.detectMultiScale(frame)
    # print bounding box for each detected face
    for box in bboxes:
        # extract
        x, y, width, height = box
        x2, y2 = x + width, y + height
        # draw a rectangle over the pixels
        cv2.rectangle(frame, (x, y), (x2, y2), (0,0,255), 1)
    # show the image
    cv2.imshow('face detection', frame)


    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")