<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/hero-dark.webp">
  <img src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/hero-light.webp" width="760" alt="A Unitree GO2 quadruped robot drawn as a field of fine particles.">
</picture>

<h1>Yusuf Guenena</h1>

<p><strong>I build the reliability layer for learned robot systems.</strong></p>

<p>Robotics &nbsp;·&nbsp; Embodied AI &nbsp;·&nbsp; Reliability</p>

</div>

<br>

I work on learned robot systems that need to fail safely, recover cleanly, and produce evidence you can trust. My work spans sim-to-real locomotion, runtime fault detection, policy monitoring, incident reconstruction, and assistive autonomy.

M.S. Robotics Engineering at Wayne State University. Most of the work here currently runs on a Unitree GO2 EDU and Jetson Orin NX, with hardware and simulation claims kept deliberately separate.

---

## Selected work

### HELIX

Self-healing runtime for ROS 2 robots that detects faults, holds the system safe, and coordinates recovery.

**8 live GO2 + Jetson sessions · 30 anomalies · 14 recovery actions**

`ROS 2 · C++ · fault recovery`

[Repository](https://github.com/yusufdxb/helix) · [Demo](https://youtu.be/PbKXB91-NSY)

<sub>Actuation closure in progress.</sub>

### GO2-Phoenix

Sim-to-real locomotion pipeline with parity-gated deployment and fail-closed safety.

**32/32 simulated stand successes · ONNX deploy parity enforced**

`Isaac Lab · PPO · ONNX · ROS 2`

[Repository](https://github.com/yusufdxb/go2-phoenix) · [Evidence](https://github.com/yusufdxb/go2-phoenix/blob/main/EVIDENCE.md)

<sub>On-robot locomotion validation in progress.</sub>

### supercombo-blindspot

Failure-awareness study of openpilot's driving model under distribution shift.

**1159-frame parity-controlled reproduction · shifted inputs expose silent internal collapse**

`ONNX Runtime · CARLA · OOD detection`

[Repository](https://github.com/yusufdxb/supercombo-blindspot) · [Demo](https://youtu.be/tnM18XGbNMY)

---

## GO2 systems

**[GO2 Seeing-Eye Dog](https://github.com/yusufdxb/GO2-seeing-eye-dog)**  
Voice recall and caller localisation.  
`ROS 2 · GCC-PHAT · Whisper · YOLOv8`

**[Come Here](https://github.com/yusufdxb/come-here)**  
Voice-triggered caller approach.  
`hardware: hear + rotate`

**[RiskGraph-GO2](https://github.com/yusufdxb/riskgraph-go2)**  
Route-risk memory and safer-route scoring.  
`111 tests · hardware validation pending`

**[GO2 Semantic Nav](https://github.com/yusufdxb/go2-semantic-nav)**  
Language-grounded 3D navigation.  
`on-robot evaluation pending`

**[GO2 Omniverse](https://github.com/yusufdxb/go2_omniverse)**  
Isaac Sim / ROS 2 digital twin.  
`upstream contribution merged`

**[go2-audio](https://github.com/yusufdxb/go2-audio)**  
Real GO2 microphone capture over WebRTC.

---

## Reliability & research

**[policy-health-monitor](https://github.com/yusufdxb/policy-health-monitor)**  
Internal-activation monitoring for learned policies.  
`295 tests · device evaluation pending`

**[BlackBoxRS](https://github.com/yusufdxb/BlackBoxRS)**  
Reproducible robot incident bundles and replay.  
`547 tests · real GO2 bag evidence`

**[IVF](https://github.com/yusufdxb/ivf)**  
Long-lived simulator acceptance evidence and replay verification.

**[IPFD](https://github.com/yusufdxb/ipfd)**  
Counterfactual simulator rewind study.  
`preregistered null result`

**[Ashfall](https://github.com/yusufdxb/ashfall)**  
Locomotion failure fine-tuning study.  
`paired 11-seed null result`

---

## Other builds

**[openvocab-tsdf](https://github.com/yusufdxb/openvocab-tsdf)** GPU open-vocabulary 3D mapping  
**[physx-newton-bench](https://github.com/yusufdxb/physx-newton-bench)** PhysX versus Newton backend benchmark  
**[inspectnet-cx](https://github.com/yusufdxb/inspectnet-cx)** industrial anomaly inspection on MVTec AD  
**[go2-jetson-setup-guide](https://github.com/yusufdxb/go2-jetson-setup-guide)** Jetson bring-up on a GO2  
**[RADAR-Telepresence-Robot](https://github.com/yusufdxb/RADAR-Telepresence-Robot)** medical telepresence with a Qt 6 operator console  
**[TicTacToe-3link-robot](https://github.com/yusufdxb/TicTacToe-3link-robot)** 3-DOF arm with closed-form IK

---

## Stack

| | |
|---|---|
| **Robotics** | ROS 2 · Isaac Sim/Lab · Nav2 · RTAB-Map |
| **Learning** | PyTorch · PPO · ONNX · OOD detection · VLMs |
| **Systems** | C++ · Python · Linux · Docker |
| **Hardware** | Unitree GO2 EDU · Jetson Orin NX · RealSense D435i |

---

<div align="center">

<p><a href="mailto:yusuf.a.guenena@gmail.com">Email</a> &nbsp;·&nbsp; <a href="https://www.linkedin.com/in/yusuf-guenena/">LinkedIn</a> &nbsp;·&nbsp; <a href="https://github.com/yusufdxb">GitHub</a></p>

</div>
