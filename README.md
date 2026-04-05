<h1 align="center">Yusuf Guenena</h1>

<p align="center">
  <strong>M.S. Robotics Engineering — Wayne State University</strong><br>
  Assistive Robots · Medical Robotics · Autonomous Systems · Real Hardware
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/yusuf-guenena"><img src="https://img.shields.io/badge/LinkedIn-yusuf--guenena-0A66C2?style=flat-square&logo=linkedin&logoColor=white" /></a>
  <a href="mailto:yusuf.a.guenena@gmail.com"><img src="https://img.shields.io/badge/Email-yusuf.a.guenena-EA4335?style=flat-square&logo=gmail&logoColor=white" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/ROS_2-22314E?style=flat-square&logo=ros&logoColor=white" />
  <img src="https://img.shields.io/badge/C++-00599C?style=flat-square&logo=c%2B%2B&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/Qt-41CD52?style=flat-square&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/Jetson-76B900?style=flat-square&logo=nvidia&logoColor=white" />
  <img src="https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=arduino&logoColor=white" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black" />
</p>

---

Robotics engineer who works across the full stack — ROS 2 architecture, C++ control, Python perception, embedded hardware, and operator GUIs — and validates on real robots. Current thesis: autonomous assistive navigation on a Unitree GO2 quadruped for visually impaired users.

---

## 🔬 Selected Projects

### 🦮 GO2 Seeing-Eye Dog — Master's Thesis

> Assistive quadruped navigation for visually impaired users on the Unitree GO2.

**Built:** ROS 2 stack with audio-bearing localization (GCC-PHAT), visual person tracking (YOLOv8 + depth), voice intent grounding (NeMo ASR), safety monitoring, and a C++ lifecycle gait controller. All components implemented and unit-tested; end-to-end hardware integration in progress.

[![Repo](https://img.shields.io/badge/GitHub-GO2--seeing--eye--dog-181717?style=flat-square&logo=github)](https://github.com/yusufdxb/GO2-seeing-eye-dog)

`ROS 2` `YOLOv8` `Whisper` `GCC-PHAT` `Unitree GO2` `Jetson Orin`

---

### 🛡️ HELIX — Fault Sensing for ROS 2

> Structured fault observability prototype with heartbeat, anomaly detection, and log parsing nodes.

**Built:** Three lifecycle-managed detection nodes publishing custom `FaultEvent` messages. Offline benchmarks reproducible without ROS. Evaluated on a live Unitree GO2 graph via Jetson Orin NX — detected real LiDAR rate anomalies in a controlled test.

**Results:** 96.5% TPR (Z=3.0) · 1.16 ms mean latency · 81K samples/sec (desktop) · 64K (Jetson)

[![Repo](https://img.shields.io/badge/GitHub-helix-181717?style=flat-square&logo=github)](https://github.com/yusufdxb/helix)
[![CI](https://github.com/yusufdxb/helix/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yusufdxb/helix/actions/workflows/ci.yml)

`ROS 2` `Python` `Lifecycle Nodes` `Jetson Orin NX`

---

### 🏥 RADAR — Medical Telepresence Robot

> ROS 2 telepresence robot for remote clinical presence with live vitals monitoring.

**Built:** Joystick teleop, live video streaming, pan-tilt camera control, and SpO2/heart-rate sensing (MAX30102) — all hardware-validated on the physical prototype. Qt 6 operator GUI implemented but not tested on hardware. Hardware access has since ended.

[![Repo](https://img.shields.io/badge/GitHub-RADAR--Telepresence--Robot-181717?style=flat-square&logo=github)](https://github.com/yusufdxb/RADAR-Telepresence-Robot)

`ROS 2` `Qt 6` `OpenCV` `MAX30102` `Raspberry Pi` `C++`

---

### 🤖 GO2 Nav2 + YOLOv8

> Full GO2 autonomy simulation: Gazebo, CHAMP, SLAM Toolbox, Nav2, and a YOLOv8 detection-to-navigation pipeline.

**Built:** End-to-end sim stack with object-triggered waypoint navigation. YOLOv8n at 53 ms / 18.8 fps on CPU. Documented 10 non-obvious DDS/TF/SLAM integration issues and fixes.

[![Repo](https://img.shields.io/badge/GitHub-ros2--go2--nav2--yolo-181717?style=flat-square&logo=github)](https://github.com/yusufdxb/ros2-go2-nav2-yolo)

`ROS 2` `YOLOv8` `Nav2` `Gazebo` `SLAM Toolbox`

---

## 🧰 Technologies

| | |
|---|---|
| **Robotics** | ROS 2, Nav2, Gazebo, MoveIt, tf2, SLAM Toolbox |
| **Perception** | YOLOv8, OpenCV, RealSense D435i, GCC-PHAT |
| **ML** | PyTorch, LSTM, OpenAI Whisper |
| **Embedded** | Arduino, Raspberry Pi, Jetson Orin, MAX30102 |
| **Languages** | C++17, Python 3, MATLAB |
| **Tools** | Git, Qt 6, Docker, CMake, Fusion 360 |

---

<p align="center">
  <a href="mailto:yusuf.a.guenena@gmail.com">yusuf.a.guenena@gmail.com</a> · <a href="https://www.linkedin.com/in/yusuf-guenena">LinkedIn</a>
</p>
