#GPIO

import RPi.GPIO as GPIO
import time

LAMP_DX=17
LAMP_SX=27
INT_SX=21
	
def my_callback(channel):
	print channel
	if channel==INT_SX:
		if GPIO.input(LAMP_SX)==0:
			GPIO.output(LAMP_SX, 1)
		else:
			GPIO.output(LAMP_SX, 0)
		
def main():

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(INT_SX, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(INT_SX, GPIO.BOTH, callback=my_callback, bouncetime=100)

	GPIO.setup(LAMP_SX, GPIO.OUT)
	GPIO.setup(LAMP_DX, GPIO.OUT)
	GPIO.output(LAMP_SX, 0)
	GPIO.output(LAMP_DX, 0)
		
	try:  
		
		#Entro in un loop infinito dove conto i secondi che passano
		while True:
			time.sleep(1)

	except KeyboardInterrupt:  
		print "Exit"	
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

	GPIO.cleanup()           # clean up GPIO on normal exit  	
	
if __name__ == '__main__':
	main()
	  
