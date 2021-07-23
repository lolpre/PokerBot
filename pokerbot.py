import discord
from discord.ext import commands
import time

from Poker.server import Server
from Poker.leaderboard import Leaderboard


intents = discord.Intents.default()
intents.members = True
description = '''A bot to play Poker with.'''
bot = commands.Bot(command_prefix='.', description=description)
bot.remove_command('help')

def main():
    try:
        bot.run('ODUwNDYyMjIyNTA4NDkwODAz.YLqEqg.HQJ4T5FOgN0Y9Ko9dw31bY4hj0w')
    finally:
        print(f'End running at {time.asctime(time.localtime(time.time()))}')
        # print("hi")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')

server_bot = Server()
leaderboard_bot = Leaderboard()

@bot.command()
async def help(ctx):
    await server_bot.help(ctx)

@bot.command()
async def create(ctx):
    server_bot.addPlayer(ctx)
    leaderboard_bot.addplayer(str(str(ctx.author.name) + "#" + str(ctx.author.discriminator)))
    await ctx.send("You have created an account!")

@bot.command()
async def top(ctx):
    await leaderboard_bot.printLeaderboard(ctx)

@bot.command()
async def balance(ctx):
    await server_bot.getBalance(ctx)

@bot.command()
async def p(ctx):
    await server_bot.initiateGame(ctx, bot)

if __name__ == '__main__':
    main()