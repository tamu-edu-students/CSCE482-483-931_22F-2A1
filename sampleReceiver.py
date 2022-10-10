import sys
import rospy
import numpy as np
from sensor_msgs.msg import Image
from PIL import Image as displayImage

def callback_sampleReceiver(data):

    # display image here!
    displayImage.show();

rospy.init_node('sample_receiver')
rospy.Subscriber("/lane_detection", Image, callback_sampleReceiver)
rospy.spin()