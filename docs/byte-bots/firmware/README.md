# Byte Bots Arduino V2 / ACKFIX firmware recovery (November 22, 2026)

**Source archive:** [ACKFIX package](ACKFIX_2026-11-10/README_ACKFIX_2026-11-10.md) · [Safety notes](ACKFIX_2026-11-10/README_SAFETY_FIRST.md) · [Arduino sketch](ACKFIX_2026-11-10/ByteBots_Safety_Firmware_V2/ByteBots_Safety_Firmware_V2.ino) · [V6.1 Pi controller](ACKFIX_2026-11-10/Pi_Software/voice_control_v6_1_ackfix.py)

This is a recovered archive from `ByteBots_Safety_V2_ACKFIX.zip`, supplied by the team on November 22. It includes the full Arduino sketch directory, its support sources and bundled ArduinoJson header, the November 10 ACKFIX change notes, and the V6.1 companion Python controller. The original ZIP has also been retained in the project recovery records.

## Provenance and verification

- The recovered `ByteBots_Safety_Firmware_V2.ino` has **SHA-256 `da8470f9658a880ac63d3be9f587a5ebabf8716c4c8e1f04ec843d5602acdeef`**, matching the filename/hash documented in the team's earlier Milestone 5 review.
- The **ACKFIX changes** themselves are in `ApplicationFunctionSet.h` and `ApplicationFunctionSet.cpp`: the delayed movement acknowledgement request tag is retained in an owned buffer rather than pointing into short-lived JSON data.
- The supplied `voice_control_v6_1_ackfix.py` waits longer for a delayed movement ACK and prints recent replies on failure. It is **a separate, unverified revision** from the V6 and V7 snapshots in [recovered source](../source/README.md).
- GitHub files were reconstructed from the recovered ZIP's text source files. The team's local ZIP should remain the canonical byte-level archive; text files in GitHub may have normalized final newlines.
- The November 10 package **explicitly says the ACKFIX was not compiled, flashed, or hardware-tested at the time it was prepared**. We have not independently verified those later steps or confirmed ACKFIX was installed for the final floor videos. Do not present it as proven deployed firmware.

## Safe reproduction boundary

The original documentation contains component configuration and Arduino IDE build notes. **Do not flash, arm, or power the motors** merely because these files are available. Any physical test requires instructor authorization, wheels elevated initially, a clear test area, and a separate accessible physical motor-power cutoff. The team documented an unexpected movement event during motor-battery disconnection, so physical stopping and cutoff behavior remain unverified. This is not a safety-rated motor controller or passenger mobility system.

## Remaining Milestone 6 evidence

1. Confirm which Python controller revision and firmware binary were actually present during each filmed floor trial (rather than assuming the recovered ACKFIX was deployed).
2. If later authorized, document Arduino UNO IDE verification/build output, libraries/board settings, installed firmware ID, actual serial responses, and observed test results.
3. Complete or explicitly disclose the remaining acceptance-criteria outcomes, live panel demonstration, and human-override limitations.

[Return to Byte Bots README](../README.md).
