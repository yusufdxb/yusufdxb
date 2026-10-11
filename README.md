<div align="center">

<h1>Yusuf Guenena</h1>

<p><strong>I build dependable autonomy for quadruped robots working around people.</strong></p>

<p>M.S. Robotics Engineering @ Wayne State University · Assistive autonomy on the Unitree GO2 · Runtime safety and recovery</p>

<p>
<a href="mailto:yusuf.a.guenena@gmail.com"><img src="https://img.shields.io/badge/Email-yusuf.a.guenena%40gmail.com-EA4335?logo=gmail&logoColor=white" alt="Email"></a>
<a href="https://www.linkedin.com/in/yusuf-guenena/"><img src="https://img.shields.io/badge/LinkedIn-yusuf--guenena-0A66C2?logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://yusufdxb.github.io"><img src="https://img.shields.io/badge/Website-yusufdxb.github.io-475569?logo=githubpages&logoColor=white" alt="Website"></a>
</p>

</div>

---

I build physical autonomy first, then the reliability systems needed to trust it. Come Here is the clearest real-robot example: a spoken command becomes a localized caller, a turn, a visual acquisition, an approach, and a sit. My M.S. thesis, *Safe Assistive Quadruped Autonomy*, researches MOSAIC, a language-model layer that turns spoken requests into sequences of robot skills under an independent safety guardian, and guiding a low-vision handler to a destination under a safety envelope that alone commands motion. Underneath is the layer that notices when learned components fail quietly: fault detection and recovery on a live robot, deploy-time parity gates, out-of-distribution monitoring on policy internals, and acceptance evidence you can re-verify a year later.

I work across the stack: C++ control loops, Python perception and RL, ROS 2 architecture, embedded firmware, CAD, and the GUIs on top. Most of it runs on a Unitree GO2. Every repo below states what has actually run on hardware and what has not, because that distinction is the whole job.

---

## Featured Work

### come-here <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/icon-dark.webp"><img height="40" align="right" src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/icon-light.webp" alt="Unitree GO2"></picture>

