from gpiozero import DigitalInputDevice, LED
from signal import pause

HALL_PIN = 17      # sensor output
LED_PIN  = 18      # indicator LED

sensor = DigitalInputDevice(HALL_PIN, pull_up=True, bounce_time=0.02)
led = LED(LED_PIN)

def magnet_detected():
    print("Magnet nearby!")
    led.on()

def magnet_gone():
    print("Magnet away.")
    led.off()

sensor.when_activated   = magnet_detected   # goes LOW when magnet near
sensor.when_deactivated = magnet_gone

print("Running. Move the magnet close to the sensor...")
pause()
