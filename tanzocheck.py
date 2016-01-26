# Semplice classe per il controllo degli accessi
# verso un Bot Telegram
# Sergio Tanzilli - sergio@tanzilli.com - @SergioTanzilli

import random
import json
import os.path

class Check():
	user_file='user_list.json'
	user_ids=[]
	user_first_names=[]
	otp=-1

	def __init__(self):
		print "TanzoCheck 0.2 is fired..."
		if os.path.exists(self.user_file):
			with open(self.user_file) as json_file:
				json_data=json.load(json_file)
				self.user_ids=json_data[0]
				self.user_first_names=json_data[1]
				
	def save_user_list(self):
		user_data=[self.user_ids,self.user_first_names]
		with open(self.user_file, 'w') as outfile:
			json.dump(user_data, outfile,indent=4)				
	
	#Controlla se l'utente e' uno user autorizzato
	def user(self,bot,update):

		#Se non c'e' lista di utenti il primo che accede diventa su
		if len(self.user_ids)==0:
			self.user_ids+=[update.message.from_user.id]
			self.user_first_names+=[update.message.from_user.first_name]
			self.save_user_list()
			print "Primo accesso"
			print "%s diventa diventa super user" % update.message.from_user.first_name
			print "Lista utenti\n%s %s " % (self.user_ids,self.user_first_names)
			return "su"

		#Se lo user e' in lista nella posizione 0 ritorna su
		if self.user_ids[0]==update.message.from_user.id:
			print "Accesso dal super user"
			print "Lista utenti\n%s %s " % (self.user_ids,self.user_first_names)
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
				self.user_first_names+=[update.message.from_user.first_name]
				self.save_user_list()
				print "Accesso da nuovo user con otp"
				print "Lista utenti\n%s %s " % (self.user_ids,self.user_first_names)
				return "user"

		#Negli altri casi nega l'accesso
		print "Accesso non autorizzato"
		print "Lista utenti\n%s %s " % (self.user_ids,self.user_first_names)
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
		

	def cmd_userdel(self,bot, update):
		if self.user(bot,update)!="su":
			print "Accesso non autorizzato"
			return

		if True:
			del self.user_ids[1:]
			bot.sendMessage(update.message.chat_id, "Cancellati tutti gli utenti" )
			print "Cancellati tutti gli user"
		else:
			print "Comando non autorizzato"
		
		print "Lista utenti" , self.user_ids

	def addTanzoCheckCommandHandler(self,dispatcher):
		dispatcher.addTelegramCommandHandler("otp",self.cmd_otp)
		dispatcher.addTelegramCommandHandler("userdel",self.cmd_userdel)

