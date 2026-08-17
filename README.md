<div align="center">

# Yusuf Guenena

### I build the reliability layer for learned robot systems.

**M.S. Robotics Engineering, Wayne State University**

ROS 2 &nbsp;·&nbsp; C++ &nbsp;·&nbsp; Sim-to-real on quadrupeds &nbsp;·&nbsp; Runtime safety for learned policies

[![Email](https://img.shields.io/badge/Email-yusuf.a.guenena%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:yusuf.a.guenena@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-yusufdxb-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/yusufdxb)

</div>

---

<div align="center">

### See it run

| [**HELIX**](https://github.com/yusufdxb/helix) | [**Phoenix**](https://github.com/yusufdxb/go2-phoenix) | [**supercombo-blindspot**](https://github.com/yusufdxb/supercombo-blindspot) |
|:---:|:---:|:---:|
| [<img src="https://img.youtube.com/vi/PbKXB91-NSY/mqdefault.jpg" width="260">](https://youtu.be/PbKXB91-NSY) | [<img src="https://img.youtube.com/vi/Nu0oWyJJbEM/mqdefault.jpg" width="260">](https://youtu.be/Nu0oWyJJbEM) | [<img src="https://img.youtube.com/vi/tnM18XGbNMY/mqdefault.jpg" width="260">](https://youtu.be/tnM18XGbNMY) |
| Self-healing loop on a live GO2 | Isaac Lab training to real robot | A production driving model going blind |

</div>

---

## What I do

Learned policies fail quietly. A locomotion network saturates, a perception model stops perceiving, a simulator's counterfactual stops being faithful, and nothing in the stack raises its hand. I build the layer that notices, and I mark on every repo what has actually run on hardware and what has not.

**Detect it** &nbsp;·&nbsp; fault sensing, OOD monitoring on policy internals, anomaly detection on a live ROS 2 graph
**Contain it** &nbsp;·&nbsp; fail-closed safety envelopes, recovery allowlists, deploy-time parity gates
**Prove it** &nbsp;·&nbsp; tamper-evident acceptance evidence, incident forensics, honest null results

---

## Featured

| Project | What it is | Where it stands |
|---|---|:---|
| **[helix](https://github.com/yusufdxb/helix)** [▶](https://youtu.be/PbKXB91-NSY) | Self-healing ROS 2 runtime: Sense, Diagnose, Recover, Explain. C++ hot-path port so it shares a Jetson with Nav2. | Live GO2 + Jetson Orin NX, 8 lab sessions. Session 8: 30 anomalies into 14 hints into 14 recovery actions. **Open:** `cmd_vel` not yet wired to an actuator fallback. |
| **[go2-phoenix](https://github.com/yusufdxb/go2-phoenix)** [▶](https://youtu.be/Nu0oWyJJbEM) | Isaac Lab sim-to-real loop: train, export through an ONNX parity gate, deploy behind a fail-closed safety layer, replay hardware failures into fine-tuning. | Deploy stack ran end to end on the real GO2. **Open:** Gate 7 on-robot stand; an export audit means every checkpoint owes a re-export and fresh parity check. |
| **[ivf](https://github.com/yusufdxb/ivf)** | Acceptance checker for simulator experiments. Declare "unchanged behavior" in YAML, get a sealed PASS/FAIL evidence bundle with SHA-256 provenance. | Flagship case: real PhysX vs Newton/MJWarp cart-pole, recorded verdict `FAIL`, 22 validity checks with 0 failed. Re-verifiable CPU-only, no GPU or simulator needed. |
| **[supercombo-blindspot](https://github.com/yusufdxb/supercombo-blindspot)** [▶](https://youtu.be/tnM18XGbNMY) | Distribution-shift teardown of the network driving openpilot. Does a production L2 model know when it is blind? | It does not, and it fails silently. Parity-controlled to comma's own output on 100% of 1159 frames within ±0.5 m/s². 8 of 10 output heads go near-constant under shift. Writeup drafted, not submitted. |
| **[BlackBoxRS](https://github.com/yusufdxb/BlackBoxRS)** | Incident intelligence for ROS 2: one command turns a field failure into a bundle with a timeline, evidence links, and an adoptable prevention rule. | Replays a genuine GO2 `rosbag2` (~94k msgs / 330 s) clean with zero anomalies; finds an injected dropout from bag timing alone. **Open:** not yet in a live control loop. |

---

## Active M.S. research

**[GO2-seeing-eye-dog](https://github.com/yusufdxb/GO2-seeing-eye-dog)** &nbsp;·&nbsp; a guide dog has to be summonable by voice, not by a phone screen.

Mic-array GCC-PHAT bearing + Whisper command parsing + YOLOv8 depth back-projection, fused into a score that must hold 5 consecutive frames before locking a target and publishing a Nav2 goal.

> **Scope, stated plainly:** this recalls the robot, it does not guide the user anywhere. Safety alerts are advisory and do not hard-gate motion. 32 unit tests pass, and nothing here has a measured accuracy or latency result on the real robot yet.

---

## The stacks

<details open>
<summary><b>Reliability &amp; runtime safety</b></summary>

| Repo | One line | Status |
|---|---|---|
| [helix](https://github.com/yusufdxb/helix) | Fault sensing, diagnosis, and recovery for a ROS 2 graph | real GO2, 8 sessions |
| [BlackBoxRS](https://github.com/yusufdxb/BlackBoxRS) | Incident bundles and failure forensics | real GO2 bag replay |
| [policy-health-monitor](https://github.com/yusufdxb/policy-health-monitor) | OOD detection on a learned policy's internals, C++ lifecycle node | 295 tests, synthetic only |
| [riskgraph-go2](https://github.com/yusufdxb/riskgraph-go2) | Persistent route-risk memory and safer-route scoring for Nav2 | hardware-unverified |

</details>

<details open>
<summary><b>Sim-to-real &amp; learned control</b></summary>

| Repo | One line | Status |
|---|---|---|
| [go2-phoenix](https://github.com/yusufdxb/go2-phoenix) | Closed-loop sim-to-real locomotion learning | ran on real GO2, Gate 7 open |
| [ivf](https://github.com/yusufdxb/ivf) | Sealed acceptance evidence for simulator experiments | `0.1.0rc2` |
| [physx-newton-bench](https://github.com/yusufdxb/physx-newton-bench) | PhysX vs Newton/MJWarp in Isaac Lab: throughput, VRAM, 10-seed curves | published |
| [go2_omniverse](https://github.com/yusufdxb/go2_omniverse) | Isaac Sim 5.0 / ROS 2 Jazzy port (merged upstream) plus an IMU-driven digital twin | upstream #84 |

</details>

<details open>
<summary><b>Perception &amp; interaction</b></summary>

| Repo | One line | Status |
|---|---|---|
| [GO2-seeing-eye-dog](https://github.com/yusufdxb/GO2-seeing-eye-dog) | Voice recall for an assistive quadruped | M.S. thesis, in progress |
| [come-here](https://github.com/yusufdxb/come-here) | Hear the call, rotate, find the person, walk to them | |
| [openvocab-tsdf](https://github.com/yusufdxb/openvocab-tsdf) | GPU open-vocabulary 3D mapping, queried in natural language | |
| [go2-semantic-nav](https://github.com/yusufdxb/go2-semantic-nav) | Open-vocab 3D scene graph feeding a language-grounded Nav2 overlay | |
| [go2-audio](https://github.com/yusufdxb/go2-audio) | Real mic audio off a GO2 over WebRTC, since the DDS topic is broken | |

</details>

<details open>
<summary><b>Model teardown &amp; evaluation</b></summary>

| Repo | One line | Status |
|---|---|---|
| [supercombo-blindspot](https://github.com/yusufdxb/supercombo-blindspot) | Does openpilot's model know when it is blind? | writeup drafted |
| [inspectnet-cx](https://github.com/yusufdxb/inspectnet-cx) | Reproducible industrial anomaly-inspection scaffold, MVTec AD baseline | |
| [convolens](https://github.com/yusufdxb/convolens) | Conversation intelligence with an honest, reproducible eval dashboard | |
| [gq-insight-mcp](https://github.com/yusufdxb/gq-insight-mcp) | MCP server for grounded, citation-faithful search over research interviews | |

</details>

<details>
<summary><b>Hardware &amp; embedded</b></summary>

| Repo | One line |
|---|---|
| [RADAR-Telepresence-Robot](https://github.com/yusufdxb/RADAR-Telepresence-Robot) | Medical telepresence robot: teleop, pan-tilt video, vital-sign sensing, Qt 6 console |
| [TicTacToe-3link-robot](https://github.com/yusufdxb/TicTacToe-3link-robot) | 3-DOF arm with closed-form IK that physically draws against a Minimax AI |
| [EcoSort-bin](https://github.com/yusufdxb/EcoSort-bin) | Multi-sensor waste sorting on an Arduino, finite-state control, no ML |
| [go2-jetson-setup-guide](https://github.com/yusufdxb/go2-jetson-setup-guide) | Bringing up a Jetson on a GO2: first boot, SSH, networking, ROS 2 bootstrap |

</details>

---

## Falsified hypotheses

Kept public with their full evidence trail, because the measurement is the contribution.

| Repo | The hypothesis | What happened |
|---|---|---|
| **[ipfd](https://github.com/yusufdxb/ipfd)** | Rewind a simulator to step `t`, re-run, and treat that branch as what the uninterrupted episode would have done. | Branches matching on exposed state, observation, *and* the replayed action sequence still reached different outcomes. The preregistered positive control needed a 50% cut in disagreement and got 38.9%, so the stopping rule fired. Archived negative result. |
| **[ashfall](https://github.com/yusufdxb/ashfall)** | Fine-tuning a locomotion policy on its own failures improves robustness. | One seed suggested +5.1 pp. Paired across 11 seeds with an exact sign-flip permutation test, the effect vanishes and more seeds moved p *away* from significance. Null holds on both terrains. The 6-mode failure detector (18/18, zero cross-fires) and the eval framework survive. |

---

## Stack

| | |
|---|---|
| **Robotics** | ROS 2 Humble · Nav2 · lifecycle nodes · tf2 · ros2_control · SLAM Toolbox · Gazebo · Isaac Lab · Isaac Sim |
| **Learning** | PyTorch · PPO / RL · sim-to-real · ONNX + parity gating · out-of-distribution detection |
| **Perception** | YOLOv8 · OpenCV · RealSense D435i · Whisper ASR · GCC-PHAT · open-vocab 3D mapping |
| **Systems** | C++17 · Python 3 · CMake · colcon · Docker · Jetson deployment · Qt 6 · Arduino |

<div align="center">

---

[yusuf.a.guenena@gmail.com](mailto:yusuf.a.guenena@gmail.com) &nbsp;·&nbsp; [github.com/yusufdxb](https://github.com/yusufdxb)

</div>
