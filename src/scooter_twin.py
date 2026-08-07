"""Starter digital twin simulator for an electric mobility scooter.

This software-only prototype intentionally does not control real hardware.
It generates simulated telemetry and applies simple safety rules.
"""

from dataclasses import dataclass
from random import uniform
from time import sleep


@dataclass
class ScooterState:
    battery_pct: float
    speed_mph: float
    motor_temp_f: float
    obstacle_distance_ft: float


def safety_action(state: ScooterState) -> str:
    if state.obstacle_distance_ft < 2.0:
        return "STOP: obstacle too close"
    if state.motor_temp_f >= 190:
        return "STOP: motor temperature critical"
    if state.motor_temp_f >= 170:
        return "SLOW: motor temperature high"
    if state.battery_pct <= 15:
        return "RETURN/CHARGE: battery low"
    return "CONTINUE"


def simulate_state(previous_battery: float) -> ScooterState:
    return ScooterState(
        battery_pct=max(0.0, previous_battery - uniform(0.2, 1.2)),
        speed_mph=uniform(0.0, 8.0),
        motor_temp_f=uniform(110.0, 185.0),
        obstacle_distance_ft=uniform(1.0, 20.0),
    )


def main() -> None:
    battery = 100.0
    print("Electric Mobility Scooter Digital Twin")
    print("Software simulation only - no physical control output.\n")

    for step in range(1, 16):
        state = simulate_state(battery)
        battery = state.battery_pct
        action = safety_action(state)

        print(
            f"Step {step:02d} | battery={state.battery_pct:5.1f}% | "
            f"speed={state.speed_mph:4.1f} mph | "
            f"motor={state.motor_temp_f:5.1f} F | "
            f"obstacle={state.obstacle_distance_ft:4.1f} ft | {action}"
        )
        sleep(0.15)


if __name__ == "__main__":
    main()
