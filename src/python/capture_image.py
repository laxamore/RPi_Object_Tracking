#!/usr/bin/env python

import sys
import time
import cv2
import os
import numpy as np

from picamera.array import PiRGBArray
from picamera import PiCamera

script_dir = os.path.dirname(os.path.realpath(__file__)) 

def main(args):
    global script_dir
    camera = PiCamera()
    camera.resolution = (426, 240)
    camera.framerate = 10

    rawCapture = PiRGBArray(camera, size=(426, 240))

    # Delay for let camera startup
    time.sleep(2)

    camera.exposure_mode = 'off'
    # camera.iso = 800
    # camera.analog_gain = 1000
    camera.awb_mode = 'off'
    camera.awb_gains = 1.75

    index = 0
    print script_dir + "/../../image_capture/image" + str(index)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imwrite(script_dir + "/../../image_capture/image" + str(index) + ".jpg", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        index = index + 1
        time.sleep(1)
        if key == ord("q"):
            break

if __name__ == '__main__':
    main(sys.argv)