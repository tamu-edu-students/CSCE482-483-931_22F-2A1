import sys
import cv2
import rospy
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

bridge = CvBridge()
def callback_old(data):

    # DO LANE DETECTION AND HYBRIDNETS THINGS HERE

    laneDetection.publish();

rospy.init_node('img_record_node')
rospy.Subscriber("/img_gray", Image, callback_old)
laneDetection = rospy.Publisher('/lane_detection', Image, queue_size=10)
rospy.spin()