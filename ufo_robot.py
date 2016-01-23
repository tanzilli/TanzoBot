from telegram import Updater

help_text = ( "/start Apertura Bot\n" 
              "/help Questo help\n" )

def gestione_messaggi(bot, update):
	print "Messaggio in arrivo: [" + update.message.text + "]"
	bot.sendMessage(update.message.chat_id, "Hai inviato: "+ update.message.text)

def comando_start(bot, update):
	print "Ricevuto /start"
	bot.sendMessage(update.message.chat_id, "Ciao %s ! Io sono @ufo_robot !\n" % ( update.message.from_user.first_name))

def comando_help(bot, update):
	global help_text
	print "Ricevuto /help"
	bot.sendMessage(update.message.chat_id, help_text)

#ufo_robot
updater = Updater(token='160682278:AAEZVm4KSGdaUg2lx67y80-gia_tnZDx-DQ')
dispatcher = updater.dispatcher

dispatcher.addTelegramMessageHandler(gestione_messaggi)
dispatcher.addTelegramCommandHandler("start",comando_start)
dispatcher.addTelegramCommandHandler("help",comando_help)

updater.start_polling()

updater.idle()


