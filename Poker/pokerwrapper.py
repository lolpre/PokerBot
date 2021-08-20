"""
PokerWrapper.
"""
import asyncio
import math
import discord
from Poker.pokerplayer import PokerPlayer
from Poker.deck import Deck
from Poker.announcer import Announcer
from Poker.evalhand import EvaluateHand


class PokerWrapper:
    """
    This is the PokerWrapper class. This class object represents one instance of
    a Poker game. It holds all the data for the game including the current players,
    the game balance, the ids, etc. Having each game represented with this class
    object allows for the PokerBot to host more than one game at a time.
    """

    def __init__(self, bot):
        self.bot = bot  # this sets the bot in discord to run
        self.game_id = 0  # plan to have multiple games so this identifies running games
        self.game_started = False  # check if there is game started
        self.num_players = 0
        self.hard_blind = 0  # represents the higher initial bet
        self.small_blind = 0  # represent lower initial bet
        self.current_pot = 0  # total reward for the winner of the round
        self.poker_ui = Announcer()  # this will allow bot to inform users what is happening
        self.game_deck = Deck()
        self.community_deck = []
        self.participants = []  # total people in the game
        self.competing = []  # users who are still playing the round
        self.join_queue = []  # list of players waiting to join the game
        self.leave_queue = []  # list of players waiting to leave the game
        self.starting_balance = 0  # set initial balance of the game

    async def start_game(self, ctx):
        """Internal bot function that waits for command to start the game."""

        await self.poker_ui.initiate_game(ctx)

    async def set_players(self, ctx, bot, players):
        """Starts the game and sets player with the embed as the message being sent."""

        embed = discord.Embed(title="Poker: Texas hold 'em",
                              description="Starting Balance: "+str(self.starting_balance) + """
                              <:chips:865450470671646760>
        Min Bet: """ + str(self.hard_blind) + """ <:chips:865450470671646760>
        \nReact to Join!""",
            color=discord.Color.green())

        # The bot will wait until all responces or until time is up
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
                        new_player = PokerPlayer(
                            user.name, i, user, self.starting_balance)
                        self.join_queue.append(new_player)

                    elif user != bot.user:
                        new_player = PokerPlayer(
                            user.name, i, user, self.starting_balance)
                        self.participants.append(new_player)
                        players[user.id].in_game = True
                        i += 1

        # Checks if there is enough players through the check emote it has
        # to be greater than 2 as the bot represents 1 of them.
        if len(self.participants) < 2:
            await ctx.send("Not enough players")
            for p_player in self.participants:
                players[p_player.user.id].in_game = False
            self.participants = []

        else:
            await ctx.send("Starting game with " + str(len(self.participants)) + " players")

    async def add_players(self, ctx, players):
        """Adds to players to the game from the list of players waiting to be added."""

        for new_player in self.join_queue:
            if len(self.participants) == 8:
                continue
            self.participants.append(new_player)
            players[new_player.user.id].in_game = True
            await self.poker_ui.player_has_joined(ctx, new_player.user)
            self.join_queue.remove(new_player)

    async def leave_game(self, ctx, players, enough_players):
        """
        Removes players based on the list of players ready to
        leave and checks if game is still able to play.
        """

        for p_player in self.leave_queue:
            players[p_player.user.id].balance += p_player.get_game_balance() - \
                self.starting_balance
            players[p_player.user.id].in_game = False
            self.participants.remove(p_player)
            if enough_players:
                await self.poker_ui.player_has_left(ctx, p_player.user)
            elif not enough_players:
                await self.poker_ui.player_kicked(ctx, p_player.user)

        self.leave_queue.clear()

    async def set_blind(self, ctx, bot):
        """Sets the blind at the start of the game and takes in input from users."""

        def represents_int(blind):
            try:
                int(blind)
                return True
            except ValueError:
                return False

        def verify(msg):
            return msg.author == ctx.message.author and represents_int(msg.content)

        await self.poker_ui.ask_bet(ctx)

        try:
            msg = await bot.wait_for('message', check=verify, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long to type the blind")
            return False

        self.hard_blind = int(msg.content)
        self.small_blind = math.floor(self.hard_blind / 2)

    async def set_balance(self, ctx):
        """This updates the players balance after the end of each round."""

        def represents_int(blind):
            try:
                int(blind)
                return True
            except ValueError:
                return False

        def verify(msg):
            return msg.author == ctx.message.author and represents_int(msg.content)

        await self.poker_ui.ask_balance(ctx)

        try:
            msg = await self.bot.wait_for('message', check=verify, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long to type the balance")
            return False

        self.starting_balance = int(msg.content)

    async def deal_cards(self, bot):
        """Deals cards to players and community card."""

        self.game_deck.shuffle()

        for p_player in self.participants:
            i = 0
            while i < 2:
                crd = self.game_deck.draw_card()
                p_player.add_card(crd)
                i = i + 1
            await p_player.send_hand()

    def check_player_balance(self):
        """Check if the current players in the game have balance to continue playing."""

        for i in self.participants:
            if i.get_game_balance() <= 0:
                self.participants.remove(i)

    def player_fold(self):
        """Removes player from current rouhd with fold command."""
        self.competing.pop(0)

    def remove_player(self, player_id):
        """Remove player from the current game."""

        for i in self.participants:
            if i.get_username() == player_id:
                self.participants.remove(i)

        self.num_players -= 1

    def create_comm_deck(self):
        """Makes community hand."""
        i = 0
        while i < 3:
            self.add_card_to_comm()
            i = i + 1

    def add_card_to_comm(self):
        """Adds card to community card."""

        self.community_deck.append(self.game_deck.draw_card())

    def find_winner(self):
        """At the end of each round find the winner."""

        evalu = EvaluateHand(self.community_deck)
        for players in self.competing:
            command_hand = self.community_deck + players.hand
            evalu = EvaluateHand(command_hand)
            players.win_condition = evalu.evaluate()

        winning_cond = max(x.win_condition[0] for x in self.competing)
        compete = []
        for players in self.competing:
            if players.win_condition[0] == winning_cond:
                compete.append(players)
        winners = evalu.winning(compete, winning_cond)
        return winners

    def reset_round(self):
        """Reset the round."""

        self.game_started = False
        self.current_pot = 0
        self.community_deck.clear()
        self.game_deck = Deck()
        self.num_players = len(self.participants)
        temp = self.participants.pop(0)
        self.participants.append(temp)
        self.competing.clear()
        for players in self.participants:
            players.hand = []
            players.game_balance = int(players.game_balance-players.in_pot)
            players.in_pot = 0
