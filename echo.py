#Echo minimale

from telegram import Updater

def echo(bot, update):
	print "Ricevuto: [" + update.message.text + "]"
	bot.sendMessage(update.message.chat_id, "Hai inviato: "+ update.message.text)

#Inserisci qui il token
updater = Updater(token='145378027:AAH5gtii0NzyGLVixxTbJ5qEr2jlkGkFliI')
dispatcher = updater.dispatcher
updater.start_polling()
dispatcher.addTelegramMessageHandler(echo)
updater.idle()


