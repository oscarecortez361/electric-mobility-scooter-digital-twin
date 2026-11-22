#!/usr/bin/env python3
"""Create a separate bounded-burst Byte Bots V7 test from existing working V6.
Does not modify firmware or the existing V6 file.
Execute on the Raspberry Pi with motor power physically OFF.
"""
from pathlib import Path
import sys

root = Path.home() / "bytebots"
source = root / "voice_control_v6_final.py"
target = root / "voice_control_v7_burst_test.py"

if not source.is_file():
    sys.exit(f"ERROR: Original program not found: {source}")
if target.exists():
    sys.exit(f"ERROR: Test file already exists; nothing overwritten: {target}")

code = source.read_text()
helper = '''def bounded_motion(ctl, phrase, cancel, gate):
    """Repeat firmware-timed pulses only within a brief, bounded test window."""
    deadline = time.monotonic() + 1.6
    try:
        while time.monotonic() < deadline and not cancel.is_set() and not ctl.fault.is_set():
            with gate:
                if cancel.is_set() or ctl.fault.is_set():
                    return
                ok = ctl.pulse(phrase)
            if not ok:
                print('Motor ACK missing; disarming.', flush=True)
                ctl.fault.set()
                cancel.set()
                with gate:
                    ctl.stop()
                return
            cancel.wait(0.03)
        if not cancel.is_set() and not ctl.fault.is_set():
            print('BURST COMPLETE; firmware-timed pulses have stopped.', flush=True)
    except Exception as exc:
        print('Motion worker error:', exc, flush=True)
        ctl.fault.set()
        cancel.set()
        with gate:
            ctl.stop()


'''
old_voice = '''                if phrase == 'stop':
                    print('HEARD STOP', flush=True)
                    ctl.stop()
                    break
                if phrase in DIRECTIONS:
                    print('HEARD:', phrase, flush=True)
                    if not ctl.pulse(phrase):
                        print('Movement not confirmed; exiting.', flush=True)
                        break
'''
new_voice = '''                if phrase == 'stop':
                    print('HEARD STOP', flush=True)
                    if motion_cancel is not None:
                        motion_cancel.set()
                    with motion_gate:
                        ctl.stop()
                    break
                if phrase in DIRECTIONS:
                    print('HEARD:', phrase, flush=True)
                    if motion_thread is not None and motion_thread.is_alive():
                        print('Burst in progress; say STOP or let it finish.', flush=True)
                        continue
                    motion_cancel = threading.Event()
                    motion_thread = threading.Thread(
                        target=bounded_motion,
                        args=(ctl, phrase, motion_cancel, motion_gate),
                        daemon=True)
                    motion_thread.start()
'''
old_final = '''        finally:
            ctl.stop()
            if microphone is not None:
'''
new_final = '''        finally:
            if motion_cancel is not None:
                motion_cancel.set()
            with motion_gate:
                ctl.stop()
            if motion_thread is not None:
                motion_thread.join(timeout=0.6)
            if microphone is not None:
'''
changes = [
    ("def main():\n", helper + "def main():\n"),
    (
        "        ctl = Controller(port)\n",
        "        ctl = Controller(port)\n"
        "        motion_gate = threading.Lock()\n"
        "        motion_cancel = None\n"
        "        motion_thread = None\n",
    ),
    (old_voice, new_voice),
    (old_final, new_final),
]
for old, new in changes:
    matches = code.count(old)
    if matches != 1:
        sys.exit(f"ERROR: Expected one code block, found {matches}. No file was written."
                 " Send the exact script for review rather than forcing this patch.")
    code = code.replace(old, new, 1)

code = code.replace(
    "BYTE BOTS V6 | VOICE + WATCHDOG + 350 ms motor pulses",
    "BYTE BOTS V7 TEST | Voice + watchdog + bounded movement window",
    1,
)
try:
    compile(code, str(target), 'exec')
except SyntaxError as exc:
    sys.exit(f"ERROR: Generated Python syntax failed: {exc}. No file was written.")

target.write_text(code)
print(f"CREATED: {target}")
print("Original V6 untouched. Not started or armed.")
print("New behavior: one spoken direction runs repeated 225-ms pulses for roughly 2 sec max.")
print("STOP cancels further pulses; physical power cutoff remains essential.")
