# Semplice classe per il controllo degli accessi
# verso un Bot Telegram
# Sergio Tanzilli - sergio@tanzilli.com - @SergioTanzilli

import random
import json
import os.path

class Check():
	user_file='user_list.json'
	user_ids=[]
	user_usernames=[]
	user_first_names=[]
	user_last_names=[]
	otp=-1

	def __init__(self):
		print "TanzoCheck 0.4 is fired..."
		if os.path.exists(self.user_file):
			with open(self.user_file) as json_file:
				json_data=json.load(json_file)
				self.user_ids=json_data[0]
				self.user_usernames=json_data[1]
				self.user_first_names=json_data[2]
				self.user_last_names=json_data[3]
				
	def save_user_list(self):
		user_data=[self.user_ids,self.user_usernames,self.user_first_names,self.user_last_names]
		with open(self.user_file, 'w') as outfile:
			json.dump(user_data, outfile,indent=4)		
		print "Saving user_list.json:"
		print user_data			
	
	#Controlla se l'utente e' uno user autorizzato
	def user(self,bot,update):

		#Se non c'e' lista di utenti il primo che accede diventa su
		if len(self.user_ids)==0:
			self.user_ids+=[update.message.from_user.id]
			self.user_usernames+=[update.message.from_user.username]
			self.user_first_names+=[update.message.from_user.first_name]
			self.user_last_names+=[update.message.from_user.last_name]
			self.save_user_list()
			print "Primo accesso"
			print "id: %s" % update.message.from_user.id
			print "username: %s" % update.message.from_user.username
			print "first_name: %s" % update.message.from_user.first_name
			print "last_name: %s" % update.message.from_user.last_name
			return "su"

		#Se lo user e' in lista nella posizione 0 ritorna su
		if self.user_ids[0]==update.message.from_user.id:
			print "Accesso dal super user"
			return "su"

		#Se lo user e' in lista torna "user"
		try:
			self.user_ids.index(update.message.from_user.id)	
			print "Accesso da user"
			return "user"
		#Se non lo e' ma ha fornito un otp memorizza e torna "user"
		except ValueError:
			if update.message.text==self.otp:
				self.otp=-1
				self.user_ids+=[update.message.from_user.id]
				self.user_usernames+=[update.message.from_user.username]
				self.user_first_names+=[update.message.from_user.first_name]
				self.user_last_names+=[update.message.from_user.last_name]
				self.save_user_list()
				print "Accesso da nuovo user con otp"
				return "user"

		#Negli altri casi nega l'accesso
		print "Accesso non autorizzato"
		return "none"		

	def cmd_otp(self,bot, update):
		if self.user(bot,update)!="su":
			print "Accesso al comandi /su negato"
			return
			
		if True:
			self.otp = "%04d" % (random.random()*9999)
			bot.sendMessage(update.message.chat_id, "One Time Password: %s" % self.otp )
			print "Generazione one time password: %s" % self.otp
		else:
			print "Comando non autorizzato"
		

	def cmd_userlist(self,bot, update):
		if self.user(bot,update)!="su":
			print "Accesso non autorizzato"
			return

		outlist=""
		for i in range (0,len(self.user_ids)):
			outlist+="%d) %s, %s " %  (i+1,self.user_first_names[i],self.user_last_names[i])
			
			if len(self.user_usernames[i])>0:
				outlist+="[@%s]" % self.user_usernames[i]
			else:	
				outlist+="[nousername]"
			outlist+="\n"

		bot.sendMessage(update.message.chat_id, outlist )

	def cmd_userdel(self,bot, update):
		if self.user(bot,update)!="su":
			print "Accesso non autorizzato"
			return

		if True:
			del self.user_ids[1:]
			del self.user_usernames[1:]
			del self.user_first_names[1:]
			del self.user_last_names[1:]
			bot.sendMessage(update.message.chat_id, "Cancellati tutti gli utenti" )
			print "Cancellati tutti gli user"
		else:
			print "Comando non autorizzato"
		
	def addTanzoCheckCommandHandler(self,dispatcher):
		dispatcher.addTelegramCommandHandler("otp",self.cmd_otp)
		dispatcher.addTelegramCommandHandler("userlist",self.cmd_userlist)
		dispatcher.addTelegramCommandHandler("userdel",self.cmd_userdel)

