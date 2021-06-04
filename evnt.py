import discord
import random
import math
import time
import os
import json
from discord.ext import commands, tasks

class Evnt(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print('Bot is running.')
		await self.client.change_presence(activity=discord.Game(".help"))


	#On message events
	@commands.Cog.listener()
	async def on_message(self, message):
		if (not message.author.bot):
			channel = message.channel
			if (1):
				if (message.content.startswith("thank you") or message.content.startswith("thanks") or 
				message.content == "ty" or message.content.startswith("ty!") or 
				message.content.startswith("tyty") or message.content.startswith("tysm") or
				message.content.startswith("ty ") or message.content.startswith("THANK YOU") or
				message.content.startswith("THANKS") or message.content == "TY" or 
				message.content.startswith("TY!") or message.content.startswith("TYTY") or 
				message.content.startswith("TYSM") or message.content.startswith("TY ")):

					responses = [
						"My pleasure",
						"You're welcome",
						"No problem",
						"Don't mention it",
						"No worries",
						"I gotchu",
						"Not a problem",
						"It was nothing",
						"I'm happy to help",
						"Not at all",
						"Anytime",
						"No big deal",
						"Glad to help",
						"I am here to help",
						"I know you'd do the same for me",
						"You deserve it",
						"It was my privilege",
					]

					
					await channel.send(random.choice(responses))

			if (1):
				if message.content.lower().startswith('im '):
					channel = message.channel
					name = message.content[3:]
					await channel.send(f"Hi {name}, I'm Unemployed Bot!")
				elif message.content.lower().startswith("i'm "):
					channel = message.channel
					name = message.content[4:]
					await channel.send(f"Hi {name}, I'm Unemployed Bot!")
				elif message.content.lower().startswith("i am "):
					channel = message.channel
					name = message.content[5:]
					await channel.send(f"Hi {name}, I'm Unemployed Bot!")
				elif message.content.lower().startswith("i’m "):
					channel = message.channel
					name = message.content[4:]
					await channel.send(f"Hi {name}, I'm Unemployed Bot!")

			if (1):
				if message.content == "D:":
					await channel.send(file=discord.File('capital_d_colon.jpg'))
				elif message.content == "Pog":
					await channel.send(file=discord.File('pog.png'))
				elif message.content == "Sadge":
					await channel.send(file=discord.File('sadge.png'))
				elif message.content == "PePeHands":
					await channel.send(file=discord.File('pepehands.png'))
				elif message.content == "Kappa":
					await channel.send(file=discord.File('kappa.png'))
				elif message.content == "POGGERS":
					await channel.send(file=discord.File('poggers.png'))
				elif message.content == "monkaW":
					await channel.send(file=discord.File('monkaw.png'))
				elif message.content == "NotLikeThis":
					await channel.send(file=discord.File('notlikethis.png'))

			if (1):
				if message.content == "FUCK U FROG":
					await channel.send("No, fuck you Leo")
				if message.content == f'<@!{self.client.user.id}>':
					await channel.send("wassup")


		# await self.client.process_commands(message)

def setup(client):
	client.add_cog(Evnt(client))