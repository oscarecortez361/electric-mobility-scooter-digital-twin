# System Architecture

## Purpose

The project separates the physical scooter concept from the software decision layer so that behavior can be tested safely before any real actuator is connected.

## Core components

1. **Telemetry layer** — battery percentage, speed, motor temperature, obstacle distance, and future sensor inputs.
2. **Digital twin state** — a software representation of the scooter at a point in time.
3. **Safety and control layer** — evaluates the twin state and produces actions such as continue, slow, stop, or return/charge.
4. **Visualization layer** — future dashboard for current status, warnings, trends, and event history.
5. **Hardware bridge** — future Raspberry Pi or microcontroller connection after software validation.

## Design principle

The digital twin should be useful even before hardware integration. Simulated faults allow repeatable testing of scenarios such as low battery, overheating, and sudden obstacles.

## Future AI components

- anomaly detection on motor and battery telemetry
- predictive maintenance
- battery range estimation
- route-aware energy planning
- adaptive speed recommendations
- confidence-aware safety escalation

## Safety boundary

The current repository is a simulation and educational prototype. No code in the initial phase commands a physical scooter motor, brake, or steering system.
