# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2


# compute and return the distance from the hand to the camera using triangle similarity
def distance_to_camera(knownWidth, focalLength, pixelWidth):
    return (knownWidth * focalLength) / pixelWidth


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# load the input image, resize it, and convert it to grayscale
image = cv2.imread(args["image"])
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# detect faces in the grayscale image
rects = detector(gray, 1)

for (i, rect) in enumerate(rects):
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)
    (x, y, w, h) = face_utils.rect_to_bb(rect)
    # Determined using a piece of paper of known length, code can be found in distance to camera
    focalLength = 350
    # The average width of a human hand (inches) http://www.theaveragebody.com/average_hand_size.php
    # added an inch since thumb is not included
    avg_width = 6.8
    # To more easily differetiate distances and detected bboxes
    color = None
    color0 = (255, 0, 0)
    color1 = (0, 50, 255)

    dist = distance_to_camera(avg_width, focalLength, int(int(w+x) - int(x)))
    distance = str(round(dist, 2))
    print(w, avg_width, focalLength, int(x), int(y), distance)

    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 2)
    # show the face number
    # cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(image, "distance:" + distance+ ' inches', (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # cv2.putText(image, 'distance: ' + str("{0:.2f}".format(dist) + ' inches'),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
    for (x, y) in shape:
        cv2.circle(image, (x, y), 1, (255, 255, 0), -1)

# show the output image with the face detections + facial landmarks
cv2.imshow("Output", image)
cv2.waitKey(0)
