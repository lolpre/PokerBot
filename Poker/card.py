##############################
# CARD                       #
# The Card class stores all  #
# the information regarding  #
# the poker card, including  #
# the suit and number of the #
# card.                      #
##############################
class Card:
	
	def __init__(self, suit, val, emote):
	"""
	 suit: the suit of the card
	 val: the number on the card 
	 emote: the graphic depiction of the card 
	"""
		self.suit = suit
		self.val = val
		self.emote = emote
	
	def show(self):
	"""
	show returns the image of the card. 
	"""
		return self.emote

	
	def get_num_val(self):
	"""
	 get_num_value gets the number value of the card
	 this is for cards above the value of 10
	 and for the ace
	 (Jack, Queen, King, Ace). 
	"""
		if self.val=="A":
			return 0
		if self.val=="K":
			return 12
		if self.val=="Q":
			return 11
		if self.val=="J":
			return 10
		return int(self.val)-1		
	
	def get_num_suit(self):
	"""
	 get_num_suit gets the suit of the card and  
	 returns a number value, one number 
	 representing a suit.
	"""
		if self.suit=="Diamonds":
			return 0
		if self.suit=="Clubs":
			return 1
		if self.suit=="Hearts":
			return 2
		if self.suit=="Spades":
			return 3
