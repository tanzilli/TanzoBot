#!/usr/bin/env python
#http://www.acmesystems.it/tpc
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
import telegram	
import logging

import time
import os					

import pygame
	
video_keyboard = telegram.ReplyKeyboardMarkup([["VIDEO 1","VIDEO 2","VIDEO 3","VIDEO 4"],["PROMO 1","PROMO 2","/help","STOP"]])
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
	bot.sendMessage(update.message.chat_id, "Ciao %s ! Sei connesso con VideoBoxBot.\n" % ( update.message.from_user.first_name))
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
		print " ----> VIDEO <----"
		newFile = bot.getFile(update.message.video.file_id)
		newFile.download('newvideo.mov')
		#os.system("sudo pkill omxplayer")
		#os.system("omxplayer --win 0,0,128,64 --orientation 270 -o local --loop video_%3d &" % video_counter)
		bot.sendMessage(update.message.chat_id, text="Salva come VIDEO x ...", reply_markup=video_keyboard)
		current_command="save"
	
	if update.message.sticker:
		os.system("sudo pkill omxplayer")
		
		print " ----> STICKER <----"
		newFile = bot.getFile(update.message.sticker.file_id)
		newFile.download('sticker.webp')
		os.system("dwebp sticker.webp -o sticker.png")

		#apt-get install webp
		#dwebp sticker.webp -o abc.png
		#apt-get install python-pygame
		screen.fill((50,50,50))
		img=pygame.image.load("sticker.png") 
		rect=img.get_rect().size
		
		if rect[0]>64:
			w=64
			h1=rect[1]*w/rect[0]

		if h1>128:
			h=128
			w=w*h/h1
		else:
			h=h1
			
		print rect
		print w
		print h
		
		img = pygame.transform.scale(img,(w,h))
		img = pygame.transform.rotate(img,90)
		
		screen.blit(img,(0,0))
		#pygame.display.flip()
		pygame.display.update()

		#pygame.quit()
	
	if update.message.photo:
		os.system("sudo pkill omxplayer")
		
		print " ----> PHOTO <----"

		newFile = bot.getFile(update.message.photo[1].file_id)

		newFile.download('photo.jpg')
		#os.system("dwebp sticker.webp -o sticker.png")

		#apt-get install webp
		#dwebp sticker.webp -o abc.png
		#apt-get install python-pygame
		#screen.fill((50,50,50))
		img=pygame.image.load("photo.jpg") 
		rect=img.get_rect().size
		
		if rect[0]>64:
			w=64
			h1=rect[1]*w/rect[0]

		if h1>128:
			h=128
			w=w*h/h1
		else:
			h=h1
			
		print rect
		print w
		print h
		
		img = pygame.transform.scale(img,(w,h))
		img = pygame.transform.rotate(img,90)
		
		screen.blit(img,(0,0))
		#pygame.display.flip()
		pygame.display.update()

		#pygame.quit()

		
	if update.message.text:
		if current_command=="save":
			if update.message.text=="VIDEO 1":
				os.system("mv -f newvideo.mov video1.mov")
				current_command="play"

			if update.message.text=="VIDEO 2":
				os.system("mv -f newvideo.mov video2.mov")
				current_command="play"

			if update.message.text=="VIDEO 3":
				os.system("mv -f newvideo.mov video3.mov")
				current_command="play"

			if update.message.text=="VIDEO 4":
				os.system("mv -f newvideo.mov video4.mov")
				current_command="play"

	if update.message.text:
		if current_command=="play":
			if update.message.text=="VIDEO 1":
				if os.path.exists("video1.mov"):
					os.system("sudo pkill omxplayer")
					os.system("omxplayer --win 0,0,128,64 --orientation 0 -o local --loop video1.mov &")
				else:
					bot.sendMessage(update.message.chat_id, "Il video non esiste")
							
			if update.message.text=="VIDEO 2":
				if os.path.exists("video2.mov"):
					os.system("sudo pkill omxplayer")
					os.system("omxplayer --win 0,0,128,64 --orientation 0 -o local --loop video2.mov &")
				else:
					bot.sendMessage(update.message.chat_id, "Il video non esiste")

			if update.message.text=="VIDEO 3":
				if os.path.exists("video3.mov"):
					os.system("sudo pkill omxplayer")
					os.system("omxplayer --win 0,0,128,64 --orientation 0 -o local --loop video3.mov &")
				else:
					bot.sendMessage(update.message.chat_id, "Il video non esiste")

			if update.message.text=="VIDEO 4":
				if os.path.exists("video4.mov"):
					os.system("sudo pkill omxplayer")
					os.system("omxplayer --win 0,0,128,64 --orientation 0 -o local --loop video4.mov &")
				else:
					bot.sendMessage(update.message.chat_id, "Il video non esiste")

			if update.message.text=="PROMO 1":
				if os.path.exists("festone.m4v"):
					os.system("sudo pkill omxplayer")
					os.system("omxplayer --win 0,0,128,64 --orientation 270 -o local --loop festone.m4v &")
				else:
					bot.sendMessage(update.message.chat_id, "Il video non esiste")

			if update.message.text=="PROMO 2":
				if os.path.exists("festone.m4v"):
					os.system("sudo pkill omxplayer")
					os.system("omxplayer --win 0,0,128,64 --orientation 270 -o local --loop festone.m4v &")
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
	updater = telegram.Updater("190181444:AAEgb3yN0kq6efTtkT-6LyDAE-IeOPi7xzc")	
	
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

	#Pygame init
	os.putenv('SDL_VIDEODRIVER', "directfb")
	pygame.display.init()
	pygame.mouse.set_visible(False)
	size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

	try:  
		# Run the bot until the you presses Ctrl-C or the process receives SIGINT,
		# SIGTERM or SIGABRT. This should be used most of the time, since
		# start_polling() is non-blocking and will stop the bot gracefully.
		updater.idle()

	except KeyboardInterrupt:  
		print "Exit"	

if __name__ == '__main__':
	main()
