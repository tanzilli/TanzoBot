import RPi.GPIO as GPIO
import time
  
GPIO.setmode(GPIO.BOARD)
  
GPIO.setup(12, GPIO.OUT)
 
## Set della frequenza a 50 Herz  (Periodo 20 mS)
servo = GPIO.PWM(12, 50)    

## Imposta il duty cycle al 5% (1 mS on)   
servo.start(5)             

for i in range(5):
	time.sleep(2)

	## Porta il duty cycle al 10% (2 mS on)   
	servo.ChangeDutyCycle(10)   

	time.sleep(2)

	## Porta il duty cycle al 5% (1 mS on)   
	servo.ChangeDutyCycle(5)   
  
servo.stop()
GPIO.cleanup() 
