# Yusuf Guenena

**Robotics & Embedded Systems Engineer**
Autonomous • Assistive • Medical Robotics

M.S. Robotics Engineering (Intelligent Control) — Wayne State University

I build **end-to-end robotic systems** that tightly integrate perception, control, embedded electronics, and real hardware — with a focus on **safety-critical and assistive applications**.

---

## 🔧 What I Build

I design and prototype **real-world robotic systems**, not simulations only. My work emphasizes:

- Perception, control, and human–robot interaction
- ROS 2 (Humble / Jazzy) system integration — C++ and Python
- Real-time gait control and legged robot locomotion
- Embedded electronics & sensor fusion
- Hardware–software co-design

My interests center on **medical robotics, assistive autonomy, and intelligent systems**.

---

## 🚀 Flagship Projects

### 🦮 GO2 Seeing-Eye Dog — Master's Thesis
[![Repo](https://img.shields.io/badge/GitHub-GO2--seeing--eye--dog-181717?logo=github)](https://github.com/yusufdxb/GO2-seeing-eye-dog)

<p align="center">
  <a href="https://youtube.com/shorts/EAaj1M6WRpo">
    <img src="https://img.youtube.com/vi/EAaj1M6WRpo/maxresdefault.jpg" width="480">
  </a>
</p>
Assistive robotics system built on the **Unitree GO2** quadruped, targeting safe and intuitive mobility for visually impaired users.

Core research: **audio-visual grounding for human intent inference** — the user speaks a command, the robot localizes the sound source, visually identifies the caller, confirms intent, and navigates toward them using safety-constrained Nav2.

**Research themes:**
- Audio perception and GCC-PHAT sound-source localization
- Audio-guided visual attention and YOLOv8 human identification
- Multimodal intent grounding and confidence-gated navigation
- Safety-critical scene perception (stairs, curbs, narrow passages, dynamic obstacles)
- Human-aware navigation with conservative Nav2 costmaps

**Also includes:** C++ ROS 2 lifecycle gait controller (IDLE → STAND → WALK → TROT) with closed-form leg IK, running at 50 Hz.

**Status:** 🟡 Active thesis research — ROS 2 stack integration and experimental validation in progress.

**Tech:** ROS 2, C++17, Python, YOLOv8, Whisper ASR, Nav2, Gazebo, tf2, ros2_control

---

### 🎤 GO2 Simple Workspace — Voice Control
[![Repo](https://img.shields.io/badge/GitHub-go2--simple--workspace-181717?logo=github)](https://github.com/yusufdxb/go2-simple-workspace)

Lightweight ROS 2 voice command interface for the GO2. Google Speech Recognition with **OpenAI Whisper** as offline fallback. Supports sit, stand, jump, flip, dance, shake hands, backflip, and more — all mapped to Unitree Sport API IDs via a ROS 2 bridge node.

**Tech:** ROS 2, Python, Whisper, SpeechRecognition, Unitree API

---

### 🤖 GO2 Nav2 + YOLOv8 — Object Navigation Demo
[![Repo](https://img.shields.io/badge/GitHub-ros2--go2--nav2--yolo-181717?logo=github)](https://github.com/yusufdxb/ros2-go2-nav2-yolo)

Gazebo simulation of the GO2 using **YOLOv8** to detect objects and **Nav2** to autonomously navigate toward them. Runs on the CHAMP quadruped controller stack — no real hardware needed.

**Tech:** ROS 2, Python, YOLOv8, Nav2, CHAMP, Gazebo, SLAM Toolbox

---

### 🏥 RADAR — Remote Autonomous Doctor Assistance Robot
[![Repo](https://img.shields.io/badge/GitHub-RADAR--Telepresence--Robot-181717?logo=github)](https://github.com/yusufdxb/RADAR-Telepresence-Robot)

ROS 2 medical telepresence robot with real-time remote control, physiological monitoring (MAX30102), and a custom Qt6 GUI. Autonomous lab deliveries using SLAM and AprilTag docking.

**Tech:** ROS 2, C++, Python, Qt6, MAX30102, TurtleBot3, SLAM, AprilTags

---

### 🎮 TicTacToe 3-Link Robot (RRP)
[![Repo](https://img.shields.io/badge/GitHub-TicTacToe--3link--robot-181717?logo=github)](https://github.com/yusufdxb/TicTacToe-3link-robot)

A 3-link robot arm (2 revolute + 1 prismatic) that plays TicTacToe autonomously — physically drawing the grid, X's, and O's on paper using a rack-and-pinion pen servo. Closed-form planar IK + Minimax AI. Arduino + MATLAB App Designer GUI.

**Tech:** MATLAB, Arduino, Servo control, Planar IK, Minimax AI, App Designer

---

### ♻️ EcoSort — Smart Waste Sorting Bin
[![Repo](https://img.shields.io/badge/GitHub-EcoSort--bin-181717?logo=github)](https://github.com/yusufdxb/EcoSort-bin)

Embedded mechatronic system for automated waste classification using multi-sensor fusion and mechanically actuated sorting.

**Tech:** Arduino, Load cells, Color & IR sensors, Servos, CAD

---

## 🧠 Technical Stack

| Category | Technologies |
|---|---|
| **Robotics** | ROS 2, Nav2, Gazebo, RViz, tf2, ros2_control, SLAM Toolbox, CHAMP |
| **Languages** | C++17, Python 3, MATLAB |
| **Perception** | YOLOv8, OpenCV, Intel RealSense D435i, GCC-PHAT audio localization |
| **AI / Speech** | OpenAI Whisper, Minimax, Multimodal intent grounding |
| **Embedded** | Arduino, Raspberry Pi, Jetson Orin, sensors & actuators |
| **Tools** | Linux, Git, Qt6, Fusion 360, Gazebo Classic |

---

## 🎯 Current Focus

- Assistive autonomy and navigation for legged robots (Unitree GO2)
- Real-time C++ gait control and legged locomotion (ROS 2 lifecycle nodes)
- Safety-critical perception — stairs, curbs, narrow passages
- Multimodal human–robot interaction (audio + vision + voice)
- Robust ROS 2 system design validated on real hardware

---

## 📊 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=yusufdxb&show_icons=true&theme=dark&hide_border=true&count_private=true" height="160"/>
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=yusufdxb&layout=compact&theme=dark&hide_border=true&langs_count=6" height="160"/>
</p>

---

## 📫 Contact

- 📧 Email: [yusuf.a.guenena@gmail.com](mailto:yusuf.a.guenena@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/yusuf-guenena](https://www.linkedin.com/in/yusuf-guenena)
