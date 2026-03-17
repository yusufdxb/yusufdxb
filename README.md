<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=58A6FF&center=true&vCenter=true&width=600&lines=Hey%2C+I'm+Yusuf+Guenena+%F0%9F%91%8B;Robotics+Engineer;ROS+2+%7C+C%2B%2B+%7C+Python+%7C+Embedded+Systems;Building+robots+that+work+in+the+real+world" alt="Typing SVG" />
  </a>
</p>

<p align="center">
  <strong>M.S. Robotics Engineering — Wayne State University</strong><br/>
  Assistive Robots · Medical Robotics · Autonomous Systems · Real Hardware
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/yusuf-guenena">
    <img src="https://img.shields.io/badge/LinkedIn-yusuf--guenena-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="mailto:yusuf.a.guenena@gmail.com">
    <img src="https://img.shields.io/badge/Email-yusuf.a.guenena@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/🎯_Actively_seeking_internship_opportunities-brightgreen?style=for-the-badge" />
</p>

---

## About Me

I'm a robotics engineer who builds **complete, functional systems** — from embedded firmware through autonomous behavior and human-robot interaction. My thesis work involves a Unitree GO2 quadruped that guides visually impaired users using audio-visual perception, which means I spend a lot of time making robots work reliably on real hardware, not just in simulation.

What makes my background unusual: I do the **full stack** — C++ control loops at 50 Hz, Python perception pipelines, ROS 2 system architecture, embedded electronics, CAD, and Qt GUIs. Every project here has been built and tested on physical hardware.

---

## Featured Projects

### 🦮 GO2 Seeing-Eye Dog — Master's Thesis
> *Assistive quadruped robot for visually impaired users*

[![Repo](https://img.shields.io/badge/GitHub-GO2--seeing--eye--dog-181717?style=flat&logo=github)](https://github.com/yusufdxb/GO2-seeing-eye-dog)
[![Demo](https://img.shields.io/badge/▶_Demo-YouTube-FF0000?style=flat&logo=youtube)](https://youtube.com/shorts/EAaj1M6WRpo)

The robot listens for a voice command → localizes the speaker with a microphone array (GCC-PHAT) → confirms identity visually with YOLOv8 → navigates toward them using safety-constrained Nav2. Also includes a C++ ROS 2 gait controller running at 50 Hz with closed-form leg IK.

`ROS 2 Humble` `C++17` `Python` `YOLOv8` `Nav2` `Whisper ASR` `GCC-PHAT` `Unitree GO2` `Jetson Orin`

---

### 🏥 RADAR — Medical Telepresence Robot
> *ROS 2 robot for remote clinical presence*

[![Repo](https://img.shields.io/badge/GitHub-RADAR--Telepresence--Robot-181717?style=flat&logo=github)](https://github.com/yusufdxb/RADAR-Telepresence-Robot)

Clinicians remotely navigate the robot, stream live video with pan-tilt control, and monitor patient SpO₂ and heart rate in real time — all through a single Qt 6 operator interface. Modular ROS 2 node architecture; fully functional and validated.

`ROS 2` `Qt 6` `OpenCV` `MAX30102` `Raspberry Pi` `C++` `Python`

---

### 🤖 GO2 Nav2 + YOLOv8
> *Autonomous object detection and navigation in simulation*

[![Repo](https://img.shields.io/badge/GitHub-ros2--go2--nav2--yolo-181717?style=flat&logo=github)](https://github.com/yusufdxb/ros2-go2-nav2-yolo)

YOLOv8 detects objects in a Gazebo environment → the GO2 autonomously navigates toward them via Nav2. Built on the CHAMP quadruped controller stack with SLAM Toolbox for mapping.

`ROS 2` `YOLOv8` `Nav2` `CHAMP` `Gazebo` `SLAM Toolbox`

---

### ♟️ TicTacToe 3-Link Robot
> *Physical robot arm that plays and draws TicTacToe*

[![Repo](https://img.shields.io/badge/GitHub-TicTacToe--3link--robot-181717?style=flat&logo=github)](https://github.com/yusufdxb/TicTacToe-3link-robot)

3-DOF RRP arm (2 revolute + 1 prismatic) computes closed-form planar IK to physically draw X's and O's on paper while a Minimax AI plays optimally. Controlled via MATLAB App Designer and Arduino.

`MATLAB` `Arduino` `Inverse Kinematics` `Minimax AI` `Servo Control`

---

### ♻️ EcoSort Bin
> *Embedded waste classifier — 97.5% accuracy, no ML required*

[![Repo](https://img.shields.io/badge/GitHub-EcoSort--bin-181717?style=flat&logo=github)](https://github.com/yusufdxb/EcoSort-bin)
[![Demo](https://img.shields.io/badge/▶_Demo-YouTube-FF0000?style=flat&logo=youtube)](https://youtu.be/RpR4vYVQu_Y)

Multi-sensor fusion (weight + color + IR + ultrasonic) on an Arduino Uno R4 classifies waste and actuates a servo-driven sorting platform. 40-trial validation, 97.5% accuracy, ~$70 BOM.

`Arduino` `Sensor Fusion` `Embedded C` `Finite State Machine`

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
  <img src="https://github-readme-stats.vercel.app/api?username=yusufdxb&show_icons=true&theme=github_dark&hide_border=true&count_private=true&include_all_commits=true" height="165"/>
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=yusufdxb&layout=compact&theme=github_dark&hide_border=true&langs_count=6" height="165"/>
</p>

---

## Let's Connect

I'm actively looking for **robotics, embedded systems, or autonomous systems internship opportunities**.

If you're working on anything involving ROS 2, perception, legged robots, or real-hardware systems — let's talk.

<p align="center">
  <a href="https://www.linkedin.com/in/yusuf-guenena">
    <img src="https://img.shields.io/badge/Connect_on_LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="mailto:yusuf.a.guenena@gmail.com">
    <img src="https://img.shields.io/badge/Send_an_Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
</p>
