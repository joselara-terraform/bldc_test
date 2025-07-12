#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import signal
import sys

ESC_PIN = 18
MIN_PULSE = 1050
MAX_PULSE = 1940
FREQ = 50

class ESCController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ESC_PIN, GPIO.OUT)
        self.pwm = GPIO.PWM(ESC_PIN, FREQ)
        self.pwm.start(0)
        self.set_throttle(0)
    
    def set_throttle(self, percent):
        percent = max(0, min(100, percent))
        pulse_ms = (MIN_PULSE + (percent / 100) * (MAX_PULSE - MIN_PULSE)) / 1000
        duty_cycle = (pulse_ms / 20) * 100  # 20ms period at 50Hz
        self.pwm.ChangeDutyCycle(duty_cycle)
    
    def cleanup(self):
        self.set_throttle(0)
        self.pwm.stop()
        GPIO.cleanup()

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