[![Repo](https://img.shields.io/badge/GitHub-come--here-181717?style=flat&logo=github)](https://github.com/yusufdxb/come-here)
[![Demo](https://img.shields.io/badge/%E2%96%B6_Demo-YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://youtu.be/Ky4fMO8ooio)
![Status](https://img.shields.io/badge/Status-Live_loop_on_the_GO2-brightgreen?style=flat)

Real-robot assistive autonomy on the Unitree GO2. Someone says *"come here"* from outside the camera's field of view and the dog has to solve the whole problem, onboard the Jetson: **hear the caller, localize them, turn, visually acquire them, approach, stop, sit.** The ReSpeaker array's firmware DOA register gives the bearing (software SRP-PHAT was tried on the mounted array and failed, which is itself the finding), a bounded whole-token Whisper matcher gates the wake so ordinary lab talk does not trigger it, the turn closes on `/utlidar/robot_odom` yaw, then YOLO11n takes over for acquisition, alignment, approach, and a bounding-box stop at 75% of frame height.

Two live end-to-end hardware runs on the GO2, one of them a blind trial with the caller's position undisclosed; that one documented trial reached the seated state about 12.8 s after wake detection. The stack can be launched through a systemd unit on the Jetson, and it refuses to arm unless the robot is already standing.

`ROS 2 Humble` `ReSpeaker 4-Mic Array` `Whisper ASR` `YOLO11n` `systemd` `Jetson Orin NX` `Unitree GO2`

### go2-phoenix

[![Repo](https://img.shields.io/badge/GitHub-go2--phoenix-181717?style=flat&logo=github)](https://github.com/yusufdxb/go2-phoenix)
[![Demo](https://img.shields.io/badge/%E2%96%B6_Demo-YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://youtu.be/eCzeuW2WKgY)
![Status](https://img.shields.io/badge/Status-Walking_on_the_GO2-yellowgreen?style=flat)

The learned-control layer under the GO2 autonomy work: closed-loop sim-to-real learning for locomotion. A policy trains on 8,192 simulated GO2s in Isaac Lab, exports to ONNX through a **torch/onnxruntime parity gate** that refuses to ship a checkpoint whose deploy-time numerics drift outside tolerance, then runs behind a **fail-closed** ROS 2 safety layer with a shared slew cap. On the real robot it gets up from lying flat, turns, sits, and takes its first untethered steps on a free floor. It passed every live stand gate at zero command (2 s, 5 s and three 10 s windows, body tilt under 0.09 rad, no safety-layer interventions).

It walks, but under-tracks: about 60% of the commanded forward distance and 20% of the commanded turn, against 89% and 76% for the same profile in MuJoCo. The cause is measured, not guessed. An active probe on the hung robot found 0.17-0.96 N m of static joint friction that the training simulator never modelled, and replaying the walk in MuJoCo at 1.25-1.5x the measured values matches the robot. Retraining with joint-friction randomization around those values is next.

`Isaac Lab` `PPO` `ONNX` `ROS 2` `Sim-to-Real` `Unitree GO2`

### FETCH (GuideDog-X)

![Repo](https://img.shields.io/badge/Repo-private-lightgrey?style=flat&logo=github)
[![Demo](https://img.shields.io/badge/%E2%96%B6_Demo-YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://youtu.be/06XPfwwHZ3M)
![Status](https://img.shields.io/badge/Status-Voice_%2B_conversation_live_on_the_GO2-brightgreen?style=flat)

A GO2 you talk to, with speech recognition, the language model and the vision-language model running on local hardware: no API key, no subscription. You say *"Fetch, describe the room."* and the dog turns through a yaw-only scan, sends each view to a local vision-language model, and speaks one grounded line per view through its own speaker, each turn waiting for the previous line to finish. The scene question is asked as closed yes/no prompts rather than open description, because an open "scene" field made the model return empty objects on live frames, and a per-view verification pass re-asks each view's top objects on the same image, which cut false objects on blank walls from 10 to 0 without losing a real one.

It also holds a conversation. Weather, the time, small talk and follow-up questions (no wake word needed for 8 s after a reply) are answered from the dog's speaker, most in under 2.5 s, across armed sessions on the real GO2 in September. A chat reply can never call a tool, so small talk never moves the dog.

The important part is what owns the wheels. A **safety envelope is the only publisher on `/cmd_vel`**: the language layer proposes, the envelope disposes, and a wireless deadman on the remote's L1 gates motion by default. Spoken stop is off by default, because *"did you stop?"* once halted the dog mid-conversation; the handheld remote, a stick takeover and the envelope are the halt paths. Room scans run voice-triggered on the real GO2 in 22 to 31 s with no degraded subsystems.

`ROS 2 Humble` `Local VLM + LLM (Ollama)` `Whisper ASR` `ReSpeaker 4-Mic Array` `Safety Envelope` `Jetson Orin NX` `Unitree GO2`

---

## Active M.S. Research

### GO2 Seeing-Eye Dog

[![Repo](https://img.shields.io/badge/GitHub-GO2--seeing--eye--dog-181717?style=flat&logo=github)](https://github.com/yusufdxb/GO2-seeing-eye-dog)
![Status](https://img.shields.io/badge/Status-Active_Research-orange?style=flat)

A guide dog has to be summonable. If the handler puts the harness down, sits on a bench, and then wants the dog back, the dog finds them by voice, not by an app or a joystick. This repository closes the **recall** half of that interaction on real hardware: a four-channel mic array gives a GCC-PHAT bearing, Whisper parses the command, YOLOv8 plus depth back-projection gives 3D person poses, and a fused audio-visual score must hold across five consecutive frames before the target locks and publishes a Nav2 goal.

`ROS 2 Humble` `GCC-PHAT` `Whisper ASR` `YOLOv8` `RealSense D435i` `Nav2` `C++ Lifecycle Node`

*Up next: **MOSAIC**, a language-model layer that chains skills like FETCH's into multi-step tasks, while an independent safety guardian keeps a hand on the leash. Stay tuned.*


---

## The GO2 Quadruped Stack

A connected body of work turning a stock quadruped into something that learns, navigates, and recovers on its own.

| Project | What it does | Status |
|---|---|---|
| **[come-here](https://github.com/yusufdxb/come-here)** | Hears "come here," localizes the voice, turns, finds the person, and walks to them. Audio-visual approach in one loop. | full recall loop live on the GO2 |
| **[go2-phoenix](https://github.com/yusufdxb/go2-phoenix)** | Sim-to-real locomotion learning: an Isaac Lab policy shipped through an ONNX parity gate and a fail-closed ROS 2 safety layer, built to replay hardware failures in simulation and fine-tune on them. | stands and walks on the GO2; joint-friction tracking gap measured, retraining next |
| **[riskgraph-go2](https://github.com/yusufdxb/riskgraph-go2)** | Persistent route-risk memory: the robot remembers where things went wrong and scores safer paths through an explainable Nav2 overlay. | hardware-unverified |
| **[go2-semantic-nav](https://github.com/yusufdxb/go2-semantic-nav)** | Open-vocab 3D semantic scene graph feeding a language-grounded Nav2 overlay on a Jetson. | workstation eval landed, robot eval pending |
| **[go2-audio](https://github.com/yusufdxb/go2-audio)** | Real microphone audio off a GO2 over WebRTC, because the DDS `/audiosender` topic is broken. | |
| **[go2_omniverse](https://github.com/yusufdxb/go2_omniverse)** | Isaac Sim 5.0 / ROS 2 Jazzy port plus an IMU-driven digital-twin mode mirroring a real GO2. | port merged upstream (#84) |
| **[ros2-go2-nav2-yolo](https://github.com/yusufdxb/ros2-go2-nav2-yolo)** | Full Gazebo autonomy stack (Nav2 + SLAM Toolbox + CHAMP + YOLOv8), with the non-obvious DDS/TF/SLAM integration bugs documented and fixed. | |
| **[go2-jetson-setup-guide](https://github.com/yusufdxb/go2-jetson-setup-guide)** | Bringing up a Jetson on a GO2: first boot, SSH, networking, internet sharing, ROS 2 bootstrap. | |

---

## Reliability & Observability for Robots

The infrastructure under the autonomy: it tells you *when your robot is about to do something stupid* and catches it on the way down.

| Project | What it does | Status |
|---|---|---|
| **[helix](https://github.com/yusufdxb/helix)** · [demo](https://youtu.be/PbKXB91-NSY) | Sense, diagnose, recover, explain. Fault handling for a live ROS 2 graph. | live GO2, 8 sessions |
| **[BlackBoxRS](https://github.com/yusufdxb/BlackBoxRS)** | Flight recorder and post-failure forensics: one command turns a field failure into an incident bundle with a timeline, evidence links, and an adoptable prevention rule. | 547 tests; real GO2 bag replay, not a live loop |
| **[policy-health-monitor](https://github.com/yusufdxb/policy-health-monitor)** | Runtime health monitor for learned policies: reads a policy's internals and the robot's own health signals and arbitrates them into one status with a safe-fallback layer. All C++. | onboard GO2, shadow mode: induced faults reach STOP 5/5, 0 false alarms in 5 min |

---

## Perception, Evaluation & 3D Scene Understanding

| Project | What it does | Status |
|---|---|---|
| **[supercombo-blindspot](https://github.com/yusufdxb/supercombo-blindspot)** · [demo](https://youtu.be/tnM18XGbNMY) | Does a production L2 driving model know when it is blind? | [writeup](https://yusufdxb.github.io/papers/silent-collapse-distribution-shift-teardown.pdf) published, not submitted |
| **[av2-city-shift](https://github.com/yusufdxb/av2-city-shift)** · [demo](https://youtu.be/X_JOo6AltDY) | Does a trajectory predictor know when it is in a new city, and does its error reach the car's driving? Pre-registered, closed loop, TensorRT. | stages 1 to 4 complete, audited |
| **[openvocab-tsdf](https://github.com/yusufdxb/openvocab-tsdf)** | GPU-accelerated open-vocabulary 3D mapping: build a TSDF and query it in natural language. | live RGB-D mapping end-to-end |
| **[physx-newton-bench](https://github.com/yusufdxb/physx-newton-bench)** | PhysX vs Newton/MJWarp in Isaac Lab: throughput scaling, per-process VRAM, 10-seed learning curves. | published |
| **[inspectnet-cx](https://github.com/yusufdxb/inspectnet-cx)** | Reproducible industrial anomaly-inspection scaffold on an MVTec AD baseline. | 80 tests, CPU-only parity |

---

## Hardware & Embedded

Where I started, and still the most satisfying when it physically moves.

| Project | What it does |
|---|---|
| **[kestrel-rt](https://github.com/yusufdxb/kestrel-rt)** · [demo](https://youtu.be/AfcJQIyyuUY) | Bare-metal Cortex-M4F runtime written from the reset vector up, with an ESP32-S3 network chip isolated behind a budgeted link. 10.4M control periods with no deadline miss on the physical board. |
| **[RADAR-Telepresence-Robot](https://github.com/yusufdxb/RADAR-Telepresence-Robot)** | Medical telepresence robot: remote teleop, live video with pan-tilt, and real-time SpO₂ / heart-rate monitoring through one Qt 6 operator console. |
| **[TicTacToe-3link-robot](https://github.com/yusufdxb/TicTacToe-3link-robot)** | A 3-DOF arm that computes closed-form IK to physically draw X's and O's while a Minimax AI plays optimally. |
| **[EcoSort-bin](https://github.com/yusufdxb/EcoSort-bin)** | Multi-sensor fusion (weight + color + IR + ultrasonic) on an Arduino classifies and sorts waste. Finite-state control, no ML. |

---

## Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/ROS_2-22314E?style=for-the-badge&logo=ros&logoColor=white" />
  <img src="https://img.shields.io/badge/Isaac_Lab-76B900?style=for-the-badge&logo=nvidia&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/ONNX-005CED?style=for-the-badge&logo=onnx&logoColor=white" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white" />
  <img src="https://img.shields.io/badge/NVIDIA_Jetson-76B900?style=for-the-badge&logo=nvidia&logoColor=white" />
</p>

| Area | Technologies |
|---|---|
| **Robotics** | ROS 2 Humble, Nav2, lifecycle nodes, tf2, ros2_control, SLAM Toolbox, Gazebo, Isaac Lab, Isaac Sim |
| **Learning** | PyTorch, PPO / reinforcement learning, sim-to-real, ONNX + parity gating, out-of-distribution detection |
| **Perception** | YOLOv8, OpenCV, RealSense D435i, Whisper ASR, GCC-PHAT, open-vocab 3D mapping |
| **Reliability** | Fault detection, incident forensics, fail-closed safety envelopes, acceptance evidence, paired statistical evaluation |
| **Embedded** | Jetson Orin NX, Arduino, Raspberry Pi, sensor/actuator integration, firmware |
| **Languages** | C++17, Python 3, Rust, MATLAB, C |
| **Tools** | Git, Docker, CMake, colcon, Qt 6, Fusion 360 |

---

[Website](https://yusufdxb.github.io) · [LinkedIn](https://www.linkedin.com/in/yusuf-guenena/) · [yusuf.a.guenena@gmail.com](mailto:yusuf.a.guenena@gmail.com)
