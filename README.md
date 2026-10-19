<h1>An Adaptive Monocular Vision-Based Human Position Tracking in a Dorsal-Following Autonomous Wheeled Robot</h1>


<h2>Description</h2>
The benefits of autonomous robots, particularly in collaborative and assistive tasks involving humans, are enormous. However, due to the high cost of state-of-the-art multimodal sensors, developing low-cost person-following robots for large-scale critical industrial sector operations has become difficult. Thus, this work presents the development and experimental evaluation of a deep learning-based vision system for a monocular sensor-based 4-wheel Robotnik Summit XL mobile robot. A YOLO-based human detector was developed and integrated with the robot's front RGB PTZ camera to identify the human body with a bounding box position, dimensions, and confidence information. A person-centred tracker algorithm was also developed to maintain the robot ‘visually engaged’ with the identity of the detected human using a unique ID tracker. The proposed system was experimentally tested and validated using nine different scenarios covering regular human indoor environment poses. The results show detection accuracies from 94.4% to 100% across person-present scenarios, with average confidence scores between 0.85 and 0.90. The system achieved detection rates of approximately 1.3 –5.3 Hz in the recorded experiments, while robot velocity commands between -0.003 m/s and 0.005 m/s were published with a sampling rate between 3.0 – 10.0 Hz. Position-estimation analysis showed variations in the horizontal target position and bounding-box height according to target movement and operating distance. But in the ‘no target’ scenario, the system achieved 100% specificity and generated zero linear velocity commands, indicating that the robot remained stationary in the absence of a detected person.
Video demonstration: https://youtu.be/fRFYVOVr5j4

<h2></h2>
<figure>
<img src="https://i.postimg.cc/Dfx50Xjt/Figure-2-3x.jpg" height="30%" width="50%" alt="Disk Sanitization Steps"/>
<figcaption style="margin-top: 8px;">Person-Following Autonomous Robot</figcaption>
</figure>
<h2></h2>

<h2>Project Development and Procedure</h2>
An adaptive vision-based human position tracking and autonomous person-following system capable of effectively following a moving person under dynamic positional and varying illumination changes condition is developed using deep learning and the ROS framework for an indoor environment task performance. The experiment systematically analysed the performance outcomes based on the indicated set of parameters.
This was achieved with these targeted objectives:
<ul>
<li>Investigate existing human-following techniques for autonomous mobile robots and design a vision-based human detection system using deep learning.</li>
<li>Develop a real-time human position estimation algorithm by implementing adaptive forward and backward following control.</li>
<li>Integrate the perception and control modules within ROS.</li>
<li>Deploy the proposed system on a real-world 4-wheeled Robotnik Summit XL mobile robot to evaluate the detection, motor control, and position estimation performance under various human-pose scenarios in an indoor environment.</li>
</ul>
 
<h2></h2>
<h4>System Design</h4>
<figure>
<img src="https://i.postimg.cc/PrZ44RrN/Figure-3-1.jpg" height="30%" width="50%" alt="Disk Sanitization Steps"/>
<figcaption style="margin-top: 8px;">Autonomous Vision-Based Human-Following System Design Framework</figcaption>
</figure>
<h2></h2>

The perception subsystem formed the first stage of the framework. An RGB camera mounted on the mobile robot continuously captured images of the surrounding environment. After successfully detecting a human, the human position estimation subsystem extracted the horizontal centre coordinate and the height of the detected bounding box. The adaptive motion control subsystem continuously received the detected human position information and compared the estimated distance with the desired following distance. Motion smoothing and safety constraints were incorporated into the controller to minimise oscillations and ensure stable robot behaviour during continuous human movement. The robot control subsystem interpreted incoming velocity commands and converted them into motor control signals that produced the corresponding translational motion. Throughout the system’s operation, the onboard camera continuously acquired new images, thereby creating a closed-loop visual feedback mechanism. This continuous perception–action cycle enabled the robot to adapt dynamically to changes in the target person's position while maintaining autonomous person-following behaviour.

<h2></h2>
<figure>
<img src="https://i.postimg.cc/wxDyb8LK/20260813-141703.jpg" height="30%" width="50%" alt="Disk Sanitization Steps"/>
<figcaption style="margin-top: 8px;">Real World Human-Follower Robot Scenario</figcaption>
</figure>
<h2></h2>

<h2>Conclusion</h2>
In this research study, a deep-learning-based vision system was developed for an autonomous person-following monocular real-world 4-wheeled robot across nine scenarios in an indoor environment. The experimental results demonstrated high detection performance across the evaluated person-present scenarios, with detection accuracy ranging from 94.4% to 100%. The system also achieved high confidence scores, generally between 0.85 and 0.90, demonstrating its ability to reliably identify the target person under different movement, distance, and lighting conditions. However, during the no-target experiment in the detection performance, 100% specificity was achieved with no false-positive movement commands, thereby demonstrating appropriate stationary behaviour when no target was present
In addition, the developed system was able to estimate and continuously monitor changes in the target's position and relative distance. This was achieved by using the horizontal centre of the detected bounding box to represent the target's image position, while the bounding-box height was used as a relative indication of distance. The results demonstrated that these measurements provided useful information about target movement and distance variation.
