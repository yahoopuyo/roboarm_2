#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import random

r = [0.6, 0.8, 0.8] #how often each joint keeps the direction
joint_range = [6.28, 2, 2] #the range of motion of each joint
tick = [0.1, 0.1, 0.1] #how much each joint moves per frame
is_continuous = [True,False,False] #whether each joint is continuos or not

def wave():
    pub1 = rospy.Publisher('/roboarm2/joint1_position_controller/command', Float64, queue_size=10)
    pub3 = rospy.Publisher('/roboarm2/joint3_position_controller/command', Float64, queue_size=10)
    pub4 = rospy.Publisher('/roboarm2/joint4_position_controller/command', Float64, queue_size=10)
    rospy.init_node('wave', anonymous=True)
    
    rate = rospy.Rate(50)
    pos = [0,0,0] #initialized position of each joint
    
    while not rospy.is_shutdown():
        for i in range(len(pos)):
            if random.random() > r[i]:
                tick[i] = -1 * tick[i] #reverse direction
            if is_continuous[i]:
                pos[i] = (pos[i] + joint_range[i] / 2 + tick[i]) % joint_range[i] - joint_range[i] / 2 #if continuous keep going

            else:
                if pos[i] + tick[i] > joint_range[i] / 2 or pos[i] + tick[i] < -1 * joint_range[i] / 2:
                    pos[i] = pos[i] - tick[i] #if the joint reaches limit, reverse direction
                else:
                    pos[i] = pos[i] + tick[i]
                            
        #pos = [random.uniform(-3.14,3.14), random.uniform(-1.0,1.0), random.uniform(-1.0,1.0)]
        #pos = [0,0,1]

        pub1.publish(pos[0])
        pub3.publish(pos[1])
        pub4.publish(pos[2])
        #rospy.loginfo("joint position %s", pos) #uncomment to print the joint position
        rate.sleep()

if __name__ == '__main__':
    try:
        wave()   
    except rospy.ROSInterruptException:
        pass
