import discord
import random
import math
import time
import os
from discord.ext import commands, tasks


client = commands.Bot(command_prefix = '.', case_insensitive = True)
client.remove_command('help')

for filename in os.listdir('./cogs'):
	if (filename == "card.py" or filename == "deck.py" or filename == "player.py"):
		continue

	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')



if __name__ == "__main__":
	pass

client.run('Nzc5MTM5MDExMTY3NzgwODY0.X7cLvw.Z1Q7wDRWoBmstcqN0UaAVWGWhTo')


