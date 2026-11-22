# Byte Bots — Recovered Raspberry Pi source snapshots

**Recovered:** November 22, 2026, by copying files from the Byte Bots Raspberry Pi to the HP laptop and reviewing the copies. These are preserved **unchanged** from the uploaded files. Python syntax was parsed successfully offline; no hardware execution or safety acceptance was performed as part of this recovery.

| File | Description | SHA-256 of recovered original |
|---|---|---|
| [`voice_control_v6_final.py`](voice_control_v6_final.py) | V6 voice-to-serial controller; short 225 ms command pulses; heartbeat and Arduino arm/disarm protocol | `4ec056b06d87549758491576a937804cd6a95a8ecf625de5d290dffd68871904` |
| [`voice_control_v7_burst_test.py`](voice_control_v7_burst_test.py) | V7 experimental burst controller; attempts bounded repeated short pulses with STOP cancellation | `b143cdb79c9c066e683e10c152752ddbc87018bf0b19ceeae856acd1a2b8c107` |
| [`bytebots_v7_patch.py`](bytebots_v7_patch.py) | Script that generates a separate V7 test file from V6; **not** the main running controller | `647b27d765ff8b7243c7fe30dfd29997ebc0c37e5fb1ac9ab53d087f3b13847b` |

## Platform assumptions present in source

- Raspberry Pi user/home: `/home/okerscooter`; source directory `~/bytebots`
- Local Vosk model: `~/bytebots/models/vosk-model-small-en-us-0.15`
- Python dependencies include `vosk` and `pyserial`, plus the Raspberry Pi OS `arecord` program and configured USB microphone
- Arduino UNO at `/dev/ttyUSB0`, 9600 baud, using project-specific JSON serial packets and responses
- Recognized phrases: `byte bots forward`, `byte bots backward`, `byte bots left`, `byte bots right`, and `stop`; unknown inputs are not mapped to movement
- The [Arduino V2 / ACKFIX firmware source archive](../firmware/README.md) has now been recovered and archived, but its exact installed/compiled hardware version and complete build reproducibility **remain unverified**.

## Important boundaries

**Archiving source is not verification of a complete reproducible motor-driving system.** These snapshots do not by themselves establish which version drove every November floor video, the exact Arduino firmware currently flashed, formal moving-STOP results, a verified independent emergency cutoff, or certified obstacle avoidance.

The V6 banner says “350 ms motor pulses,” but its `PULSE_MS` constant is actually **225 ms**. V7's bounded-motion deadline is **1.6 seconds**; the patch script's printed description rounds this to roughly two seconds. The archived source is intentionally unmodified so reviewers can trace the exact recovered bytes.

**Safety:** This is a small educational robot, **not** a passenger-carrying wheelchair or safety-certified assistive device. The project recorded unexpected movement during a prior battery-disconnection test. Never use serial STOP as a substitute for a verified independent physical motor cutoff. No person should ride or rely on this prototype. Do not run the recovered controller in powered tests without instructor-approved procedures, controlled space, and physical cutoff supervision.

## Missing for full Milestone 6 reproducibility

1. Confirm the flashed Arduino board image/version against the recovered V2/ACKFIX source; the ACKFIX package's own notes state it had not been compiled, flashed, or hardware-tested when created.
2. Record a frozen, witnessed mapping of Python controller + firmware + hardware setup to the final demonstration, including dependencies and safe setup/operations.
3. Complete or transparently mark unverified final acceptance tests and live industry-panel demonstration separately from these code-recovery artifacts.

Return to [Byte Bots project summary](../README.md).
