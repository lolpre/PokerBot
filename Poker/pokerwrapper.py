from Poker.player import Player
from Poker.pokerplayer import PokerPlayer
from Poker.deck import Deck
from Poker.card import Card
from Poker.announcer import Announcer
from Poker.evalhand import EvaluateHand
import asyncio
import discord
import math

#this class runs the game functions and uses the other class made to support the game
class PokerWrapper:
    def __init__(self, bot):
        self.bot=bot             #this sets the bot in discord to run
        self.gameID=0            #plan to have multiple games so this identifies running games
        self.gameStarted = False #check if there is game started
        self.numPlayers = 0 
        self.hardBlind = 0       #represents the higher initial bet
        self.smallBlind=0        #represent lower initial bet
        self.currentPot = 0      #total reward for the winner of the round
        self.pokerUI = Announcer()  #this will allow bot to inform users what is happening
        self.gameDeck = Deck()
        self.communityDeck = []
        self.participants = []   #total people in the game
        self.competing = []      #users who are still playing the round
        self.joinQueue=[]        #list of players waiting to join the game
        self.leaveQueue=[]       #list of players waiting to leave the game
        self.startingBalance = 0 #set initial balance of the game

    #internal bot function that waits for command to start the game
    async def startGame(self, ctx):
        await self.pokerUI.initiateGame(ctx)
        
    #starts the game and sets player with the embed as the message being sent
    async def setPlayers(self, ctx, bot, players):
        embed = discord.Embed(title="Poker: Texas hold 'em",
                              description="Starting Balance: "+str(self.startingBalance)+""" <:chips:865450470671646760>
        Min Bet: """+str(self.hardBlind)+""" <:chips:865450470671646760>
        \nReact to Join!""",
            color=discord.Color.green())
        #the bot will wait until all responces or until time is up
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await asyncio.sleep(10)

        message = await ctx.fetch_message(message.id)
        #checks for the check emotes which represents a player
        for reaction in message.reactions:
            if reaction.emoji == '✅':
                i = 1
                async for user in reaction.users():
                    if user != bot.user and user.id not in players:
                        await self.pokerUI.noAccount(ctx, user)
                        continue

                    if user != bot.user and players[user.id].inGame:
                        await self.pokerUI.playerAlreadyInGame(ctx, user)
                        continue

                    if user != bot.user and len(self.participants) == 8:
                        await self.pokerUI.gameIsFull(ctx, user)
                        newPlayer= PokerPlayer(user.name, i, user, self.startingBalance)
                        self.joinQueue.append(newPlayer)

                    elif user != bot.user:
                        newPlayer= PokerPlayer(user.name, i, user, self.startingBalance)
                        self.participants.append(newPlayer)
                        players[user.id].inGame = True
                        i += 1
        #checks if there is enough players through the check emote it has to be greater than 2 as the bot represents 1 of them
        if len(self.participants) < 2:
            await ctx.send("Not enough players")
            for p in self.participants:
                players[p._user.id].inGame = False
            self.participants = []
            return False
        else:
            await ctx.send("Starting game with " + str(len(self.participants)) + " players")
    
    #adds to players to the game from the list of players waiting to be added
    async def addPlayers(self, ctx, players):
        for newPlayer in self.joinQueue:
            if len(self.participants) == 8:
                continue
            self.participants.append(newPlayer)
            players[newPlayer._user.id].inGame = True
            await self.pokerUI.playerHasJoined(ctx, newPlayer._user)
            self.joinQueue.remove(newPlayer)
        # self.joinQueue.clear()
    
    #removes players based on the list of players ready to leave and checks if game is still able to play
    async def leaveGame(self, ctx, players, enoughPlayers):
        for x in self.leaveQueue:
            players[x._user.id].balance+= x.getGameBalance()-self.startingBalance
            players[x._user.id].inGame = False
            self.participants.remove(x)
            if enoughPlayers:
                await self.pokerUI.playerHasLeft(ctx, x._user)
            elif not enoughPlayers:
                await self.pokerUI.playerKicked(ctx, x._user)
            
        self.leaveQueue.clear()
    
    #sets the blind at the start of the game and takes in input from users
    async def setBlind(self, ctx, bot):

        def representsInt(s):
            try:
                int(s)
                return True
            except ValueError:
                return False

        def verify(m):
            return m.author == ctx.message.author and representsInt(m.content)

        await self.pokerUI.askBet(ctx)

        try:
            msg = await bot.wait_for('message', check=verify, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry, you took too long to type the blind")
            return False

        self.hardBlind = int(msg.content)
        self.smallBlind = math.floor(self.hardBlind/2)

        # await Announcer.reportBet(ctx, blind)
    
    #this updats the players balance after the end of each round
    async def setBalance(self, ctx):

        def representsInt(s):
            try: 
                int(s)
                return True
            except ValueError:
                return False

        def verify(m):
            return m.author == ctx.message.author and representsInt(m.content)

        await self.pokerUI.askBalance(ctx)

        try:
            msg = await self.bot.wait_for('message', check = verify, timeout = 30)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry, you took too long to type the balance")
            return False

        self.startingBalance = int(msg.content)

    #Deals cards to players and community card
    async def dealCards(self, bot):
        self.gameDeck.shuffle()

        for p in self.participants:
            for i in range(2):
                c = self.gameDeck.drawCard()
                p.addCard(c)
            await p.send_hand(bot)
    
    #check if the current players in the game have balance to continue playing
    def checkPlayerBalance(self):
        for i in self.participants:
            if i.getGameBalance() <= 0:
                # print(i.username(), "has left the table")
                self.participants.remove(i)
    
    #removes player from current rouhd with fold command
    def playerFold(self, id):
        self.competing.pop(0)
    
    #remove player from the current game
    def removePlayer(self, id):
        for i in self.participants:
            if i.username() == id:
                self.participants.remove(i)
        self.numPlayers -= 1
    
    #makes community hand
    def createCommDeck(self):
        i = 0
        for i in range(3):
            self.addCardtoComm()
    
    #adds card to community card
    def addCardtoComm(self):
        self.communityDeck.append(self.gameDeck.drawCard())
    
    #at the end of each round find the winner
    def findWinner(self):
        Eval = EvaluateHand(self.communityDeck)
        for x in self.competing:
            commAndHand = self.communityDeck + x._hand
            Eval = EvaluateHand(commAndHand)
            x._winCondition = Eval.evaluate()
            # print (x._username)

        winningCond = max(x._winCondition[0] for x in self.competing)
        compete = []
        for x in self.competing:
            if x._winCondition[0] == winningCond:
                compete.append(x)
        winners = Eval.winning(compete, winningCond)
        return winners
    
    #reset the round
    def resetRound(self):
        self.gameStarted = False
        self.currentPot = 0
        self.communityDeck.clear()
        self.gameDeck = Deck()
        self.numPlayers = len(self.participants)
        temp = self.participants.pop(0)
        self.participants.append(temp)
        self.competing.clear()
        for x in self.participants:
            x._hand = []
            x._gameBalance=int(x._gameBalance-x._inPot)
            x._inPot=0
            

    async def setDealer(self, ctx):
        return
    
    async def takeBlinds(self, ctx):
        return
