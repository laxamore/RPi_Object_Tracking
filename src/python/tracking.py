#!/usr/bin/env python3

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
 
camera = PiCamera()
camera.resolution = (426, 240)
camera.framerate = 15

rawCapture = PiRGBArray(camera, size=(426, 240))
 
# Delay for let camera startup
time.sleep(2)

camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = 1.75
 
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
 
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	rawCapture.truncate(0)
 
	if key == ord("q"):
		break