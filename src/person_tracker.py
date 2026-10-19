#!/usr/bin/env python3

import rospy
import numpy as np

from std_msgs.msg import Float32MultiArray


class PersonTracker:

    def __init__(self):

        rospy.init_node("person_tracker")

        rospy.loginfo("Person Tracker Started")

        # Subscriber from YOLO
        self.sub = rospy.Subscriber(
            "/person_detection",
            Float32MultiArray,
            self.detection_callback,
            queue_size=1
        )

        # Output tracked target
        self.pub = rospy.Publisher(
            "/tracked_person",
            Float32MultiArray,
            queue_size=1
        )


        # Tracking variables

        self.target_locked = False

        self.target_id = None

        self.next_id = 1


        self.target = None

        self.last_seen = rospy.Time.now()


        # Parameters

        self.lock_distance_threshold = 250


        rospy.spin()



    def detection_callback(self, msg):


        data = msg.data


        detected = data[0]


        if detected == 0:

            self.publish_lost()

            return



        x = data[1]

        y = data[2]

        width = data[3]

        height = data[4]

        confidence = data[5]



        current_person = {

            "x": x,

            "y": y,

            "width": width,

            "height": height,

            "confidence": confidence

        }



        # First detected person

        if not self.target_locked:


            self.target_locked = True

            self.target_id = self.next_id

            self.next_id += 1


            self.target = current_person


            rospy.loginfo(
                "Target locked ID: %d",
                self.target_id
            )


        else:


            # Compare with previous target

            distance = abs(
                current_person["x"]
                -
                self.target["x"]
            )



            if distance < self.lock_distance_threshold:


                self.target = current_person

                self.last_seen = rospy.Time.now()


            else:


                rospy.logwarn_throttle(
                    2,
                    "Different person detected. Keeping ID %d",
                    self.target_id
                )



        self.publish_target()



    def publish_target(self):


        if self.target is None:

            return


        msg = Float32MultiArray()


        msg.data = [

            float(self.target_id),

            float(self.target["x"]),

            float(self.target["y"]),

            float(self.target["width"]),

            float(self.target["height"]),

            float(self.target["confidence"])

        ]


        self.pub.publish(msg)



    def publish_lost(self):


        if self.target_locked:


            elapsed = (
                rospy.Time.now()
                -
                self.last_seen
            ).to_sec()



            if elapsed > 3.0:


                rospy.logwarn(
                    "Target lost. Unlocking ID %d",
                    self.target_id
                )


                self.target_locked = False

                self.target_id = None

                self.target = None



        msg = Float32MultiArray()


        msg.data = [

            0,

            0,

            0,

            0,

            0,

            0

        ]


        self.pub.publish(msg)



if __name__ == "__main__":

    try:

        PersonTracker()

    except rospy.ROSInterruptException:

        pass
