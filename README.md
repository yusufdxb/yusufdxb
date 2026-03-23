# Yusuf Guenena

**M.S. Robotics Engineering, Wayne State University**  
Assistive robotics · ROS 2 integration · embedded systems · real hardware

[![LinkedIn](https://img.shields.io/badge/LinkedIn-yusuf--guenena-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yusuf-guenena)
[![Email](https://img.shields.io/badge/Email-yusuf.a.guenena%40gmail.com-EA4335?logo=gmail&logoColor=white)](mailto:yusuf.a.guenena@gmail.com)

## Focus

I build robotics systems that combine perception, control, operator interfaces, and embedded hardware. Most of my public work is centered on ROS 2, real sensors and actuators, and the engineering needed to make whole systems run outside of idealized demos.

Current emphasis:
- Assistive robotics on the Unitree GO2
- ROS 2 system integration, perception, and navigation
- Embedded sensing and actuator control
- Hardware-backed prototypes rather than simulation-only coursework

## Selected Projects

### GO2 Seeing-Eye Dog
[Repository](https://github.com/yusufdxb/GO2-seeing-eye-dog)

Master's thesis work on an assistive quadruped for visually impaired users. The public repo contains the real project structure: audio perception, human perception, intent grounding, safety monitoring, voice command, custom messages, and a C++ gait controller.

Signal:
- Real hardware target: Unitree GO2 + Jetson Orin + RealSense + microphone array + LiDAR
- System scope is intentionally narrow: identity-gated guidance behaviors instead of a broad but vague autonomy claim
- Public repo reflects active implementation, not just a proposal

`ROS 2` `C++` `Python` `Nav2` `YOLOv8` `Whisper` `RealSense` `Unitree GO2`

### RADAR Telepresence Robot
[Repository](https://github.com/yusufdxb/RADAR-Telepresence-Robot)

ROS 2 telepresence robot for clinical settings. Hardware-tested subsystems include teleoperation, video streaming, pan-tilt actuation, and MAX30102 vital sign sensing. The Qt operator GUI is implemented in the repo and documented separately from the hardware-validated path.

Signal:
- Combines operator UI, sensing, teleop, and embedded I/O in one system
- Public docs distinguish what was hardware-tested from what was implemented but not validated on the prototype

`ROS 2` `Qt 6` `OpenCV` `Python` `C++` `Raspberry Pi` `MAX30102`

### GO2 Navigation Stack in Gazebo
[Repository](https://github.com/yusufdxb/ros2-go2-nav2-yolo)

GO2 simulation stack integrating Gazebo, CHAMP, SLAM Toolbox, Nav2, and a perception-to-navigation pipeline. In simulation the repo uses a position publisher instead of YOLO because Gazebo's rendered person model is not reliably detectable; the real-hardware YOLO path remains in the codebase.

Signal:
- Strongest public example of debugging and systems integration work
- Documents specific fixes for DDS history replay, Gazebo software rendering, SLAM startup timing, LiDAR frame configuration, and Nav2 controller tuning

`ROS 2` `Nav2` `Gazebo` `CHAMP` `YOLOv8` `SLAM Toolbox`

### Embedded and Mechatronics Projects
[EcoSort Bin](https://github.com/yusufdxb/EcoSort-bin)  
Rule-based waste classification on Arduino Uno R4 using weight, color, IR, and ultrasonic sensing with a servo-actuated sorter.

[TicTacToe 3-Link Robot](https://github.com/yusufdxb/TicTacToe-3link-robot)  
Physical 3-DOF robot arm with closed-form planar IK, MATLAB control tooling, and Arduino actuation to draw and play TicTacToe on paper.

## Technical Areas

| Area | Tools and Platforms |
|---|---|
| Robotics | ROS 2, Nav2, Gazebo, RViz, tf2, ros2_control, SLAM Toolbox |
| Perception | YOLOv8, OpenCV, Intel RealSense D435i, RGB-D fusion |
| Speech and Audio | Whisper, microphone arrays, GCC-PHAT |
| Embedded | Arduino, Raspberry Pi, Jetson Orin, sensor and actuator integration |
| Languages | C++, Python, MATLAB, C |
| Interfaces and Tools | Qt 6, CMake, Git, Docker, Fusion 360 |

## Contact

[yusuf.a.guenena@gmail.com](mailto:yusuf.a.guenena@gmail.com) · [LinkedIn](https://www.linkedin.com/in/yusuf-guenena)
