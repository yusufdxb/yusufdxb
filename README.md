# Yusuf Guenena

**Robotics engineer. I build real systems that run on real hardware.**

M.S. Robotics Engineering @ Wayne State University · Assistive & autonomous robots · Sim-to-real on quadrupeds

[![Email](https://img.shields.io/badge/Email-yusuf.a.guenena%40gmail.com-EA4335?logo=gmail&logoColor=white)](mailto:yusuf.a.guenena@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-yusufdxb-181717?logo=github&logoColor=white)](https://github.com/yusufdxb)

---

Most of what I build lives on a Unitree GO2 quadruped: perception, learned control, navigation, safety, and the unglamorous reliability layer that keeps it all from falling over in the real world. I like the part of robotics where the simulation lies to you and the hardware tells the truth. A lot of my repos document the bugs I hit getting there, because that is the part nobody writes down and the part that actually matters.

I work across the stack: C++ control loops, Python perception and RL, ROS 2 architecture, embedded firmware, CAD, and the GUIs on top. The list below is the stuff I am proud of, grouped by what it actually does.

---

## 🦮 Flagship: GO2 Seeing-Eye Dog (M.S. Thesis)

[![Repo](https://img.shields.io/badge/GitHub-GO2--seeing--eye--dog-181717?style=flat&logo=github)](https://github.com/yusufdxb/GO2-seeing-eye-dog)
![Stars](https://img.shields.io/github/stars/yusufdxb/GO2-seeing-eye-dog?style=flat&color=yellow)
![Status](https://img.shields.io/badge/Status-Active_Research-orange?style=flat)

An assistive quadruped that guides visually impaired users using audio-visual perception. The hard part is not following a person, it is following the *right* person and reacquiring them after they disappear behind an obstacle. The system covers audio localization, visual person re-identification, intent grounding, safety monitoring, custom ROS 2 messages, and a C++ gait controller, benchmarked against AprilTag-only, phone-only, and stock Unitree baselines.

`ROS 2` `Person Re-ID` `Whisper ASR` `GCC-PHAT` `Nav2` `Jetson Orin NX` `Unitree GO2`

---

## 🤖 The GO2 Quadruped Stack

A connected body of work turning a stock quadruped into something that learns, navigates, and recovers on its own.

| Project | What it does |
|---|---|
| **[go2-phoenix](https://github.com/yusufdxb/go2-phoenix)** | Closed-loop sim-to-real locomotion learning in Isaac Lab, exported to ONNX and verified for train/deploy parity (max-abs diff 9.5e-7) before it ever touches the robot. |
| **[ashfall](https://github.com/yusufdxb/ashfall)** | Failure-driven reinforcement learning: the robot learns from where it falls, not just where it succeeds. |
| **[come-here](https://github.com/yusufdxb/come-here)** | Hears "come here," localizes the voice, turns, finds the person, and walks to them. Audio-visual approach in one loop. |
| **[riskgraph-go2](https://github.com/yusufdxb/riskgraph-go2)** | Persistent route-risk memory: the robot remembers where things went wrong and scores safer paths next time. |
| **[ros2-go2-nav2-yolo](https://github.com/yusufdxb/ros2-go2-nav2-yolo)** ⭐ | Full Gazebo autonomy stack (Nav2 + SLAM Toolbox + CHAMP + YOLOv8). YOLOv8n at 53 ms / 18.8 fps on CPU, with 10 non-obvious DDS/TF/SLAM bugs documented and fixed. |
| **[go2-audio](https://github.com/yusufdxb/go2-audio)** | The GO2's `/audiosender` DDS topic is broken, so I pulled real mic audio off the robot over WebRTC instead. |

---

## 🛡️ Reliability & Observability for Robots

The layer that tells you *when your robot is about to do something stupid* and catches it on the way down.

| Project | What it does |
|---|---|
| **[helix](https://github.com/yusufdxb/helix)** | ROS 2 fault-sensing: heartbeat monitoring, Z-score anomaly detection, log parsing, publishing structured `FaultEvent`s instead of raw logs. Caught real LiDAR rate anomalies on a live GO2 graph. 96.5% TPR, 1.16 ms latency, 81K samples/sec. |
| **[BlackBoxRS](https://github.com/yusufdxb/BlackBoxRS)** | A flight recorder for ROS 2 robots: observability and post-failure forensics so you can actually answer "what happened" after a crash. |
| **[policy-health-monitor](https://github.com/yusufdxb/policy-health-monitor)** | Runtime safety net for learned policies: detects when a neural controller's internals go out of distribution and intervenes before it acts on garbage. |
| **[supercombo-blindspot](https://github.com/yusufdxb/supercombo-blindspot)** ⭐ | Distribution-shift teardown of openpilot's production self-driving model. The question: does an L2 driving model know when it is blind? Threshold-free OOD metrics, recurrent-state-correct reproduction, the works. |

---

## 🗺️ Perception & 3D Scene Understanding

| Project | What it does |
|---|---|
| **[openvocab-tsdf](https://github.com/yusufdxb/openvocab-tsdf)** | GPU-accelerated open-vocabulary 3D mapping: build a TSDF and query it in natural language. |
| **[go2-semantic-nav](https://github.com/yusufdxb/go2-semantic-nav)** | Open-vocab 3D semantic scene graph feeding a language-grounded Nav2 overlay, running on Jetson Orin NX. |

---

## ⚙️ Hardware & Embedded

Where I started, and still the most satisfying when it physically moves.

| Project | What it does |
|---|---|
| **[RADAR-Telepresence-Robot](https://github.com/yusufdxb/RADAR-Telepresence-Robot)** | Medical telepresence robot: remote teleop, live video with pan-tilt, and real-time SpO₂ / heart-rate monitoring through one Qt 6 operator console. |
| **[TicTacToe-3link-robot](https://github.com/yusufdxb/TicTacToe-3link-robot)** | A 3-DOF arm that computes closed-form IK to physically draw X's and O's while a Minimax AI plays optimally. [▶ Demo](https://www.youtube.com/watch?v=9wfI7847dPw) |
| **[EcoSort-bin](https://github.com/yusufdxb/EcoSort-bin)** | Multi-sensor fusion (weight + color + IR + ultrasonic) on an Arduino classifies and sorts waste. 97.5% accuracy over 40 trials, ~$70 BOM, zero ML. |

---

## 🛠️ Also: developer tooling

**[vex](https://github.com/yusufdxb/vex)** routes Claude Code tasks across Opus, Sonnet, Haiku, and local Ollama models by scoring confidence, impact, and risk, because watching tokens burn on trivial edits bothered me enough to fix it.

---

## Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/ROS_2-22314E?style=for-the-badge&logo=ros&logoColor=white" />
  <img src="https://img.shields.io/badge/Isaac_Lab-76B900?style=for-the-badge&logo=nvidia&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white" />
  <img src="https://img.shields.io/badge/NVIDIA_Jetson-76B900?style=for-the-badge&logo=nvidia&logoColor=white" />
</p>

| Area | Technologies |
|---|---|
| **Robotics** | ROS 2, Nav2, SLAM Toolbox, ros2_control, tf2, Gazebo, Isaac Lab, MoveIt |
| **Learning** | PyTorch, reinforcement learning, sim-to-real, ONNX, out-of-distribution detection |
| **Perception** | YOLOv8, OpenCV, RealSense D435i, person re-ID, GCC-PHAT, open-vocab 3D mapping |
| **Embedded** | Jetson Orin NX, Arduino, Raspberry Pi, sensor/actuator integration, firmware |
| **Languages** | C++17, Python 3, MATLAB, C |
| **Tools** | Git, Docker, CMake, Qt 6, Fusion 360 |

---

📫 [yusuf.a.guenena@gmail.com](mailto:yusuf.a.guenena@gmail.com)
