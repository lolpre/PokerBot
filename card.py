class Card:
	def __init__(self, suit, val):
		self.suit = suit
		self.val = val

	def show(self):
		return "{} of {}".format(self.val, self.suit)

