from telegram import Updater

def gestione_messaggi(bot, update):
	bot.sendMessage(update.message.chat_id, "Hai inviato: "+ update.message.text)

def comando_start(bot, update):
	mittente = update.message.from_user.first_name
	bot.sendMessage(update.message.chat_id, "Ciao %s !\n" % mittente)

updater = Updater(token='160682278:AAEZVm4KSGdaUg2lx67y80-gia_tnZDx-DQ')
dispatcher = updater.dispatcher

dispatcher.addTelegramMessageHandler(gestione_messaggi)
dispatcher.addTelegramCommandHandler("start",comando_start)

updater.start_polling()

updater.idle()


