#!/usr/bin/env python
#http://www.acmesystems.it/tpc

import telegram
import logging

import RPi.GPIO as GPIO
import time
import os

emoji = telegram.Emoji
bouncetime = 200

welcome_text = 	"Benvenuto ! Io sono @TanzoBot..." + emoji.SMILING_FACE_WITH_SUNGLASSES + "\n" 

menu_keyboard = telegram.ReplyKeyboardMarkup([['/luci','/foto','/video','/logo','/start'],['/dog','/warner','/mute','/pdf','/menu']])
menu_keyboard.one_time_keyboard=False
menu_keyboard.resize_keyboard=True

luci_keyboard = telegram.ReplyKeyboardMarkup([[ 'SX ON', 'DX ON' ],[ 'SX OFF', 'DX OFF' ], ['/menu']])
luci_keyboard.one_time_keyboard=False
luci_keyboard.resize_keyboard=True

foto_keyboard = telegram.ReplyKeyboardMarkup([['CAMERA 1','CAMERA 2','CAMERA 3'],['/menu' ]])
foto_keyboard.one_time_keyboard=False
foto_keyboard.resize_keyboard=True

video_keyboard = telegram.ReplyKeyboardMarkup([['VCAMERA 1','VCAMERA 2','VCAMERA 3'],['/menu' ]])
video_keyboard.one_time_keyboard=False
video_keyboard.resize_keyboard=True
	
# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)

def switch_handler(channel):	
	if channel==INT_SX:
		if GPIO.input(LAMP_SX)==0:
			GPIO.output(LAMP_SX, 1)
		else:
			GPIO.output(LAMP_SX, 0)


def start(bot, update):
	bot.sendMessage(update.message.chat_id, welcome_text)	
	menu(bot,update)

def menu(bot, update):
	bot.sendMessage(update.message.chat_id, text="Seleziona un comando", reply_markup=menu_keyboard)

def send_menu_luci(bot, update):	
	bot.sendMessage(update.message.chat_id, text="Seleziona il comando", reply_markup=luci_keyboard)

def send_menu_foto(bot, update):	
	bot.sendMessage(update.message.chat_id, text="Seleziona la camera", reply_markup=foto_keyboard)

def send_menu_video(bot, update):	
	bot.sendMessage(update.message.chat_id, text="Seleziona la camera", reply_markup=video_keyboard)

def send_logo(bot, update):
	bot.sendPhoto(update.message.chat_id, photo='http://www.acmesystems.it/www/tpc/telegram_bulb.jpg')

def send_pdf(bot, update):
	bot.sendDocument(update.message.chat_id, open('acme.pdf'))

def send_warner(bot, update):
	bot.sendAudio(update.message.chat_id, open("That's All Forks 1937.m4a"))

def send_dog(bot, update):
	os.system("omxplayer -o local angrydog.m4a &")

def send_mute(bot, update):
	os.system("pkill omxplayer")

def send_stop(bot, update):	
	reply_markup = telegram.ReplyKeyboardHide()
	bot.sendMessage(update.message.chat_id, text="Bye", reply_markup=reply_markup)

def echo(bot, update):
	global bouncetime
	
	print "----> Mittente: : [" + update.message.from_user.username + "]"
	print "      Testo     : [" + update.message.text + "]"
	
	#print update.message
	
	if update.message.voice:
		print " ----> VOCE <----"
		#bot.sendVoice(update.message.chat_id, update.message.voice.file_id)
		#https://github.com/python-telegram-bot/python-telegram-bot#api
		newFile = bot.getFile(update.message.voice.file_id)
		newFile.download('voice')
		os.system("omxplayer -o local voice")

	if update.message.audio:
		print " ----> AUDIO <----"
		newFile = bot.getFile(update.message.audio.file_id)
		newFile.download('audio')
		os.system("omxplayer -o local audio &")
		
	if update.message.sticker:
		print " ----> STICKER <----"

	if update.message.text:
		if update.message.text=="SX ON":
			GPIO.remove_event_detect(INT_SX)
			GPIO.output(LAMP_SX, 1)
			GPIO.add_event_detect(INT_SX, GPIO.BOTH, switch_handler, bouncetime)	

		if update.message.text=="SX OFF":
			GPIO.remove_event_detect(INT_SX)
			GPIO.output(LAMP_SX, 0)
			GPIO.add_event_detect(INT_SX, GPIO.BOTH, switch_handler, bouncetime)	

		if update.message.text=="DX ON":
			GPIO.remove_event_detect(INT_SX)
			GPIO.output(LAMP_DX, 1)
			GPIO.add_event_detect(INT_SX, GPIO.BOTH, switch_handler, bouncetime)	

		if update.message.text=="DX OFF":
			GPIO.remove_event_detect(INT_SX)
			GPIO.output(LAMP_DX, 0)
			GPIO.add_event_detect(INT_SX, GPIO.BOTH, switch_handler, bouncetime)	

		if update.message.text=="CAMERA 1":
			os.system("fswebcam -d /dev/video0 -r 320x240 photo0.jpg")
			bot.sendPhoto(update.message.chat_id, photo=open('photo0.jpg'))

		if update.message.text=="CAMERA 2":
			os.system("fswebcam -d /dev/video1 -r 320x240 photo1.jpg")
			bot.sendPhoto(update.message.chat_id, photo=open('photo1.jpg'))

		if update.message.text=="CAMERA 3":
			os.system("fswebcam -d /dev/video2 -r 320x240 photo2.jpg")
			bot.sendPhoto(update.message.chat_id, photo=open('photo2.jpg'))

		#Ancora non funziona
		#if update.message.text=="VCAMERA 1":
		#	os.system("avconv -t 10 -y -f video4linux2 -i /dev/video0 video0.avi")
		#	bot.sendVideo(update.message.chat_id, video=open('video0.avi'))

		if update.message.text=="OK":
			reply_markup = telegram.ReplyKeyboardHide()
			bot.sendMessage(update.message.chat_id, text="Ok", reply_markup=reply_markup)
		
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	# Creata l'EventHandler e gli passa il token assegnato al bot
	# Cambia questo Token con quello che ti ha assegnato BotFather
	
	updater = telegram.Updater("Inserisci qui il Token assegnato da BotFather")	

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# Definisce gli handler di gestione dei comandi
	dp.addTelegramCommandHandler("start", start)
	dp.addTelegramCommandHandler("menu", menu)
	dp.addTelegramCommandHandler("luci", send_menu_luci)
	dp.addTelegramCommandHandler("foto", send_menu_foto)
	dp.addTelegramCommandHandler("video", send_menu_video)
	dp.addTelegramCommandHandler("logo", send_logo)
	dp.addTelegramCommandHandler("pdf", send_pdf)
	dp.addTelegramCommandHandler("warner", send_warner)
	dp.addTelegramCommandHandler("dog", send_dog)
	dp.addTelegramCommandHandler("mute", send_mute)
	dp.addTelegramCommandHandler("stop", send_stop)

	# on noncommand i.e message - echo the message on Telegram
	dp.addTelegramMessageHandler(echo)

	# log all errors
	dp.addErrorHandler(error)

	# Start the Bot
	updater.start_polling()

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
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	LAMP_DX=17
	LAMP_SX=27
	INT_SX=21

	GPIO.setup(LAMP_SX, GPIO.OUT)
	GPIO.setup(LAMP_DX, GPIO.OUT)

	GPIO.output(LAMP_SX, 0)
	GPIO.output(LAMP_DX, 0)

	GPIO.setup(INT_SX, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	
	GPIO.add_event_detect(INT_SX, GPIO.BOTH, switch_handler, bouncetime)	
	main()
