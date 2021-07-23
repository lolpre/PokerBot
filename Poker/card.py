class Card:
	def __init__(self, suit, val):
		self.suit = suit
		self.val = val
		self.emote = None

	def show(self):
		return f"{self.val} of {self.suit}"

	def getNumVal(self):
		if self.val=="A":
			return 0
		if self.val=="K":
			return 12
		if self.val=="Q":
			return 11
		if self.val=="J":
			return 10
		return int(self.val)-1		

	def getNumSuit(self):
		if self.suit=="Diamonds":
			return 0
		if self.suit=="Clubs":
			return 1
		if self.suit=="Hearts":
			return 2
		if self.suit=="Spades":
			return 3
	
