from telegram import Updater
import logging
import time

help_text = (
	"/start Abilita ricezione allarmi\n"
	"/stop Disabilita ricezione allarmi\n"
)

job_queue=None
chat_ids=[]

# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)

def messaggi_in_arrivo(bot, update):
	print "Messaggio in arrivo"
	pass

def comando_start(bot, update):	
	global chat_ids
	job_queue.bot.sendMessage(update.message.chat_id, text=help_text)
	chat_ids+=[update.message.chat_id]

def comando_stop(bot, update):	
	global chat_ids
	try:
		chat_ids.remove(update.message.chat_id)	
		return
	except ValueError:
		pass

updater = Updater(token='415378027:AAGKpq8P6hggT8oAqoWJ6Y_qcXoXJ2Zn96w')
job_queue = updater.job_queue

dispatcher = updater.dispatcher
dispatcher.addTelegramMessageHandler(messaggi_in_arrivo)
dispatcher.addTelegramCommandHandler("start",comando_start)
dispatcher.addTelegramCommandHandler("stop",comando_stop)
update_queue = updater.start_polling()

counter=0
while True:
	time.sleep(2)
	print "Counter %d\n" % counter 
	counter+=1
	if len(chat_ids)>=0:
		for chat_id in chat_ids:
			job_queue.bot.sendMessage(chat_id, text="Counter: %03d\n" % counter )
	 
