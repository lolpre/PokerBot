from Poker.player import Player
from Poker.pokerplayer import PokerPlayer
from Poker.card import Card
from Poker.announcer import Announcer
import asyncio
import discord

class PokerWrapper:
    def __init__(self):
        self.gameID
        self.gameStarted=False
        self.numPlayers=0
        self.hardBlind=0
        self.currentPot=0
        self.pokerUI
        self.gamedeck
        self.communityDeck
        self.participants = []
        self.startingBalance
    
    async def startGame(self, ctx):
        await Announcer.initiateGame(ctx)
    
    async def setPlayers(self, ctx, bot):
        embed = discord.Embed(title="Poker: Texas hold 'em", 
        description="Starting Balance: "+str(self.startingBalance)+""" <:chips:865450470671646760>
        Min Bet: """+str(self.hardBlind)+""" <:chips:865450470671646760> 
        \nReact to Join!""",
        color=discord.Color.green())

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await asyncio.sleep(10)

        message = await ctx.fetch_message(message.id)

        for reaction in message.reactions:
            if reaction.emoji == '✅':
                i = 1
                async for user in reaction.users():
                    if user != bot.user:
                        self.participants.append(PokerPlayer(user.id, i))
                        i += 1
        if i < 3:
            await ctx.send("Not enough players")
            return False
        else:
            await ctx.send("Starting game with " + str(i) + " players")
            

    async def setBlind(self, ctx):
        
        def representsInt(s):
            try: 
                int(s)
                return True
            except ValueError:
                return False
        
        def verify(m):
            return m.author == ctx.message.author and representsInt(m.content)

        await Announcer.askBet(ctx)

        try:
            msg = await self.client.wait_for('message', check = verify, timeout = 30)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry, you took too long to type the blind")
            return False
        
        self.hardBlind = int(msg.content)

        #await Announcer.reportBet(ctx, blind)
        

