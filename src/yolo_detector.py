#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
import time

from sensor_msgs.msg import Image, CompressedImage
from std_msgs.msg import Float32MultiArray


from ultralytics import YOLO


class YOLODetector:

    def __init__(self):

        rospy.init_node("yolo_detector")

        rospy.loginfo("Starting YOLO Person Detector")


        # Load YOLO model
        self.model = YOLO("yolov8n.pt")

        # Camera input
        self.image_topic = rospy.get_param(
            "~image_topic",
            "/summit_xl/front_ptz_camera/image_color/compressed"
        )

        # Detection publisher
        self.person_pub = rospy.Publisher(
            "/person_detection",
            Float32MultiArray,
            queue_size=10
        )

        # Debug image publisher
        self.debug_pub = rospy.Publisher(
            "/yolo/debug_image",
            Image,
            queue_size=1
        )

        self.image_sub = rospy.Subscriber(
            self.image_topic,
            CompressedImage,
            self.image_callback,
            queue_size=1
        )


    def image_callback(self, msg):

        try:

            np_arr = np.frombuffer(
                msg.data,
                np.uint8
            )

            frame = cv2.imdecode(
                np_arr,
                cv2.IMREAD_COLOR
            )

        except Exception as e:

            rospy.logerr(e)
            return

        start = time.time()

        results = self.model(
            frame,
            verbose=False
        )


        person_found = False


        for result in results:

            boxes = result.boxes


            for box in boxes:

                cls = int(box.cls[0])

                confidence = float(box.conf[0])


                # COCO class 0 = person
                if cls == 0 and confidence > 0.5:


                    person_found = True


                    x1,y1,x2,y2 = box.xyxy[0]


                    x_center = (
                        float(x1)+float(x2)
                    ) / 2

                    rospy.loginfo(
                        "BBox x1=%0.1f x2=%0.1f center=%0.1f image_width=%d",
                        float(x1),
                        float(x2),
                        x_center,
                        frame.shape[1]
                    )

                    y_center = (
                        float(y1)+float(y2)
                    ) / 2


                    width = (
                        float(x2)-float(x1)
                    )


                    height = (
                        float(y2)-float(y1)
                    )


                    detection = Float32MultiArray()

                    detection.data = [

                        1.0,          # person detected

                        x_center,
                        y_center,

                        width,
                        height,

                        confidence

                    ]


                    self.person_pub.publish(
                        detection
                    )


                    cv2.rectangle(
                        frame,
                        (int(x1),int(y1)),
                        (int(x2),int(y2)),
                        (0,255,0),
                        2
                    )


        if not person_found:

            detection = Float32MultiArray()

            detection.data = [
                0.0,
                0,
                0,
                0,
                0,
                0
            ]

            self.person_pub.publish(
                detection
            )

        frame = np.asarray(frame, dtype=np.uint8)

        try:

            debug_msg = Image()

            debug_msg.header.stamp = rospy.Time.now()
            debug_msg.height = frame.shape[0]
            debug_msg.width = frame.shape[1]

            debug_msg.encoding = "bgr8"
            debug_msg.is_bigendian = False

            debug_msg.step = frame.shape[1] * 3

            debug_msg.data = frame.tobytes()

            self.debug_pub.publish(debug_msg)

        except Exception as e:
            rospy.logerr(
                "Debug image publish failed: %s" % e
            )

        elapsed = time.time() - start
        fps = 1.0 / elapsed
        
        rospy.loginfo(
            "YOLO>FPS: %.2f Inference Time: %.1f ms",
            fps,
            elapsed * 1000
        )


if __name__ == "__main__":

    try:

        detector = YOLODetector()

        rospy.spin()


    except rospy.ROSInterruptException:

        pass
