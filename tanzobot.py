#!/usr/bin/env python
#http://www.acmesystems.it/tpc

import telegram
import logging

import RPi.GPIO as GPIO
import time
import os

emoji = telegram.Emoji

help_text= (
			"Benvenuto ! Io sono @TanzoBot..." + emoji.SMILING_FACE_WITH_SUNGLASSES + "\n"
			"Menu dei comandi disponibili:\n"
			"/help Elenco comandi\n"
			"/luci Attuazione rele\n"
			"/webcam Scatta una foto da webcam\n"
			"/webimage Immagine presa da web\n"
			"/pdf Invia un PDF memorizzato su microSD\n"
			"/mp3 Invia un MP3 memorizzato su microSD\n"
			"/dog Riproduce il ringhio di un cane sugli speaker\n" 
			"/mute Blocca omxplayer\n"
			)
			
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LAMP_DX=17
LAMP_SX=27

GPIO.setup(LAMP_SX, GPIO.OUT)
GPIO.setup(LAMP_DX, GPIO.OUT)

GPIO.output(LAMP_SX, 0)
GPIO.output(LAMP_DX, 0)

# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
	bot.sendMessage(update.message.chat_id, text=help_text)

def help(bot, update):
	bot.sendMessage(update.message.chat_id, text=help_text)

def send_luci(bot, update):	
	custom_keyboard = [[ 'LAMP SX ON', 'LAMP DX ON' ],[ 'LAMP SX OFF', 'LAMP DX OFF' ], ['/webcam'],  ['OK']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	reply_markup.one_time_keyboard=False
	reply_markup.resize_keyboard=True
	bot.sendMessage(update.message.chat_id, text="Seleziona il comando", reply_markup=reply_markup)


def send_foto_da_webcam(bot, update):	
	custom_keyboard = [['CAMERA 1','CAMERA 2','CAMERA 3'],['/luci'],[ 'OK' ]]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	reply_markup.one_time_keyboard=False
	reply_markup.resize_keyboard=True
	bot.sendMessage(update.message.chat_id, text="Seleziona la camera", reply_markup=reply_markup)

def send_webimage(bot, update):
	bot.sendPhoto(update.message.chat_id, photo='http://www.acmesystems.it/www/tpc/telegram_bulb.jpg')

def send_pdf(bot, update):
	bot.sendDocument(update.message.chat_id, open('acme.pdf'))

def send_mp3(bot, update):
	bot.sendAudio(update.message.chat_id, open('idilio.mp3'))

def send_dog(bot, update):
	os.system("omxplayer -o local angrydog.m4a &")

def send_mute(bot, update):
	os.system("pkill omxplayer")

def send_stop(bot, update):	
	reply_markup = telegram.ReplyKeyboardHide()
	bot.sendMessage(update.message.chat_id, text="Bye", reply_markup=reply_markup)

def echo(bot, update):
	
	print "----> Mittente: : [" + update.message.from_user.username + "]"
	print "      Testo     : [" + update.message.text + "]"
	
	print update.message
	
	if update.message.voice:
		print " ----> VOCE <----"
		#bot.sendVoice(update.message.chat_id, update.message.voice.file_id)
		#https://github.com/python-telegram-bot/python-telegram-bot#api
		newFile = bot.getFile(update.message.voice.file_id)
		newFile.download('voice')
		os.system("omxplayer -o local voice &")

	if update.message.audio:
		print " ----> AUDIO <----"
		#bot.sendVoice(update.message.chat_id, update.message.voice.file_id)
		#https://github.com/python-telegram-bot/python-telegram-bot#api
		newFile = bot.getFile(update.message.audio.file_id)
		newFile.download('audio')
		os.system("omxplayer -o local audio &")
		
	if update.message.sticker:
		print " ----> STICKER <----"

	if update.message.text:
		if update.message.text=="LAMP SX ON":
			GPIO.output(LAMP_SX, 1)

		if update.message.text=="LAMP SX OFF":
			GPIO.output(LAMP_SX, 0)

		if update.message.text=="LAMP DX ON":
			GPIO.output(LAMP_DX, 1)

		if update.message.text=="LAMP DX OFF":
			GPIO.output(LAMP_DX, 0)

		if update.message.text=="CAMERA 1":
			os.system("fswebcam -d /dev/video0 -r 640x360 photo0.jpg")
			bot.sendPhoto(update.message.chat_id, photo=open('photo0.jpg'))

		if update.message.text=="CAMERA 2":
			os.system("fswebcam -d /dev/video1 -r 640x360 photo1.jpg")
			bot.sendPhoto(update.message.chat_id, photo=open('photo1.jpg'))

		if update.message.text=="CAMERA 3":
			os.system("fswebcam -d /dev/video2 -r 640x360 photo2.jpg")
			bot.sendPhoto(update.message.chat_id, photo=open('photo2.jpg'))

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
	dp.addTelegramCommandHandler("help", help)
	dp.addTelegramCommandHandler("luci", send_luci)
	dp.addTelegramCommandHandler("webcam", send_foto_da_webcam)
	dp.addTelegramCommandHandler("webimage", send_webimage)
	dp.addTelegramCommandHandler("pdf", send_pdf)
	dp.addTelegramCommandHandler("mp3", send_mp3)
	dp.addTelegramCommandHandler("dog", send_dog)
	dp.addTelegramCommandHandler("mute", send_mute)
	dp.addTelegramCommandHandler("stop", send_stop)

	# on noncommand i.e message - echo the message on Telegram
	dp.addTelegramMessageHandler(echo)

	# log all errors
	dp.addErrorHandler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until the you presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
	main()

#Link utili:
#https://core.telegram.org/bots
#https://irazasyed.github.io/telegram-bot-sdk/usage/keyboards/
#https://github.com/python-telegram-bot/python-telegram-bot/blob/master/telegram/replykeyboardmarkup.py
