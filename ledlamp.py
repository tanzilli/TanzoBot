#!/usr/bin/env python
from rgbmatrix import RGBMatrix
import telegram
import logging
import time

red = 10
green = 0
blue = 0
max=100
step=5
myMatrix = 0   

menu_keyboard = telegram.ReplyKeyboardMarkup([['OFF','ON',"000"],['R-','R+','G-','G+','B-','B+']])
menu_keyboard.one_time_keyboard=False
menu_keyboard.resize_keyboard=False

# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def cmd_start(bot, update):
	bot.sendMessage(update.message.chat_id, text="Hi %s ! I'm LedLampBot.\n" % ( update.message.from_user.first_name), reply_markup=menu_keyboard)

def echo(bot, update):
	global red 
	global green
	global blue
	
	print "      Testo     : [" + update.message.text + "]"

	if update.message.text=="ON":
		if red==0 and green==0 and blue==0:
			red=step
			green=step
			blue=step
		myMatrix.Fill(red, green, blue)

	if update.message.text=="OFF":
		myMatrix.Clear()

	if update.message.text=="000":
		red=0
		green=0
		blue=0
		myMatrix.Clear()
	
	if update.message.text=="R+":
		if red<=max:
			red+=step
		myMatrix.Fill(red, green, blue)

	if update.message.text=="R-":
		if red>=step:
			red-=step
		myMatrix.Fill(red, green, blue)

	if update.message.text=="G+":
		if green<=max:
			green+=step
		myMatrix.Fill(red, green, blue)

	if update.message.text=="G-":
		if green>=step:
			green-=step
		myMatrix.Fill(red, green, blue)

	if update.message.text=="B+":
		if blue<=max:
			blue+=step
		myMatrix.Fill(red, green, blue)

	if update.message.text=="B-":
		if blue>=step:
			blue-=step
		myMatrix.Fill(red, green, blue)
		

def main():	
	global update_queue
	global myMatrix
	
	rows = 32
	chains = 4
	parallel = 1
	
	# @LedlampBot
	updater = telegram.Updater("194376022:AAHLWzfrLediKJwE3CXk1vYhRwVVBpmRJLQ")	
	
	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# Definisce gli handler di gestione dei comandi
	dp.addTelegramCommandHandler("start", cmd_start)
			
	# on noncommand i.e message - echo the message on Telegram
	dp.addTelegramMessageHandler(echo)

	# log all errors
	dp.addErrorHandler(error)

	# Start the Bot
	update_queue = updater.start_polling()

	myMatrix = RGBMatrix(rows, chains, parallel)
	myMatrix.Fill(0, 0, 0)

	try:  
		# Run the bot until the you presses Ctrl-C or the process receives SIGINT,
		# SIGTERM or SIGABRT. This should be used most of the time, since
		# start_polling() is non-blocking and will stop the bot gracefully.
		updater.idle()

	except KeyboardInterrupt:  
		print "Exit"	


if __name__ == '__main__':
	main()


