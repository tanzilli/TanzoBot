#!/usr/bin/env python
#http://www.acmesystems.it/tpc

import telegram
import logging

import RPi.GPIO as GPIO
import time
import os

help_text= (
			"Comandi disponibili:\n"
			"/rele Attuazione rele\n"
			"/webcam Scatta una foto da webcam\n"
			"/webimage Prende una immagine da web e la invia\n"
			"/pdf Invia un PDF memorizzato su microSD\n"
			"\n"
			"Per info http://www.acmesystems.it/tpc\n"
			)
			
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED=4
RELE1=17
RELE2=27

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(RELE1, GPIO.OUT)
GPIO.setup(RELE2, GPIO.OUT)

GPIO.output(LED, 0)
GPIO.output(RELE1, 0)
GPIO.output(RELE2, 0)

# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)
emoji = telegram.Emoji

def start(bot, update):
	bot.sendMessage(update.message.chat_id, text='Benvenuto. Io sono @TanzoBot !' + emoji.SMILING_FACE_WITH_SUNGLASSES)
	bot.sendMessage(update.message.chat_id, text=help_text)

def help(bot, update):
	bot.sendMessage(update.message.chat_id, text=help_text)

def send_comandi_rele(bot, update):	
	custom_keyboard = [['RELE 1'],['RELE 2'],[ 'Led ON', 'Led OFF' ], ['Fatto']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	reply_markup.one_time_keyboard=False
	reply_markup.resize_keyboard=True
	bot.sendMessage(update.message.chat_id, text="Seleziona il comando", reply_markup=reply_markup)


def send_foto_da_webcam(bot, update):	
	custom_keyboard = [['CAMERA 1'],['CAMERA 2'],[ 'Fatto' ]]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	reply_markup.one_time_keyboard=False
	reply_markup.resize_keyboard=True
	bot.sendMessage(update.message.chat_id, text="Seleziona la camera", reply_markup=reply_markup)

def send_webimage(bot, update):
	bot.sendPhoto(update.message.chat_id, photo='http://www.acmesystems.it/www/tpc/telegram_bulb.jpg')

def send_pdf(bot, update):
	bot.sendDocument(update.message.chat_id, open('acme.pdf'))

def send_stop(bot, update):	
	reply_markup = telegram.ReplyKeyboardHide()
	bot.sendMessage(update.message.chat_id, text="Bye", reply_markup=reply_markup)

def echo(bot, update):
	
	print "----> Mittente: : [" + update.message.from_user.username + "]"
	print "      Testo     : [" + update.message.text + "]"
	
	if update.message.text=="RELE 1":
		print "Rele 1 acceso per 1 sec"
		bot.sendMessage(update.message.chat_id, "Rele 1 acceso per 1 sec")
		GPIO.output(RELE1, 1)
		time.sleep(1)
		GPIO.output(RELE1, 0)

	if update.message.text=="RELE 2":
		print "Rele 2 acceso per 1 sec"
		bot.sendMessage(update.message.chat_id, "Rele 2 acceso per 1 sec")
		GPIO.output(RELE2, 1)
		time.sleep(1)
		GPIO.output(RELE2, 0)

	if update.message.text=="Led ON":
		print "Led acceso"
		bot.sendMessage(update.message.chat_id, "Led acceso")
		GPIO.output(LED, 1)

	if update.message.text=="Led OFF":
		print "Led spento"
		bot.sendMessage(update.message.chat_id, "Led spento")
		GPIO.output(LED, 0)

	if update.message.text=="CAMERA 1":
		bot.sendMessage(update.message.chat_id, text='Ricezione foto da camera 1...')
		os.system("fswebcam -d /dev/video0 -r 1280x720 photo1.jpg")
		bot.sendPhoto(update.message.chat_id, photo=open('photo1.jpg'))

	if update.message.text=="CAMERA 2":
		bot.sendMessage(update.message.chat_id, text='Ricezione foto da camera 2...')
		os.system("fswebcam -d /dev/video1 -r 1280x720 photo2.jpg")
		bot.sendPhoto(update.message.chat_id, photo=open('photo2.jpg'))

	if update.message.text=="Fatto":
		reply_markup = telegram.ReplyKeyboardHide()
		bot.sendMessage(update.message.chat_id, text="Ok", reply_markup=reply_markup)
		
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	# Creata l'EventHandler e gli passa il token assegnato al bot
	updater = telegram.Updater("Inserisci qui il Token assegnato da BotFather")

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# Definisce gli handler di gestione dei comandi
	dp.addTelegramCommandHandler("start", start)
	dp.addTelegramCommandHandler("help", help)
	dp.addTelegramCommandHandler("rele", send_comandi_rele)
	dp.addTelegramCommandHandler("webcam", send_foto_da_webcam)
	dp.addTelegramCommandHandler("webimage", send_webimage)
	dp.addTelegramCommandHandler("pdf", send_pdf)
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
