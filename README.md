# Yusuf Guenena

**I build the reliability layer for learned robot systems.**

M.S. Robotics Engineering @ Wayne State University · Runtime safety for learned policies · Sim-to-real on quadrupeds

[![Email](https://img.shields.io/badge/Email-yusuf.a.guenena%40gmail.com-EA4335?logo=gmail&logoColor=white)](mailto:yusuf.a.guenena@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-yusufdxb-181717?logo=github&logoColor=white)](https://github.com/yusufdxb)

---

Learned policies fail quietly. A locomotion network saturates, a perception model stops perceiving, a simulator's counterfactual stops being faithful, and nothing in the stack raises its hand. Most of what I build is the layer that notices: fault detection and recovery on a live robot, deploy-time parity gates, out-of-distribution monitoring on policy internals, and acceptance evidence you can re-verify a year later.

I work across the stack: C++ control loops, Python perception and RL, ROS 2 architecture, embedded firmware, CAD, and the GUIs on top. Most of it runs on a Unitree GO2. Every repo below states what has actually run on hardware and what has not, because that distinction is the whole job.

<p align="center">
  <a href="https://youtu.be/PbKXB91-NSY"><img src="https://img.youtube.com/vi/PbKXB91-NSY/mqdefault.jpg" width="250"></a>
  <a href="https://youtu.be/Nu0oWyJJbEM"><img src="https://img.youtube.com/vi/Nu0oWyJJbEM/mqdefault.jpg" width="250"></a>
  <a href="https://youtu.be/tnM18XGbNMY"><img src="https://img.youtube.com/vi/tnM18XGbNMY/mqdefault.jpg" width="250"></a>
</p>
<p align="center">
  <em>HELIX self-healing on a live GO2 · Phoenix sim-to-real · a production driving model going blind</em>
</p>

---

## Flagship: HELIX

[![Repo](https://img.shields.io/badge/GitHub-helix-181717?style=flat&logo=github)](https://github.com/yusufdxb/helix)
![Stars](https://img.shields.io/github/stars/yusufdxb/helix?style=flat&color=yellow)
[![Demo](https://img.shields.io/badge/%E2%96%B6_Demo-YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://youtu.be/PbKXB91-NSY)
![Status](https://img.shields.io/badge/Status-Validated_on_live_GO2-brightgreen?style=flat)

A self-healing runtime for ROS 2 robots, built as a four-tier loop. **Sense**: lifecycle nodes emit structured `FaultEvent`s from a rolling Z-score detector, a heartbeat monitor, and a log parser. **Diagnose**: deterministic rules turn faults into `RecoveryHint`s. **Recover**: a single `cmd_vel` publisher behind a strict allowlist and cooldown. **Explain**: an advisory local LLM that is never on the safety-critical path. Hot-path sensing nodes are being ported from Python to C++ so HELIX can share a Jetson with Nav2 and perception instead of competing with them.

Validated on a live Unitree GO2 and Jetson Orin NX across eight hardware lab sessions. The Session 8 bag runs the loop end to end: 30 anomalies into 14 recovery hints into 14 recovery actions.

> **Open limitation:** `/helix/cmd_vel` currently has no downstream subscribers, so `STOP_AND_HOLD` is a void publish. Closing the recovery loop physically, through a `twist_mux` fallback, is the next hardware task.

`ROS 2 Humble` `C++17` `Lifecycle Nodes` `Jetson Orin NX` `Unitree GO2` `Local LLM`

---

## Featured Work

### go2-phoenix

[![Repo](https://img.shields.io/badge/GitHub-go2--phoenix-181717?style=flat&logo=github)](https://github.com/yusufdxb/go2-phoenix)
![Stars](https://img.shields.io/github/stars/yusufdxb/go2-phoenix?style=flat&color=yellow)
[![Demo](https://img.shields.io/badge/%E2%96%B6_Demo-YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://youtu.be/Nu0oWyJJbEM)
![Status](https://img.shields.io/badge/Status-Gate_7_open-orange?style=flat)

Closed-loop sim-to-real learning for the GO2. A locomotion policy trains in Isaac Lab, exports to ONNX through a **torch/onnxruntime parity gate** that refuses to ship a checkpoint whose deploy-time numerics drift outside tolerance, then runs behind a **fail-closed** ROS 2 safety layer with a shared slew cap. Failures captured on hardware replay in simulation under randomized physics and feed a fine-tuning curriculum. The deploy stack has run end to end on the real robot, on the Jetson.

> **Where it stands:** on-robot locomotion validation (Gate 7) is open. An export audit found pre-audit checkpoints silently dropped observation normalization, so every checkpoint owes a re-export and a fresh parity check before the retry. The adaptation loop has not yet closed once on real failure data. [`EVIDENCE.md`](https://github.com/yusufdxb/go2-phoenix/blob/main/EVIDENCE.md) is the verified / inferred / not-validated ledger.

`Isaac Lab` `PPO` `ONNX` `ROS 2` `Sim-to-Real` `Unitree GO2`

### ivf

[![Repo](https://img.shields.io/badge/GitHub-ivf-181717?style=flat&logo=github)](https://github.com/yusufdxb/ivf)
![Stars](https://img.shields.io/github/stars/yusufdxb/ivf?style=flat&color=yellow)
![Status](https://img.shields.io/badge/Status-0.1.0rc2-blue?style=flat)

Offline acceptance and evidence for simulator experiments. You declare what "unchanged behavior" means in a YAML file (which signals, which tolerances and units, which controls must hold, what the minimum sample is). IVF checks the experiment was even valid before letting any result decide a verdict, then seals the manifest, signals, reasoning, provenance, and per-file SHA-256 digests into one auditable bundle.

The flagship case is a real PhysX versus Newton/MJWarp cart-pole comparison whose recorded verdict is `FAIL`, with 22 validity checks (18 pass, 3 unverifiable, 1 not applicable, 0 failed). Anyone can re-verify the shipped bundle from its seal, CPU only, with no GPU and no simulator install. IVF is not a benchmark: it does not measure throughput and does not designate a reference engine.

`Python` `Isaac Lab` `PhysX` `Newton / MJWarp` `SHA-256 provenance` `CLI`

### supercombo-blindspot

[![Repo](https://img.shields.io/badge/GitHub-supercombo--blindspot-181717?style=flat&logo=github)](https://github.com/yusufdxb/supercombo-blindspot)
![Stars](https://img.shields.io/github/stars/yusufdxb/supercombo-blindspot?style=flat&color=yellow)
[![Demo](https://img.shields.io/badge/%E2%96%B6_Demo-YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://youtu.be/tnM18XGbNMY)
![Status](https://img.shields.io/badge/Status-Study_complete-brightgreen?style=flat)

A distribution-shift teardown of the neural network that drives openpilot, an L2 driver-assistance system deployed on public roads. One question: presented with input outside its training distribution, does it fail conspicuously or silently?

Silently. The study rests on a parity-controlled reimplementation of v0.9.7 inference that agrees with comma's own reference output on 100% of 1159 real frames within ±0.5 m/s², so the negative result is attributable to the model and not the harness. Under shift, 8 of 10 tracked output readouts go near-constant, the recurrent state contracts to a point, and the exported uncertainty heads never leave their nominal real-driving range. An internal recurrent signal does encode the failure and is recoverable, but the model never exposes it. Writeup drafted, not submitted.

`ONNX Runtime` `CARLA` `OOD Detection` `Recurrent State` `openpilot`

### BlackBoxRS

[![Repo](https://img.shields.io/badge/GitHub-BlackBoxRS-181717?style=flat&logo=github)](https://github.com/yusufdxb/BlackBoxRS)
![Stars](https://img.shields.io/github/stars/yusufdxb/BlackBoxRS?style=flat&color=yellow)
![Status](https://img.shields.io/badge/Status-Real_GO2_bag_replay-brightgreen?style=flat)

Incident intelligence for ROS 2 robots. A daemon watches the graph and host; when a failure fires, one command builds a reproducible incident bundle: a timeline, raw evidence, config and version signatures, a likely-cause narrative where every claim links to the evidence file backing it, and a prevention rule you can adopt so the same failure blocks the next launch.

The offline replay path runs against a genuine `rosbag2` recording from a physical GO2 (about 94k messages over 330 seconds). Played untouched it replays clean with zero anomalies, which is the point: the detectors are not inventing failures. Inject a pose dropout into that real window and the detector finds it from bag timing alone.

> **Honest boundary:** this has not run in a closed control loop on a live robot. A live onboard capture during a real field failure is the one thing still owed.

`ROS 2` `rosbag2` `Python` `Incident Forensics` `CLI`

---

## Active M.S. Research

### GO2 Seeing-Eye Dog

[![Repo](https://img.shields.io/badge/GitHub-GO2--seeing--eye--dog-181717?style=flat&logo=github)](https://github.com/yusufdxb/GO2-seeing-eye-dog)
![Stars](https://img.shields.io/github/stars/yusufdxb/GO2-seeing-eye-dog?style=flat&color=yellow)
![Status](https://img.shields.io/badge/Status-Active_Research-orange?style=flat)

A guide dog has to be summonable. If the handler puts the harness down, sits on a bench, and then wants the dog back, the dog finds them by voice, not by an app or a joystick. This repository closes the **recall** half of that interaction on real hardware: a four-channel mic array gives a GCC-PHAT bearing, Whisper parses the command, YOLOv8 plus depth back-projection gives 3D person poses, and a fused audio-visual score must hold across five consecutive frames before the target locks and publishes a Nav2 goal.

> **Scope, stated plainly:** this recalls the robot, it does not guide the user anywhere. Safety alerts are advisory and do not hard-gate motion. 32 unit tests pass, and nothing here has a measured accuracy or latency result on the real robot yet. End-to-end recall on hardware is the open item.

`ROS 2 Humble` `GCC-PHAT` `Whisper ASR` `YOLOv8` `RealSense D435i` `Nav2` `C++ Lifecycle Node`

---

## The GO2 Quadruped Stack

A connected body of work turning a stock quadruped into something that learns, navigates, and recovers on its own.

| Project | What it does | Status |
|---|---|---|
| **[riskgraph-go2](https://github.com/yusufdxb/riskgraph-go2)** | Persistent route-risk memory: the robot remembers where things went wrong and scores safer paths through an explainable Nav2 overlay. | hardware-unverified |
| **[come-here](https://github.com/yusufdxb/come-here)** | Hears "come here," localizes the voice, turns, finds the person, and walks to them. Audio-visual approach in one loop. | |
| **[go2-audio](https://github.com/yusufdxb/go2-audio)** | Real microphone audio off a GO2 over WebRTC, because the DDS `/audiosender` topic is broken. | |
| **[go2_omniverse](https://github.com/yusufdxb/go2_omniverse)** | Isaac Sim 5.0 / ROS 2 Jazzy port (merged upstream) plus an IMU-driven digital-twin mode mirroring a real GO2. | upstream #84 |
| **[ros2-go2-nav2-yolo](https://github.com/yusufdxb/ros2-go2-nav2-yolo)** | Full Gazebo autonomy stack (Nav2 + SLAM Toolbox + CHAMP + YOLOv8), with the non-obvious DDS/TF/SLAM integration bugs documented and fixed. | |
| **[go2-jetson-setup-guide](https://github.com/yusufdxb/go2-jetson-setup-guide)** | Bringing up a Jetson on a GO2: first boot, SSH, networking, internet sharing, ROS 2 bootstrap. | |

---

## Reliability & Observability for Robots

The layer that tells you *when your robot is about to do something stupid* and catches it on the way down.

| Project | What it does | Status |
|---|---|---|
| **[helix](https://github.com/yusufdxb/helix)** | Sense, diagnose, recover, explain. Fault handling for a live ROS 2 graph. | live GO2, 8 sessions |
| **[BlackBoxRS](https://github.com/yusufdxb/BlackBoxRS)** | Flight recorder and post-failure forensics: incident bundles you can read. | real GO2 bag replay |
| **[policy-health-monitor](https://github.com/yusufdxb/policy-health-monitor)** | Runtime OOD detection on a learned policy's internals, arbitrated into one health status with a safe-fallback layer. C++ managed-lifecycle node. | 295 tests, synthetic only |
| **[ivf](https://github.com/yusufdxb/ivf)** | Sealed, re-verifiable acceptance evidence for simulator experiments. | `0.1.0rc2` |

---

## Perception, Evaluation & 3D Scene Understanding

| Project | What it does | Status |
|---|---|---|
| **[supercombo-blindspot](https://github.com/yusufdxb/supercombo-blindspot)** | Does a production L2 driving model know when it is blind? | writeup drafted |
| **[openvocab-tsdf](https://github.com/yusufdxb/openvocab-tsdf)** | GPU-accelerated open-vocabulary 3D mapping: build a TSDF and query it in natural language. | |
| **[go2-semantic-nav](https://github.com/yusufdxb/go2-semantic-nav)** | Open-vocab 3D semantic scene graph feeding a language-grounded Nav2 overlay on a Jetson. | |
| **[physx-newton-bench](https://github.com/yusufdxb/physx-newton-bench)** | PhysX vs Newton/MJWarp in Isaac Lab: throughput scaling, per-process VRAM, 10-seed learning curves. | published |
| **[inspectnet-cx](https://github.com/yusufdxb/inspectnet-cx)** | Reproducible industrial anomaly-inspection scaffold on an MVTec AD baseline. | |

---

## Falsified Hypotheses

Two projects exist because the idea did not survive contact with measurement. Both stay public with their full evidence trail, because the measurement is the contribution.

| Project | The hypothesis | What happened |
|---|---|---|
| **[ipfd](https://github.com/yusufdxb/ipfd)** | Rewind a simulator to step `t`, re-run it, and treat that branch as what the uninterrupted episode would have done. | Branches matching the reference on exposed simulator state, on the immediate observation, *and* on the exact replayed action sequence still reached different terminal outcomes. The preregistered positive control needed to cut disagreement by 50% and cut it by 38.9%, so the stopping rule fired. Archived negative result. |
| **[ashfall](https://github.com/yusufdxb/ashfall)** | Fine-tuning a locomotion policy on a curriculum of its own failures improves robustness. | One seed suggested a +5.1 pp lift. Paired across 11 seeds with an exact sign-flip permutation test, the effect vanishes, and adding seeds moved the p-value *away* from significance. The null holds on both terrains. What survives: a 6-mode failure detector at 18/18 with zero cross-fires, the paired evaluation framework, and a seed-propagation bug fixed upstream. |

---

## Hardware & Embedded

Where I started, and still the most satisfying when it physically moves.

| Project | What it does |
|---|---|
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
| **Languages** | C++17, Python 3, MATLAB, C |
| **Tools** | Git, Docker, CMake, colcon, Qt 6, Fusion 360 |

---

[yusuf.a.guenena@gmail.com](mailto:yusuf.a.guenena@gmail.com)
