#!/usr/bin/env python

import telegram
import logging

import RPi.GPIO as GPIO
import time
import os

help_text= (
			"Comandi disponibili:\n"
			"/comandi Tastiera comandi\n"
			"/foto Scatta una Foto\n"
			"/volantino Pdf della nuova brochure NoiNet\n"
			"/logo Logo NoiNet\n"
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
#emoji = telegram.Emoji

def start(bot, update):
	bot.sendMessage(update.message.chat_id, text='Benvenuto. Io sono @TanzoBot ' + telegram.Emoji.SMILING_FACE_WITH_SUNGLASSES)
	bot.sendMessage(update.message.chat_id, text=help_text)

def help(bot, update):
	bot.sendMessage(update.message.chat_id, text=help_text)

def send_logo_noinet(bot, update):
	bot.sendPhoto(update.message.chat_id, photo='http://www.noinet.eu/wp-content/uploads/2013/06/Noinet_pubblicita-300x210.jpg')

def send_volantino_noinet(bot, update):
	bot.sendDocument(update.message.chat_id, open('noinet.pdf'))

def send_comandi(bot, update):	
	custom_keyboard = [['RELE 1'],['RELE 2'],[ 'Led ON', 'Led OFF' ], ['Fatto']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	reply_markup.one_time_keyboard=False
	reply_markup.resize_keyboard=True
	bot.sendMessage(update.message.chat_id, text="Seleziona il comando", reply_markup=reply_markup)

def send_foto(bot, update):	
	custom_keyboard = [['CAMERA 1'],['CAMERA 2'],[ 'Fatto' ]]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	reply_markup.one_time_keyboard=False
	reply_markup.resize_keyboard=True
	bot.sendMessage(update.message.chat_id, text="Seleziona la webcam", reply_markup=reply_markup)

def send_stop(bot, update):	
	reply_markup = telegram.ReplyKeyboardHide()
	bot.sendMessage(update.message.chat_id, text="Bye", reply_markup=reply_markup)

def echo(bot, update):
	
	print "Messaggio dallo user " + update.message.from_user.username
	
	if update.message.text=="RELE 1":
		GPIO.output(RELE1, 1)
		time.sleep(1)
		GPIO.output(RELE1, 0)

	if update.message.text=="RELE 2":
		GPIO.output(RELE2, 1)
		time.sleep(1)
		GPIO.output(RELE2, 0)

	if update.message.text=="Led ON":
		GPIO.output(LED, 1)

	if update.message.text=="Led OFF":
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


		
	bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	# Create the EventHandler and pass it your bot's token.
	updater = telegram.Updater("Inserisci qui il Token assegnato da BotFather")

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.addTelegramCommandHandler("start", start)
	dp.addTelegramCommandHandler("help", help)
	dp.addTelegramCommandHandler("comandi", send_comandi)
	dp.addTelegramCommandHandler("foto", send_foto)
	dp.addTelegramCommandHandler("logo", send_logo_noinet)
	dp.addTelegramCommandHandler("volantino", send_volantino_noinet)
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
