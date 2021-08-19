import asyncio
import discord
from Poker.deck import Deck
from Poker.card import Card

'''

This is the class for each Poker Player object.
A Poker Player object will be created for each user before
they can join/play a poker game. The poker game interacts with 
only the Poker Player objects and not the Player objects.

'''
class PokerPlayer:
    
    # This is the constructor for the PokerPlayer class
    # It initializes the variables stored in a PokerPlayer object 
    def __init__(self, username, seatNumber, user, startBalance):
        self.user = user # Stores the PokerPlayer's Discord.User object
        self.username = username # Represents the PokerPlayer's username
        self.seat_number = seatNumber # Represents the PokerPlayer's seat number in the current game
        self.hand = [] # Stores the PokerPlayer's hands
        self.game_balance = startBalance # Stores the PokerPlayer's amount of money in the game
        self.player_action = 0 # Stores the move that the PokerPlayer wants to make
        self.in_game = True # Shows if the PokerPlayer is still in the game
        self.win_condition = [0] # Stores the winning condition of the PokerPlayer
        self.in_pot=0 # Stores the amount of money that the PokerPlayer has in the pot

    # This method sends card emotes as a direct message to the PokerPlayer
    async def send_hand(self, bot):
        hand_string = ""
        await self.user.send("**Hand:**")
        for card in self.hand:
            hand_string += card.emote
        await self.user.send(hand_string)

    # This method returns the PokerPlayer’s username
    def username(self):
        return self.username
    
    # This method returns the PokerPlayer's seat number within the
    # current game
    def seat_number(self):
        return self.seatNumber

    # This method returns the PokerPlayer’s status in the game. 
    def get+status(self):
        return self.in_game

    # This method sets the _inGame variable to True if the player is in 
    # the current game round, and False otherwise
    def set_status(self, status):
        self.in_game = status

    # This method returns the PokerPlayer’s hand
    def get_hand(self):
        return self.hand

    # This method adds a maximum of 2 cards to the 
    # PokerPlayer's hand
    def add_card(self, c):
        if len(self.hand) < 2:
            self.hand.append(c)

    # This method returns the PokerPlayer's gameBalance
    def get_game_balance(self):
        return self.game_balance-self.in_pot
    
    
    # This method sets the PokerPlayer’s balance
    # Where opType represents the type of operation: 
    # 1 for addition and 0 for subtraction
    def set_balance(self, opType, amount):
        if opType:
            self.game_balance += amount
        else:
            if self.game_balance > 0:
                current = self.game_balance - amount
                self.game_balance = current if (current > 0) else 0
                if self.game_balance == 0:
                    self.set_status(False)

    # This method returns the PokerPlayer's intended action
    def get_action(self):
        return self.player_action

    # This method sets the PokerPlayer's intended action
    def set_action(self, action):
        self.player_action = action

    # This method returns the PokerPlayer's win condition
    def get_win_cond(self):
        if self.win_condition[0] == 10:
            return "ROYAL FLUSH"
        elif self.win_condition[0] == 9:
            return "STRAIGHT FLUSH"
        elif self.win_condition[0] == 8:
            return "FOUR OF A KIND"
        elif self.win_condition[0] == 7:
            return "FULL HOUSE"
        elif self.win_condition[0] == 6:
            return "FLUSH"
        elif self.win_condition[0] == 5:
            return "STRAIGHT"
        elif self.win_condition[0] == 4:
            return "THREE OF A KIND"
        elif self.win_condition[0] == 3:
            return "TWO PAIR"
        elif self.win_condition[0] == 2:
            return "ONE PAIR"
        elif self.win_condition[0] == 1:
            return "HIGH CARD"
