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
        self._user = user # Stores the PokerPlayer's Discord.User object
        self._username = username # Represents the PokerPlayer's username
        self._seatNumber = seatNumber # Represents the PokerPlayer's seat number in the current game
        self._hand = [] # Stores the PokerPlayer's hands
        self._gameBalance = startBalance # Stores the PokerPlayer's amount of money in the game
        self._playerAction = 0 # Stores the move that the PokerPlayer wants to make
        self._inGame = True # Shows if the PokerPlayer is still in the game
        self._winCondition = [0] # Stores the winning condition of the PokerPlayer
        self._inPot=0 # Stores the amount of money that the PokerPlayer has in the pot

    # This method sends card emotes as a direct message to the PokerPlayer
    async def send_hand(self, bot):
        handString = ""
        await self._user.send("**Hand:**")
        for card in self._hand:
            handString += card.emote
        await self._user.send(handString)

    # This method returns the PokerPlayer’s username
    def username(self):
        return self._username
    
    # This method returns the PokerPlayer's seat number within the
    # current game
    def seatNumber(self):
        return self._seatNumber

    # This method returns the PokerPlayer’s status in the game. 
    def getStatus(self):
        return self._inGame

    # This method sets the _inGame variable to True if the player is in 
    # the current game round, and False otherwise
    def setStatus(self, status):
        self._inGame = status

    # This method returns the PokerPlayer’s hand
    def getHand(self):
        return self._hand

    # This method adds a maximum of 2 cards to the 
    # PokerPlayer's hand
    def addCard(self, c):
        if len(self._hand) < 2:
            self._hand.append(c)

    # This method returns the PokerPlayer's gameBalance
    def getGameBalance(self):
        return self._gameBalance-self._inPot
    
    
    # This method sets the PokerPlayer’s balance
    # Where opType represents the type of operation: 
    # 1 for addition and 0 for subtraction
    def setBalance(self, opType, amount):
        if opType:
            self._gameBalance += amount
        else:
            if self._gameBalance > 0:
                current = self._gameBalance - amount
                self._gameBalance = current if (current > 0) else 0
                if self._gameBalance == 0:
                    self.setStatus(False)

    # This method returns the PokerPlayer's intended action
    def getAction(self):
        return self._playerAction

    # This method sets the PokerPlayer's intended action
    def setAction(self, action):
        self._playerAction = action

    # This method returns the PokerPlayer's win condition
    def getWinCond(self):
        if self._winCondition[0] == 10:
            return "ROYAL FLUSH"
        elif self._winCondition[0] == 9:
            return "STRAIGHT FLUSH"
        elif self._winCondition[0] == 8:
            return "FOUR OF A KIND"
        elif self._winCondition[0] == 7:
            return "FULL HOUSE"
        elif self._winCondition[0] == 6:
            return "FLUSH"
        elif self._winCondition[0] == 5:
            return "STRAIGHT"
        elif self._winCondition[0] == 4:
            return "THREE OF A KIND"
        elif self._winCondition[0] == 3:
            return "TWO PAIR"
        elif self._winCondition[0] == 2:
            return "ONE PAIR"
        elif self._winCondition[0] == 1:
            return "HIGH CARD"
