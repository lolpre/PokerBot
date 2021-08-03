class Player:
	def __init__(self, id, balance):
		self.id = id        #unique ID to identify the user
		self.balance = balance
		self.inGame = False #check if player is in game

	def getBalance(self):
		return self.balance
	
	def setBalance(self, value):
		self.balance = value #updates player balance after each game
