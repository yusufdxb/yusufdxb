# Yusuf Guenena

**I build the reliability layer for learned robot systems.**

M.S. Robotics Engineering, Wayne State University. ROS 2, C++, sim-to-real on quadrupeds.

Learned policies fail quietly. A locomotion network saturates, a perception model stops perceiving, a simulator's counterfactual stops being faithful, and nothing in the stack raises its hand. Most of my work is the layer that notices: fault detection and recovery on a live robot, deploy-time parity gates, out-of-distribution monitoring on policy internals, and acceptance evidence you can re-verify a year later. Each repo states what has actually been run on hardware and what has not.

[![Email](https://img.shields.io/badge/Email-yusuf.a.guenena%40gmail.com-EA4335?logo=gmail&logoColor=white)](mailto:yusuf.a.guenena@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-yusufdxb-181717?logo=github&logoColor=white)](https://github.com/yusufdxb)

---

## Featured

### 1. [helix](https://github.com/yusufdxb/helix) &nbsp;·&nbsp; [▶ Demo](https://youtu.be/PbKXB91-NSY)

Self-healing runtime for ROS 2 robots, built as a four-tier loop: **Sense** (lifecycle nodes emit structured `FaultEvent`s from a rolling Z-score detector, heartbeat monitor, and log parser), **Diagnose** (deterministic rules produce `RecoveryHint`s), **Recover** (a single `cmd_vel` publisher behind a strict allowlist and cooldown), and **Explain** (an advisory local LLM, never on the safety-critical path).

Validated on a live Unitree GO2 and Jetson Orin NX across eight hardware lab sessions. The Session 8 bag runs the loop end to end: 30 anomalies into 14 recovery hints into 14 recovery actions. Hot-path sensing nodes are being ported from Python to C++ so the stack can share the Jetson with Nav2 and perception; the anomaly detector port has landed and is launch-gated behind a hardware parity re-confirmation.

Open limitation, stated in the repo: `/helix/cmd_vel` currently has no downstream subscribers, so `STOP_AND_HOLD` is a void publish. Closing the recovery loop physically, through a `twist_mux` fallback, is the next hardware task.

### 2. [go2-phoenix](https://github.com/yusufdxb/go2-phoenix) &nbsp;·&nbsp; [▶ Demo](https://youtu.be/Nu0oWyJJbEM)

Closed-loop sim-to-real learning for the GO2. A locomotion policy trains in Isaac Lab, exports to ONNX through a torch/onnxruntime **parity gate** that refuses to ship a checkpoint whose deploy-time numerics drift outside tolerance, then runs behind a **fail-closed** ROS 2 safety layer with a shared slew cap. Failures captured on hardware replay in simulation under randomized physics and feed a fine-tuning curriculum.

The deploy stack has run end to end on the real robot, on the Jetson. That live run is also what surfaced the current blocker: per-step slew-rate saturation the policy has not yet cleared on a stand.

Current boundary: **on-robot locomotion validation (Gate 7) is open.** An export audit found that pre-audit checkpoints silently dropped observation normalization, so every checkpoint owes a re-export and a fresh parity check before the retry. The adaptation loop has not closed once on real failure data. [`EVIDENCE.md`](https://github.com/yusufdxb/go2-phoenix/blob/main/EVIDENCE.md) is the verified / inferred / not-validated ledger.

### 3. [ivf](https://github.com/yusufdxb/ivf)

Offline acceptance and evidence for simulator experiments. You declare what "unchanged behavior" means in YAML (which signals, which tolerances and units, which controls must hold, what the minimum sample is), and IVF checks the experiment was even valid before letting any result decide a verdict, then seals manifest, signals, reasoning, provenance, and per-file SHA-256 digests into one evidence bundle.

The flagship case is a real PhysX versus Newton/MJWarp cart-pole comparison whose recorded verdict is `FAIL`, with 22 validity checks (18 pass, 3 unverifiable, 1 not applicable, 0 failed). Anyone can re-verify the shipped bundle from its seal, CPU only, without a GPU or a simulator install. IVF is not a benchmark: it does not measure throughput and does not designate a reference engine.

### 4. [supercombo-blindspot](https://github.com/yusufdxb/supercombo-blindspot) &nbsp;·&nbsp; [▶ Demo](https://youtu.be/tnM18XGbNMY)

Distribution-shift teardown of the neural network that drives openpilot, a production L2 system on public roads. One question: presented with input outside its training distribution, does it fail conspicuously or silently?

Silently. Built on a parity-controlled reimplementation of v0.9.7 inference that agrees with comma's own reference output on 100% of 1159 real frames within ±0.5 m/s², so the negative result is attributable to the model and not the harness. Under shift, 8 of 10 tracked output readouts go near-constant, the recurrent state contracts to a point, and the exported uncertainty heads never leave their nominal real-driving range. An internal recurrent signal does encode the failure and is recoverable, but the model never exposes it. Writeup drafted, not submitted.

### 5. [BlackBoxRS](https://github.com/yusufdxb/BlackBoxRS)

Incident intelligence for ROS 2 robots. A daemon watches the graph and host; when a failure fires, one command builds a reproducible incident bundle: timeline, raw evidence, config and version signatures, a likely-cause narrative where every claim links to the evidence file backing it, and a prevention rule you can adopt so the same failure blocks the next launch.

The offline replay path runs against a genuine `rosbag2` recording from a physical GO2 (about 94k messages over 330 seconds). Played untouched it replays clean with zero anomalies, which is the point: the detectors are not inventing failures. Inject a pose dropout into that real window and the detector finds it from bag timing alone. Honest boundary: this has not run in a closed control loop on a live robot.

---

## Active M.S. research

### [GO2-seeing-eye-dog](https://github.com/yusufdxb/GO2-seeing-eye-dog)

A guide dog has to be summonable. If the handler puts the harness down and later wants the dog back, the dog finds them by voice, not by a phone screen. This repository closes the **recall** half of that interaction on real hardware: a four-channel mic array gives a GCC-PHAT bearing, Whisper parses the command, YOLOv8 plus depth back-projection gives 3D person poses, and a fused audio-visual score must hold across five consecutive frames before the target locks and publishes a Nav2 goal.

Scope, stated plainly: this recalls the robot, it does not guide the user anywhere. Safety alerts are advisory and do not yet hard-gate motion. 32 unit tests pass; **nothing here has a measured accuracy or latency result on the real robot yet**, and end-to-end recall on hardware is the open item.

---

## Reliability stack

| Project | What it does |
|---|---|
| **[policy-health-monitor](https://github.com/yusufdxb/policy-health-monitor)** | Runtime OOD monitoring on a learned policy's internals, arbitrated into one health status with a safe-fallback layer. ROS 2 with a C++ managed-lifecycle detector node. Synthetic streams only so far, no hardware validation. |
| **[riskgraph-go2](https://github.com/yusufdxb/riskgraph-go2)** | Persistent route-risk memory: the robot remembers where things went wrong and scores safer paths through an explainable Nav2 overlay. Hardware-unverified. |
| **[come-here](https://github.com/yusufdxb/come-here)** | Audio-visual approach on the GO2: hear the call, rotate toward it, find the person, walk to them. |
| **[physx-newton-bench](https://github.com/yusufdxb/physx-newton-bench)** | PhysX versus Newton/MJWarp in Isaac Lab: throughput scaling, per-process VRAM, 10-seed learning curves, and an open-loop dynamics-equivalence probe. |
| **[openvocab-tsdf](https://github.com/yusufdxb/openvocab-tsdf)** | GPU-accelerated open-vocabulary 3D mapping: build a TSDF, query it in natural language. |

---

## Falsified hypotheses

Two projects exist because the idea did not survive contact with measurement. Both are kept public with their full evidence trail.

**[ipfd](https://github.com/yusufdxb/ipfd)** asked whether you can rewind a simulator to step `t`, re-run it, and treat that branch as a stand-in for what the uninterrupted episode would have done. On a contact-rich Isaac Lab lift task, restored branches that matched the reference on exposed simulator state, on the immediate policy observation, and on the exact replayed action sequence still reached a different terminal outcome. The preregistered positive control needed to cut that disagreement by 50% and cut it by 38.9%, so the stopping rule fired. "Save the state, restore it, try again" sits unexamined under a lot of simulation tooling; here it is measured directly, and equality at the restore boundary does not imply equality of the outcome.

**[ashfall](https://github.com/yusufdxb/ashfall)** asked whether fine-tuning a locomotion policy on a curriculum enriched with its own failures improves robustness. A single seed suggested a +5.1 pp lift. Paired across 11 seeds and scored with an exact sign-flip permutation test, the effect disappears and adding seeds moved the p-value away from significance. The null verdict holds on both terrains, and the p-floor column shows the sample size was never the limitation. What survives is the machinery: a 6-mode failure detector at 18/18 with zero cross-fires, the paired evaluation framework, and a seed-propagation bug fixed upstream.

---

## Stack

| | |
|---|---|
| **Robotics** | ROS 2 (Humble), Nav2, lifecycle nodes, tf2, ros2_control, SLAM Toolbox, Gazebo, Isaac Lab, Isaac Sim |
| **Learning** | PyTorch, PPO / RL, sim-to-real, ONNX + parity gating, out-of-distribution detection |
| **Perception** | YOLOv8, OpenCV, RealSense D435i, Whisper ASR, GCC-PHAT, open-vocab 3D mapping |
| **Systems** | C++17, Python 3, CMake, colcon, Docker, Jetson deployment, Qt 6, Arduino |

---

[yusuf.a.guenena@gmail.com](mailto:yusuf.a.guenena@gmail.com) &nbsp;·&nbsp; [github.com/yusufdxb](https://github.com/yusufdxb)
