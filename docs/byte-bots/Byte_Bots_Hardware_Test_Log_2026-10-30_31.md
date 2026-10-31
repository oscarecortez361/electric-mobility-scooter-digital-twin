# Byte Bots — Hardware Recovery and Bench-Test Log

**Course:** ITAI 4376 — AI Controls for Robotics  
**Project:** Voice-Controlled Assistive Wheelchair/Scooter — *scaled ELEGOO model robot only*  
**Test dates:** October 30–31, 2026 (evening/overnight)  
**Hands-on tests documented by:** Oscar Cortez  
**Current team:** Oscar Cortez and Andrew Kuruvilla

> These are informal elevated-wheel model-robot tests, **not** certification for human transport, a full-size wheelchair, or operation around people.

## Goal

Restore Raspberry Pi 5 → Arduino UNO → ELEGOO Smart Robot Car V4.0 serial control, confirm manufacturer firmware responses, and exercise five basic actions: forward, backward, left, right, STOP. Keep the classroom demonstration minimal.

## Hardware / software baseline

- Raspberry Pi 5, newly imaged Raspberry Pi OS 64-bit, SSH operational
- ELEGOO UNO R3-compatible Arduino board; **SmartCar-Shield-V1.1**; ELEGOO Smart Robot Car V4.0 with wheels raised
- CH340 USB adapter: `/dev/ttyUSB0` (Pi) / `COM5` (HP Windows laptop); serial at **9600 baud**
- PySerial **3.5**, Arduino IDE **2.3.10**, official ELEGOO Arduino firmware **v2.1.2**
- Arduino dependencies: FastLED **3.10.3**, IRremote **4.7.1**, MPU6050 **1.4.5**, Servo

## Test results

| Check | Direct observation | Finding |
|---|---|---|
| Raspberry Pi SSH + USB enumeration | Pi booted; SSH connected; CH340 enumerated with `lsusb`; `/dev/ttyUSB0` accessible to account in `dialout` | Passed |
| Pre-update listen-only test | Eight blank `b''` reads; no unsolicited data after reset at 9600 baud | No unsolicited serial message; not proof of failure |
| Pre-update Windows/Pi echo | `ECHO FROM CAR: {"TEST":"BYTEBOTS"}` on Pi after arbitrary input | Two-way echo confirmed |
| Arduino compile | Dependencies installed; `__vector_11` linker conflict with FastLED 3.10.8 and Servo; resolved on FastLED 3.10.3 | Passed |
| Firmware upload | Arduino IDE reported `Done uploading` | Passed |
| Firmware startup | `Smart Robot Car V4.0 - System Ready` | Passed |
| Status command | Request `{"N":23,"H":"1"}`; response `{1_true}` on both Windows and Pi | Command processing confirmed; sensor accuracy not measured |
| STOP command | Request `{"N":110,"H":"2"}`; response `{2_ok}` | STOP acknowledged; alone does not verify stopping dynamics |
| Forward | Timed wheels-up forward rotation, then stopped | Passed observed bench test |
| Backward | Timed wheels-up reverse rotation, then stopped | Passed observed bench test |
| Left / Right | Timed turns observed on raised wheels, then stopped | Passed observed bench tests |

### Commands and parameters

Status query: `{"N":23,"H":"1"}`  
STOP: `{"N":110,"H":"2"}`

Timed movement commands used **N=2**, speed **D2=90**, timer **T=350 ms** and direction codes:

| Direction | D1 |
|---|---|
| Forward | 3 |
| Backward | 4 |
| Left | 1 |
| Right | 2 |

A STOP request was sent before and after each short movement test; motor battery cutoff remained accessible. Physical stopping was *visually* observed at the end of each timed test.

## What we did **not** verify

- Separate STOP effectiveness during sustained motion or measured stopping time/distance
- Automatic stop on communications loss, Pi crash, Arduino failure or unexpected command
- Repeatability across multiple quantified runs, obstacle detection, floor driving, or load carrying
- Speech-recognition accuracy and microphone integration
- Safe real-wheelchair or human-use operation

## Next actions — KISS

1. Obtain a basic USB microphone compatible with Raspberry Pi OS.
2. Adapt the earlier Raspberry Pi Vosk voice prototype to send the tested **USB serial** protocol. The original `gpiozero.Robot` direct-GPIO version is **not** the validated Arduino command path.
3. Test priority STOP behavior, command expiry/timeout and communications-loss handling on an elevated model.
4. Only then perform controlled low-speed model-only floor trials, with a physical battery cutoff.

## Attribution

Oscar Cortez performed these October 30–31 troubleshooting and elevated-wheel tests. Anthony Randall worked on the earlier robot hardware/integration and provided a handover before withdrawing. Andrew Kuruvilla remains on the team; no unverified test actions are attributed to him.

**Manufacturer source (not Byte Bots original code):** https://github.com/elegooofficial/ELEGOO-Smart-Robot-Car-Kit-V4.0-New

Screenshots and original course milestone PDFs have **not yet been committed** to this repository; this text documents the observed session.
