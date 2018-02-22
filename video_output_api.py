
#python video_output_api.py --video videos/cm-far_2018-02-01_15-54.mkv 
# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
from imutils.video import VideoStream
import os
import datetime
import glob
import imageio
import requests
import json

fps = 12

url = 'http://www.bordersec.olbx.in/ci/test_api'
gif_name = 'outputName'

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=4500, help="minimum area size")

args = vars(ap.parse_args())
camera = cv2.VideoCapture(args["video"])
 
# initialize the first frame in the video stream
firstFrame = None

frame_list = np.empty([480,640])


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output_video/original.avi',fourcc, 20.0, (640,480))
out2 = cv2.VideoWriter('output_video/detected.avi',fourcc, 20.0, (640,480))

frame_count_object = 0
# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	(grabbed, frame) = camera.read()
	text = "Unoccupied"
	# if the frame could not be grabbed, then we have reached the end of the video
	if not grabbed:
		break
 	# resize the frame, convert it to grayscale, and blur it
	# frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame_single = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (7, 7), 0)
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue
	# compute the absolute difference between the current frame and first frame then perform thresholding
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=8)
	(_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 	
	out.write(frame)
	frame_list = np.dstack((frame_list,frame))

	# loop over the contours

	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

	print(frame_count_object)
	if(text == "Occupied"):
		frame_count_object = frame_count_object + 1

	if(frame_count_object >= 30):
		frame_count_object = 0
		print("Intrusion for more than 1 second")
		filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
		cv2.imwrite("detection_images/detetected"+filename1+".png", frame)
		os.system("aplay sounds/siren3.wav")
		files = {'file': open('/home/zaverichintan/Study/final_year_project/file-video-stream/detection_images/detetected'+filename1+'.png', 'rb')}
		payload = {"device":"gabriel","data_type":"data","zone":1,"camera_no":1}
		data = json.dumps(payload)
		r = requests.post(url, files=files, data = payload)
		print(r.text)



	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 

	out2.write(frame)
	
	cv2.imshow('Numpy Horizontal Concat', frame)
	key = cv2.waitKey(1) & 0xFF
	
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break



# cleanup the camera and close any open windows
camera.release()
out.release()
out2.release()
cv2.destroyAllWindows()
