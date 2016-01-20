#!/usr/bin/env python
import telegram
import logging

import acmepins as GPIO
import time
import os

token_string="144698784:AAFiwSmBktYVu5VmSTF35aQ4zgC3RvVhK9M"

welcome_text = 	"Arietta Stoplight !\n" 

menu_keyboard = telegram.ReplyKeyboardMarkup([['RED ON','YELLOW ON','GREEN ON'],['RED OFF','YELLOW OFF','GREEN OFF']])
menu_keyboard.one_time_keyboard=False
menu_keyboard.resize_keyboard=True

# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
	bot.sendMessage(update.message.chat_id, welcome_text)	
	menu(bot,update)

def menu(bot, update):
	bot.sendMessage(update.message.chat_id, text="Seleziona un comando", reply_markup=menu_keyboard)

def send_stop(bot, update):	
	reply_markup = telegram.ReplyKeyboardHide()
	bot.sendMessage(update.message.chat_id, text="Bye", reply_markup=reply_markup)

def echo(bot, update):
	print "----> Mittente: : [" + update.message.from_user.username + "]"
	print "      Testo     : [" + update.message.text + "]"
	
	if update.message.text:
		if update.message.text=="RED ON":
			GPIO.output(RED, 1)
			bot.sendMessage(update.message.chat_id, text="Led rosso ON")

		if update.message.text=="RED OFF":
			GPIO.output(RED, 0)
			bot.sendMessage(update.message.chat_id, text="Led rosso OFF")

		if update.message.text=="YELLOW ON":
			GPIO.output(YELLOW,1)
			bot.sendMessage(update.message.chat_id, text="Led giallo ON")

		if update.message.text=="YELLOW OFF":
			GPIO.output(YELLOW, 0)
			bot.sendMessage(update.message.chat_id, text="Led giallo OFF")

		if update.message.text=="GREEN ON":
			GPIO.output(GREEN,1)
			bot.sendMessage(update.message.chat_id, text="Led verde ON")

		if update.message.text=="GREEN OFF":
			GPIO.output(GREEN, 0)
			bot.sendMessage(update.message.chat_id, text="Led verde OFF")
		
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():	
	print "Token:" , token_string
	updater = telegram.Updater(token_string)	
	
	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# Definisce gli handler di gestione dei comandi
	dp.addTelegramCommandHandler("start", start)
	dp.addTelegramCommandHandler("menu", menu)
	dp.addTelegramCommandHandler("help", menu)
	
	# on noncommand i.e message - echo the message on Telegram
	dp.addTelegramMessageHandler(echo)

	# log all errors
	dp.addErrorHandler(error)

	# Start the Bot
	update_queue = updater.start_polling(poll_interval=0.1, timeout=10)

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
	#GPIO.setwarnings(False)

	RED="J4.40"
	YELLOW="J4.38"
	GREEN="J4.36"

	GPIO.setup(RED, GPIO.OUT)
	GPIO.setup(YELLOW, GPIO.OUT)
	GPIO.setup(GREEN, GPIO.OUT)

	GPIO.output(RED, 0)
	GPIO.output(YELLOW, 0)
	GPIO.output(GREEN, 0)

	main()
