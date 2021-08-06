from Poker.pokerwrapper import PokerWrapper
from Poker.announcer import Announcer
from Poker.pokerplayer import PokerPlayer
from Poker.evalhand import EvaluateHand
import discord
from Poker.player import Player
import asyncio

########################################################
# SERVER                                               #
# The Server class manages all the Poker Game classes  #
# and executes the game. All the methods of other      #
# classes will be called in this server.               #
########################################################
class Server:
    
    # the constructor of Server
    # input: bot -> a class object. part of the Discord API, the bot information 
    # initialized values: games -> a set of PokerWrapper objects. a set of all the ongoing games 
    #                     bot -> initializes the bot 
    #                     players -> a set of Player objects. a set of all registered players in a server
    #                     resets -> an integer. the number of times the administrator reset the leaderboard
    #                     announcerUI -> an Announcer object for the output
    def __init__(self, bot):
        self.games= {}
        self.bot=bot
        self.players = {}
        self.resets = 0
        self.announcerUI = Announcer()
    
    # adds the player to the player set 
    # input: ctx -> a class object. part of Discord API, the context of the message
    async def addPlayer(self, ctx):
        if ctx.author.id not in self.players:
            player = Player(ctx.author.id, 3000)
            self.players[ctx.author.id] = player
            await ctx.send("You have created an account!")
            return True
        else:
            await ctx.send("You already created an account!")
            return False
    
    # gets the balance of a player 
    # input: ctx -> a class object. part of Discord API, the context of the message
    async def getBalance(self, ctx):
        if ctx.author.id not in self.players:
            await ctx.send("You do not have an account! Use the .create command to create an account!")
        else:
            player = self.players[ctx.author.id]
            balance=player.getBalance()
            embed = discord.Embed(title=ctx.author.name+"'s Balance:", 
            description=str(balance)+" <:chips:865450470671646760>",
            color=discord.Color.green())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    # resets the leaderboard and the balacnes of all players 
    def reset(self):
        for player in self.players:
            player.setBalance(3000)
        self.resets += 1
    
    # the help command calls this method. the tutorial and list of all 
    # the commands to help a new user get started with the bot 
    # input: ctx -> a class object. part of Discord API, the context of the message
    async def help(self, ctx):
        embed = discord.Embed(title="List of Commands", 
        description="""**.create** - Create your profile for the server 
        **.p** - Create and play a game of Texas Hold'Em Poker
        **.balance** - Check to see how many chips you have
        **.top** - Check the leaderboards to see who is on top
        **.join** - Join an already existing Poker game
        **(Mods Only) .reset** - Reset the balances of everyone in the server""",
        color=0xffffff)
        embed.set_thumbnail(url="https://s.wsj.net/public/resources/images/JR-AA451_IFPOKE_GR_20191031164807.jpg")
        await ctx.send(embed=embed)
    
    # outputs the formatted leaderboard. sorts leaderboard by player balance. 
    # input: ctx -> a class object. part of Discord API, the context of the message
    async def printLeaderboard(self, ctx):
        sort_byvalue=sorted(self.players.items(),key=lambda x:x[1].balance,reverse=True)
        leaderboard=""
        k=1
        for i in sort_byvalue:
            name = str(await self.bot.fetch_user(i[1].id))
            leaderboard+= str(k)+". "+name+" - "+ str(i[1].balance)+" <:chips:865450470671646760>\n"
            k+=1
        embed = discord.Embed(title=ctx.message.guild.name+" Leaderboard:",
        description=leaderboard,
        color=discord.Color.red())
        embed.set_thumbnail(url=ctx.message.guild.icon_url) 
        await ctx.send(embed=embed)

    # def validate_game(ctx): #check if in game in channel is in progress
    #     return

    async def validate_game(self, ctx): #check if in game in channel is in progress
        if ctx.message.channel.id in self.games:
            await self.announcerUI.gameAlreadyInProgress(ctx)
            return False
        return True

    # checks if the player has an account created. if not, output error message 
    # input: ctx -> a class object. part of Discord API, the context of the message
    async def validate_player(self, ctx):
        if ctx.author.id not in self.players:
            await self.announcerUI.noAccount(ctx, ctx.author)
            return False
        if self.players[ctx.author.id].inGame:
            await self.announcerUI.playerAlreadyInGame(ctx, ctx.author)
            return False
        return True
    
    # initializes the game
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        id -> an integer. each game is assigned their own id. this can help with 
    #              searching for a game in the game set. 
    #        bot -> a class object. part of the Discord API the bot information. 
    async def initiateGame(self, ctx, id, bot):
        new_game = PokerWrapper(bot)
        if await self.startGame(ctx, new_game, bot) == False:
            return
        self.games[id] = new_game
        boolVal = await new_game.setPlayers(ctx, bot, self.players)
        if boolVal==False:
            del self.games[id] 
            return
        await self.startRounds(ctx, new_game, bot)
        await self.findWinner(ctx, new_game)
        await self.resetRound(ctx, new_game, bot)
    
    # re-initializes the game
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper class object. holds game information 
    #        bot -> a class object. part of the Discord API, the bot information 
    async def redoGame(self, ctx, game, bot):
        # await self.startGame(ctx, game, bot)
        await self.startRounds(ctx, game, bot)
        await self.findWinner(ctx, game)
        await self.resetRound(ctx, game, bot)

    # begins the gameplay 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper class object. holds game information 
    #        bot -> a class object. part of the Discord API, the bot information 
    async def startGame(self, ctx, game, bot):
        if await self.validate_player(ctx) == False:
            return False
        if await self.validate_game(ctx) == False:
            return False
        await game.startGame(ctx)
        await game.setBalance(ctx) #change this function later
        await game.setBlind(ctx, bot)
        
    # implements the leave command, called when a player wants to leave the game 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        id -> the game id. an integer
    async def leave(self, ctx, id):
        if id not in self.games:
            self.announcerUI.noGame(ctx)
            return

        for x in self.games[id].leaveQueue:
            if x._user.id == ctx.author.id:
                await self.announcerUI.alreadyInLeaveQueue(ctx, ctx.author)
                return

        if id in self.games:
            for x in self.games[id].participants:
                if x._user.id==ctx.author.id:
                    self.games[id].leaveQueue.append(x)
                    await self.announcerUI.addedToLeaveQueue(ctx, x._user)
                    return
                
            await self.announcerUI.notInGame(ctx, ctx.author)

    # implements the join command, called when the player wants to join the game 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        id -> the game id. an integer 
    async def join(self, ctx, id):
        if await self.validate_player(ctx) == False:
            return
        
        for x in self.games[id].joinQueue:
            if x._user.id == ctx.author.id:
                await self.announcerUI.alreadyInJoinQueue(ctx, ctx.author)
                return

        if id in self.games:
            self.games[id].joinQueue.append(PokerPlayer(ctx.message.author.name, 0, ctx.message.author, self.games[id].startingBalance))
            await self.announcerUI.addedToJoinQueue(ctx, ctx.author)
        else:
            await self.announcerUI.noGame(ctx)
    
    # begins the round of a game. 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper object. holds the game information 
    #        bot -> a class object. part of the Discord API, the bot information 
    async def startRounds(self, ctx, game, bot):
        for i in game.participants:
            game.competing.append(i)
        await game.dealCards(bot) #needs to send dm's
        # game.setDealer(ctx) #needs to be implemented
        await self.takeBlinds(ctx,game) #needs to be implemented
        await self.nextTurns(ctx, game, bot)
        await self.flop(ctx, game)
        if len(game.competing) != 1:
            await self.nextTurns(ctx, game, bot)
        await self.turn(ctx, game)
        if len(game.competing) != 1:
            await self.nextTurns(ctx, game, bot)
        await self.river(ctx, game)
        if len(game.competing) != 1:
            await self.nextTurns(ctx, game, bot)
            await game.pokerUI.showCommCards(ctx, game.communityDeck)

    # creates the community deck and reveals the first three cards. 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper object, holds the game information 
    async def flop(self, ctx, game):
        game.createCommDeck()
        commDeck = game.communityDeck
        await self.announcerUI.showCommCards(ctx, commDeck)
        for x in game.participants:
            commAndHand = commDeck + x._hand
            Eval = EvaluateHand(commAndHand)
            x._winCondition = Eval.evaluate()
            await x._user.send(x.getWinCond())

    # sets the blinds for two players. one player will get the big blind, 
    # and the other gets the small blind. 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper object, holds the game information 
    async def takeBlinds(self, ctx, game):
        await self.announcerUI.showPlayer(ctx,game)
        game.competing[0]._inPot=game.smallBlind
        await ctx.send(game.competing[0].username() + "\nSmall Blind: " + str(game.smallBlind)+" <:chips:865450470671646760>\n")
        game.currentPot+=game.competing[0]._inPot
        temp = game.competing.pop(0)
        game.competing.append(temp)

        await self.announcerUI.showPlayer(ctx,game)
        game.competing[0]._inPot=game.hardBlind
        await ctx.send(game.competing[0].username() + "\nBig Blind: " + str(game.hardBlind)+" <:chips:865450470671646760>\n")
        game.competing[0].setAction("blind")
        game.currentPot+=game.competing[0]._inPot

    
    # begins asking players for what their plan of action is. players can either 
    # check, raise, or fold. a call value is only available when someone has raised 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper object, holds the game information 
    #        bot -> a class object. part of the Discord API, the context of the message 
    async def nextTurns(self, ctx, game, bot):
            # pool=[]
            # for i in game.competing:
            #     pool.append(i)

            while True:
                pool_actions = []
                hasRaised = False
                blind=False
                i = 0
                raiseAmt=0
                raiseRound=0
                while True:
                    calledAction=False
                    if (game.competing[0].getAction()=="raise" and game.competing[0]._inPot==raiseAmt) or i==len(game.competing):
                        for x in game.competing:
                            x.setAction(0)
                        return
                    if game.competing[0].getAction()=="blind":
                        blind=True
                        raiseAmt=game.competing[0]._inPot
                        raiseRound=game.competing[0]._inPot
                        game.competing[0].setAction("called blind")
                        i=0
                        temp = game.competing.pop(0)
                        game.competing.append(temp)
                        continue
                    if game.competing[0].getAction()=="called blind":
                        blind=False
                    await self.announcerUI.showPlayer(ctx,game)
                    await self.announcerUI.askMove(ctx, "<@"+str(game.competing[0]._user.id)+">", hasRaised, blind, bot)
                    
                    def verify(m):
                        return game.competing[0]._user == m.author

                    try:
                        msg = await bot.wait_for('message', check=verify, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send(f"Sorry, you took too long to type your decision")
                        return False
                    format_msg = msg.content.lower().strip().split()

                    # if hasRaised == False and format_msg == "call":
                    #     await ctx.send("No one has raised.")

                    game.competing[0].setAction(format_msg)
                    if format_msg[0] == "raise":
                        if(raiseRound > competing[0]._gameBalance):
                            continue
                        await self.announcerUI.reportRaise(ctx, game.competing[0].username(), format_msg[1]) 
                        hasRaised = True
                        raiseRound=int(format_msg[1])
                        game.competing[0]._inPot+=raiseRound
                        game.currentPot+=raiseRound
                        raiseAmt=game.competing[0]._inPot
                        calledAction=True
                        temp = game.competing.pop(0)
                        game.competing.append(temp)
                        i=0
                        # for player in pool:
                        #     print(player.username())
                    elif format_msg[0] == "call": 
                        await self.announcerUI.reportCall(ctx, game.competing[0].username())
                        game.currentPot+=(raiseAmt-game.competing[0]._inPot)
                        game.competing[0]._inPot=raiseAmt
                        temp = game.competing.pop(0)
                        game.competing.append(temp)
                        calledAction=True
                    elif format_msg[0] == "check":
                        await self.announcerUI.reportCheck(ctx, game.competing[0].username())
                        temp = game.competing.pop(0)
                        game.competing.append(temp)
                        calledAction=True
                    elif format_msg[0] == "fold":
                        await self.announcerUI.reportFold(ctx, game.competing[0].username())
                        game.competing.pop(0)
                        if len(game.competing) == 1:
                            return
                    else:
                        continue 
                    if calledAction:
                        i+=1

                
            
    # reveals the fourth card in the community deck 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper object, holds the game information 
    async def turn(self, ctx, game):
        game.addCardtoComm()
        commDeck = game.communityDeck
        await game.pokerUI.showCommCards(ctx, commDeck)
        for x in game.participants:
            commAndHand = commDeck + x._hand
            Eval = EvaluateHand(commAndHand)
            x._winCondition = Eval.evaluate()
            await x._user.send(x.getWinCond())
    
    # reveals the fifth card in the community deck 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper object, holds the game information 
    async def river(self, ctx, game):
        game.addCardtoComm()
        commDeck = game.communityDeck
        await game.pokerUI.showCommCards(ctx, commDeck)
        for x in game.participants:
            commAndHand = commDeck + x._hand
            Eval = EvaluateHand(commAndHand)
            x._winCondition = Eval.evaluate()
            await x._user.send(x.getWinCond())
    
    # finds the winner out of all the players hand 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper object, holds the game information 
    async def findWinner(self, ctx, game):
        for x in game.competing:
            await ctx.send("**"+x.username()+"'s Hand:**")
            await self.announcerUI.showCards(ctx,x._hand)
        winners = game.findWinner() #needs to return a list of winners
        for x in winners:
            embed = discord.Embed(title="WINNER: "+x._username, description= x.getWinCond(), color=discord.Color.green())
            embed.set_image(url=x._user.avatar_url)
            await ctx.send(embed=embed)
            x._gameBalance+=int(game.currentPot/len(winners))
            
        #announce the winner(s) of the game

    # resets the round after the initial round has finished. 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper object, holds the game information 
    #        bot -> a class object. part of Discord API, the bot information 
    async def resetRound(self, ctx, game, bot):
        # await game.pokerUI.askLeave(ctx) #needs to be implemented
        # await self.join(ctx, game, bot)
        game.resetRound()
        await self.announcerUI.showBalances(ctx, game.participants)
        await self.announcerUI.askLeave(ctx)
        await asyncio.sleep(10)
        await game.addPlayers(ctx, self.players)
        await game.leaveGame(ctx, self.players, True)
        if len(game.participants)<2:
            for x in game.participants:
                game.leaveQueue.append(x)
            await ctx.send("Not enough players! Terminating game")
            await game.leaveGame(ctx, self.players, False)
            del self.games[ctx.message.channel.id]
            return
        await self.announcerUI.resetGame(ctx)
        await self.redoGame(ctx, game, bot)
