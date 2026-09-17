<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/hero-dark.webp">
  <img src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/hero-light.webp" width="700" alt="A Unitree GO2 quadruped robot drawn as a field of fine particles sampled from the robot's own surface geometry.">
</picture>

<h1>Yusuf Guenena</h1>

<p><strong>I build the reliability layer for learned robot systems.</strong></p>

<p>Robotics &nbsp;·&nbsp; Embodied AI &nbsp;·&nbsp; Reliability</p>

<p><sub>Unitree GO2 EDU</sub></p>

</div>

<br>

Learned policies fail quietly. A locomotion network saturates, a perception model stops perceiving, a simulator's counterfactual stops being faithful, and nothing in the stack raises its hand. Most of what I build is the layer that notices: fault detection and recovery on a live robot, deploy-time parity gates, out-of-distribution monitoring on policy internals, and acceptance evidence that can be re-verified a year later.

M.S. Robotics Engineering at Wayne State University. The work runs on a Unitree GO2 EDU with a Jetson Orin NX, and every repository states what has actually run on hardware and what has not, because that distinction is the whole job.

---

## Selected work

### [helix](https://github.com/yusufdxb/helix) &nbsp;·&nbsp; a self-healing runtime for ROS 2 robots

Sense a fault, diagnose it, hold the robot safe, explain it afterwards. One publisher behind a strict allowlist owns the response; the advisory LLM that narrates it is never on the safety path.

**Validated across eight live GO2 and Jetson sessions.** Session 8 runs the loop end to end: 30 anomalies into 14 recovery hints into 14 actions. Not yet physically closed, `/helix/cmd_vel` has no downstream subscriber.

