"""Player"""


class Player:
    """
    This is the Player class. This class object represents each user in the
    Discord server. This player object will be created each time a Discord
    user uses the ".create" command, regitering an account.
    """

    def __init__(self, player_id, balance):
        """
        This is the constructor for the Player class. It initializes the id,
        balance, and the boolean that states whether the user is in a game or not.
        """
        self.id = player_id  # unique ID to identify the user
        self.balance = balance  # current balance of the player
        self.in_game = False   # check if player is in game

    def get_balance(self):
        """This method returns the current balance of the player."""
        return self.balance

    def set_balance(self, value):
        """This method sets the balance of the player to a specific value."""
        self.balance = value  # updates player balance after each game
