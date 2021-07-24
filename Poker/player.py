class Player:
	def __init__(self, id, balance):
		self.id = id
		self.balance = balance

	def getBalance(self):
		return self.balance
	
	def setBalance(self, value):
		self.balance = value