`ROS 2 Humble` `C++17` `lifecycle nodes` &nbsp;·&nbsp; [demo](https://youtu.be/PbKXB91-NSY)

### [go2-phoenix](https://github.com/yusufdxb/go2-phoenix) &nbsp;·&nbsp; closed-loop sim-to-real locomotion

Train in Isaac Lab, export through a parity gate that refuses any checkpoint whose deploy-time numerics drift outside tolerance, run behind a fail-closed safety layer.

**Sim-verified:** 32 of 32 stand successes at 3.30% slew against a 5% gate. On-robot locomotion validation is open, and the adaptation loop has not yet closed on real failure data.

`Isaac Lab` `PPO` `ONNX` `ROS 2` &nbsp;·&nbsp; [demo](https://youtu.be/Nu0oWyJJbEM) &nbsp;·&nbsp; [evidence ledger](https://github.com/yusufdxb/go2-phoenix/blob/main/EVIDENCE.md)

### [GO2-seeing-eye-dog](https://github.com/yusufdxb/GO2-seeing-eye-dog) &nbsp;·&nbsp; voice recall for an assistive quadruped

A guide dog has to be summonable. Mic-array bearing, Whisper, and YOLOv8 depth fuse into a target lock that must hold five consecutive frames before a Nav2 goal is published.

**Scope stated plainly:** this recalls the robot, it does not guide anyone. 32 unit tests pass, and nothing here has a measured accuracy or latency result on the real robot yet.

`ROS 2 Humble` `GCC-PHAT` `Whisper` `YOLOv8` `RealSense D435i`

### [supercombo-blindspot](https://github.com/yusufdxb/supercombo-blindspot) &nbsp;·&nbsp; does a shipped driving model know when it is blind?

A distribution-shift teardown of the network that drives openpilot on public roads. Outside its training distribution, does it fail conspicuously or silently?

**Silently.** On a parity-controlled reimplementation matching comma's reference output on 100% of 1159 frames within ±0.5 m/s², 8 of 10 tracked readouts fall below 1% of real activity under shift, and 0 of 219 shifted frames exceed the real uncertainty p95. An internal signal does encode the failure; the model never exposes it.

`ONNX Runtime` `CARLA` `OOD detection` &nbsp;·&nbsp; [demo](https://youtu.be/tnM18XGbNMY)

---

## The GO2 stack

| | | |
|---|---|---|
| [**riskgraph-go2**](https://github.com/yusufdxb/riskgraph-go2) | Route-risk memory and explainable safer-route scoring for Nav2 | 111 tests, hardware-unverified |
| [**go2-semantic-nav**](https://github.com/yusufdxb/go2-semantic-nav) | Open-vocabulary 3D scene graph driving a language-grounded Nav2 overlay | on-robot eval pending |
| [**come-here**](https://github.com/yusufdxb/come-here) | Hears "come here", localises the voice, turns, walks to the person | hear and rotate on hardware |
| [**go2_omniverse**](https://github.com/yusufdxb/go2_omniverse) | Isaac Sim 5.0 and ROS 2 Jazzy port, plus an IMU-driven digital twin | [merged upstream](https://github.com/abizovnuralem/go2_omniverse/pull/84) |
| [**ros2-go2-nav2-yolo**](https://github.com/yusufdxb/ros2-go2-nav2-yolo) | Gazebo autonomy stack with the DDS, TF and SLAM integration bugs fixed | sim, plus a real YOLO path |
| [**go2-audio**](https://github.com/yusufdxb/go2-audio) | Real microphone audio off a GO2 over WebRTC, because the DDS topic is broken | tool |

---

## Reliability and research

[**policy-health-monitor**](https://github.com/yusufdxb/policy-health-monitor) watches a learned policy's own internal activations rather than its outputs, and arbitrates several detectors worst-wins into a single health status with a safe fallback underneath. A C++ managed lifecycle node. 295 tests pass; on-device latency and false-positive rate are not measured yet.

[**BlackBoxRS**](https://github.com/yusufdxb/BlackBoxRS) turns a field failure into a reproducible incident bundle: a timeline, the raw evidence, config and version signatures, and a preflight rule you can adopt so the same failure blocks the next launch. 547 tests pass, and the committed evidence is an incident built from a real GO2 bag, replayed offline rather than captured live.

[**ivf**](https://github.com/yusufdxb/ivf) seals simulator acceptance evidence so a verdict can be re-verified a year later, CPU only. Its flagship bundle records `FAIL` on a real PhysX versus Newton cart-pole, over 22 validity checks: 18 pass, 3 unverifiable, 1 not applicable, 0 failed.

**Two archived null results stay public with their full evidence trail,** because the measurement is the contribution. [**ipfd**](https://github.com/yusufdxb/ipfd) asked whether a rewound simulator branch is a faithful counterfactual; branches matching on state, observation and the replayed action sequence still ended differently, and the preregistered control needed a 50% cut in disagreement but delivered 38.9%. [**ashfall**](https://github.com/yusufdxb/ashfall) asked whether fine-tuning a locomotion policy on its own failures improves robustness; one seed suggested +5.1 points, and paired across 11 seeds with an exact sign-flip permutation test the effect is null.

The supercombo teardown is written up and not yet submitted. M.S. thesis work on assistive quadruped autonomy is in progress and stays private until defense.

---

## Also

[**openvocab-tsdf**](https://github.com/yusufdxb/openvocab-tsdf) GPU open-vocabulary 3D mapping queried in natural language &nbsp;·&nbsp; [**physx-newton-bench**](https://github.com/yusufdxb/physx-newton-bench) PhysX versus Newton/MJWarp in Isaac Lab &nbsp;·&nbsp; [**inspectnet-cx**](https://github.com/yusufdxb/inspectnet-cx) reproducible industrial anomaly inspection on MVTec AD &nbsp;·&nbsp; [**go2-jetson-setup-guide**](https://github.com/yusufdxb/go2-jetson-setup-guide) bringing a Jetson up on a GO2

Earlier hardware: [**RADAR-Telepresence-Robot**](https://github.com/yusufdxb/RADAR-Telepresence-Robot) medical telepresence with teleop, pan-tilt video and live SpO₂ in one Qt 6 console &nbsp;·&nbsp; [**TicTacToe-3link-robot**](https://github.com/yusufdxb/TicTacToe-3link-robot) a 3-DOF arm solving closed-form IK against a minimax opponent &nbsp;·&nbsp; [**EcoSort-bin**](https://github.com/yusufdxb/EcoSort-bin) multi-sensor waste sorting on an Arduino

---

## Stack

| | |
|---|---|
| **Robotics** | ROS 2 Humble · Nav2 · lifecycle nodes · tf2 · ros2_control · SLAM Toolbox · RTAB-Map · Isaac Sim · Isaac Lab · Gazebo |
| **Learning** | PyTorch · PPO and reinforcement learning · sim-to-real · ONNX with parity gating · out-of-distribution detection · VLMs |
| **Perception** | YOLOv8 · OpenCV · RealSense D435i · Whisper ASR · GCC-PHAT · open-vocabulary 3D mapping |
| **Reliability** | fault detection and recovery · incident forensics · fail-closed envelopes · acceptance evidence · paired statistical evaluation |
| **Systems** | C++17 · Python 3 · MATLAB · Linux · Docker · CMake · colcon · Qt 6 |
| **Hardware** | Unitree GO2 EDU · Jetson Orin NX · Arduino · Raspberry Pi · Fusion 360 |

---

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/activity-dark.png">
  <img src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/activity-light.png" width="380" alt="Sparkline of weekly GitHub contributions over the last twelve months.">
</picture>

<p><sub><!--activity-->Last 12 months: <b>3,148</b> contributions on <b>150</b> days, across <b>27</b> public repositories.<!--/activity--></sub></p>

<p><sub>The hero is a particle rendering of the GO2's own <code>go2_description</code> visual meshes, assembled with the URDF joint transforms. <a href="https://github.com/yusufdxb/yusufdxb/tree/main/tools/readme">How it is generated</a>.</sub></p>

<p>
<a href="mailto:yusuf.a.guenena@gmail.com">Email</a> &nbsp;·&nbsp;
<a href="https://www.linkedin.com/in/yusuf-guenena/">LinkedIn</a> &nbsp;·&nbsp;
<a href="https://github.com/yusufdxb">GitHub</a>
</p>

</div>
