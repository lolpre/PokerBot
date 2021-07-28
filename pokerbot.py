import asyncio
import discord
from discord.ext import commands
import time
import os

from Poker.server import Server
from Poker.pokerwrapper import PokerWrapper

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
description = '''A bot to play Poker with.'''
bot = commands.Bot(command_prefix='.', description=description)
bot.remove_command('help')

def main():
    try:
        bot.run(TOKEN)
    finally:
        print(f'End running at {time.asctime(time.localtime(time.time()))}')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')

server_bot = Server(bot)
# leaderboard_bot = Leaderboard(bot)


@bot.command()
async def help(ctx):
    await server_bot.help(ctx)
    

@bot.command()
async def create(ctx):
    await server_bot.addPlayer(ctx)
        


@bot.command()
async def top(ctx):
    await server_bot.printLeaderboard(ctx)


@bot.command()
async def balance(ctx):
    await server_bot.getBalance(ctx)


@bot.command() 
async def p(ctx):
    await server_bot.initiateGame(ctx, ctx.message.channel.id, bot)
    
@bot.command() 
async def join(ctx):
    await server_bot.join(ctx, ctx.message.channel.id)        
        
@bot.command() 
async def leave(ctx):
    await server_bot.leave(ctx, ctx.message.channel.id)      

@bot.command() 
async def reset(ctx):
    if ctx.message.author.guild_permissions.administrator:
        await server_bot.reset()
    
if __name__ == '__main__':
    main()
