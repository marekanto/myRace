#!/usr/bin/env python
from cv_bridge import CvBridge
import numpy as np
import rospy
import cv2 as cv
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import signal
import time
from sensor_msgs.msg import Image
from sensor_msgs.msg import Range
import sys


def set_vel(vel, sidevel, omg):
    global twist
    global pub
    twist = Twist()
    twist.linear.x = vel
    twist.angular.z = omg
    twist.linear.y = sidevel
    pub.publish(twist)


def start_vel_publisher():
    global pub
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=3)
    rospy.init_node('Control', anonymous=True)


def listner():
    global bridge
    # create a window to display results in
    cv.namedWindow("image_view", 1)
    bridge = CvBridge()
    image_sub = rospy.Subscriber("/rgb_image", Image, callback1, queue_size=1)
    depth_sub = rospy.Subscriber("/depth_image", Image, callback2, queue_size=1)
    sensor1_sub = rospy.Subscriber('/s1', Range, callback_sens, 'msg1')
    sensor2_sub = rospy.Subscriber('/s2', Range, callback_sens, 'msg2')
    sensor3_sub = rospy.Subscriber('/s3', Range, callback_sens, 'msg3')

def callback_sens(msg,case):
    if case=='msg1':
        activity['s1']=msg.range
    elif case=='msg2':
        activity['s2']=msg.range
    else:
        activity['s3']=msg.range

    sensor(activity)
    # set_vel(0,5,0)

def sensor(act):

    if act['s1'] <=1 and act['s3'] <=1:
        set_vel(-5,0,0)

    elif act['s2'] <=1:
        set_vel(5,0,0)

    elif act['s1'] <=1:
        set_vel(0,-2,0)

    elif act['s3'] <=1:
        set_vel(0,2,0)


def callback1(rgb_data):
    # This is a callback which recieves images and processes them.
    RGB_image(rgb_data)


def callback2(depth_data):
    remove_ground(depth_data)

def save_to_file(depth_array):
    np.savetxt("Ground_Data.csv",depth_array,delimiter=",")
    sys.exit(0)

def remove_ground(depth_data):
    depth_array = Depth_image(depth_data)
    flag=0
    obs_data=[]
    #print(depth_array)
    #save_to_file(depth_array)
    ground_array=np.genfromtxt("Ground_Data.csv",delimiter=",")
    #rows,cols=ground_array.shape
    # print(rows,cols)
    rows, cols = depth_array.shape
    print(rows,cols)
    diff=np.amin(depth_array - ground_array)
    np.savetxt("diff.csv",depth_array - ground_array, delimiter=",")
    sys.exit(0)
    # for col in range(0, cols):
    #     for row in range(0, 190):
    #          if depth_array[row][col] < ground_array[row][col] - 0.0025: # removing noise
    #             flag=1
    #             break
    #
    # if flag == 1:
    #     set_vel(0,0,0)
    #             obs_data[row][col]=depth_array[row][col]





    #print(ground_array)
    # height =17.06 # height of kinect above ground in cm 4 cm from mounting (to be checked)
    # aplha=0 #tilt angle of kinec
    # rows, cols = depth_array.shape
    # cy=cols/2
    # cx=rows/2
    # jmin = list(depth_array[0])
    # for col in range(0, cols):
    #     for row in range(100, 300):
    #         if depth_array[row][col] < jmin[col]:
    #             jmin[col]=depth_array[row][col]

    #print(jmin)
    #print(jmin)

    # for col in range(0, cols, 10):
    #     print(depth_array[rows / 2][col])
        # if (depth_array[rows/2][col]!=0.7):
        #    set_vel(-5,0,0)
        #    time.sleep(1)
        #   break
    # set_vel(3,0,2)

    # row=depth_array[rows/2]
    # print(min(row))
    # (msg.step/msg.width) #bytes for signle pixel


def RGB_image(rgb_data):
    # This is a callback which recieves images and processes them.
    # convert image into openCV format
    rgb_image = bridge.imgmsg_to_cv2(rgb_data, "bgr8")

    # Convert the image to a Numpy array since most cv2 functions
    # require Numpy arrays.
    cv.imshow("image_view", rgb_image)
    cv.waitKey(3)


def Depth_image(depth_data):
    # convert image into openCV format
    depth_image = bridge.imgmsg_to_cv2(depth_data, "32FC1")

    # Convert the image to a Numpy array since most cv2 functions
    depth_array = np.array(depth_image, dtype=np.dtype('f8'))
    cv.normalize(depth_array,depth_array, 0, 1, cv.NORM_MINMAX)
    flipped = cv.flip(depth_array, 0)

    cv.imshow("depth_image_view", flipped)
    cv.waitKey(3)

    return depth_array


def exit_int():
    sys.exit(0)


if __name__ == '__main__':

    activity={}
    #python dictionary to check the cases becase 2 sensors at a time can be active
    activity={'s1':0,'s2':0,'s3':0}
    print('started')

    signal.signal(signal.SIGINT, exit_int)
    start_vel_publisher()
    print('publisher started')
    listner()
    time.sleep(1)
    set_vel(-2, 0, 0)

    rospy.spin()  # for infinite loop

    cv.destroyAllWindows()
    # keeps your node from exiting until the node has been shutdown
