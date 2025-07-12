#!/usr/bin/env python3
import pigpio
import time
import signal
import sys

ESC_PIN = 18
MIN_PULSE = 1050
MAX_PULSE = 1940

class ESCController:
    def __init__(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            sys.exit(1)
        self.set_throttle(0)
    
    def set_throttle(self, percent):
        percent = max(0, min(100, percent))
        pulse_width = MIN_PULSE + (percent / 100) * (MAX_PULSE - MIN_PULSE)
        self.pi.set_servo_pulsewidth(ESC_PIN, pulse_width)
    
    def cleanup(self):
        self.set_throttle(0)
        self.pi.stop()

def main():
    esc = ESCController()
    
    def signal_handler(sig, frame):
        esc.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Motor control ready. Enter 0-100 for throttle %, 's' to stop, Ctrl+C to exit")
    
    while True:
        try:
            cmd = input("> ").strip().lower()
            if cmd == 's':
                esc.set_throttle(0)
            else:
                throttle = float(cmd)
                esc.set_throttle(throttle)
        except ValueError:
            pass

if __name__ == "__main__":
    main()