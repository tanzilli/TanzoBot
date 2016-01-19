#!/usr/bin/env python
#http://www.acmesystems.it/tpc

#Inserire nel file mytokens.py il token assegnato da BotFather
import mytokens

import telegram
import logging

import RPi.GPIO as GPIO
import time
import os

# We use this var to save the last chat id, so we can reply to it
last_chat_id = 0

voice_file_counter=0

emoji = telegram.Emoji
update_queue = 0

welcome_text = 	"Benvenuto ! Io sono @TanzoBot v 1.3" + emoji.SMILING_FACE_WITH_SUNGLASSES + "\n" 

menu_keyboard = telegram.ReplyKeyboardMarkup([['/rele','/foto','/video','/logo','/start'],['/dog','/music','/jingle','/pdf'],['/mute','/menu']])
menu_keyboard.one_time_keyboard=False
menu_keyboard.resize_keyboard=True

rele_keyboard = telegram.ReplyKeyboardMarkup([[ 'REL1 ON', 'REL2 ON' ],[ 'REL1 OFF', 'REL2 OFF' ], ['/menu']])
rele_keyboard.one_time_keyboard=False
rele_keyboard.resize_keyboard=True

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
	if GPIO.input(REL1)==0:
		GPIO.output(REL1, 1)
	else:
		GPIO.output(REL1, 0)

def pir_handler(channel):
	global update_queue
	
	print "PIR alarm"
	update_queue.put("pir_alarm");
	#os.system("fswebcam -d /dev/video0 -r 320x240 photo0.jpg")
	#bot.sendPhoto(update.message.chat_id, photo=open('photo0.jpg'))

def start(bot, update):
	bot.sendMessage(update.message.chat_id, welcome_text)	
	menu(bot,update)

def menu(bot, update):
	bot.sendMessage(update.message.chat_id, text="Seleziona un comando", reply_markup=menu_keyboard)

def send_menu_rele(bot, update):	
	bot.sendMessage(update.message.chat_id, text="Seleziona il comando", reply_markup=rele_keyboard)

def send_menu_foto(bot, update):	
	bot.sendMessage(update.message.chat_id, text="Seleziona la camera", reply_markup=foto_keyboard)

def send_menu_video(bot, update):	
	bot.sendMessage(update.message.chat_id,"Non ancora implementato, pardon ... !")
	#bot.sendMessage(update.message.chat_id, text="Seleziona la camera", reply_markup=video_keyboard)

def send_logo(bot, update):
	bot.sendPhoto(update.message.chat_id, photo='http://www.acmesystems.it/www/tpc/telegram_bulb.jpg')

def send_pdf(bot, update):
	bot.sendDocument(update.message.chat_id, open('acme.pdf'))

def send_music(bot, update):
	bot.sendAudio(update.message.chat_id, open("thats_all_folks.m4a"))

def send_dog(bot, update):
	os.system("omxplayer -o local angrydog.m4a &")

def send_jingle(bot, update):
	os.system("omxplayer -o local thats_all_folks.m4a &")

def send_mute(bot, update):
	os.system("pkill omxplayer")

def send_stop(bot, update):	
	reply_markup = telegram.ReplyKeyboardHide()
	bot.sendMessage(update.message.chat_id, text="Bye", reply_markup=reply_markup)

def send_pir_alarm(bot, update):	
	if last_chat_id is not 0:
		bot.sendMessage(chat_id=last_chat_id, text="PIR Alarm")

def any_message(bot, update):
	# Save last chat_id to use in reply handler
	global last_chat_id

	print "any_message"

	last_chat_id = update.message.chat_id

	logger.info("New message\nFrom: %s\nchat_id: %d\nText: %s" %
				(update.message.from_user,
				 update.message.chat_id,
				 update.message.text))


