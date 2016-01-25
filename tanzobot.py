#!/usr/bin/env python
#http://www.acmesystems.it/tpc
#https://github.com/python-telegram-bot/python-telegram-bot#api

# Sergio Tanzilli - sergio@tanzilli.com
 
#Inserire nel file mytokens.py il token assegnato da BotFather
import mytokens

import telegram				#Wrapper Bot API Telegram
import logging

import RPi.GPIO as GPIO		#Gestione GPIO
import time
import os					
import pygal				# Creazione grafici
import picamera				# Gestione picam

# We use this var to save the last chat id, so we can reply to it
last_chat_id = 0

#Contatori usati per avere un buffer di 10 file per ogni 
#messaggio 
video_file_counter=0
photo_file_counter=0
voice_file_counter=0
graph_file_counter=0

update_queue = 0

menu_keyboard = telegram.ReplyKeyboardMarkup([['/rele','/foto','/video','/logo','/start'],['/dog','/music','/jingle','/pdf','/graph'],['/mute','/menu']])
menu_keyboard.one_time_keyboard=False
menu_keyboard.resize_keyboard=True

rele_keyboard = telegram.ReplyKeyboardMarkup([[ 'REL1 ON', 'REL2 ON' ],[ 'REL1 OFF', 'REL2 OFF' ], ['/menu']])
rele_keyboard.one_time_keyboard=False
rele_keyboard.resize_keyboard=True

comandi=["rele","foto","video","logo","pdf","music","dog","jingle","graph"]
chiamate=[0,0,0,0,0,0,0,0,0]

startup_time = "Comandi usati dalle %s ore %s" % (time.strftime("%d/%m/%Y"),time.strftime("%H:%M:%S"))
	
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
	print update_queue
	update_queue.put("pir_alarm");

def start(bot, update):
	bot.sendMessage(update.message.chat_id, "Ciao %s ! Io sono TanzoBot.\n" % ( update.message.from_user.first_name))
	menu(bot,update)

def menu(bot, update):
	bot.sendMessage(update.message.chat_id, text="Seleziona un comando dalla tastiera qui sotto oppure invia un messaggio vocale da riprodurre sulle casse di TanzoBot...", reply_markup=menu_keyboard)

def send_menu_rele(bot, update):	
	global comandi
	global chiamate
	
	chiamate[comandi.index("rele")]+=1
	bot.sendMessage(update.message.chat_id, text="Puoi accendere o spegnere entrambe i rele collegati a TanzoBot...", reply_markup=rele_keyboard)

#Pacchetti da installare per poter utilizzare la picam
#sudo apt-get install python-picamera

#Doc API
#http://picamera.readthedocs.org/en/release-1.10/quickstart.html

def send_video(bot, update):	
	global comandi
	global chiamate
	global video_file_counter
		
	chiamate[comandi.index("video")]+=1

	video_file_counter=video_file_counter+1		
	if video_file_counter==10:
		video_file_counter=1

	os.system("rm video%d.mp4" % video_file_counter)	
	os.system("rm video%d.h264" % video_file_counter)	

	bot.sendMessage(update.message.chat_id, "Sto girando un video di 4 secondi, un momento prego...")
	os.system("omxplayer -o local movie_camera_sound.mp3 &")
	time.sleep(3.7)
	with picamera.PiCamera() as camera:
		camera.resolution = (320,240)
		camera.start_recording('video%d.h264' % video_file_counter)
		camera.wait_recording(4)
		camera.stop_recording()

	os.system("MP4Box -add video%d.h264 video%d.mp4" %(video_file_counter,video_file_counter))
	bot.sendVideo(update.message.chat_id, video=open('video%d.mp4' % video_file_counter))

#http://picamera.readthedocs.org/en/release-1.10/quickstart.html
def send_photo(bot, update):
	global comandi
	global chiamate
	global photo_file_counter

	chiamate[comandi.index("foto")]+=1

	photo_file_counter=photo_file_counter+1		
	if photo_file_counter==10:
		photo_file_counter=1

	os.system("rm photo%d.jpg" % photo_file_counter)	
	
	bot.sendMessage(update.message.chat_id, "Sto scattando la foto, un momento prego...")
	os.system("omxplayer -o local saycheese.mp3 &")
	time.sleep(2.5)
	with picamera.PiCamera() as camera:
		camera.resolution = (1280,720)
		camera.capture('photo%d.jpg' % photo_file_counter)

	bot.sendPhoto(update.message.chat_id, photo=open('photo%d.jpg' % photo_file_counter))

#Pacchetti da installare per poter generare grafici

#sudo apt-get install python-pip
#sudo pip install pygal
#sudo pip install tinycss
#sudo apt-get install python-cairosvg
#sudo apt-get install python-lxml
#sudo apt-get install python-cssselect
		
