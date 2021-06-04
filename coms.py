import discord
import random
import math
import time
import os
from discord.ext import commands, tasks

class Coms(commands.Cog):

	def __init__(self, client):
		self.client = client

	#Help command
	@commands.command()
	async def help(self, ctx):
		author = ctx.message.author

		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.set_author(name = "List of commands")
		embed.add_field(name = '.8ball <Question>', value = 'Ask a yes/no question and you shall receive an answer!', inline = False)
		embed.add_field(name = '.bitch', value = 'Returns a bitch answer!', inline = False)
		embed.add_field(name = '.vs <Subject A> <Subject B> <Number of fights>', 
			value = 'Battle 2 subjects against each other to see who comes out on top!', inline = False)
		embed.add_field(name = 'List of Emotes', value = 'D:, Pog, Sadge, PePeHands, Kappa, POGGERS, monkaW, NotLikeThis', inline = False)
		embed.add_field(name = '.<Turb>', value = 'Get a quote from a turb!', inline = False)
		embed.add_field(name = '.guess <Number>', value = "Try to guess the number between 1 and the number of your choosing!"
			+ "\n\u200b", inline = False)
		embed.add_field(name = 'Casino Commands', value = "**.register:** Register a bank account for your money!\n" + 
			"**.balance** Check how much money you have in your account!\n" + "**.cashin <Kakera>:** Cash in kakera for cash!\n" + 
			"**.cashout: <Dollars>** Cash out cash for kakera!\n" + "**.blackjack <Betting Money>:** Play a game of Blackjack with bets!\n" +
			"**.bjrules** Read the rules of the Blackjack game!", inline = False)




		await ctx.send("DM sent!")
		await ctx.message.author.send(author, embed = embed)

	#8ball command
	@commands.command(aliases=['8ball'])
	async def _8ball(self, ctx, *, question):
		responses = [
			"It is certain.",
			"It is decidedly so.",
			"Without a doubt.",
			"Yes - definitely.",
			"You may rely on it.",
			"As I see it, yes.",
			"Most likely.",
			"Outlook good.",
			"Yes.",
			"Signs point to yes.",
			"Reply hazy, try again.",
			"Ask again later.",
			"Better not tell you now.",
			"Cannot predict now.",
			"Concentrate and ask again.",
			"Don't count on it.",
			"My reply is no.",
			"My sources say no.",
			"Outlook not so good.",
			"Very doubtful.",
			"No.",
			"Most likely not.",
			"No - definitely not.",
			"My answer is no.",
			"Signs point to no."
			]
		await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

	@_8ball.error
	async def _8ball_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please ask a question.')

	#Bitch command
	@commands.command()
	async def bitch(self, ctx):
		responses = [
			"biiiiitch",
			"no you're the bitch",
			"bitch?",
			"BITCH",
			"ahhhhh it's a bitch!",
			"stop being a bitch",
			"bitch please",
			"bitch you guessin",
			"why are you such a bitch?",
			"bitch bitch bitch bitch bitch bitch bitch bitch bitch",
			"you're a bitch",
			"Beautiful Individual That Correct Hoes",
			"stop bitchin",
			"b\ni\nt\nc\nh",
			"hoe"
			]
		await ctx.send(random.choice(responses))

	#VS command
	@commands.command()
	async def vs(self, ctx, a, b, n=1):
		tmp = [a, b]
		if n == 1:
			await ctx.send(f"{a} and {b} battle it out...")
			await ctx.send(f"The winner is: {random.choice(tmp)}!")
		elif n < 1:
			await ctx.send(f"Please let them fight at least once")
		elif n > 1 and n <= 1000000:
			aCounter = 0
			bCounter = 0
			i = 0
			while i < n:
				if random.choice(tmp) == a:
					aCounter += 1
				else:
					bCounter += 1
				i += 1
			await ctx.send(f"{a} and {b} battle it out...")
			await ctx.send(f"{a} has won {aCounter} times and {b} has won {bCounter} times!")
		elif n > 1000000:
			stop = ["Stop", "No", "Don't make me"]
			await ctx.send(f"{random.choice(stop)}")

	@commands.command()
	async def josh(self, ctx):
		choices = ["I was asleep", "아니..뭐해?", "크 이거지", "Wtf", 
		"OK *insert name*", "아니 시발 이게 죽어?", "Fuck maan"]
		await ctx.send(random.choice(choices))

	@commands.command()
	async def stefan(self, ctx):
		choices = ["I am SPEED", "It's time to roll", "I JUST said that", "you suck"]
		await ctx.send(random.choice(choices))

	@commands.command()
	async def andrew(self, ctx):
		choices = ["Can't wait to clap some CHEEKS", "Fellas", "Big tiddy anime girl"]
		await ctx.send(random.choice(choices))

	@commands.command()
	async def lauren(self, ctx):
		choices = ["STAAAAHP", "Broski", "thank"]
		await ctx.send(random.choice(choices))

	@commands.command()
	async def john(self, ctx):
		choices = ["Tall people scare me", "Hooow's it goooin?", "Stwooaapp"]
		await ctx.send(random.choice(choices))

	@commands.command(aliases=["gwyneth"])
	async def gwyn(self, ctx):
		await ctx.send("CARAMEL OPPAAAA")

	@commands.command(aliases=["catherine"])
	async def cat(self, ctx):
		choices = ["AS *clap* YOU *clap* SHOULD", "Oh my gawwwwd Yes!", "Hellooooooo"]
		await ctx.send(random.choice(choices))

	@commands.command()
	async def jared(self, ctx):
		await ctx.send("Oh my god, there's a Pikachu in the area!")

	@commands.command()
	async def betsy(self, ctx):
		await ctx.send("Hong Kong number one babyyyyyyyyy")

	@commands.command()
	async def eric(self, ctx):
		await ctx.send("Nothing can stop my study and my horny")
	
	@commands.command()
	async def jakin(self, ctx):
		choices = ["No.", "Do you want to play ARAM", "Hello there", "너를 욕하는건 되지만 아스나를 욕하는 더더욱 돼"
		, "Fuck this dogshit game", "You can't catch me I'm the gingerbread man"]
		await ctx.send(random.choice(choices))
	
	@commands.command()
	async def leo(self, ctx):
		choices = ["I love lolis", "응 아스나", "나를 욕하는건 되지만 아스나를 욕하는건 더더욱 안돼", "숨도 쉬지마"
		, "근손실", "하암~졸려", "이게 나야~"]
		await ctx.send(random.choice(choices))

	@commands.command()
	async def gerry(self, ctx):
		choices = ["귀찮아", "야 ㄱ..ㄱㄱ.ㄱㄱ...그거 알아?", "니 A미요!", "꺼져 이 *C*발로마", "Meet you at the top *BRO*",
		"시..시..시발롬아!", "아니야 이길수있어 이길수있어", "안돼ㅐㅐㅐㅐㅐ"]
		await ctx.send(random.choice(choices))

	@commands.command()
	async def bjrules(self, ctx):
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.set_author(name = "Black Jack")
		embed.add_field(name = "Basic Rules:",
		 value = "**1.** The player and the dealer gets dealt 2 cards each. Only 1 of the dealer's cards will be shown.\n" + 
		 "**2.** The main goal is to get to a sum of 21 as close as possible. If the player goes over 21, they 'bust' and lose the game.\n" + 
		 "**3.** Kings, Queens, and Jacks are worth 10. An Ace can either be counted as a 1 or 11.\n" +
		 "**4.** The player can either hit, stand, or double down. More info on these moves down below.\n" +
		 "**5.** If the player gets to 21 closer than the dealer, the player wins. \
		  If the dealer gets closer, the dealer wins. If they tie, it is called a 'push'.\n" + 
		 "**6.** When a player stands, the player's turn is over and the dealer will draw cards until his total is at least 17.\n" +
		 "**7.** A player can only bet from $1 to $125 for one Blackjack game.\n", inline = False)
		embed.add_field(name = "Player Moves:", value = "**1. Hit:** If a player hits, they will get dealt one card from the deck. They \
			will not be able to double down if they have already hit at least once.\n" + "**2. Stand:** If a player stands, they will \
			keep their current hand and end their turn.\n" + "**3. Double Down:** If a player double downs, their bet will be doubled \
			and then will be dealt another card. Their only move after doubling down is to stand.\n" + "**4. Split:** If a player splits, \
			their 2 cards will be split into 2 separate hands, placing another bet (equal to the original bet) on the additional hand. If \
			two Aces get split, the player will only be allowed to stand after.")


		
		await ctx.send(embed = embed)


def setup(client):
	client.add_cog(Coms(client))

if __name__ == "__main__":
	pass