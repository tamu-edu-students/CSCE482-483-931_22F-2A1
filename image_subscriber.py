#Checkout http://wiki.ros.org/cv_bridge/Tutorials
import sys
import cv2
import rospy
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

bridge = CvBridge()
def callback_Img(data):
    img = bridge.imgmsg_to_cv2(data, desired_encoding='rgb8')
    # Start coordinate, here (5, 5)
# represents the top left corner of rectangle
    start_point = (5, 5)
  
# Ending coordinate, here (220, 220)
# represents the bottom right corner of rectangle
    end_point = (220, 220)
  
# Blue color in BGR
    color = (255, 0, 0)
  
# Line thickness of 2 px
    thickness = 2
    img = cv2.rectangle(img, start_point, end_point, color, thickness)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayImageMsg = CvBridge().cv2_to_imgmsg(gray.astype(np.uint8))
    grayImageMsg.header = data.header
    grayImageMsg.encoding = '8UC1'
    grayImgPub.publish(grayImageMsg)

rospy.init_node('img_record_node')
rospy.Subscriber("/front_camera/image_raw", Image, callback_Img)
grayImgPub = rospy.Publisher('/img_gray', Image, queue_size=10)
rospy.spin()
