import datetime
import imutils
import time
import cv2
import numpy as np
from imutils.video import VideoStream

names = ['videos/cm-far3_2018-02-01_15-56.mkv', 'videos/vani-farslow.mkv'];
window_titles = ['first', 'second']

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (480, 1920))
out2 = cv2.VideoWriter('output2.avi',fourcc, 20.0, (480, 1920))


cap = [cv2.VideoCapture(i) for i in names]

# initialize the first frame in the video stream
firstFrame = [None] * len(names);
frameDelta = [None] * len(names)
thresh = [None] * len(names)
cnts = [None] * len(names)
cont = [None] * len(names)
x = [None] * len(names)
y = [None] * len(names)
w = [None] * len(names)
h = [None] * len(names)
numpy_horizontal_concat = [None] * len(names)
frames = [None] * len(names);
gray = [None] * len(names);
ret = [None] * len(names);

while True:

    for i,c in enumerate(cap):
        if c is not None:
            ret[i], frames[i] = c.read();

    for i,f in enumerate(frames):
        
        if ret[i] is True:
            gray[i] = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            gray[i] = cv2.GaussianBlur(gray[i], (7, 7), 0)
            if firstFrame[i] is None:
                firstFrame[i] = gray[i]
                continue

            frameDelta[i] = cv2.absdiff(firstFrame[i], gray[i])
            thresh[i] = cv2.threshold(frameDelta[i], 15, 255, cv2.THRESH_BINARY)[1]
         
            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh[i] = cv2.dilate(thresh[i], None, iterations=4)
            (_,cnts[i], _) = cv2.findContours(thresh[i].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
         
            # loop over the contours
            for cont[i] in cnts[i]:
                # if the contour is too small, ignore it
                if cv2.contourArea(cont[i]) < 500:
                    continue
         
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x[i], y[i], w[i], h[i]) = cv2.boundingRect(cont[i])
                cv2.rectangle(gray[i], (x[i], y[i]), (x[i] + w[i], y[i] + h[i]), (0, 255, 0), 2)
                text = "Occupied"

            # show the frame and record if the user presses a key
            numpy_horizontal_concat[i] = np.concatenate((gray[i],thresh[i],frameDelta[i]), axis=1)

            

            print(numpy_horizontal_concat[i].shape)
            cv2.imshow(window_titles[i], numpy_horizontal_concat[i]);

    if cv2.waitKey(50) & 0xFF == ord('q'):
       break


for c in cap:
    if c is not None:
        c.release();