def send_graph(bot, update):
	global comandi
	global chiamate
	global graph_file_counter
	
	chiamate[comandi.index("graph")]+=1
	
	graph_file_counter=graph_file_counter+1		
	if graph_file_counter==10:
		graph_file_counter=1

	os.system("rm graph%d.png" % graph_file_counter)	
	
	bot.sendMessage(update.message.chat_id, "Genero la statistica dei comandi ricevuti finora...")

	line_chart = pygal.HorizontalBar()
	line_chart.title = startup_time
	line_chart.add('rele', chiamate[comandi.index("rele")])
	line_chart.add('foto', chiamate[comandi.index("foto")])
	line_chart.add('video', chiamate[comandi.index("video")])
	line_chart.add('logo', chiamate[comandi.index("logo")])
	line_chart.add('pdf', chiamate[comandi.index("pdf")])
	line_chart.add('music', chiamate[comandi.index("music")])
	line_chart.add('dog', chiamate[comandi.index("dog")])
	line_chart.add('jingle', chiamate[comandi.index("jingle")])
	line_chart.add('graph', chiamate[comandi.index("graph")])
	line_chart.render_to_png('graph%d.png' % graph_file_counter)

	bot.sendPhoto(update.message.chat_id,open('graph%d.png' % graph_file_counter))


def send_logo(bot, update):
	global comandi
	global chiamate
	
	chiamate[comandi.index("logo")]+=1

	bot.sendMessage(update.message.chat_id, "Sto scaricando il Logo di TanzoBot da Web, un momento prego...")			
	bot.sendPhoto(update.message.chat_id, photo='http://www.acmesystems.it/www/tpc/telegram_bulb.jpg')
	bot.sendMessage(update.message.chat_id, "http://www.acmesystems.it/tpc")			

def send_pdf(bot, update):
	global comandi
	global chiamate

	chiamate[comandi.index("pdf")]+=1
	bot.sendMessage(update.message.chat_id, "Ti sto inviando un documento pdf, un momento prego...")			
	bot.sendDocument(update.message.chat_id, open('acme.pdf'))

def send_music(bot, update):
	global comandi
	global chiamate

	chiamate[comandi.index("music")]+=1
	bot.sendMessage(update.message.chat_id, "Ti sto inviando un file audio, un momento prego...")			
	bot.sendAudio(update.message.chat_id, open("thats_all_folks.m4a"))

def send_dog(bot, update):
	global comandi
	global chiamate

	chiamate[comandi.index("dog")]+=1
	bot.sendMessage(update.message.chat_id, "Hai fatto abbaiare i cani :-)")			
	os.system("omxplayer -o local angrydog.m4a &")

def send_jingle(bot, update):
	global comandi
	global chiamate

	chiamate[comandi.index("jingle")]+=1
	bot.sendMessage(update.message.chat_id, "Hai fatto partire il Jingle Acme ! :-)")			
	os.system("omxplayer -o local thats_all_folks.m4a &")

def send_mute(bot, update):
	bot.sendMessage(update.message.chat_id, "Hai messo in stop tutti i sound effects.")			
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

	last_chat_id = update.message.chat_id
	logger.info("New message\nFrom: %s\nchat_id: %d\nText: %s" %
				(update.message.from_user,
				 update.message.chat_id,
				 update.message.text))

def echo(bot, update):
	global voice_file_counter
	
	print "----> Mittente: : [" + update.message.from_user.username + "]"
	print "      Testo     : [" + update.message.text + "]"
	
	if update.message.voice:
		print " ----> VOCE <----"
				
		voice_file_counter=voice_file_counter+1		
		if voice_file_counter==10:
			voice_file_counter=1

		os.system("rm voice%d" % voice_file_counter)	

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
			bot.sendMessage(update.message.chat_id, "Hai acceso il rele 1")
			GPIO.output(REL1, 1)

		if update.message.text=="REL1 OFF":
			bot.sendMessage(update.message.chat_id, "Hai spento il rele 1")
			GPIO.output(REL1, 0)

		if update.message.text=="REL2 ON":
			bot.sendMessage(update.message.chat_id, "Hai acceso il rele 2")			
			GPIO.output(REL2, 1)

		if update.message.text=="REL2 OFF":
			bot.sendMessage(update.message.chat_id, "Hai spento il rele 2")			
			GPIO.output(REL2, 0)

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
	dp.addTelegramCommandHandler("foto", send_photo)
	dp.addTelegramCommandHandler("video", send_video)
	dp.addTelegramCommandHandler("logo", send_logo)
	dp.addTelegramCommandHandler("pdf", send_pdf)
	dp.addTelegramCommandHandler("music", send_music)
	dp.addTelegramCommandHandler("dog", send_dog)
	dp.addTelegramCommandHandler("jingle", send_jingle)
	dp.addTelegramCommandHandler("graph", send_graph)
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
