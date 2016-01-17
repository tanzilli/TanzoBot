#GPIO

import RPi.GPIO as GPIO
import time
	
def my_callback(channel):
	print channel
	print GPIO.input(channel)

def main():
	try:  
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.cleanup()

		GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		time.sleep(0.1)
		
		GPIO.remove_event_detect(21) 
		GPIO.add_event_detect(21, GPIO.BOTH, callback=my_callback, bouncetime=100)
		
		#Entro in un loop infinito dove conto i secondi che passano
		while True:
			time.sleep(1)

	except KeyboardInterrupt:  
		print "Exit"	
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

	GPIO.cleanup()           # clean up GPIO on normal exit  	
	
if __name__ == '__main__':
	main()
	  
