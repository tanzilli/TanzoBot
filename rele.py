import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RELE1=27
RELE2=22

GPIO.setup(RELE1, GPIO.OUT)
GPIO.setup(RELE2, GPIO.OUT)

delay=0.5
while True:
	GPIO.output(RELE1, 1)
	time.sleep(delay)
	GPIO.output(RELE2, 1)
	time.sleep(delay)
	
	GPIO.output(RELE1, 0)
	time.sleep(delay)
	GPIO.output(RELE2, 0)
	time.sleep(delay)
