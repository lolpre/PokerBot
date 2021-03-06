"""
This is the main class for the Poker Bot.
It configures the Discord bot and uses the token to start it.
"""
import os
import time
import discord
from discord.ext import commands

from Poker.server import Server

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
DESCRIPTION = '''A bot to play Poker with.'''
bot = commands.Bot(command_prefix='.', description = DESCRIPTION)
bot.remove_command('help')

def main():
    """This is the main function that runs the Discord bot"""
    try:
        bot.run(TOKEN)
    finally:
        print(f'End running at {time.asctime(time.localtime(time.time()))}')

@bot.event
async def on_ready():
    """
    This is a Discord event that executes
    when the bot first comes online.
    """
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')

server_bot = Server(bot)  # Creates a Server object and passes in the bot object

@bot.command()
async def help(ctx):
    """
    This is the function that handles the help command.
    It returns the help menu for the bot.
    """
    await server_bot.help(ctx)

@bot.command()
async def create(ctx):
    """
    This is the function that handles the create command.
    It creates a new player object and adds it to the server.
    """
    await server_bot.add_player(ctx)

@bot.command()
async def top(ctx):
    """
    This is the function that handles the top command.
    It returns the current leaderboard in the server.
    """
    await server_bot.print_leaderboard(ctx)

@bot.command()
async def balance(ctx):
    """
    This is the function that handles the balance command.
    It returns the balance of a player.
    """
    await server_bot.get_balance(ctx)

@bot.command(aliases = ['p'])
async def poker(ctx):
    """
    This is the function that handles the poker command.
    it starts a new poker game.
    """
    await server_bot.initiate_game(ctx, ctx.message.channel.id, bot)

@bot.command()
async def join(ctx):
    """
    This is the function that handles the join command.
    It allows players to join an existing poker game.
    """
    await server_bot.join(ctx, ctx.message.channel.id)

@bot.command()
async def leave(ctx):
    """
    This is the function that handles the leave command.
    It removes a player from an existing poker game.
    """
    await server_bot.leave(ctx, ctx.message.channel.id)

@bot.command()
async def reset(ctx):
    """
    This is the function that handles the reset command.
    It allows Discord mods to reset the leaderboard and game.
    balances within a server.
    """
    if ctx.message.author.guild_permissions.administrator:
        await server_bot.reset()

if __name__ == '__main__':
    main()
