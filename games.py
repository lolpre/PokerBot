import discord
import random
import math
import time
import os
import asyncio
import json
from discord.ext import commands, tasks
from player import Player
from deck import Deck 
from card import Card




class Games(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.servers = {616806825278308390: 0, 783077057633976340: 0}
		self.suits = {"Spades": "♤", "Clubs": "♧", "Diamonds": "♢", "Heart": "♡"}
		self.cardValues = { 'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10 }
		self.accounts = {}
		self.loadAccounts()
		

# if ctx.author.id != 261877058525724685:
		# 	return

	def loadAccounts(self):
		try:
			with open('accounts.json') as f:
				self.accounts = json.load(f)
		except FileNotFoundError:
			print("Could not load accounts.json")

	@commands.command()
	async def register(self, ctx):
		id = str(ctx.author.id)
		if id not in self.accounts:
			self.accounts[id] = 0
			await ctx.send("You have successfully registered your account! Your current balance is $0.")
			self.save()
		else:
			await ctx.send("You have already made an account!") 


	@commands.command()
	async def balance(self, ctx):
		id = str(ctx.author.id)
		if id not in self.accounts:
			return await ctx.send("You do not have an account!")
		else:
			await ctx.send(f"You have ${self.accounts[id]:.2f}!")

	def save(self):
		with open('accounts.json', 'w+') as f:
			json.dump(self.accounts, f)

	@commands.command()
	async def cashin(self, ctx, kakera):
		id = str(ctx.author.id)
		if id not in self.accounts:
			return await ctx.send("You do not have an account!")
		if (kakera.isdigit() == False or int(kakera) < 2):
			return await ctx.send("Please enter a valid number of kakera. At least 2 ka minimum.")
		def verify(m):
			return ((m.author == ctx.message.author) and (
				" ".join(m.content.lower().split()) == f"$me <@!{self.client.user.id}> {kakera} ka" or 
				" ".join(m.content.lower().split()) == f"$me <@!{self.client.user.id}> {kakera}ka")) or (
					m.author == ctx.message.author and m.content.lower() == ".exit")

		dollars = round((int(kakera) / 100) - 0.01, 2)
		money = self.accounts[id]
		await ctx.send(f"Please type in the command: $me <@!{self.client.user.id}> {kakera} ka")
		try:
			msg = await self.client.wait_for('message', check = verify, timeout = 30)
		except asyncio.TimeoutError:
			return await ctx.send(f"Sorry, you took too long to type the command")
		if msg.content == ".exit":
			return await ctx.send("Cash-in Procedure Has Stopped")

		await asyncio.sleep(3)
		await ctx.send("1 ka")
		
		def exchanged(m):
			return m.author.id == 432610292342587392 and f"The exchange is over" in m.content

		try:
			msg2 = await self.client.wait_for('message', check = exchanged, timeout = 30)
		except asyncio.TimeoutError:
			return await ctx.send("Sorry, the exchange time took too long!")

		self.accounts[id] = money + dollars
		self.save()
		return await ctx.send(f"${float(dollars):.2f} has been added to your account!")
	# @cashin.error
	# async def cashin_error(self, ctx, error):
	# 	if isinstance(error, commands.MissingRequiredArgument):
	# 		await ctx.send("Format: .cashin <kakera>")


	@commands.command()
	async def cashout(self, ctx, dollars):
		id = str(ctx.author.id)
		if id not in self.accounts:
			return await ctx.send("You do not have an account!")
		try:
			float(dollars)
		except ValueError:
			return await ctx.send("Please enter a valid amount of dollars")

		money = self.accounts[id]
		if float(dollars) > money:
			return await ctx.send("You don't have that money my dude.")

		def verify(m):
			return (m.author == ctx.message.author and (" ".join(m.content.lower().split()) == f"$me <@!{self.client.user.id}> 1 ka" or 
														" ".join(m.content.lower().split()) == f"$me <@!{self.client.user.id}> 1ka")) or (
					m.author == ctx.message.author and m.content == ".exit")

		kakera = float(dollars) * 100 + 1
		await ctx.send(f"Please type in the command: $me <@!{self.client.user.id}> 1 ka")
		try:
			msg = await self.client.wait_for('message', check = verify, timeout = 30)
		except asyncio.TimeoutError:
			return await ctx.send(f"Sorry, you took too long to type the command")

		if msg.content == ".exit":
			return await ctx.send("Cash-out Procedure Has Stopped")

		await asyncio.sleep(3)
		await ctx.send(f"{kakera} ka")

		def exchanged(m):
			return m.author.id == 432610292342587392 and f"The exchange is over" in m.content

		try:
			msg2 = await self.client.wait_for('message', check = exchanged, timeout = 30)
		except asyncio.TimeoutError:
			return await ctx.send("Sorry, the exchange time took too long!")

		self.accounts[id] = money - float(dollars)
		self.save()
		return await ctx.send("You have successfully cashed out your money!")
	@cashout.error
	async def cashout_error(self,ctx,error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Format: .cashout <dollars>")

	
#Blackjack commands-------------------------------------------------------------------------------------------------
#add another line for 100ka for stefan
#
	def changeBet(self, isWin, id, dollars):
			if isWin == True:
				self.accounts[id] += float(dollars)
			else:
				self.accounts[id] -= float(dollars)
			self.save()

	def is_number(self, string):
		try:
			float(string)
			return True
		except ValueError:
			return False

	def makeHands(self, hands, dHand, calc2, inPlay):
		embed = discord.Embed(colour = discord.Colour.orange())

		if inPlay == True:
			dealerString = ""
			for card in dHand:
				dealerString += self.suits[card.suit] + card.val + ":black_medium_small_square:"
			dealerString += f"\n\nTotal = {calc2}"
		elif inPlay == False:
			dealerString = ""
			for card in dHand:
				dealerString += self.suits[card.suit] + card.val + ":black_medium_small_square:"
				firstVal = card.val
				break

			dealerString += f"\n\nTotal = {self.cardValues[firstVal]}"

		handString = ""
		i = 1
		for hand in hands:
			handString += f"Hand {i}:\n"
			for card in hand:
				handString += self.suits[card.suit] + card.val + ":black_medium_small_square:"
			calc = self.calcHand(hand)
			handString += f"\nTotal = {calc}"
			handString += "\n\n"
			i += 1
		
		embed.add_field(name = "Dealer's Hand:", value = dealerString, inline = False)
		embed.add_field(name = chr(173), value = chr(173), inline = False)
		embed.add_field(name = "Player's Hand(s):", value = handString, inline = False)
		return embed

	def calcHand(self, hand):
		total = 0
		Acounter = 0
		values = self.cardValues
		for card in hand:
			if card.val == 'A':
				Acounter += 1
			else:
				total += values[card.val]
		i = 0
		while i < Acounter:
			if total >= 11: total += 1
			else: total += 11
			i += 1

		return total

	def makeHand(self, hand):
		printHand = []
		for card in hand:
			printHand.append(f"{card.val} of {card.suit}")
		return printHand
	def checkServer(self, serverID):
		if self.servers[serverID] == 1:
			return True
		else:
			return False

	def changeState(self, serverID):
		if self.servers[serverID] == 1:
			self.servers[serverID] = 0
		else:
			self.servers[serverID] = 1

	def isPair(self, hand):
		if len(hand) == 2 and (hand[0].val == hand[1].val):
			return True
		else:
			return False
 

	@commands.command(aliases = ["bj"])
	async def blackjack(self, ctx, bet):
		serverid = ctx.message.guild.id
		if self.checkServer(serverid) == 1:
			return await ctx.send("There is already a game in progress!")
		self.changeState(serverid)
		id = str(ctx.author.id)
		if id not in self.accounts:
			self.changeState(serverid)
			return await ctx.send("You do not have an account!")

		if not self.is_number(bet):
			self.changeState(serverid)
			return await ctx.send("Please enter a valid amount of money")

		id = str(ctx.author.id)
		money = self.accounts[id]
		if float(bet) > money:
			self.changeState(serverid)
			return await ctx.send("You don't have that money my dude.")

		bet = float(bet)
		if bet < 1:
			self.changeState(serverid)
			return await ctx.send("You can not bet less than 1 dollar!")
		if bet > 125:
			self.changeState(serverid)
			return await ctx.send("You can not bet more than $125!")

		await ctx.send("Welcome to Blackjack! Try to beat the dealer by getting closer to 21!\n" + 
			"Type in the command .bjrules for more info!")
		

		def verify(m):
			return m.author == ctx.author and (m.content == "y" or m.content == "n")

		await ctx.send(f"Are you sure you want to play and bet ${bet:.2f}? (y/n)")
		try:
			msg = await self.client.wait_for('message', check = verify, timeout=30)
		except asyncio.TimeoutError:
			self.changeState(serverid)
			return await ctx.send("Sorry, it took you too long to answer!")

		if msg.content == "n":
			self.changeState(serverid)
			return await ctx.send("Game has been stopped.")

		deck = Deck()
		deck.shuffle()

		dealer = Player()
		player = Player()
		
		await ctx.send("Dealing 2 cards to each player...")
		player.draw(deck)
		dealer.draw(deck)
		player.draw(deck)
		dealer.draw(deck)

		pHands = []
		pHands.append(player.getHand())

		dHand = dealer.getHand()
		dTotal = dealer.calc_hand()

		if player.calc_hand() == 21 and dealer.calc_hand() != 21 and player.getNumber() == 2:
			bet = bet * 1.5
			self.changeBet(True, id, bet)
			self.changeState(serverid)
			await ctx.send(embed = self.makeHands(pHands, dHand, dTotal, True))
			await ctx.send(f"Congratulations you got a Blackjack! You have won ${bet:.2f}!")
			return await ctx.send(f"You now have ${self.accounts[id]:.2f}.")

		elif player.calc_hand() == 21 and dealer.calc_hand() == 21:
			self.changeState(serverid)
			await ctx.send(embed = self.makeHands(pHands, dHand, dTotal, True))
			return await ctx.send(f"Push! You have both tied! You lost $0.")

		

		i = 0
		betList = []
		pHands2 = list(pHands)
		for hand in pHands2:
			i += 1
			doubled = False
			didHit = False
			aceSplit = False
			tmpBet = bet
			while True:
				await ctx.send(embed = self.makeHands(pHands, dHand, dTotal, False))

				if self.calcHand(hand) > 21:
					if len(pHands) == 1:
						self.changeState(serverid)
						self.changeBet(False, id, tmpBet)
						await ctx.send(f"You have busted! You have lost ${tmpBet:.2f}")
						return await ctx.send(f"You now have ${self.accounts[id]:.2f}.")
					else:
						self.changeBet(False, id, tmpBet)
						await ctx.send(f"This hand has busted! You have lost ${tmpBet:.2f}")
						pHands.remove(hand)
						break
					
				def com1(m):
					return m.author == ctx.author and (m.content == "h" or m.content == "s" or m.content == "d")
				def com2(m):
					return m.author == ctx.author and (m.content == "h" or m.content == "s")
				def com3(m):
					return m.author == ctx.author and (m.content == "s")
				def com4(m):
					return m.author == ctx.author and (m.content == "h" or m.content == "s" or m.content == "d" or m.content == "sp")
				def com5(m):
					return m.author == ctx.author and (m.content == "h" or m.content == "s" or m.content == "sp")

				if doubled == True or aceSplit == True:
					await ctx.send("Please stand to continue. (s)")
					try:
						msg = await self.client.wait_for('message', check = com3, timeout = 120)
					except asyncio.TimeoutError:
						self.changeState(serverid)
						self.changeBet(False, id, bet)
						await ctx.send(f"Sorry you took too long. You have lost ${tmpBet:.2f}.")
						return await ctx.send(f"You now have ${self.accounts[id]:.2f}.")
				# elif (bet <= money / 2 and didHit == True) and self.isPair(hand):
				# 	await ctx.send(f"**Hand{i}:** Would you like to hit, stand, or split? (h, s, sp)")
				# 	try:
				# 		msg = await self.client.wait_for('message', check = com5, timeout = 120)
				# 	except asyncio.TimeoutError:
				# 		self.changeState(serverid)
				# 		self.changeBet(False, id, bet)
				# 		await ctx.send(f"Sorry you took too long. You have lost ${tmpBet:.2f}.")
				# 		return await ctx.send(f"You now have ${self.accounts[id]:.2f}.")
				elif (bet > money / 2 or didHit == True):
					await ctx.send(f"**Hand{i}:** Would you like to hit or stand? (h, s)")
					try:
						msg = await self.client.wait_for('message', check = com2, timeout = 120)
					except asyncio.TimeoutError:
						self.changeState(serverid)
						self.changeBet(False, id, bet)
						await ctx.send(f"Sorry you took too long. You have lost ${tmpBet:.2f}.")
						return await ctx.send(f"You now have ${self.accounts[id]:.2f}.")
				elif (bet <= money / 2) and self.isPair(hand):
					await ctx.send(f"**Hand{i}:** Would you like to hit, stand, double down, or split? (h, s, d, sp)")
					try:
						msg = await self.client.wait_for('message', check = com4, timeout = 120)
					except asyncio.TimeoutError:
						self.changeState(serverid)
						self.changeBet(False, id, bet)
						await ctx.send(f"Sorry you took too long. You have lost ${tmpBet:.2f}.")
						return await ctx.send(f"You now have ${self.accounts[id]:.2f}.")
				elif bet <= money / 2:
					await ctx.send(f"**Hand{i}:** Would you like to hit, stand, or double down? (h, s, d)")
					try:
						msg = await self.client.wait_for('message', check = com1, timeout = 120)
					except asyncio.TimeoutError:
						self.changeState(serverid)
						self.changeBet(False, id, bet)
						await ctx.send(f"Sorry you took too long. You have lost ${tmpBet:.2f}.")
						return await ctx.send(f"You now have ${self.accounts[id]:.2f}.")

				if msg.content == "h":
					didHit = True
					hand.append(deck.drawCard())
					continue
				elif msg.content == "d":
					doubled = True
					hand.append(deck.drawCard())
					tmpBet *= 2
					continue
				elif msg.content == "s":
					betList.append(tmpBet)
					break
				elif msg.content == "sp":
					money -= tmpBet
					newHand = []

					if hand[0].val == "A" and hand[1].val == "A":
						aceSplit = True

					newHand.append(hand.pop())
					newHand.append(deck.drawCard())
					hand.append(deck.drawCard())

					pHands.append(newHand)
					pHands2.append(newHand)

					continue
		
		await ctx.send(embed = self.makeHands(pHands, dHand, dTotal, True))
		while True:
			await asyncio.sleep(1)
			if dealer.calc_hand() < 17:
				dealer.draw(deck)
				dTotal = dealer.calc_hand()
				await ctx.send(embed = self.makeHands(pHands, dHand, dTotal, True))
			else:
				await asyncio.sleep(1)
				break

		i = 1
		for hand in pHands:
			tmpBet = betList[i - 1]
			if dealer.calc_hand() > 21:
				self.changeBet(True, id, tmpBet)
				await ctx.send(f"Hand {i} has won! You have won ${tmpBet:.2f}!")
			elif dealer.calc_hand() == self.calcHand(hand):
				await ctx.send(f"Hand {i} has tied! You have lost $0!")
			elif dealer.calc_hand() > self.calcHand(hand):
				self.changeBet(False, id, tmpBet)
				await ctx.send(f"Hand {i} has lost! You have lost ${tmpBet:.2f}!")
			elif dealer.calc_hand() < self.calcHand(hand):
				self.changeBet(True, id, tmpBet)
				await ctx.send(f"Hand {i} has won! You have won ${tmpBet:.2f}!")
			i += 1
		await ctx.send(f"You now have ${self.accounts[id]:.2f}.")
		self.changeState(serverid)

	# @blackjack.error
	# async def black_jack_error(self, ctx, error):
	# 	if isinstance(error, commands.MissingRequiredArgument):
	# 		await ctx.send("Format: .blackjack <betting money> (You can bet from $1 to $125)")

	@commands.command()
	async def test(self, ctx):
		deck = Deck()
		deck.shuffle()
		p = Player()
		d = Player()
		d.draw(deck)
		d.draw(deck)
		d.draw(deck)
		d.draw(deck)
		d.draw(deck)
		p.draw(deck)
		p.draw(deck)
		p.draw(deck)
		p.draw(deck)
		p.draw(deck)
		p.draw(deck)
		pHand = p.getHand()
		dHand = d.getHand()
		val = p.calc_hand()
		val2 = d.calc_hand()
		# await ctx.send(embed = self.makeHands(pHands,and, val2))

	@commands.command()
	async def guess(self, ctx, number):
		serverid = ctx.message.guild.id
		if self.checkServer(serverid) == 1:
			return await ctx.send("Game in progress, try again later.")

		self.changeState(serverid)

		if (number.isdigit() == False or int(number) <= 1):
			self.changeState(serverid)
			return await ctx.send("Please enter a number that is at least greater than 1")

		def is_author(m):
			return m.author == ctx.message.author and m.content.isdigit()

		num = random.randint(1, int(number))
		gss = 3

		while gss != 0:
			await ctx.send(f"Pick a number between 1 and {number}")
			try:
				msg = await self.client.wait_for('message', check = is_author, timeout=10)
			except asyncio.TimeoutError:
				self.changeState(serverid)
				return await ctx.send(f"Sorry, you took too long it was {num}.")
			attempt = int(msg.content)
			gss -= 1
			if gss == 0:
				break

			if attempt > int(number):
				await ctx.send("That number is too high!")
				continue
			if attempt < 1:
				await ctx.send("That number is too low!")
				continue

			if attempt > num:
				if gss > 1:
					await ctx.send(f"{gss} guesses left...")
				elif gss == 1:
					await ctx.send(f"{gss} guess left...")
				await ctx.send("Try going lower")

			elif attempt < num:
				if gss > 1:
					await ctx.send(f"{gss} guesses left...")
				elif gss == 1:
					await ctx.send(f"{gss} guess left...")
				await ctx.send("Try going higher")

			elif attempt == int(num):
				await ctx.send("Good job, you got it!")
				self.changeState(serverid)
				return
			

		await ctx.send(f"Aw you couldn't get it. The answer was {num}!")
		self.changeState(serverid)
	@guess.error
	async def guess_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Format: .guess <number>')



def setup(client):
	client.add_cog(Games(client))