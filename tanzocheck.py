#Semplice classe per il controllo degli accessi
#ad un Bot Telegram

# Sergio Tanzilli - sergio@tanzilli.com - @SergioTanzilli

import random

class Check():
	user_ids=[]
	otp=-1

	def __init__(self):
		print "TanzoCheck 0.1 is fired..."
		pass
				
	#Controlla se l'utente e' uno user autorizzato
	def user(self,bot,update):

		#Se non c'e' lista di utenti il primo che accede diventa su
		if len(self.user_ids)==0:
			self.user_ids+=[update.message.from_user.id]
			print "Primo accesso"
			print "%s diventa diventa super user" % update.message.from_user.first_name
			print "Lista utenti:" , self.user_ids
			return "su"

		#Se lo user e' in lista nella posizione 0 ritorna su
		if self.user_ids[0]==update.message.from_user.id:
			print "Accesso dal super user"
			print "Lista utenti" , self.user_ids
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
				print "Accesso da nuovo user con otp"
				print "Lista utenti" , self.user_ids
				return "user"

		#Negli altri casi nega l'accesso
		print "Accesso non autorizzato"
		print "Users:" , self.user_ids
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

