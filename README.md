# Electric Mobility Scooter Digital Twin & AI Control System

> **Featured 2026 hardware showcase:** [Byte Bots — Voice-Controlled Robotic Mobility](docs/byte-bots/README.md). A separate hands-on ITAI 4376 scaled robot project featuring a Raspberry Pi 5, local Vosk speech recognition, Arduino/USB serial control, and November floor-trial documentation. **Not a passenger-carrying or safety-certified mobility device.**

A portfolio and capstone-style project exploring how a digital twin can represent, monitor, and safely assist an electric mobility scooter. The project combines simulated telemetry, rule-based control, AI-ready decision logic, and a path toward future hardware integration.

## Project goals

- Model the scooter as a live digital twin with battery, speed, motor temperature, and obstacle-distance telemetry.
- Detect unsafe operating conditions and generate clear control actions.
- Simulate low-battery, overheating, and obstacle scenarios before connecting to real hardware.
- Create a foundation for future autonomous assistance, predictive maintenance, and route-aware control.

## Current prototype

The first version is software-only and uses simulated sensor data. This keeps development safe and repeatable while the control logic is tested.

```text
Sensors / simulated telemetry
          |
          v
  Digital Twin State
          |
          v
 Safety + Control Logic
          |
          v
 Stop / Slow / Continue / Return recommendation
          |
          v
 Dashboard + event log
```

## Repository structure

```text
.
├── README.md
├── data/
│   └── sample_telemetry.csv
├── docs/
│   └── ARCHITECTURE.md
└── src/
    └── scooter_twin.py
```

## Safety logic in the starter build

- **Obstacle too close:** stop.
- **Motor temperature high:** reduce speed or stop if critical.
- **Battery low:** recommend return or charging.
- **Normal conditions:** continue operation.

## Run the simulator

```bash
python src/scooter_twin.py
```

The starter code uses only the Python standard library.

## Roadmap

1. Simulated telemetry and safety rules.
2. Live dashboard and historical logging.
3. Machine-learning based anomaly detection and predictive maintenance.
4. Route and battery-range estimation.
5. Raspberry Pi or microcontroller sensor bridge.
6. Optional real-scooter integration after software validation and hardware safety review.

## Project status

**Phase 1: active prototype.** The repository currently focuses on the digital twin model and safe control logic before any physical scooter control is attempted.

## Author

Oscar Cortez  
AI and Robotics Engineering

---

## Physical model-robot workstream — Byte Bots (ITAI 4376)

Byte Bots is **separate from the digital-twin simulator documented above**. Oscar Cortez and Andrew Kuruvilla developed a scaled ELEGOO robot with Raspberry Pi 5, Vosk, and Arduino UNO integration for a voice-assisted mobility proof of concept. Earlier bench-testing notes remain linked below; the new stand-alone showcase covers the later November floor trials, battery/cord configurations, local Pi-to-laptop connectivity, engineering lessons, and unclosed safety tests.

**[Read the full Byte Bots professional showcase →](docs/byte-bots/README.md)**

- [Byte Bots milestone index](docs/byte-bots/Byte_Bots_Milestone_Index.md)
- [October 30–31 hardware recovery and bench-test log](docs/byte-bots/Byte_Bots_Hardware_Test_Log_2026-10-30_31.md)

**Attribution:** Oscar Cortez — project management, safety, documentation, and hands-on testing; Andrew Kuruvilla — team software/voice integration workstream; Anthony Randall — earlier assembly and integration contributions. ELEGOO firmware and Vosk are third-party technologies.

> **Safety:** Classroom model only. Formal powered STOP, emergency cutoff, obstacle calibration, and full-system acceptance remain incomplete. No human mobility claims.
