'''

This is the Player class. This class object represents each user in the
Discord server. This player object will be created each time a Discord
user uses the ".create" command, regitering an account. 

'''
class Player:

	# This is the constructor for the Player class. It initializes the id,
	# balance, and the boolean that states whether the user is in a game or not.
	def __init__(self, id, balance):
		self.id = id  # unique ID to identify the user
		self.balance = balance  # current balance of the player
		self.inGame = False   # check if player is in game

	# This method returns the current balance of the player.
	def get_balance(self):
		return self.balance
	
	# This method sets the balance of the player to a specific value.
	def set_balance(self, value):
		self.balance = value  # updates player balance after each game
