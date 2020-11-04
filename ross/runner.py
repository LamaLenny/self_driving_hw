#! /usr/bin/python

import rospy
from geometry_msgs.msg import Twist
from rospy import Publisher, Subscriber
from turtlesim.msg import Pose
import math

EPS = 1e-1

class Run_Misha_Run:
    # Misha follows turtle1
    def __init__(self):
        self.pub_Misha = Publisher('/Misha/cmd_vel', Twist, queue_size=10)
        self.sub_Misha = Subscriber('/Misha/pose', Pose, self.give_pose_Misha)
        self.pose_Misha = Pose()
        self.sub_turtle1 = Subscriber('/turtle1/pose', Pose, self.follow_turtle1)        

    def give_pose_Misha(self, pose):
        # pose - Misha's pose
        self.pose_Misha = pose

    def distance_to_Misha(self, pose):
        return math.sqrt(math.pow(self.pose_Misha.x - pose.x, 2) + math.pow(self.pose_Misha.y - pose.y, 2))

    def rotate_Misha(self, pose):
        desired_angle = math.atan2((pose.y - self.pose_Misha.y) , (pose.x - self.pose_Misha.x))
        rotate = desired_angle - self.pose_Misha.theta   
        if rotate < -math.pi:
            rotate += 2 * math.pi
        elif rotate > math.pi:
            rotate -= 2 * math.pi
        return rotate        

    def follow_turtle1(self, pose):
        # pose - turtle1's pose
        msg = Twist()
        distance = self.distance_to_Misha(pose) # If EPS is near to 0, Misha can't stop :(
        if distance < EPS:
            return
        rotate = self.rotate_Misha(pose)
        msg.linear.x = distance
        msg.angular.z = rotate
        self.pub_Misha.publish(msg)


rospy.init_node('run_Misha_run')
Run_Misha_Run()
rospy.spin()
