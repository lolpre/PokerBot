import discord
from discord.ext import commands
import time


intents = discord.Intents.default()
intents.members = True
description = '''A bot to play Poker with.'''
bot = commands.Bot(command_prefix='.', description=description)

def main():
    try:
        bot.run('ODUwNDYyMjIyNTA4NDkwODAz.YLqEqg.HQJ4T5FOgN0Y9Ko9dw31bY4hj0w')
    finally:
        print(f'End running at {time.asctime(time.localtime(time.time()))}')
        # print("hi")


if __name__ == '__main__':
    main()