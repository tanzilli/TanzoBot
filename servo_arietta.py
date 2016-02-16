import acmepins as GPIO
import time
  
GPIO.setmode(GPIO.BOARD)

min = 4
max = 14

#GPIO.setup("J4.34", GPIO.OUT)
 
## Set della frequenza a 50 Herz  (Periodo 20 mS)
servo = GPIO.PWM("J4.34", 50)    

## Imposta il duty cycle al 5% (1 mS on)   
servo.start(min)             

for i in range(10):
	time.sleep(2)

	## Porta il duty cycle al 10% (2 mS on)   
	servo.ChangeDutyCycle(max)   

	time.sleep(2)

	## Porta il duty cycle al 5% (1 mS on)   
	servo.ChangeDutyCycle(min)   
  
servo.stop()
GPIO.cleanup() 
