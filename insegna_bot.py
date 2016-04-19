#!/usr/bin/env python
#http://www.acmesystems.it/tpc
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
import telegram.ext
import logging

import time
import os					

video_keyboard = telegram.ReplyKeyboardMarkup([["VIDEO1","VIDEO2","VIDEO3","VIDEO4"],["STOP"]])
video_keyboard.one_time_keyboard=False
video_keyboard.resize_keyboard=True

current_command="play"

screen = None
		
# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)

def cmd_start(bot, update):
	bot.sendMessage(update.message.chat_id, "Ciao %s ! Sei connesso con la tua insegna.\n" % ( update.message.from_user.first_name))
	bot.sendMessage(update.message.chat_id, text="Seleziona un video per farne il play ...", reply_markup=video_keyboard)

def cmd_play(bot, update):
	global current_command	
	bot.sendMessage(update.message.chat_id, text="Che video vuoi riprodurre ?", reply_markup=video_keyboard)
	current_command="play"
	
def cmd_delete(bot, update):
	pass

def cmd_cancel(bot, update):
	global current_command
	current_command=None
	bot.sendMessage(update.message.chat_id, text="Comando cancellato")
	
def echo(bot, update):	
	global current_command
	global screen
	
	print "----> Mittente: : [" + update.message.from_user.username + "]"
	print "      Testo     : [" + update.message.text + "]"
 
	if update.message.video:
		newFile = bot.getFile(update.message.video.file_id)
		newFile.download("newvideo.mov")
		bot.sendMessage(update.message.chat_id, text="Salva come VIDEO x ...", reply_markup=video_keyboard)
		current_command="save"
		
	if update.message.text:
		if current_command=="save":
			if update.message.text=="VIDEO1":
				os.system("mv -f newvideo.mov video1.mov")
				current_command="play"

			if update.message.text=="VIDEO2":
				os.system("mv -f newvideo.mov video2.mov")
				current_command="play"

			if update.message.text=="VIDEO3":
				os.system("mv -f newvideo.mov video3.mov")
				current_command="play"

			if update.message.text=="VIDEO4":
				os.system("mv -f newvideo.mov video4.mov")
				current_command="play"

	if update.message.text:
		if current_command=="play":
			if update.message.text=="VIDEO1":
				if os.path.exists("video1.mov"):
					os.system("sudo pkill omxplayer")
					os.system("omxplayer --win 0,0,128,64 --orientation 0 -o local --loop video1.mov &")
				else:
					bot.sendMessage(update.message.chat_id, "Il video non esiste")
							
			if update.message.text=="VIDEO2":
				if os.path.exists("video2.mov"):
					os.system("sudo pkill omxplayer")
					os.system("omxplayer --win 0,0,128,64 --orientation 0 -o local --loop video2.mov &")
				else:
					bot.sendMessage(update.message.chat_id, "Il video non esiste")

			if update.message.text=="VIDEO3":
				if os.path.exists("video3.mov"):
					os.system("sudo pkill omxplayer")
					os.system("omxplayer --win 0,0,128,64 --orientation 0 -o local --loop video3.mov &")
				else:
					bot.sendMessage(update.message.chat_id, "Il video non esiste")

			if update.message.text=="VIDEO4":
				if os.path.exists("video4.mov"):
					os.system("sudo pkill omxplayer")
					os.system("omxplayer --win 0,0,128,64 --orientation 0 -o local --loop video4.mov &")
				else:
					bot.sendMessage(update.message.chat_id, "Il video non esiste")

		if update.message.text=="STOP":
			os.system("sudo pkill omxplayer")
			screen.fill((0,0,0))
			pygame.display.update()
			
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():	
	global update_queue
	global screen
	
	#@VideoBoxBot
	updater = telegram.ext.Updater(mytokens.token_insegna_bot)	
	
	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# Definisce gli handler di gestione dei comandi
	dp.addTelegramCommandHandler("start",   cmd_start)
	dp.addTelegramCommandHandler("cancel",  cmd_cancel)	
		
	# on noncommand i.e message - echo the message on Telegram
	dp.addTelegramMessageHandler(echo)

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

if __name__ == '__main__':
	main()
