# Byte Bots V6.1 / Arduino Safety V2 — Timer ACK correction (2026-11-10)

**Why this revision exists**
In the Arduino Safety V2 code, `commandSerialNumber` was a `char*` into `StaticJsonDocument` memory in `serialEvent`. The `N=2` motion reply is delayed until the 350 ms timer expires. In the meantime, repeated 100 ms heartbeat JSON packets reuse that temporary memory; the tag may be lost/changed, so Pi V6 reports `No confirmed motor ACK`. This may explain the screenshot; it is not a physical wheel-motion diagnosis.

**Changes**
- `ApplicationFunctionSet.h`: store request tag in an owned 20-char array.
- `ApplicationFunctionSet.cpp`: safely copy `H` with `strncpy` and NUL termination; test for a nonempty tag.
- Python V6.1: wait 1.20 sec for the delayed movement completion acknowledgement, and print the actual recent serial reply if it is missing. Still fail-closed on missing ACK; STOP/disarm and 100 ms heartbeat remain.
- No changes to motor timing, allowed speed, 450 ms heartbeat expiry, STOP latch, or actuator modes.

**Before any movement**
Motor power OFF. Arduino IDE open `ByteBots_Safety_Firmware_V2/ByteBots_Safety_Firmware_V2.ino`, Verify and inspect flash/RAM, then upload only if the instructor-approved firmware replacement is authorized. Do not flash while motors powered. Copy V6.1 to Pi. Repeat only the **new V6.1 wheels-elevated powered movement and physical stop verification**, under instructor-approved controlled test conditions, with accessible independent physical cutoff. Do not drive on the floor or near people until actual physical stopping is verified.

**Limits**
Not compiled on this computer (Arduino CLI unavailable). Not flashed or hardware-tested. Code still does NOT implement fail-closed obstacle avoidance. Do not present software voice STOP as a safety-rated e-stop.
