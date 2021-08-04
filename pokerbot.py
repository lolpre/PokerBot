import asyncio
import discord
from discord.ext import commands
import time
import os

from Poker.server import Server
from Poker.pokerwrapper import PokerWrapper

'''
This is the main class for the Poker Bot. 
It configures the Discord bot and uses the token to start it.
'''

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
description = '''A bot to play Poker with.'''
bot = commands.Bot(command_prefix='.', description=description)
bot.remove_command('help')

# This is the main function that runs the Discord bot
def main():
    try:
        bot.run(TOKEN)
    finally:
        print(f'End running at {time.asctime(time.localtime(time.time()))}')

# This is a Discord event that executes 
# when the bot first comes online
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')

server_bot = Server(bot) # Creates a Server object and passes in the bot object
# leaderboard_bot = Leaderboard(bot)

# This is the function that handles the help command
# It returns the help menu for the bot
@bot.command()
async def help(ctx):
    await server_bot.help(ctx)
    
# This is the function that handles the create command
# It creates a new player object and adds it to the server
@bot.command()
async def create(ctx):
    await server_bot.addPlayer(ctx)
        

# This is the function that handles the top command
# It returns the current leaderboard in the server
@bot.command()
async def top(ctx):
    await server_bot.printLeaderboard(ctx)

# This is the function that handles the balance command
# It returns the balance of a player
@bot.command()
async def balance(ctx):
    await server_bot.getBalance(ctx)

# This is the function that handles the poker command
# it starts a new poker game
@bot.command() 
async def p(ctx):
    await server_bot.initiateGame(ctx, ctx.message.channel.id, bot)

# This is the function that handles the join command
# It allows players to join an existing poker game
@bot.command() 
async def join(ctx):
    await server_bot.join(ctx, ctx.message.channel.id)        

# This is the function that handles the leave command
# It removes a player from an existing poker game
@bot.command() 
async def leave(ctx):
    await server_bot.leave(ctx, ctx.message.channel.id)      

# This is the function that handles the reset command
# It allows Discord mods to reset the leaderboard and game 
# balances within a server
@bot.command() 
async def reset(ctx):
    if ctx.message.author.guild_permissions.administrator:
        await server_bot.reset()
    
if __name__ == '__main__':
    main()
