from Poker.player import Player
from Poker.pokerplayer import PokerPlayer
from Poker.deck import Deck
from Poker.card import Card
from Poker.announcer import Announcer
from Poker.evalhand import EvaluateHand
import asyncio
import discord
import math

'''

This is the PokerWrapper class. This class object represents one instance of 
a Poker game. It holds all the data for the game including the current players,
the game balance, the ids, etc. Having each game represented with this class
object allows for the PokerBot to host more than one game at a time.


'''


class PokerWrapper:
    def __init__(self, bot):
        self.bot=bot             #this sets the bot in discord to run
        self.game_id=0            #plan to have multiple games so this identifies running games
        self.game_started = False #check if there is game started
        self.num_players = 0 
        self.hard_blind = 0       #represents the higher initial bet
        self.small_blind=0        #represent lower initial bet
        self.current_pot = 0      #total reward for the winner of the round
        self.poker_ui = Announcer()  #this will allow bot to inform users what is happening
        self.game_deck = Deck()
        self.community_deck = []
        self.participants = []   #total people in the game
        self.competing = []      #users who are still playing the round
        self.join_queue=[]        #list of players waiting to join the game
        self.leave_queue=[]       #list of players waiting to leave the game
        self.starting_balance = 0 #set initial balance of the game

    #internal bot function that waits for command to start the game
    async def start_game(self, ctx):
        await self.poker_ui.initiate_game(ctx)
        
    #starts the game and sets player with the embed as the message being sent
    async def set_players(self, ctx, bot, players):
        embed = discord.Embed(title="Poker: Texas hold 'em",
                              description="Starting Balance: "+str(self.starting_balance)+""" <:chips:865450470671646760>
        Min Bet: """+str(self.hard_blind)+""" <:chips:865450470671646760>
        \nReact to Join!""",
            color=discord.Color.green())
        #the bot will wait until all responces or until time is up
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await asyncio.sleep(10)

        message = await ctx.fetch_message(message.id)
        
        # Checks for the check emotes which represents a player.
        for reaction in message.reactions:
            if reaction.emoji == '✅':
                i = 1
                async for user in reaction.users():
                    if user != bot.user and user.id not in players:
                        await self.poker_ui.no_account(ctx, user)
                        continue

                    if user != bot.user and players[user.id].in_game:
                        await self.poker_ui.player_already_in_game(ctx, user)
                        continue

                    if user != bot.user and len(self.participants) == 8:
                        await self.poker_ui.game_is_full(ctx, user)
                        new_player= PokerPlayer(user.name, i, user, self.starting_balance)
                        self.join_queue.append(new_player)

                    elif user != bot.user:
                        new_player= PokerPlayer(user.name, i, user, self.starting_balance)
                        self.participants.append(new_player)
                        players[user.id].in_game = True
                        i += 1
                        
        # Checks if there is enough players through the check emote it has to be greater than 2 as the bot represents 1 of them.
        if len(self.participants) < 2:
            await ctx.send("Not enough players")
            for p in self.participants:
                players[p.user.id].in_game = False
            self.participants = []
            return False
        else:
            await ctx.send("Starting game with " + str(len(self.participants)) + " players")
    
    # Adds to players to the game from the list of players waiting to be added.
    async def add_players(self, ctx, players):
        for new_player in self.join_queue:
            if len(self.participants) == 8:
                continue
            self.participants.append(new_player)
            players[new_player.user.id].in_game = True
            await self.poker_ui.player_has_joined(ctx, new_player.user)
            self.join_queue.remove(new_player)
        
    
    # Removes players based on the list of players ready to leave and checks if game is still able to play.
    async def leave_game(self, ctx, players, enough_players):
        for x in self.leave_queue:
            players[x.user.id].balance+= x.get_game_balance()-self.starting_balance
            players[x.user.id].in_game = False
            self.participants.remove(x)
            if enough_players:
                await self.poker_ui.player_has_left(ctx, x.user)
            elif not enough_players:
                await self.poker_ui.player_kicked(ctx, x.user)
            
        self.leave_queue.clear()
    
    # Sets the blind at the start of the game and takes in input from users.
    async def set_blind(self, ctx, bot):

        def represents_int(s):
            try:
                int(s)
                return True
            except ValueError:
                return False

        def verify(m):
            return m.author == ctx.message.author and represents_int(m.content)

        await self.poker_ui.ask_bet(ctx)

        try:
            msg = await bot.wait_for('message', check=verify, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry, you took too long to type the blind")
            return False

        self.hard_blind = int(msg.content)
        self.small_blind = math.floor(self.hard_blind/2)

    
    
    # This updates the players balance after the end of each round.
    async def set_balance(self, ctx):

        def represents_int(s):
            try: 
                int(s)
                return True
            except ValueError:
                return False

        def verify(m):
            return m.author == ctx.message.author and represents_int(m.content)

        await self.poker_ui.ask_balance(ctx)

        try:
            msg = await self.bot.wait_for('message', check = verify, timeout = 30)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry, you took too long to type the balance")
            return False

        self.starting_balance = int(msg.content)

    # Deals cards to players and community card.
    async def deal_cards(self, bot):
        self.game_deck.shuffle()

        for p in self.participants:
            for i in range(2):
                c = self.game_deck.draw_card()
                p.add_card(c)
            await p.send_hand(bot)
    
    # Check if the current players in the game have balance to continue playing.
    def check_player_balance(self):
        for i in self.participants:
            if i.get_game_balance() <= 0:
                self.participants.remove(i)
    
    # Removes player from current rouhd with fold command.
    def player_fold(self, id):
        self.competing.pop(0)
    
    # Remove player from the current game.
    def remove_player(self, id):
        for i in self.participants:
            if i.username() == id:
                self.participants.remove(i)
        self.num_players -= 1
    
    # Makes community hand.
    def create_comm_deck(self):
        i = 0
        for i in range(3):
            self.add_card_to_comm()
    
    # Adds card to community card
    def add_card_to_comm(self):
        self.community_deck.append(self.game_deck.draw_card())
    
    # At the end of each round find the winner.
    def find_winner(self):
        eval = EvaluateHand(self.community_deck)
        for x in self.competing:
            command_hand = self.community_deck + x.hand
            Eval = EvaluateHand(command_hand)
            x.win_condition = Eval.evaluate()

        winning_cond = max(x.win_condition[0] for x in self.competing)
        compete = []
        for x in self.competing:
            if x.win_condition[0] == winning_cond:
                compete.append(x)
        winners = Eval.winning(compete, winning_cond)
        return winners
    
    # Reset the round.
    def reset_round(self):
        self.game_started = False
        self.current_pot = 0
        self.community_deck.clear()
        self.game_deck = Deck()
        self.num_players = len(self.participants)
        temp = self.participants.pop(0)
        self.participants.append(temp)
        self.competing.clear()
        for x in self.participants:
            x.hand = []
            x.game_balance=int(x.game_balance-x.in_pot)
            x.in_pot=0
            
