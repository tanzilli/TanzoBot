import RPi.GPIO as GPIO
import time

LAMP_SX=11
LAMP_DX=13
INT_SX=40
INT_DX=38
	
def handler_int_sx(channel):
	print channel
	if channel==INT_SX:
		if GPIO.input(LAMP_SX)==0:
			GPIO.output(LAMP_SX, 1)
		else:
			GPIO.output(LAMP_SX, 0)

def handler_int_dx(channel):
	print channel
	if channel==INT_DX:
		if GPIO.input(LAMP_DX)==0:
			GPIO.output(LAMP_DX, 1)
		else:
			GPIO.output(LAMP_DX, 0)
		
def main():

	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	GPIO.setup(LAMP_SX, GPIO.OUT)
	GPIO.setup(LAMP_DX, GPIO.OUT)
	
	GPIO.output(LAMP_SX, 0)
	GPIO.output(LAMP_DX, 0)

	GPIO.setup(INT_SX, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(INT_DX, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	GPIO.add_event_detect(INT_SX, GPIO.BOTH, callback=handler_int_sx, bouncetime=100)
	GPIO.add_event_detect(INT_DX, GPIO.BOTH, callback=handler_int_dx, bouncetime=100)
		
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
	  
