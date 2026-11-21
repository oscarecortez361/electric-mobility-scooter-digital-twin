# Byte Bots — ITAI 4376 Milestone Index

**Project:** Voice-Controlled Assistive Wheelchair/Scooter (Scaled Proof of Concept)  
**Course:** ITAI 4376 — AI Controls for Robotics  
**Current team:** Oscar Cortez and Andrew Kuruvilla

> This is a progress index of the Byte Bots physical model-robot workstream. It does not replace the original submitted milestone documents. The existing electric-mobility-scooter digital-twin simulation remains a separate software workstream within this portfolio.

| Milestone | Scope | Record status |
|---|---|---|
| 0 — Team formation | Team roles, Option C student-proposed project; initial membership: Anthony Randall, Andrew Kuruvilla, Oscar Cortez | Coursework document exists; original submission not yet attached here |
| 1 — Charter and requirements | Problem, stakeholder, measurable acceptance criteria, risk identification | Charter exists; original submission not yet attached here |
| 2 — Feasibility and direction | Scaled robot feasibility, voice-command concept, stakeholder alignment, safety planning | Revised submission dated Sep. 25, 2026; original file not yet attached here |
| 3 — Midterm project blueprint | Voice-controlled scaled wheelchair/scooter design and planned integration | Blueprint prepared Oct. 22, 2026; original file not yet attached here |
| 4 — Integration progress | UART/shield troubleshooting and hardware handover | Documented historically; consult original course submission |\n| 5 — Integration and test review | Nov. 6 unpowered STOP/heartbeat/ultrasonic observations | Review written Nov. 9; formal acceptance incomplete |\n| Final panel preparation | Later November floor-trial recordings, demo and fallback plan | Showcase and review materials prepared; Canvas submission not verified |

## October 30–31, 2026: bench-testing milestone

- Re-imaged Raspberry Pi 5 with Raspberry Pi OS (64-bit); enabled SSH and connected to ELEGOO UNO over USB serial.
- Verified the CH340 adapter and bidirectional communication at **9600 baud**.
- Replaced the Arduino's simple echo firmware with official **ELEGOO Smart Robot Car V4.0 firmware v2.1.2**.
- Installed required Arduino build dependencies; switching **FastLED 3.10.8 → 3.10.3** resolved a Servo/FastLED linker conflict.
- Confirmed official firmware startup message; received sensor-status response `{1_true}` and STOP acknowledgement `{2_ok}`.
- Observed short, timed **forward, backward, left, and right** bench movement and stopping, with all four wheels lifted off the ground.

See [Hardware Recovery and Bench-Test Log](Byte_Bots_Hardware_Test_Log_2026-10-30_31.md) for observations and limitations.

## Contributions and attribution

- **Oscar Cortez:** October 30–31 hands-on Raspberry Pi setup, serial troubleshooting, firmware installation and elevated-wheel motor tests.
- **Andrew Kuruvilla:** Remaining team member. This entry does not attribute these particular bench tests to Andrew.
- **Anthony Randall:** Earlier chassis/build/integration work and hardware handover before leaving the team.

The ELEGOO firmware is the **manufacturer's code**, not original Byte Bots software.

## November testing: progress and evidence limits

- **Nov. 4:** A controlled five-word recognition experiment improved from 33/100 to 100/100 after adding a recording cue. This is not final moving-control acceptance.
- **Nov. 6:** Serial STOP acknowledgement `{BB_ok}`, heartbeat-to-`LINK_LOST`, `DISARMED` rejection, and ultrasonic BLOCK/ALLOW dry-run outcomes were documented with safety limitations. Unexpected wheel movement during battery disconnection and a possible ultrasonic false-clear remained findings.
- **Later November:** Oscar conducted seven recorded floor-trial clips and reports tests using battery and cord-assisted power, external network access, and a direct local laptop-to-Pi connection without external Wi-Fi/internet. Those observations do not by themselves establish a fully controlled, instrumented acceptance matrix.

See the [stand-alone professional Byte Bots write-up](README.md) for the system architecture, actual results, and future improvements.

## Still unverified / unfinished

Formal measured speech-to-wheel latency; repeated powered voice STOP trials; independent physical emergency cutoff; bounded physical motor stop under link loss; sensor calibration; full blueprint repeatability/endurance scenarios; frozen release and synchronized command-to-motion proof. The local wireless connection does not require internet but uses the Pi's own Wi-Fi radio. **No human-occupied mobility-device testing is supported by these results.**

## Evidence/privacy

Preserve original milestone submissions, approved copies, raw console outputs, and dated screenshots. Avoid publishing credentials, private Wi-Fi details, student IDs, or private stakeholder contacts.