def echo(bot, update):
	global voice_file_counter
	
	print "----> Mittente: : [" + update.message.from_user.username + "]"
	print "      Testo     : [" + update.message.text + "]"
	
	#print update.message
	
	if update.message.voice:
		print " ----> VOCE <----"
		#bot.sendVoice(update.message.chat_id, update.message.voice.file_id)
		#https://github.com/python-telegram-bot/python-telegram-bot#api
				
		voice_file_counter=voice_file_counter+1		
		if voice_file_counter==10:
			voice_file_counter=1

		newFile = bot.getFile(update.message.voice.file_id)
		newFile.download('voice%d' % voice_file_counter )
		os.system("omxplayer -o local voice%d &" % voice_file_counter)

	if update.message.audio:
		print " ----> AUDIO <----"
		newFile = bot.getFile(update.message.audio.file_id)
		newFile.download('audio')
		os.system("omxplayer -o local audio &")

	if update.message.video:
		print " ----> VIDEO <----"
		newFile = bot.getFile(update.message.video.file_id)
		newFile.download('video')
		os.system("omxplayer -o local video &")
		
	if update.message.sticker:
		print " ----> STICKER <----"

	if update.message.text:
		if update.message.text=="REL1 ON":
			GPIO.output(REL1, 1)

		if update.message.text=="REL1 OFF":
			GPIO.output(REL1, 0)

		if update.message.text=="REL2 ON":
			GPIO.output(REL2, 1)

		if update.message.text=="REL2 OFF":
			GPIO.output(REL2, 0)

		if update.message.text=="CAMERA 1":
			os.system("fswebcam -d /dev/video0 -r 320x240 photo0.jpg")
			bot.sendPhoto(update.message.chat_id, photo=open('photo0.jpg'))

		if update.message.text=="CAMERA 2":
			os.system("fswebcam -d /dev/video1 -r 320x240 photo1.jpg")
			bot.sendPhoto(update.message.chat_id, photo=open('photo1.jpg'))

		if update.message.text=="CAMERA 3":
			os.system("fswebcam -d /dev/video2 -r 320x240 photo2.jpg")
			bot.sendPhoto(update.message.chat_id, photo=open('photo2.jpg'))

		if update.message.text=="VCAMERA 1":
			os.system("avconv -t 10 -y -f video4linux2 -i /dev/video0 video0.mp4")
			bot.sendVideo(update.message.chat_id, video=open('video0.mp4'))

		if update.message.text=="VCAMERA 2":
			os.system("avconv -t 10 -y -f video4linux2 -i /dev/video0 video1.mp4")
			bot.sendVideo(update.message.chat_id, video=open('video1.mp4'))

		if update.message.text=="VCAMERA 2":
			os.system("avconv -t 10 -y -f video4linux2 -i /dev/video0 video2.mp4")
			bot.sendVideo(update.message.chat_id, video=open('video2.mp4'))

		if update.message.text=="OK":
			reply_markup = telegram.ReplyKeyboardHide()
			bot.sendMessage(update.message.chat_id, text="Ok", reply_markup=reply_markup)
		
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():	
	global update_queue
	
	# Creata l'EventHandler e gli passa il token assegnato al bot
	# Cambia questo Token con quello che ti ha assegnato BotFather
	# Il token e' memorizzato nel file mytoken.py
	print "Token:" , mytokens.token_string
	updater = telegram.Updater(mytokens.token_string)	
	
	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# Definisce gli handler di gestione dei comandi
	dp.addTelegramCommandHandler("start", start)
	dp.addTelegramCommandHandler("menu", menu)
	dp.addTelegramCommandHandler("help", menu)
	dp.addTelegramCommandHandler("rele", send_menu_rele)
	dp.addTelegramCommandHandler("foto", send_menu_foto)
	dp.addTelegramCommandHandler("video", send_menu_video)
	dp.addTelegramCommandHandler("logo", send_logo)
	dp.addTelegramCommandHandler("pdf", send_pdf)
	dp.addTelegramCommandHandler("music", send_music)
	dp.addTelegramCommandHandler("dog", send_dog)
	dp.addTelegramCommandHandler("jingle", send_jingle)
	dp.addTelegramCommandHandler("mute", send_mute)
	dp.addTelegramCommandHandler("stop", send_stop)
	
    # Regex handlers will receive all updates on which their regex matches
	dp.addTelegramRegexHandler('.*', any_message)

	dp.addStringCommandHandler('pir_alarm', send_pir_alarm)
	
	
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
	GPIO.setwarnings(False)

	REL1=13
	REL2=11
	INFRAROSSO=18
	INTERRUTTORE=40

	GPIO.setup(REL1, GPIO.OUT)
	GPIO.setup(REL2, GPIO.OUT)

	GPIO.output(REL1, 0)
	GPIO.output(REL2, 0)

	GPIO.setup(INFRAROSSO, GPIO.IN, pull_up_down=GPIO.PUD_UP)	
	GPIO.add_event_detect(INFRAROSSO, GPIO.RISING, pir_handler, 200)
	
	GPIO.setup(INTERRUTTORE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(INTERRUTTORE, GPIO.BOTH, switch_handler, 200)	

	main()
