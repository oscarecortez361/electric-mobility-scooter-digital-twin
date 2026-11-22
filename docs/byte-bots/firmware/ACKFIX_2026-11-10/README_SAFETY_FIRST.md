# Byte Bots Safety Firmware V2 — UNTESTED BENCH CANDIDATE

**Created 2026-11-06** from the archived ELEGOO Smart Robot Car V4.0 firmware v2.1.2. Original remains unchanged.

## CAUTION

This code is NOT compiled, flashed, or physically validated by ChatGPT. Do not operate around people, on the floor, with riders, or with motor battery installed without independent instructor-approved testing. A software watchdog does not replace a physical power cutoff, independent e-stop or certified safety controller. Arduino IDE compile first: Arduino UNO ~91% flash already occupied before changes.

## Change summary

* `DeviceDriverSet_Motor::control()` forces both PWM values to zero unless `byteBotsMotorsAllowed` is true; startup motor driver standby LOW, PWM=0.
* While armed, silence of 450 ms from accepted N=112 heartbeat disarms and stops the motors. This is the **code threshold**, not a proven physical stop time (serial parsing, control-loop, PWM and mechanical delays must be measured).
* STOP commands N=110 and N=100 force stop and disarm. The latch will not clear until an explicit N=111 D1=1 ARM command. A new N=112 heartbeat cannot re-arm.
* Only `N=2` timed movement and `N=21` ultrasonic distance reads remain enabled. Key/IR autonomous-mode polling is disabled in this demo build.
* Valid moving commands: `N=2`, D1=1..4, speed D2=1..90, duration T=1..350 ms. All other motor commands rejected.
* 350-ms timed callback STOP is preserved. Original CPU watchdog (~4 s) is distinct from communications timeout.

## Protocol — motor battery OFF until code reviewed and approval scope checked

Read sensor while disarmed:
`{"N":21,"H":"910","D1":2}` -> `{910_...}`

Attempt motion while disarmed (MUST NOT move):
`{"N":2,"H":"BB","D1":3,"D2":90,"T":350}` -> `{BB_DISARMED}`

After separate operator action, ARM:
`{"N":111,"H":"BB","D1":1}` -> `{BB_ARMED}`

Heartbeat (Pi must send every ~100 ms while armed; Arduino does not ACK to avoid serial traffic):
`{"N":112,"H":"HB"}`

Moving command after ARM+heartbeats, ONLY in later instructor-approved wheels-up tests:
`{"N":2,"H":"BB","D1":3,"D2":90,"T":350}` -> timed stop callback response. Note: latest `H` may be overwritten by intermediate commands in original firmware; do not interpret ACK as exact movement latency.

Software STOP and latch (can be sent even when disarmed):
`{"N":110,"H":"BB"}` -> `{BB_ok}`

When heartbeat stops: `{BB_LINK_LOST}` once; later movement -> `{BB_DISARMED}`. Re-arm requires explicit operator command N=111 D1=1.

## IMPORTANT integration caveats

1. **Do not upload yet.** The current Raspberry Pi V2 voice controller does not send heartbeat or an explicit re-arm, so this firmware will reject its movement commands until the Pi application is updated.
2. The ultrasonic N=21 reading is supported, but fail-closed ultrasonic gating is **not integrated** into this firmware. Existing V3 is a **dry-run** prototype only.
3. Original serial JSON parser may wait up to 1000 ms on partial packet; safety check is called inside that wait loop, but other blocking code and actual latency remain unmeasured.
4. A 4-second processor watchdog reset, motor timer and serial heartbeat are different safeguards.
5. The 450-ms threshold is a design target, not a measured ≤500-ms physical STOP result. Prove it in logged wheels-elevated trials.
6. The exact scope of McManus's November 3 signed safety review must be checked before powered hardware testing.
7. Keep manual independent motor-battery power cutoff accessible. No riders.
8. Inspect code and verify the UNO build fits (FLASH/RAM); Arduino libraries, settings and hardware must match the original successfully compiled IDE project.

## Open in Arduino IDE

Unzip. Open `ByteBots_Safety_Firmware_V2/ByteBots_Safety_Firmware_V2.ino`. Choose Arduino UNO. **Click Verify (checkmark), NOT Upload (right arrow)**. Save output for evidence. If too large or failed, stop and report output; do not flash.
