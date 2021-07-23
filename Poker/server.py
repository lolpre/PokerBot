from Poker.player import Player
from Poker.pokerwrapper import PokerWrapper
from Poker.announcer import Announcer

class Server:
    def __init__(self):
        self.players = {}
        self.resets = 0
        self.announcerUI = Announcer()
    
    def addPlayer(self, ctx):
        player = Player(ctx.author.name, 3000)
        self.players[ctx.author.id] = player
    
    async def getBalance(self, ctx):
        if ctx.author.id not in self.players:
            await ctx.send("You do not have an account! Use the .create command to create an account!")
        else:
            player = self.players[ctx.author.id]
            await ctx.send("You currently have " + str(player.getBalance()) + " chips!")
    
    def reset(self):
        for player in self.players:
            player.setBalance(3000)
        self.resets += 1
    
    async def help(self, ctx):
        await ctx.send("```List of commands\n\
.create - Create your profile for the server\n\
.p - Create and play a game of Texas Hold'Em Poker\n\
.balance - Check to see how many chips you have\n\
.top - Check the leaderboards to see who is on top\n\
.join - Join an already existing Poker game\n\
(Mods Only) .reset - Reset the balances of everyone in the server```")

    def validate_game(self, ctx): #check if in game in channel is in progress
        return

    async def initiateGame(self, ctx, bot):
        new_game = PokerWrapper()
        await self.startGame(ctx, new_game, bot)
        await self.join(ctx, new_game, bot)
        await self.startRounds(ctx, new_game, bot)
        await self.findWinner(ctx)
        await self.resetRound(ctx, new_game, bot)
    
    async def redoGame(self, ctx, game, bot):
        await self.startGame(ctx, game)
        await self.join(ctx, game, bot)
        await self.startRounds(ctx, game, bot)
        await self.findWinner(ctx)
        await self.resetRound(ctx, game, bot)

    async def startGame(self, ctx, game, bot):
        self.validate_game(ctx)
        await game.startGame(ctx)
        await game.setBlind(ctx, bot)
        game.setBalance(ctx, 1000) #change this function later

    
    async def join(self, ctx, game, bot):
        await game.setPlayers(ctx, bot)
        """
        - 
        """
    
    async def startRounds(self, ctx, game, bot):
        await game.dealCards(bot) #needs to send dm's
        game.setDealer(ctx) #needs to be implemented
        game.takeBlinds(ctx) #needs to be implemented
        await self.flop(ctx, game)
        await self.nextTurns()
        await self.turn(ctx, game)
        await self.nextTurns()
        await self.river(ctx, game)
        await self.nextTurns()
    
    async def flop(self, ctx, game):
        game.createCommDeck()
        commDeck = game.communityDeck
        await self.announcerUI.showCommCards(ctx, commDeck)

    async def nextTurns(self, ctx):
        return
    
    async def turn(self, ctx, game):
        game.addCardtoComm()
        commDeck = game.communityDeck
        await Announcer.showCommCards(ctx, commDeck)
    
    async def river(self, ctx, game):
        game.addCardtoComm()
        commDeck = game.communityDeck
        await Announcer.showCommCards(ctx, commDeck)
    
    async def findWinner(self, ctx, game):
        winners = game.findWinner() #needs to return a list of winners
        #announce the winner(s) of the game

    async def resetRound(self, ctx, game, bot):
        await Announcer.askLeave() #needs to be implemented
        await self.join(ctx, game, bot)
        game.resetRound()
        await self.redoGame(ctx, game, bot)

    

    


