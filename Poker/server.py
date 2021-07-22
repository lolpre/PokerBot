from Poker.player import Player
from Poker.pokerwrapper import PokerWrapper
from Poker.announcer import Announcer

class Server:
    def __init__(self):
        self.players = {}
        self.resets = 0
    
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

    def validate_game(ctx): #check if in game in channel is in progress
        return

    async def initiateGame(self, ctx, bot):
        new_game = PokerWrapper()
        self.startGame(ctx, new_game)
        self.join(ctx, new_game, bot)
        self.startRounds(ctx, new_game, bot)
        self.findWinner(ctx)
        self.resetRound(ctx, new_game, bot)
    
    async def redoGame(self, ctx, game, bot):
        self.startGame(ctx, game)
        self.join(ctx, game, bot)
        self.startRounds(ctx, game, bot)
        self.findWinner(ctx)
        self.resetRound(ctx, game, bot)

    async def startGame(self, ctx, game):
        self.validate_game(ctx)
        game.startGame(ctx)
        game.setBlind(ctx)
        game.setBalance(ctx) #change this function later

    
    async def join(self, ctx, game, bot):
        game.setPlayers(ctx)
        """
        - 
        """
    
    async def startRounds(self, ctx, game, bot):
        game.dealCards(bot) #needs to send dm's
        game.setDealer() #needs to be implemented
        game.takeBlinds() #needs to be implemented
        self.flop(ctx, game)
        self.nextTurns()
        self.turn(ctx, game)
        self.nextTurns()
        self.river(ctx, game)
        self.nextTurns()
    
    async def flop(self, ctx, game):
        game.createCommDeck()
        commDeck = game.communityDeck
        Announcer.showCommCards(ctx, commDeck)

    async def nextTurns(self, ctx):
        return
    
    async def turn(self, ctx, game):
        game.addCardtoComm()
        commDeck = game.communityDeck
        Announcer.showCommCards(ctx, commDeck)
    
    async def river(self, ctx, game):
        game.addCardtoComm()
        commDeck = game.communityDeck
        Announcer.showCommCards(ctx, commDeck)
    
    async def findWinner(self, ctx, game):
        winners = game.findWinner() #needs to return a list of winners
        #announce the winner(s) of the game

    async def resetRound(self, ctx, game, bot):
        Announcer.askLeave() #needs to be implemented
        self.join(ctx, game, bot)
        game.resetRound()
        self.redoGame(ctx, game, bot)

    


