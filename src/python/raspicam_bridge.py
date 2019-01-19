#!/usr/bin/env python

from picamera.array import PiRGBArray
from picamera import PiCamera

import sys
import time
import cv2

import roslib
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def main(args):
    rospy.init_node('raspi_cam_pub', anonymous=True)
    
    image_pub = rospy.Publisher("raspi_cam_img", Image)
    bridge = CvBridge()

    camera = PiCamera()
    camera.resolution = (426, 240)
    camera.framerate = 15

    rawCapture = PiRGBArray(camera, size=(426   , 240))
    
    # Delay for let camera startup
    time.sleep(2)

    camera.exposure_mode = 'off'
    camera.awb_mode = 'off'
    camera.awb_gains = 1.75

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
    
        try:
            image_pub.publish(bridge.cv2_to_imgmsg(image, "bgr8"))
        except CvBridgeError as e:
            print(e)

        cv2.waitKey(1)    
        rawCapture.truncate(0)

if __name__ == '__main__':
    main(sys.argv)