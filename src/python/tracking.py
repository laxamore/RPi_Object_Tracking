#!/usr/bin/env python3

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import yaml
import os

script_dir = os.path.dirname(os.path.realpath(__file__)) 

stream = file(script_dir + '/../../cfg/cv/tracking_calibration.yaml', 'r')
calibValue = yaml.load(stream)

lower = [
	calibValue['h_low'],
	calibValue['s_low'],
	calibValue['v_low']
]

upper = [
	calibValue['h_up'],
	calibValue['s_up'],
	calibValue['v_up']
]

# print lower, upper

camera = PiCamera()
camera.resolution = (426, 240)
camera.framerate = 15

rawCapture = PiRGBArray(camera, size=(426, 240))
 
# Delay for let camera startup
time.sleep(2)

camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = 1.75

kernel = np.ones((3, 3), np.uint8)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
 	
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	
	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

	objCntr = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

	if len(objCntr) > 0:
        c = max(objCntr, key=cv2.contourArea)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		cv2.circle(image, center, 5, (0, 255, 0), -1)
	
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	rawCapture.truncate(0)
 
	if key == ord("q"):
		break