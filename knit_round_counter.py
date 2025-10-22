# file: knit_round_counter.py
# Requires: sudo apt-get install python3-gpiozero
# Run: python3 knit_round_counter.py

import time
from gpiozero import DigitalInputDevice, LED

SENSOR_PIN = 17   # Hall sensor OUT -> GPIO17 (pin 11)
LED_PIN    = 18   # optional status LED (pin 12). If no LED, set to None

LOCKOUT_SEC = 0.80  # ignore subsequent triggers within this window

# Pull-up True so idle is HIGH, magnet present pulls it LOW
sensor = DigitalInputDevice(SENSOR_PIN, pull_up=True, bounce_time=0.01)
led = LED(LED_PIN) if LED_PIN is not None else None

round_count = 0
last_trigger_ts = 0.0

def trigger():
    global round_count, last_trigger_ts
    now = time.monotonic()
    if now - last_trigger_ts < LOCKOUT_SEC:
        return  # within lockout window -> ignore
    round_count += 1
    last_trigger_ts = now
    if led:
        led.on()
    print(f"[{time.strftime('%H:%M:%S')}] Round: {round_count}")
    # brief visual blink
    if led:
        time.sleep(0.05)
        led.off()

print("Knit Round Counter (Pi + Hall sensor)")
print("Bring the magnetized stitch marker near the sensor to increment.")
print("Press Ctrl+C to stop.\n")

try:
    # Count on the transition to LOW (magnet present)
    sensor.when_activated = trigger  # activated = input goes LOW with pull_up=True
    # Keep the program alive
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting. Final round count:", round_count)
