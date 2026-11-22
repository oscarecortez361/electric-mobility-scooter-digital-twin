#!/usr/bin/env python3
"""Byte Bots V6: short, voice-triggered motor pulses with Arduino V2 watchdog.
Classroom prototype only. Not a physical emergency stop or certified obstacle avoidance.
Use only in approved, supervised testing with a separate physical motor power cutoff.
"""
import json
import subprocess
import threading
import time

import serial
from vosk import KaldiRecognizer, Model, SetLogLevel

PORT = '/dev/ttyUSB0'
BAUD = 9600
MODEL = '/home/okerscooter/bytebots/models/vosk-model-small-en-us-0.15'
GRAMMAR = ['byte bots forward', 'byte bots backward', 'byte bots left',
           'byte bots right', 'stop', '[unk]']
DIRECTIONS = {'byte bots forward': 3, 'byte bots backward': 4,
              'byte bots left': 1, 'byte bots right': 2}
PULSE_MS = 225
SPEED = 40
SetLogLevel(-1)

class Controller:
    def __init__(self, port):
        self.port = port
        self.tx_lock = threading.Lock()
        self.cv = threading.Condition()
        self.received = ''
        self.done = threading.Event()
        self.fault = threading.Event()
        self.number = 3000
        self.reader = threading.Thread(target=self.receive, daemon=True)
        self.beater = threading.Thread(target=self.heartbeat, daemon=True)

    def transmit(self, packet):
        payload = (json.dumps(packet, separators=(',', ':')) + '\n').encode()
        with self.tx_lock:
            self.port.write(payload)
            self.port.flush()

    def receive(self):
        while not self.done.is_set():
            try:
                data = self.port.read(64)
                if not data:
                    continue
                message = data.decode(errors='replace')
                with self.cv:
                    self.received = (self.received + message)[-8192:]
                    self.cv.notify_all()
                if 'BB_LINK_LOST' in self.received:
                    print('FAULT: Arduino heartbeat lost. Disarmed.', flush=True)
                    self.fault.set()
                    return
            except (serial.SerialException, OSError) as exc:
                print('FAULT: serial receive:', exc, flush=True)
                self.fault.set()
                return

    def heartbeat(self):
        while not self.done.is_set() and not self.fault.is_set():
            try:
                self.transmit({'N': 112, 'H': 'HB'})
            except (serial.SerialException, OSError) as exc:
                print('FAULT: heartbeat:', exc, flush=True)
                self.fault.set()
                return
            self.done.wait(0.10)

    def expect(self, token, timeout=0.35):
        deadline = time.monotonic() + timeout
        with self.cv:
            while token not in self.received and not self.fault.is_set():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return False
                self.cv.wait(min(remaining, 0.04))
            return token in self.received and not self.fault.is_set()

    def stop(self):
        try:
            self.transmit({'N': 110, 'H': 'BB'})
            print('STOP/disarm sent.', flush=True)
        except (serial.SerialException, OSError) as exc:
            print('STOP not confirmed; CUT MOTOR POWER PHYSICALLY:', exc, flush=True)

    def arm(self):
        self.transmit({'N': 111, 'H': 'BB', 'D1': 1})
        return self.expect('{BB_ARMED}', 0.35)

    def pulse(self, phrase):
        if self.fault.is_set() or self.done.is_set():
            return False
        self.number += 1
        tag = str(self.number)
        try:
            self.transmit({'N': 2, 'H': tag, 'D1': DIRECTIONS[phrase],
                           'D2': SPEED, 'T': PULSE_MS})
            if not self.expect('{' + tag + '_ok}', 0.45):
                print('No confirmed motor ACK; stopping.', flush=True)
                return False
            return not self.fault.is_set()
        except (serial.SerialException, OSError) as exc:
            print('Motor command error:', exc, flush=True)
            self.fault.set()
            return False

    def close(self):
        self.done.set()
        self.stop()
        self.beater.join(timeout=0.25) if self.beater.is_alive() else None
        self.reader.join(timeout=0.25) if self.reader.is_alive() else None


def bounded_motion(ctl, phrase, cancel, gate):
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


def main():
    print('BYTE BOTS V7 TEST | Voice + watchdog + bounded movement window')
    print('NOT a safety-rated emergency-stop or obstacle-avoidance system.')
    print('For instructor-approved wheels-up motor tests only until physical STOP is verified.')
    print('Keep a separate physical motor power cutoff accessible.')
    model = Model(MODEL)
    recognizer = KaldiRecognizer(model, 16000, json.dumps(GRAMMAR))
    microphone = None
    with serial.Serial(PORT, BAUD, timeout=0.05, write_timeout=0.1) as port:
        time.sleep(3)  # Arduino resets on serial open
        port.reset_input_buffer()
        ctl = Controller(port)
        motion_gate = threading.Lock()
        motion_cancel = None
        motion_thread = None
        ctl.reader.start()
        try:
            ctl.stop()
            if not ctl.expect('{BB_ok}', 0.4):
                print('Initial STOP not acknowledged. No arming.')
                return
            ctl.beater.start()
            answer = input('Wheels elevated, physical cutoff ready, approval confirmed? Type ARM: ').strip()
            if answer != 'ARM':
                print('Not armed.')
                return
            if not ctl.arm():
                print('Arduino ARM not acknowledged. No motion.')
                return
            print('ARMED. Say "Byte Bots forward" etc., or "stop". Ctrl-C to quit.')
            microphone = subprocess.Popen(
                ['arecord', '-q', '-D', 'plughw:2,0', '-f', 'S16_LE',
                 '-r', '16000', '-c', '1', '-t', 'raw'], stdout=subprocess.PIPE)
            while not ctl.fault.is_set():
                audio = microphone.stdout.read(4000)
                if not audio:
                    print('Microphone disconnected; stopping.')
                    break
                if not recognizer.AcceptWaveform(audio):
                    continue
                phrase = json.loads(recognizer.Result()).get('text', '').strip().lower()
                if phrase == 'stop':
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
        except KeyboardInterrupt:
            print('Operator interrupted.')
        finally:
            if motion_cancel is not None:
                motion_cancel.set()
            with motion_gate:
                ctl.stop()
            if motion_thread is not None:
                motion_thread.join(timeout=0.6)
            if microphone is not None:
                microphone.terminate()
                try:
                    microphone.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    microphone.kill()
            ctl.close()
            print('Disarmed. If any wheel continues turning, cut motor power physically.')

if __name__ == '__main__':
    main()
