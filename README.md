# Yusuf Guenena

**M.S. Robotics Engineering — Wayne State University**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-yusuf--guenena-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yusuf-guenena)
[![Email](https://img.shields.io/badge/Email-yusuf.a.guenena%40gmail.com-EA4335?logo=gmail&logoColor=white)](mailto:yusuf.a.guenena@gmail.com)

Robotics engineer focused on assistive and medical systems. I work across the full stack — ROS 2 architecture, C++ control, Python perception, embedded hardware, and operator GUIs — and validate on real robots, not just simulation. Current thesis: autonomous assistive navigation on a Unitree GO2 quadruped.

---

## Selected Projects

### GO2 Seeing-Eye Dog — Master's Thesis
Assistive quadruped navigation for visually impaired users on the Unitree GO2.

**What I built:** ROS 2 stack with audio-bearing localization (GCC-PHAT), visual person tracking (YOLOv8 + depth), voice intent grounding (NeMo ASR), safety monitoring, and a C++ lifecycle gait controller. All components implemented and unit-tested; end-to-end hardware integration in progress.

`ROS 2` `YOLOv8` `Whisper` `GCC-PHAT` `Unitree GO2` `Jetson Orin`

[![Repo](https://img.shields.io/badge/GitHub-GO2--seeing--eye--dog-181717?style=flat&logo=github)](https://github.com/yusufdxb/GO2-seeing-eye-dog)

---

### HELIX — Fault Sensing for ROS 2
Structured fault observability prototype with heartbeat, anomaly detection, and log parsing nodes.

**What I built:** Three lifecycle-managed detection nodes publishing custom `FaultEvent` messages. Offline benchmarks reproducible without ROS. Evaluated on a live Unitree GO2 graph via Jetson Orin NX — detected real LiDAR rate anomalies in a controlled test.

**Results:** 96.5% TPR (Z=3.0) · 1.16 ms mean latency · 81K samples/sec (desktop) · 64K (Jetson)

`ROS 2` `Python` `Lifecycle Nodes` `Jetson Orin NX`

[![Repo](https://img.shields.io/badge/GitHub-helix-181717?style=flat&logo=github)](https://github.com/yusufdxb/helix) [![CI](https://github.com/yusufdxb/helix/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yusufdxb/helix/actions/workflows/ci.yml)

---

### RADAR — Medical Telepresence Robot
ROS 2 telepresence robot for remote clinical presence with live vitals monitoring.

**What I built:** Joystick teleop, live video streaming, pan-tilt camera control, and SpO2/heart-rate sensing (MAX30102) — all hardware-validated on the physical prototype. Qt 6 operator GUI implemented but not tested on hardware. Hardware access has since ended.

`ROS 2` `Qt 6` `OpenCV` `MAX30102` `Raspberry Pi` `C++`

[![Repo](https://img.shields.io/badge/GitHub-RADAR--Telepresence--Robot-181717?style=flat&logo=github)](https://github.com/yusufdxb/RADAR-Telepresence-Robot)

---

### GO2 Nav2 + YOLOv8
Full GO2 autonomy simulation: Gazebo, CHAMP, SLAM Toolbox, Nav2, and a YOLOv8 detection-to-navigation pipeline.

**What I built:** End-to-end sim stack with object-triggered waypoint navigation. YOLOv8n at 53 ms / 18.8 fps on CPU. Documented 10 non-obvious DDS/TF/SLAM integration issues and fixes.

`ROS 2` `YOLOv8` `Nav2` `Gazebo` `SLAM Toolbox`

[![Repo](https://img.shields.io/badge/GitHub-ros2--go2--nav2--yolo-181717?style=flat&logo=github)](https://github.com/yusufdxb/ros2-go2-nav2-yolo)

---

## Technologies

C++17 · Python 3 · MATLAB · ROS 2 · Nav2 · Gazebo · OpenCV · YOLOv8 · PyTorch · Qt 6 · Arduino · Raspberry Pi · NVIDIA Jetson · Docker · CMake · Git

---

[yusuf.a.guenena@gmail.com](mailto:yusuf.a.guenena@gmail.com) · [LinkedIn](https://www.linkedin.com/in/yusuf-guenena)
