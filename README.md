<div align="center">

<img src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/hero.gif" width="900" alt="LiDAR-style point cloud reconstruction of a Unitree GO2 EDU quadruped, with a telemetry panel listing compute, middleware, simulation and navigation stack. Yusuf Guenena, robotics, embodied AI, autonomy.">

</div>

<br>

### <samp>02 &nbsp;//&nbsp; CURRENT MISSION</samp>

**Reliable autonomy for quadruped robots working around people.**

Learned policies fail quietly. A locomotion network saturates, a perception model stops perceiving, a simulator's counterfactual stops being faithful, and nothing in the stack raises its hand. Most of what I build is the layer that notices: fault detection and recovery on a live robot, deploy-time parity gates, out-of-distribution monitoring on policy internals, and acceptance evidence that can be re-verified a year later.

The work runs on a Unitree GO2 EDU with a Jetson Orin NX. Every repository below states what has actually run on hardware and what has not, because that distinction is the whole job.

---

### <samp>03 &nbsp;//&nbsp; FLAGSHIP SYSTEMS</samp>

#### <samp>helix &nbsp;·&nbsp; SELF-HEALING ROS 2 RUNTIME</samp>

A four-tier loop on a live ROS 2 graph. Lifecycle nodes emit structured fault events from a rolling Z-score detector, a heartbeat monitor and a log parser. Deterministic rules turn those into recovery hints. One publisher behind a strict allowlist and a cooldown owns the response. An advisory local LLM explains it afterwards, never on the safety-critical path.

```
STACK      ROS 2 Humble · C++17 · lifecycle nodes · Orin NX
SENSE      VERIFIED  8 live GO2 lab sessions, April 2026
DIAGNOSE   VERIFIED  session 8: 30 anomalies, 14 hints, 14 actions
RECOVER    OPEN      /helix/cmd_vel has no subscriber yet
C++ PORT   PARTIAL   -56% RSS, -60% CPU, gated off by default
```

