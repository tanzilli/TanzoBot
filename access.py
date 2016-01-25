#Link utili
#https://docs.python.org/2/library/json.html


from telegram import Updater
import os
import os.path
import json 

def gestione_messaggi(bot, update):
	bot.sendMessage(update.message.chat_id, "Hai inviato: "+ update.message.text)

def comando_start(bot, update):
	bot.sendMessage(update.message.chat_id, "ok")

	print update.message.from_user	
	
	user = {
		"first_name": update.message.from_user.first_name,
		"last_name": update.message.from_user.last_name,
		"id": update.message.from_user.id,
		"username": update.message.from_user.username,
	}
	

	if os.path.exists("users.json"):
		print "File exists"
		in_file = open("users.json","r")
		users = json.load(in_file)
		in_file.close()
		
		print users
	else:
		print "File doesn't exist"
		#Se il file users.json non esiste prende il primo contatto che arriva come admin 
		user["type"]="admin"
		out_file = open("users.json","w")
		json.dump(user,out_file, indent=4)                                    
		out_file.close()


updater = Updater(token='145378027:AAGKpq8P6hggT8oAqoWJ6Y_qcXoXJ2Zn96w')
dispatcher = updater.dispatcher

dispatcher.addTelegramMessageHandler(gestione_messaggi)
dispatcher.addTelegramCommandHandler("start",comando_start)

updater.start_polling()

updater.idle()

