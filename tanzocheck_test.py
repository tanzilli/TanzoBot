#Prova d'uso del modulo tanzocheck.py

from telegram import Updater
import logging
from tanzocheck import Check

help_text = (
	"/otp Genera una one time password\n"
	"/userdel Cancella tutti gli utenti\n"
)

check=Check()

# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)

def messaggi_in_arrivo(bot, update):
	#Prima di elaborare un messaggio controlla che tipo di utente e':
	user_type= check.user(bot,update)
	
	if user_type=="none":
		bot.sendMessage(update.message.chat_id, "Accesso negato")
		return

	if user_type=="user":
		bot.sendMessage(update.message.chat_id, "User")
		return

	if user_type=="su":
		bot.sendMessage(update.message.chat_id, "Super user")
		return

def comando_start(bot, update):	
	#Prima di elaborare un comando controlla che tipo di utente e':
	user_type= check.user(bot,update)
	
	if user_type=="none":
		bot.sendMessage(update.message.chat_id, "Accesso negato")
		return

	if user_type=="user":
		bot.sendMessage(update.message.chat_id, "User: %s" % help_text )
		return

	if user_type=="su":
		bot.sendMessage(update.message.chat_id, "Super user: %s" % help_text)
		return

updater = Updater(token='415378027:AAGKpq8P6hggT8oAqoWJ6Y_qcXoXJ2Zn96w')
dispatcher = updater.dispatcher
dispatcher.addTelegramMessageHandler(messaggi_in_arrivo)
dispatcher.addTelegramCommandHandler("start",comando_start)
check.addTanzoCheckCommandHandler(dispatcher)
updater.start_polling()
updater.idle()