[**Open helix**](https://github.com/yusufdxb/helix) &nbsp;·&nbsp; [demo video](https://youtu.be/PbKXB91-NSY) &nbsp;·&nbsp; [status table](https://github.com/yusufdxb/helix#status)

#### <samp>go2-phoenix &nbsp;·&nbsp; SIM-TO-REAL LOCOMOTION RELIABILITY</samp>

Isaac Lab to ONNX to ROS 2 to GO2, closed. A locomotion policy trains in simulation and exports through a torch/onnxruntime parity gate that refuses to ship a checkpoint whose deploy-time numerics drift outside tolerance, then runs behind a fail-closed safety layer with a shared slew cap. Failures captured on hardware replay in simulation under randomised physics.

```
STACK      Isaac Lab · PPO · ONNX · ROS 2 · Orin NX
SIM        VERIFIED  stand-v3-h25: 32/32 success, 3.30% slew
POLICY     VERIFIED  parity gate blocks a drifting export
SAFETY     VERIFIED  fail-closed, shared slew cap on deploy
HARDWARE   OPEN      Gate 7 on-robot locomotion not yet passed
LOOP       OPEN      no hardware failure capture has fed it yet
```

[**Open go2-phoenix**](https://github.com/yusufdxb/go2-phoenix) &nbsp;·&nbsp; [demo video](https://youtu.be/Nu0oWyJJbEM) &nbsp;·&nbsp; [EVIDENCE.md](https://github.com/yusufdxb/go2-phoenix/blob/main/EVIDENCE.md)

#### <samp>GO2-seeing-eye-dog &nbsp;·&nbsp; VOICE RECALL FOR AN ASSISTIVE QUADRUPED</samp>

A guide dog has to be summonable. Put the harness down, sit on a bench, call the dog back: by voice, not by an app. A four-channel mic array gives a GCC-PHAT bearing, Whisper parses the command, YOLOv8 plus depth back-projection gives 3D person poses, and a fused audio-visual score must hold across five consecutive frames before the target locks and a Nav2 goal is published.

```
STACK      ROS 2 Humble · GCC-PHAT · Whisper · YOLOv8 · D435i
SCOPE      recall only. It does not guide the user anywhere
SAFETY     alerts are advisory. They do not hard-gate motion
TESTS      VERIFIED  32 unit tests pass
HARDWARE   OPEN      end-to-end recall on the robot is pending
MEASURED   nothing yet. Quoted values are defaults, not results
```

[**Open GO2-seeing-eye-dog**](https://github.com/yusufdxb/GO2-seeing-eye-dog)

#### <samp>policy-health-monitor &nbsp;·&nbsp; RUNTIME OOD ON POLICY INTERNALS</samp>

Watch a learned policy's own internal activations rather than its outputs, run several detectors over them, and arbitrate worst-wins into a single health status with a safe-fallback layer underneath. Written as a C++ managed lifecycle node so it can be brought up and torn down with the rest of the graph.

```
STACK      ROS 2 · C++ managed lifecycle · worst-wins arbiter
TESTS      VERIFIED  295 pass, no ROS install required
DETECTORS  synthetic streams only, not yet a real policy
HARDWARE   OPEN      on-device latency and FPR not measured
```

[**Open policy-health-monitor**](https://github.com/yusufdxb/policy-health-monitor)

#### <samp>BlackBoxRS &nbsp;·&nbsp; FLIGHT RECORDER AND FAILURE FORENSICS</samp>

A daemon watches the ROS 2 graph and the host. When a failure fires, one command builds a reproducible incident bundle: a timeline, the raw evidence, config and version signatures, a likely-cause narrative grounded in that evidence, and a preflight rule you can adopt so the same failure blocks the next launch instead of recurring on another robot two weeks later.

```
STACK      ROS 2 Humble · Python 3.10-3.12 · Docker CI
TESTS      VERIFIED  547 pass, 2 gated skips
EVIDENCE   VERIFIED  incident bundle built from a real GO2 bag
LIVE       OPEN      offline replay, not yet an onboard capture
```

[**Open BlackBoxRS**](https://github.com/yusufdxb/BlackBoxRS)

#### <samp>supercombo-blindspot &nbsp;·&nbsp; DOES A SHIPPED DRIVING MODEL KNOW IT IS BLIND</samp>

A distribution-shift teardown of the neural network that drives openpilot, an L2 driver-assistance system deployed on public roads. One question: presented with input outside its training distribution, does it fail conspicuously or silently? An internal recurrent signal does encode the failure and is recoverable. The model never exposes it.

```
ANSWER     silently
PARITY     VERIFIED  100% of 1159 frames within ±0.5 m/s²
COLLAPSE   VERIFIED  8/10 tracked readouts fall below 1% of real
BLINDNESS  VERIFIED  0/219 shifted frames exceed the real p95
REPLICATED on v0.9.6, which fails differently: not a freeze but
           chaotic amplification, and the monitor does not carry
WRITEUP    drafted, not submitted
```

[**Open supercombo-blindspot**](https://github.com/yusufdxb/supercombo-blindspot) &nbsp;·&nbsp; [demo video](https://youtu.be/tnM18XGbNMY)

---

<div align="center">

<img src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/system-map.png" width="900" alt="System map: six layers from perception down through reasoning, planning, safety, control and the GO2 platform, with the repository that owns each layer, and a reliability return path from the platform back up to the safety layer.">

</div>

#### <samp>MORE SYSTEMS ON THE SAME STACK</samp>

| Repository | What it does | Where it stands |
|---|---|---|
| [**ivf**](https://github.com/yusufdxb/ivf) | Sealed, re-verifiable acceptance evidence for simulator experiments. Its flagship bundle records `FAIL` on a real PhysX versus Newton cart-pole, over 22 validity checks: 18 pass, 3 unverifiable, 1 not applicable, 0 failed | 265 tests pass |
| [**riskgraph-go2**](https://github.com/yusufdxb/riskgraph-go2) | Route-risk memory and explainable safer-route scoring for Nav2 | 111 tests, hardware-unverified |
| [**go2-semantic-nav**](https://github.com/yusufdxb/go2-semantic-nav) | Open-vocabulary 3D scene graph driving a language-grounded Nav2 overlay | on-robot eval pending |
| [**come-here**](https://github.com/yusufdxb/come-here) | Hears "come here", localises the voice, turns, walks to the person | hear and rotate on hardware |
| [**openvocab-tsdf**](https://github.com/yusufdxb/openvocab-tsdf) | GPU open-vocabulary 3D mapping, queried in natural language | library |
| [**go2_omniverse**](https://github.com/yusufdxb/go2_omniverse) | Isaac Sim 5.0 and ROS 2 Jazzy port, plus an IMU-driven digital twin | [merged upstream as #84](https://github.com/abizovnuralem/go2_omniverse/pull/84) |
| [**physx-newton-bench**](https://github.com/yusufdxb/physx-newton-bench) | PhysX versus Newton/MJWarp in Isaac Lab: throughput, VRAM, 10-seed curves | complete |
| [**ros2-go2-nav2-yolo**](https://github.com/yusufdxb/ros2-go2-nav2-yolo) | Gazebo autonomy stack with the DDS, TF and SLAM integration bugs fixed | sim, plus a real YOLO path |
| [**go2-audio**](https://github.com/yusufdxb/go2-audio) | Real microphone audio off a GO2 over WebRTC, because the DDS topic is broken | tool |
| [**inspectnet-cx**](https://github.com/yusufdxb/inspectnet-cx) | Reproducible industrial anomaly-inspection scaffold on an MVTec AD baseline | study |

**Earlier hardware.** [RADAR-Telepresence-Robot](https://github.com/yusufdxb/RADAR-Telepresence-Robot), medical telepresence with teleop, pan-tilt video and live SpO₂ in one Qt 6 console &nbsp;·&nbsp; [TicTacToe-3link-robot](https://github.com/yusufdxb/TicTacToe-3link-robot), a 3-DOF arm solving closed-form IK against a minimax opponent &nbsp;·&nbsp; [EcoSort-bin](https://github.com/yusufdxb/EcoSort-bin), weight, colour, IR and ultrasonic fusion on an Arduino &nbsp;·&nbsp; [go2-jetson-setup-guide](https://github.com/yusufdxb/go2-jetson-setup-guide), bringing a Jetson up on a GO2 start to finish

---

### <samp>05 &nbsp;//&nbsp; RESEARCH</samp>

```
PUBLISHED    none yet
IN REVIEW    none. Nothing here is under submission

IN DEVELOPMENT
  M.S. thesis           assistive quadruped autonomy,
                        private until defense
  supercombo-blindspot  teardown written up, not submitted

ARCHIVED NULL RESULTS   public, with the evidence trail
  ipfd      Rewind a simulator, re-run, treat the branch as
            what the episode would have done. The
            preregistered control needed a 50% cut in
            disagreement and delivered 38.9%, so the
            stopping rule fired
  ashfall   Fine-tune a locomotion policy on its own
            failures. One seed suggested +5.1 pp. Paired
            across 11 seeds with an exact sign-flip
            permutation test, the effect is null

MERGED UPSTREAM
  go2_omniverse #84     Ubuntu 24.04 / Isaac Sim 5.0 / Jazzy
```

Both null results stay public because the measurement is the contribution. [ipfd](https://github.com/yusufdxb/ipfd) &nbsp;·&nbsp; [ashfall](https://github.com/yusufdxb/ashfall)

---

### <samp>06 &nbsp;//&nbsp; STACK</samp>

| Area | Tools |
|---|---|
| **ROBOTICS** | ROS 2 Humble · Nav2 · lifecycle nodes · tf2 · ros2_control · SLAM Toolbox · RTAB-Map · Gazebo · Isaac Sim · Isaac Lab |
| **LEARNING** | PyTorch · PPO and reinforcement learning · sim-to-real · ONNX with parity gating · out-of-distribution detection · VLMs |
| **PERCEPTION** | YOLOv8 · OpenCV · RealSense D435i · Whisper ASR · GCC-PHAT · open-vocabulary 3D mapping |
| **RELIABILITY** | fault detection and recovery · incident forensics · fail-closed envelopes · acceptance evidence · paired statistical evaluation |
| **SYSTEMS** | C++17 · Python 3 · MATLAB · Linux · Docker · CMake · colcon · Qt 6 |
| **HARDWARE** | Unitree GO2 EDU · Jetson Orin NX · Arduino · Raspberry Pi · Fusion 360 |

---

<div align="center">

<img src="https://raw.githubusercontent.com/yusufdxb/yusufdxb/main/assets/readme/activity.png" width="900" alt="GitHub activity panel: total contributions, active days, longest streak and public repository count over the last twelve months, with a weekly contribution sparkline.">

</div>

---

### <samp>08 &nbsp;//&nbsp; CONTACT</samp>

[yusuf.a.guenena@gmail.com](mailto:yusuf.a.guenena@gmail.com) &nbsp;·&nbsp; [GitHub](https://github.com/yusufdxb) &nbsp;·&nbsp; [LinkedIn](https://www.linkedin.com/in/yusuf-guenena/)

<sub>The hero and the system map are interface graphics, not a live robot feed. The activity panel is real: it is regenerated from the GitHub contributions API by <a href="https://github.com/yusufdxb/yusufdxb/blob/main/.github/workflows/readme-activity.yml">a workflow in this repo</a>, with the raw response committed alongside it as <a href="https://github.com/yusufdxb/yusufdxb/blob/main/assets/readme/activity.json">activity.json</a>. Artwork generated by <a href="https://github.com/yusufdxb/yusufdxb/tree/main/tools/readme">tools/readme</a>.</sub>
