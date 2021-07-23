from Poker.player import Player
from Poker.pokerwrapper import PokerWrapper
from Poker.announcer import Announcer
import asyncio

class Server:
    def __init__(self):
        self.players = {}
        self.resets = 0
        self.pokerWrapper = PokerWrapper()
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
        
    async def nextTurns(self, ctx, game, bot):
        for i in game.participants:
            game.competing.append(i)

        while True:
            pool_actions = []
            hasRaised = False
            i = 0
            while i < len(game.competing):
                await self.announcerUI.askMove(ctx, game.competing[i].username(), hasRaised, bot)
                
                def verify(m):
                    return game.competing[i]._user == m.author

                try:
                    msg = await bot.wait_for('message', check=verify, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send(f"Sorry, you took too long to type your decision")
                    return False
                format_msg = msg.content.lower().strip().split()

                # if hasRaised == False and format_msg == "call":
                #     await ctx.send("No one has raised.")

                game.competing[i].setAction(format_msg)
                pool_actions.append(format_msg)
                if format_msg[0] == "raise":
                    await self.announcerUI.reportRaise(ctx, game.competing[i].username(), format_msg[1]) 
                    hasRaised = True
                    # temp = pool.pop(i)
                    # pool.append(temp)
                    for player in game.competing:
                        print(player.username())
                elif format_msg[0] == "call": 
                    await self.announcerUI.reportCall(ctx, game.competing[i].username())
                elif format_msg[0] == "check":
                    await self.announcerUI.reportCheck(ctx, game.competing[i].username())
                elif format_msg[0] == "fold":
                    await self.announcerUI.reportFold(ctx, game.competing[i].username())
                    self.pokerWrapper.removePlayer(game.competing[i].username())
                    game.competing.pop(i) 
                    i -= 1
                    if len(game.competing) == 1:
                        return
                else:
                    continue 
                i += 1
                
            if "raise" not in pool_actions:
                break
        
        game.competing.clear()

            

    def validate_game(self, ctx): #check if in game in channel is in progress
        return

    async def initiateGame(self, ctx, bot):
        new_game = PokerWrapper()
        await self.startGame(ctx, new_game, bot)
        await self.join(ctx, new_game, bot)
        await self.startRounds(ctx, new_game, bot)
        await self.findWinner(ctx, new_game)
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
        await game.setDealer(ctx) #needs to be implemented
        await game.takeBlinds(ctx) #needs to be implemented
        await self.nextTurns(ctx, game, bot)
        if len(game.competing) == 1:
            return
        await self.flop(ctx, game)
        await self.nextTurns(ctx, game, bot)
        if len(game.competing) == 1:
            return
        await self.turn(ctx, game)
        await self.nextTurns(ctx, game, bot)
        if len(game.competing) == 1:
            return
        await self.river(ctx, game)
        await self.nextTurns(ctx, game, bot)

    async def flop(self, ctx, game):
        game.createCommDeck()
        commDeck = game.communityDeck
        await self.announcerUI.showCommCards(ctx, commDeck)

    # async def nextTurns(self, ctx):
    #     return
    
    async def turn(self, ctx, game):
        game.addCardtoComm()
        commDeck = game.communityDeck
        await self.announcerUI.showCommCards(ctx, commDeck)
    
    async def river(self, ctx, game):
        game.addCardtoComm()
        commDeck = game.communityDeck
        await self.announcerUI.showCommCards(ctx, commDeck)
    
    async def findWinner(self, ctx, game):
        winners = game.findWinner() #needs to return a list of winners
        #announce the winner(s) of the game
        for x in winners:
            await ctx.send(x._username+": " + x.getWinCond())

    async def resetRound(self, ctx, game, bot):
        await self.announcerUI.askLeave() #needs to be implemented
        await self.join(ctx, game, bot)
        game.resetRound()
        await self.redoGame(ctx, game, bot)

    

    


