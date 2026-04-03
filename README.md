# Yusuf Guenena

**M.S. Robotics Engineering — Wayne State University**
Assistive Robots · Medical Robotics · Autonomous Systems · Real Hardware

[![LinkedIn](https://img.shields.io/badge/LinkedIn-yusuf--guenena-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yusuf-guenena)
[![Email](https://img.shields.io/badge/Email-yusuf.a.guenena%40gmail.com-EA4335?logo=gmail&logoColor=white)](mailto:yusuf.a.guenena@gmail.com)

---

## About Me

I'm a robotics engineer who builds **complete, functional systems** — from embedded firmware through autonomous behavior and human-robot interaction. My thesis work involves a Unitree GO2 quadruped that guides visually impaired users using audio-visual perception, which means I spend a lot of time making robots work reliably on real hardware, not just in simulation.

What's my background: I do the **full stack** — C++ control loops, Python perception pipelines, ROS 2 system architecture, embedded electronics, CAD, and Qt GUIs. Most of my projects have been built and validated on physical hardware, and my current thesis work is pushing that further into assistive robotics research.

Currently building assistive robotics thesis work on the Unitree GO2, with public projects spanning ROS 2 autonomy, telepresence, embedded sensing, and mechatronics.

---

## Featured Projects

### 🦮 GO2 Seeing-Eye Dog — Master's Thesis *(In Progress)*
> *Assistive quadruped robot for visually impaired users — active research*

[![Repo](https://img.shields.io/badge/GitHub-GO2--seeing--eye--dog-181717?style=flat&logo=github)](https://github.com/yusufdxb/GO2-seeing-eye-dog)
![Status](https://img.shields.io/badge/Status-Research_%26_Design_Phase-orange?style=flat)

Research into reliable human-following and identity-gated navigation on the Unitree GO2 for visually impaired users. The focus is a publishable behavior set — follow me, walk with me, stop/wait, and robust reacquisition after occlusion — with comparisons against AprilTag-only, phone-only, and stock Unitree baselines.

Public repo includes audio perception, visual perception, intent grounding, safety monitoring, custom ROS 2 messages, and a C++ gait controller.

`ROS 2` `YOLOv8` `Nav2` `Whisper ASR` `GCC-PHAT` `Unitree GO2` `Jetson Orin` `Person Re-ID`

---

### 🏥 RADAR — Medical Telepresence Robot
> *ROS 2 robot for remote clinical presence*

[![Repo](https://img.shields.io/badge/GitHub-RADAR--Telepresence--Robot-181717?style=flat&logo=github)](https://github.com/yusufdxb/RADAR-Telepresence-Robot)

Clinicians remotely navigate the robot, stream live video with pan-tilt control, and monitor patient SpO₂ and heart rate in real time — all through a single Qt 6 operator interface. Hardware-tested across teleop, video, pan-tilt control, and vitals sensing; Qt operator GUI implemented in the public repo.

`ROS 2` `Qt 6` `OpenCV` `MAX30102` `Raspberry Pi` `C++` `Python`

---

### 🤖 GO2 Nav2 + YOLOv8
> *Autonomous object detection and navigation in Gazebo simulation*

[![Repo](https://img.shields.io/badge/GitHub-ros2--go2--nav2--yolo-181717?style=flat&logo=github)](https://github.com/yusufdxb/ros2-go2-nav2-yolo)

Full GO2 simulation stack integrating Gazebo Classic, CHAMP, SLAM Toolbox, Nav2, and a YOLOv8 detection-to-navigation pipeline. YOLOv8n benchmarked at 53 ms mean latency / 18.8 fps on CPU. Documents 10 non-obvious DDS/TF/SLAM integration bugs and fixes.

`ROS 2` `YOLOv8` `Nav2` `CHAMP` `Gazebo` `SLAM Toolbox`

---

### 🔧 HELIX — ROS 2 Fault Detection System
> *Lifecycle-node monitoring for robotics fault sensing*

[![Repo](https://img.shields.io/badge/GitHub-helix-181717?style=flat&logo=github)](https://github.com/yusufdxb/helix)

ROS 2 fault monitoring prototype: heartbeat liveness checks, rolling Z-score anomaly detection, and log-pattern parsing — all publishing structured `FaultEvent` messages. AnomalyDetector benchmarked at 46k samples/sec with 100% TPR and 0% FPR across all tested thresholds.

`ROS 2` `Python` `Fault Detection` `Lifecycle Nodes` `Systems Monitoring`

---

### ♟️ TicTacToe 3-Link Robot
> *Physical robot arm that plays and draws TicTacToe*

[![Repo](https://img.shields.io/badge/GitHub-TicTacToe--3link--robot-181717?style=flat&logo=github)](https://github.com/yusufdxb/TicTacToe-3link-robot)

3-DOF RRP arm (2 revolute + 1 prismatic) computes closed-form planar IK to physically draw X's and O's on paper while a Minimax AI plays optimally. Controlled via MATLAB App Designer and Arduino. Also supports ROS 2 remote play and a 4-strategy AI tournament runner.

`MATLAB` `Arduino` `Inverse Kinematics` `Minimax AI` `Servo Control`

---

### ♻️ EcoSort Bin
> *Embedded waste classifier — 97.5% accuracy, no ML required*

[![Repo](https://img.shields.io/badge/GitHub-EcoSort--bin-181717?style=flat&logo=github)](https://github.com/yusufdxb/EcoSort-bin)

Multi-sensor fusion (weight + color + IR + ultrasonic) on an Arduino Uno R4 classifies waste and actuates a servo-driven sorting platform. 40-trial validation, 97.5% accuracy, ~$70 BOM.

`Arduino` `Sensor Fusion` `Embedded C` `Finite State Machine`

---

### 🛡️ HELIX — ROS 2 Fault Sensing Prototype
> *Lifecycle-node fault detection middleware for robotics systems*

[![Repo](https://img.shields.io/badge/GitHub-helix-181717?style=flat&logo=github)](https://github.com/yusufdxb/helix)
[![CI](https://github.com/yusufdxb/helix/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yusufdxb/helix/actions/workflows/ci.yml)

ROS 2 middleware for early fault detection: heartbeat monitoring, Z-score anomaly detection, and log-pattern parsing — publishing structured `FaultEvent` messages instead of raw logs. Phase 1 prototype with benchmarked throughput (46K samples/sec) and 100% TPR at all tested thresholds.

`ROS 2` `Fault Detection` `Lifecycle Nodes` `Python` `System Monitoring`

---

## Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/MATLAB-E16737?style=for-the-badge&logo=mathworks&logoColor=white" />
  <img src="https://img.shields.io/badge/ROS_2-22314E?style=for-the-badge&logo=ros&logoColor=white" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white" />
  <img src="https://img.shields.io/badge/Raspberry_Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white" />
  <img src="https://img.shields.io/badge/NVIDIA_Jetson-76B900?style=for-the-badge&logo=nvidia&logoColor=white" />
</p>

| Area | Technologies |
|---|---|
| **Robotics** | ROS 2, Nav2, Gazebo, RViz, tf2, ros2_control, SLAM Toolbox, MoveIt |
| **Perception** | YOLOv8, OpenCV, Intel RealSense D435i, GCC-PHAT audio localization |
| **AI / Speech** | OpenAI Whisper, Minimax, Multimodal intent grounding |
| **Embedded** | Arduino, Raspberry Pi, NVIDIA Jetson Orin, sensor/actuator integration |
| **Languages** | C++17, Python 3, MATLAB, C |
| **Tools** | Git, Qt 6, Fusion 360, Docker, CMake |

---

## GitHub Stats

<p align="center">
  <img src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/profile-summary-card-output/github_dark/0-profile-details.svg" width="100%"/>
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/profile-summary-card-output/github_dark/1-repos-per-language.svg" width="32%"/>
  <img src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/profile-summary-card-output/github_dark/2-most-commit-language.svg" width="32%"/>
  <img src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/profile-summary-card-output/github_dark/3-stats.svg" width="32%"/>
</p>

---

## Contact

[yusuf.a.guenena@gmail.com](mailto:yusuf.a.guenena@gmail.com) · [LinkedIn](https://www.linkedin.com/in/yusuf-guenena)
