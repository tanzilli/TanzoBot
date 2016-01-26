#Link utili
#https://docs.python.org/2/library/json.html


from telegram import Updater
import os
import os.path
import json 
import random

users=[]
otp=-1

def gestione_messaggi(bot, update):
	global users
	global otp

	user_id=update.message.text

	if len(users)==0:
		users+=[user_id]
		bot.sendMessage(update.message.chat_id, "Congratulazioni sei diventato Admin !")
	else:
		if (user_id in users)==True:
			if users.index(user_id)==0:
				bot.sendMessage(update.message.chat_id, "Ciao Admin")
			else:
				bot.sendMessage(update.message.chat_id, "Ciao Guest")
		else:
			if update.message.text==otp:
				otp=-1
				users+=[user_id]
				bot.sendMessage(update.message.chat_id, "Complimenti sei diventato Guest !")
			else:
				bot.sendMessage(update.message.chat_id, "Allarme ! Utente non autorizzato")

	print "Users:" , users

def comando_start(bot, update):	
	bot.sendMessage(update.message.chat_id, "ok")

def comando_otp(bot, update):
	global otp
	global users
	
	if True:
		otp = "%04d" % (random.random()*9999)
		bot.sendMessage(update.message.chat_id, "One Time Password: %s" % otp )
	else:
		bot.sendMessage(update.message.chat_id, "Comando non autorizzato" )
	
	#user_id=update.message.from_user.id

def comando_cancella_utenti(bot, update):
	global otp
	global users
	
	if True:
		del users[1:]
		bot.sendMessage(update.message.chat_id, "Cancellati tutti gli utenti" )
		
	else:
		bot.sendMessage(update.message.chat_id, "Comando non autorizzato" )
	
	print "Users:" , users
	#user_id=update.message.from_user.id

updater = Updater(token='145378027:AAGKpq8P6hggT8oAqoWJ6Y_qcXoXJ2Zn96w')
dispatcher = updater.dispatcher

dispatcher.addTelegramMessageHandler(gestione_messaggi)
dispatcher.addTelegramCommandHandler("start",comando_start)
dispatcher.addTelegramCommandHandler("otp",comando_otp)
dispatcher.addTelegramCommandHandler("cancella_utenti",comando_cancella_utenti)

updater.start_polling()

updater.idle()

