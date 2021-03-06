"""
 PokerPlayer.
"""


class PokerPlayer:
    """
    This is the class for each Poker Player object.
    A Poker Player object will be created for each user before
    they can join/play a poker game. The poker game interacts with
    only the Poker Player objects and not the Player objects.
    """

    def __init__(self, username, seat_number, user, start_balance):
        """This is the constructor for the PokerPlayer class."""
        self.user = user  # Stores the PokerPlayer's Discord.User object
        self.username = username  # Represents the PokerPlayer's username
        # Represents the PokerPlayer's seat number in the current game
        self.seat_number = seat_number
        self.hand = []  # Stores the PokerPlayer's hands
        # Stores the PokerPlayer's amount of money in the game
        self.game_balance = start_balance
        self.player_action = 0  # Stores the move that the PokerPlayer wants to make
        self.in_game = True  # Shows if the PokerPlayer is still in the game
        # Stores the winning condition of the PokerPlayer
        self.win_condition = [0]
        self.in_pot = 0  # Stores the amount of money that the PokerPlayer has in the pot

    async def send_hand(self):
        """This method sends card emotes as a direct message to the PokerPlayer."""
        hand_string = ""
        await self.user.send("**Hand:**")
        for card in self.hand:
            hand_string += card.emote
        await self.user.send(hand_string)

    def get_username(self):
        """This method returns the PokerPlayer’s username."""
        return self.username

    # def get_seat_number(self):
    #     """
    #     This method returns the PokerPlayer's seat number within the
    #     current game.
    #     """
    #     return self.seat_number

    def get_status(self):
        """This method returns the PokerPlayer’s status in the game."""
        return self.in_game

    def set_status(self, status):
        """
        This method sets the _inGame variable to True if the player is in
        the current game round, and False otherwise.
        """
        self.in_game = status

    def get_hand(self):
        """This method returns the PokerPlayer’s hand."""
        return self.hand

    def add_card(self, crd):
        """
        This method adds a maximum of 2 cards to the
        PokerPlayer's hand.
        """
        if len(self.hand) < 2:
            self.hand.append(crd)

    def get_game_balance(self):
        """This method returns the PokerPlayer's gameBalance."""
        return self.game_balance - self.in_pot

    def set_balance(self, op_type, amount):
        """
        This method sets the PokerPlayer’s balance.
        Where opType represents the type of operation:
        1 for addition and 0 for subtraction.
        """
        if op_type:
            self.game_balance += amount
        else:
            if self.game_balance > 0:
                current = self.game_balance - amount
                self.game_balance = current if (current > 0) else 0
                if self.game_balance == 0:
                    self.set_status(False)

    def get_action(self):
        """This method returns the PokerPlayer's intended action."""
        return self.player_action

    def set_action(self, action):
        """This method sets the PokerPlayer's intended action."""
        self.player_action = action

    def get_win_cond(self):
        """This method returns the PokerPlayer's win condition."""
        return_value = ""
        if self.win_condition[0] == 10:
            return_value = "ROYAL FLUSH"
        elif self.win_condition[0] == 9:
            return_value = "STRAIGHT FLUSH"
        elif self.win_condition[0] == 8:
            return_value = "FOUR OF A KIND"
        elif self.win_condition[0] == 7:
            return_value = "FULL HOUSE"
        elif self.win_condition[0] == 6:
            return_value = "FLUSH"
        elif self.win_condition[0] == 5:
            return_value = "STRAIGHT"
        elif self.win_condition[0] == 4:
            return_value = "THREE OF A KIND"
        elif self.win_condition[0] == 3:
            return_value = "TWO PAIR"
        elif self.win_condition[0] == 2:
            return_value = "ONE PAIR"
        elif self.win_condition[0] == 1:
            return_value = "HIGH CARD"
        return return_value
