import random 
import discord
import asyncio 

######################################################
# ANNOUNCER                                          #
# The Announcer class is the interface of Poker Bot, # 
# and the class that will be interacting with the    #
# user the most. All the information stored inside   #
# the other classes will be communicated through the #
# Announcer class.                                   #
######################################################
class Announcer:
    
    # outputs the announcing message that begins the Poker Game
    # input: ctx (part of Discord API, the context of the message)
    # output: none
    async def initiateGame(self, ctx):
        await ctx.send("WELCOME TO POKER BOT!")
        await ctx.send("If this is your first time with Poker Bot," + 
        " please type \'.create\'. Please type \'.help\' for the rules" + 
        " and betting system.")
    
    # outputs the announcing message that asks users for Bets 
    # in the beginning of the game. 
    # input: ctx -> part of Discord API, the context of the message
    async def askBet(self, ctx):
        await ctx.send("What is the big blind (minimum bet) amount?")
    
    # outputs the announcing message that reveals the winner of the game
    # input: ctx -> part of Discord API, the context of the message
    #        sorted_players -> a sorted list of players, the winner 
    #                          at the beginning of list
    # output: none
    async def announceWinner(self, ctx, sorted_players, com_deck, currentPot):
        #sending community hands
        winner = sorted_players[0].username()
        self.showCommCards(com_deck)
        await ctx.send(winner + " has won, receiving " + str(currentPot))
            
    # outputs the announcing message that asks participants for their next move 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        member -> a class object. part of Discord API, the information about the Discord User
    #        hasRaised -> a boolean that checks if the previous user has increased bet
    #        blind -> a boolean that checks if the blind has been set 
    #        bot -> a class object. part of Discord API, the bot information 
    async def askMove(self, ctx, member, hasRaised, blind, bot):
        if hasRaised or blind:
            await ctx.send("{}, Would you like to call, raise, or fold?".format(member))
        else:
            await ctx.send("{}, Would you like to check, raise, or fold?".format(member))
    
    # outputs the announcing message that asks participant for the starting balance 
    # for the game
    # input: ctx -> part of Discord API, the context of the message
    async def askBalance(self, ctx):
        await ctx.send("What should be the starting game balance of all players?")

    # limits the time given for someone to join the game. the timer is 
    # 30 seconds long
    # input: ctx -> part of Discord API, the context of the message
    async def joinTimer(self, ctx):
        time = 30
        while time != 0:
            if time == 5: 
                await ctx.send("Entries close in 5 seconds.")
            time -= 1
            await asyncio.sleep(1)
    
    # outputs the announcing message that opens the game for people to join 
    # input: ctx -> a class object. part of Discord API, the context of the message
    async def joinQueue(self, ctx):
        await ctx.send("Please click on the green checkmark to join the game!")
        await ctx.send("A timer will begin now. You will have 60 seconds to join the game.")
        await self.joinTimer()
        await ctx.send("Time is up. The game will be starting shortly...")

    # reveals all the cards in a hand. outputs the message into the game channel.
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        hand -> an array of the Card object 
    async def showCards(self, ctx, hand):
        cards=""
        for card in hand:
            cards+=card.show()
        await ctx.send(cards)

    # reveals the community deck. outputs the mesasge into the game channel
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        comm_deck -> an array of the Card object, ideally where the community deck is stored
    async def showCommCards(self, ctx, comm_deck):
        await ctx.send("**CURRENT COMMUNITY DECK**")
        commCards=""
        i=0
        for card in comm_deck:
            commCards+=card.show()
            i+=1
        for j in range(5-i):
            commCards+="<:back:867926963061411871>"
        await ctx.send(commCards)
    
    # outputs the announcing message that someone has raised the bet amount 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        name -> the string of the player's name
    #        amount -> the string of the raise amount 
    async def reportRaise(self, ctx, name, amount):
        await ctx.send(name + " has raised to " + amount + " <:chips:865450470671646760>!")

    # outputs the announcing message that someone has called
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        name -> the string of the player name 
    async def reportCall(self, ctx, name):
        await ctx.send(name + " has called!")

    # outputs the announcing message that someone has folded 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        name -> the string of the player name
    async def reportFold(self, ctx, name):
        await ctx.send(name + " has folded!")
    
    # outputs the announcing message that someone has checked 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        name -> the string of the player name 
    async def reportCheck(self, ctx, name):
        await ctx.send(name + " has checked!")

    # outputs the balances of all the participating poker players 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        pkr_players -> a list of Poker Player objects. a list of all the particpants
    async def showBalances(self, ctx, pkr_players):
        await ctx.send("CURRENT BALANCES:")
        for player in pkr_players:
            await ctx.send(player.username() + ": " + str(player.getGameBalance())+ " <:chips:865450470671646760>")
    
    # outputs the formatted player profile 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        game -> a PokerWrapper object. the current game information 
    async def showPlayer(self, ctx, game):
        embed = discord.Embed(title=game.competing[0].username(), 
        description="Balance: "+str(game.competing[0].getGameBalance())+" <:chips:865450470671646760>" + """
        In Pot: """ + str(game.competing[0]._inPot)+""" <:chips:865450470671646760>
        
        Current Pot: """+ str(game.currentPot),
        color=discord.Color.green())
        embed.set_thumbnail(url=game.competing[0]._user.avatar_url)
        await ctx.send(embed=embed)

    # outputs the announcing message that requests if anyone would like to leave the poker game
    # input: ctx -> a class object. part of Discord API, the context of the message
    async def askLeave(self, ctx):
        await ctx.send("If you would like to leave the game, type the command .leave")
    
    # outputs the announcing message that a game has restarted 
    # input: ctx -> a class object. part of Discord API, the context of the message
    async def resetGame(self, ctx):
        await ctx.send("\n\n**A NEW GAME HAS STARTED**")

    # outputs the error message that a game is already ongoing in the current channel 
    # input: ctx -> a class object. part of Discord API, the context of the message
    async def gameAlreadyInProgress(self, ctx):
        await ctx.send("Cannot create game: Game is already in progress in this channel!")

    # outputs the error message that the player does not have a profile created 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API, the user information 
    async def noAccount(self, ctx, user):
        await ctx.send(f"{user.mention} You do not have an account! Use the command .create to create an account!")
    
    # outputs the error message that a player tried to join a game that they are already in 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API, the user information 
    async def playerAlreadyInGame(self, ctx, user):
        await ctx.send(f"{user.mention} You are already in game! Use the .leave command to exit your current game to join a new one!")
    
    # outputs the error message that there is no ongoing game
    # input: ctx -> a class object. part of Discord API, the context of the message
    async def noGame(self, ctx):
        await ctx.send(f"There is no game currently running in this channel")
    
    # outputs the announcing message that a player will join the game the next round 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API, the user information 
    async def addedToJoinQueue(self, ctx, user):
        await ctx.send(f"{user.mention} You have been added to the join queue! You will be in the next game once the round is over.")
    
    # outputs the announcing message that a player will leave the game the next round 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API, the user information 
    async def addedToLeaveQueue(self, ctx, user):
        await ctx.send(f"{user.mention} You have been added to the leave queue! You will exit the game once the round is over.")
    
    # outputs the announcing message that the player has joined the game for the new round 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API, the user information 
    async def playerHasJoined(self, ctx, user):
        await ctx.send(f"{user.mention} has joined the game!")
    
    # outputs the announcing message that the player has left for the new round 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API, the user information 
    async def playerHasLeft(self, ctx, user):
        await ctx.send(f"{user.mention} has left the game!")

    # outputs the announcing message that the player has been kicked when there are not enough 
    # participants 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API the user information 
    async def playerKicked(self, ctx, user):
        await ctx.send(f"{user.mention} You have been removed from the game as there are not enough players")
    
    # outputs the error message that a user in the current channel are typing in commands in a game 
    # they are not participating in 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API, the user information 
    async def notInGame(self, ctx, user):
        await ctx.send(f"{user.mention} You are not in this game! Use the .join command to join the game")

    # outputs the error message that a participant has already requested to leave the game 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API, the user information 
    async def alreadyInLeaveQueue(self, ctx, user):
        await ctx.send(f"{user.mention} You are already in the leave queue! You will be removed from the game after this round")
    
    # outputs the error message that a participant has already requested to join the game 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API, the user information 
    async def alreadyInJoinQueue(self, ctx, user):
        await ctx.send(f"{user.mention} You are already in the join queue! You will be added to the game after this round")

    async def gameIsFull(self, ctx, user):
        await ctx.send(f"{user.mention} Game is currently full. You will be added to the join queue.")
    
    #outputs the error message that a particpant has wagered an amount higher than their game balance 
    # input: ctx -> a class object. part of Discord API, the context of the message
    #        user -> a class object. part of the Discord API, the user information 
    async def aboveBalance(self, ctx, user):
        await ctx.send(f"{user.mention} You exceeded your game balance. Please wager a new amount.")
