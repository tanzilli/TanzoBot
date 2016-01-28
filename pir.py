#!/usr/bin/env python
#http://www.acmesystems.it/tpc
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
import telegram				#Wrapper Bot API Telegram
import logging

import RPi.GPIO as GPIO		#Gestione GPIO
import time
import os					
import picamera				# Gestione picam

job_queue=None
chat_ids=[]
	
# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)

def pir_handler(channel):
	global job_queue
	global chat_ids

	#os.system("omxplayer -o local angrydog.m4a &")

	print "PIR alarm"
	if len(chat_ids)>=0:
		for chat_id in chat_ids:
			job_queue.bot.sendMessage(chat_id, text="Allarme" )

	with picamera.PiCamera() as camera:
		camera.resolution = (1280,720)
		camera.capture('photo.jpg')

	if len(chat_ids)>=0:
		for chat_id in chat_ids:
			job_queue.bot.sendPhoto(chat_id, photo=open('photo.jpg'))

def start(bot, update):
	global chat_ids

	chat_ids+=[update.message.chat_id]	
	bot.sendMessage(update.message.chat_id, "Ciao %s ! Io sono PirBot.\n" % ( update.message.from_user.first_name))
		
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():	
	global job_queue
	
	#@InfraredBot
	updater = telegram.Updater("134968583:AAEXYeTdmbi96qbnqQ3pdBpq3l-4RN8bkMQ")	
	job_queue = updater.job_queue	

	# Get the dispatcher to register handlers
	dp = updater.dispatcher
	dp.addTelegramCommandHandler("start",start)

	
	# log all errors
	dp.addErrorHandler(error)

	# Start the Bot
	update_queue = updater.start_polling()

	try:  
		# Run the bot until the you presses Ctrl-C or the process receives SIGINT,
		# SIGTERM or SIGABRT. This should be used most of the time, since
		# start_polling() is non-blocking and will stop the bot gracefully.
		updater.idle()

	except KeyboardInterrupt:  
		print "Exit"	
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

	GPIO.cleanup()           # clean up GPIO on normal exit  	

if __name__ == '__main__':
	
	#Riferimento ai GPIO per numero pin
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	INFRAROSSO=18

	GPIO.setup(INFRAROSSO, GPIO.IN, pull_up_down=GPIO.PUD_UP)	
	GPIO.add_event_detect(INFRAROSSO, GPIO.RISING, pir_handler, 200)

	main()
