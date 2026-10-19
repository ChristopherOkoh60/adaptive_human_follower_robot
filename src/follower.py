#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist


class SimpleFollower:

    def __init__(self):

        rospy.init_node("simple_follower")

        rospy.loginfo("----------------------------------")
        rospy.loginfo(" Summit XL Simple Follow Controller")
        rospy.loginfo(" Proof Of Concept V6")
        rospy.loginfo("----------------------------------")

        # -----------------------------
        # Parameters
        # -----------------------------

        
        # Distance reference
        # Adjust only after robot is stable
        self.target_height = 720

        # Dead zone
        self.height_deadband = 60


        # VERY slow indoor motion
        self.MAX_FORWARD = 0.005
        
        self.MAX_REVERSE = 0.003
        
        self.KP_DISTANCE = 0.0003

        # Current detection
        self.person_seen = False

        self.height = 0


        # Publisher
        self.cmd_pub = rospy.Publisher(
            "/summit_xl/cmd_vel",
            Twist,
            queue_size=1
        )


        rospy.Subscriber(
            "/person_detection",
            Float32MultiArray,
            self.person_callback
        )


        self.rate = rospy.Rate(10)


        rospy.loginfo("Listening: /person_detection")
        rospy.loginfo("Publishing: /summit_xl/cmd_vel")


    def person_callback(self, msg):

        if len(msg.data) < 6:
            return

        self.person_seen = bool(msg.data[0])

        if not self.person_seen:
            return

        self.height = float(msg.data[4])


    def control(self):

        while not rospy.is_shutdown():

            cmd = Twist()

            if self.person_seen:

            #-----------------------------------------
            # Distance control only
            #-----------------------------------------

                height_error = self.target_height - self.height

                linear_speed = self.KP_DISTANCE * height_error


            # Stop when close enough
                if abs(height_error) < self.height_deadband:
                    linear_speed = 0.0


            # Limit forward speed
                if linear_speed > self.MAX_FORWARD:
                    linear_speed = self.MAX_FORWARD


            # Limit reverse speed (slower Indoors)
                if linear_speed < -self.MAX_REVERSE:
                    linear_speed = -self.MAX_REVERSE


                cmd.linear.x = linear_speed

            # Completely disable turning
                cmd.angular.z = 0.0


                rospy.loginfo(
                    "height=%.1f target=%.1f error=%.1f linear=%.3f",
                    self.height,
                    self.target_height,
                    height_error,
                    cmd.linear.x
                )

            else:

                cmd.linear.x = 0.0
                cmd.angular.z = 0.0

            self.cmd_pub.publish(cmd)

            self.rate.sleep()
    
    
if __name__=="__main__":

    try:

        follower = SimpleFollower()
        follower.control()


    except rospy.ROSInterruptException:

        pass
