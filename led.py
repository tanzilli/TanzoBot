#Led lampeggiante

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led_dotpin=4

GPIO.setup(led_dotpin, GPIO.OUT)

delay=0.5
while True:
	GPIO.output(led_dotpin, 1)
	time.sleep(delay)
	
	GPIO.output(led_dotpin, 0)
	time.sleep(delay)
	