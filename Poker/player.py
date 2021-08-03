#represents the User and stores infor related to it
class Player:
	def __init__(self, id, balance):
		self.id = id
		self.balance = balance
		self.inGame = False #checks if the user is in a game

	def getBalance(self):
		return self.balance
	
	def setBalance(self, value):
		self.balance = value #used to update player balance after games
