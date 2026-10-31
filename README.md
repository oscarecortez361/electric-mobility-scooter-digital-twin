# Electric Mobility Scooter Digital Twin & AI Control System

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

The original **electric-mobility-scooter digital twin** above remains a **software/simulation project**. A related but distinct hands-on classroom proof of concept is being documented here under **Byte Bots**: a *scaled ELEGOO Smart Robot Car V4.0*, controlled by a Raspberry Pi 5 over USB serial through an Arduino UNO. This is **not** a full-size wheelchair or a person-carrying mobility system.

**October 30–31, 2026 bench status:** ELEGOO firmware v2.1.2 uploaded; two-way Pi↔Arduino commands verified at 9600 baud; forward, reverse, left and right briefly observed with the wheels elevated, followed by stopping. Voice controls, lost-communication safeguards, measured stopping performance and floor tests are **not yet validated**.

- [ITAI 4376 Byte Bots milestone index](docs/byte-bots/Byte_Bots_Milestone_Index.md)
- [October 30–31 hardware recovery and bench-test log](docs/byte-bots/Byte_Bots_Hardware_Test_Log_2026-10-30_31.md)

**Team record:** Oscar Cortez and Andrew Kuruvilla remain on Byte Bots; Anthony Randall contributed earlier assembly/integration before departing. The October 30–31 at-home tests were performed by Oscar. The official ELEGOO firmware is manufacturer-authored.

> **Safety:** Scaled proof-of-concept only. No human-use, autonomous transport, or commercial assistive-device safety claims are made.
