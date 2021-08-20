"""
SERVER
"""

import asyncio
from Poker.pokerwrapper import PokerWrapper
from Poker.announcer import Announcer
from Poker.pokerplayer import PokerPlayer
from Poker.evalhand import EvaluateHand
import discord
from Poker.player import Player

class Server:
    """
    The Server class manages all the Poker Game classes
    and executes the game. All the methods of other
    classes will be called in this server.
    """

    def __init__(self, bot):
        """
        the constructor of Server
        input: bot -> a class object. part of the Discord API, the bot information
        initialized values:
            games -> a set of PokerWrapper objects. a set of all the ongoing games
            bot -> initializes the bot
            players -> a set of Player objects. a set of all registered players in a server
            resets -> an integer. the number of times the administrator reset the leaderboard
            announcer_ui -> an Announcer object for the output
        """

        self.games = {}
        self.bot = bot
        self.players = {}
        self.resets = 0
        self.announcer_ui = Announcer()

    async def add_player(self, ctx):
        """
        adds the player to the player set
        input: ctx -> a class object. part of Discord API, the context of the message
        """
        if ctx.author.id not in self.players:
            player = Player(ctx.author.id, 3000)
            self.players[ctx.author.id] = player
            await ctx.send("You have created an account!")
            return True

        await ctx.send("You already created an account!")
        return False

    async def get_balance(self, ctx):
        """
        gets the balance of a player
        input: ctx -> a class object. part of Discord API, the context of the message
        """
        if ctx.author.id not in self.players:
            await ctx.send("You do not have an account! \
                            Use the .create command to create an account!")
        else:
            player = self.players[ctx.author.id]
            balance = player.get_balance()
            embed = discord.Embed(title=ctx.author.name + "'s Balance:",
                                  description=str(
                                      balance)+" <:chips:865450470671646760>",
                                  color=discord.Color.green())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    async def reset(self):
        """resets the leaderboard and the balacnes of all players"""

        for key in self.players:
            self.players[key].set_balance(3000)
        self.resets += 1

    async def help(self, ctx):
        """
        the help command calls this method. the tutorial and list of all
        the commands to help a new user get started with the bot
        input: ctx -> a class object. part of Discord API, the context of the message
        """
        embed = discord.Embed(title="List of Commands",
                              description="""**.create** - Create your profile for the server
        **.p** - Create and play a game of Texas Hold'Em Poker
        **.balance** - Check to see how many chips you have
        **.top** - Check the leaderboards to see who is on top
        **.join** - Join an already existing Poker game
        **(Mods Only) .reset** - Reset the balances of everyone in the server""",
                              color=0xffffff)
        embed.set_thumbnail(url="https://s.wsj.net/public/resources/\
                            images/JR-AA451_IFPOKE_GR_20191031164807.jpg")
        await ctx.send(embed=embed)

    async def print_leaderboard(self, ctx):
        """
        This method outputs the formatted leaderboard and sorts leaderboard by player balance.
        input: ctx -> a class object. part of Discord API, the context of the message.
        """
        sort_byvalue = sorted(self.players.items(),
                              key=lambda x: x[1].balance, reverse=True)
        leaderboard = ""
        k = 1
        for i in sort_byvalue:
            name = str(await self.bot.fetch_user(i[1].id))
            leaderboard += str(k)+". "+name+" - " + \
                str(i[1].balance) + " <:chips:865450470671646760>\n"
            k += 1
        embed = discord.Embed(title=ctx.message.guild.name + " Leaderboard:",
                              description=leaderboard,
                              color=discord.Color.red())
        embed.set_thumbnail(url=ctx.message.guild.icon_url)
        await ctx.send(embed=embed)

    async def validate_game(self, ctx):
        """This method checks if in game in channel is in progress."""
        if ctx.message.channel.id in self.games:
            await self.announcer_ui.game_already_in_progress(ctx)
            return False
        return True

    async def validate_player(self, ctx):
        """
        This method checks if the player has an account created. if not, output error message
        input: ctx -> a class object. part of Discord API, the context of the message.
        """
        if ctx.author.id not in self.players:
            await self.announcer_ui.no_account(ctx, ctx.author)
            return False
        if self.players[ctx.author.id].in_game:
            await self.announcer_ui.player_already_in_game(ctx, ctx.author)
            return False
        return True

    async def initiate_game(self, ctx, id_, bot):
        """
        This method initializes the game.
        input: ctx -> a class object. part of Discord API, the context of the message
               id -> an integer. each game is assigned their own id. this can help with
                     searching for a game in the game set.
               bot -> a class object. part of the Discord API the bot information.
        """
        new_game = PokerWrapper(bot)
        if await self.start_game(ctx, new_game, bot) is False:
            return
        self.games[id_] = new_game
        bool_val = await new_game.set_players(ctx, bot, self.players)
        if bool_val is False:
            del self.games[id_]
            return
        await self.start_rounds(ctx, new_game, bot)
        await self.find_winner(ctx, new_game)
        await self.reset_round(ctx, new_game, bot)

    async def redo_game(self, ctx, game, bot):
        """
        This method re-initializes the game.
        input: ctx -> a class object. part of Discord API, the context of the message
               game -> a PokerWrapper class object. holds game information
               bot -> a class object. part of the Discord API, the bot information
        """
        await self.start_rounds(ctx, game, bot)
        await self.find_winner(ctx, game)
        await self.reset_round(ctx, game, bot)

    async def start_game(self, ctx, game, bot):
        """
        This method begins the gameplay.
        input: ctx -> a class object. part of Discord API, the context of the message
               game -> a PokerWrapper class object. holds game information
               bot -> a class object. part of the Discord API, the bot information
        """
        if await self.validate_player(ctx) is False:
            return False
        if await self.validate_game(ctx) is False:
            return False
        await game.start_game(ctx)
        await game.set_balance(ctx)  # change this function later
        await game.set_blind(ctx, bot)

    async def leave(self, ctx, id_):
        """
        This method implements the leave command and is called when a
        player wants to leave the game.
        input: ctx -> a class object. part of Discord API, the context of the message
               id -> the game id. an integer.
        """
        if id_ not in self.games:
            self.announcer_ui.no_game(ctx)
            return

        for player in self.games[id_].leave_queue:
            if player.user.id == ctx.author.id:
                await self.announcer_ui.already_in_leave_queue(ctx, ctx.author)
                return

        if id_ in self.games:
            for player in self.games[id_].participants:
                if player.user.id == ctx.author.id:
                    self.games[id_].leave_queue.append(player)
                    await self.announcer_ui.added_to_leave_queue(ctx, player.user)
                    return

            await self.announcer_ui.not_in_game(ctx, ctx.author)

    async def join(self, ctx, id_):
        """
        This method implements the join command, called when the player wants to join the game.
        input: ctx -> a class object. part of Discord API, the context of the message
               id -> the game id. an integer
        """
        if await self.validate_player(ctx) is False:
            return

        for player in self.games[id_].join_queue:
            if player.user.id == ctx.author.id:
                await self.announcer_ui.already_in_join_queue(ctx, ctx.author)
                return

        if id_ in self.games:
            self.games[id_].join_queue.append(PokerPlayer(
                ctx.message.author.name, 0, ctx.message.author, self.games[id_].starting_balance))
            await self.announcer_ui.added_to_join_queue(ctx, ctx.author)
        else:
            await self.announcer_ui.no_game(ctx)

    async def start_rounds(self, ctx, game, bot):
        """
        This method begins the round of a game.
        input: ctx -> a class object. part of Discord API, the context of the message
               game -> a PokerWrapper object. holds the game information
               bot -> a class object. part of the Discord API, the bot information
        """
        for i in game.participants:
            game.competing.append(i)
        await game.deal_cards(bot)  # needs to send dm's
        await self.take_blinds(ctx, game)  # needs to be implemented
        await self.next_turns(ctx, game, bot)
        await self.flop(ctx, game)
        if len(game.competing) != 1:
            await self.next_turns(ctx, game, bot)
        await self.turn(ctx, game)
        if len(game.competing) != 1:
            await self.next_turns(ctx, game, bot)
        await self.river(ctx, game)
        if len(game.competing) != 1:
            await self.next_turns(ctx, game, bot)
            await game.poker_ui.show_comm_cards(ctx, game.community_deck)

    async def flop(self, ctx, game):
        """
        This method creates the community deck and reveals the first three cards.
        input: ctx -> a class object. part of Discord API, the context of the message
               game -> a PokerWrapper object, holds the game information
        """
        game.create_comm_deck()
        comm_deck = game.community_deck
        await self.announcer_ui.show_comm_cards(ctx, comm_deck)
        for player in game.participants:
            comm_and_hand = comm_deck + player.hand
            eval = EvaluateHand(comm_and_hand)
            player.win_condition = eval.evaluate()
            await player.user.send(player.get_win_cond())

    async def take_blinds(self, ctx, game):
        """
        This method sets the blinds for two players. one player will get the big blind,
        and the other gets the small blind.
        input: ctx -> a class object. part of Discord API, the context of the message
               game -> a PokerWrapper object, holds the game information
        """
        await self.announcer_ui.show_player(ctx, game)
        game.competing[0].in_pot = game.small_blind
        await ctx.send(game.competing[0].get_username()
                       + "\nSmall Blind: "
                       + str(game.small_blind)
                       + " <:chips:865450470671646760>\n")
        game.current_pot += game.competing[0].in_pot
        temp = game.competing.pop(0)
        game.competing.append(temp)

        await self.announcer_ui.show_player(ctx, game)
        game.competing[0].in_pot = game.hard_blind
        await ctx.send(game.competing[0].get_username()
                       + "\nBig Blind: "
                       + str(game.hard_blind)
                       + " <:chips:865450470671646760>\n")
        game.competing[0].set_action("blind")
        game.current_pot += game.competing[0].in_pot

    async def next_turns(self, ctx, game, bot):
        """
        This method begins asking players for what their plan of action is. Players can either
        check, raise, or fold. a call value is only available when someone has raised.
        input: ctx -> a class object. part of Discord API, the context of the message
               game -> a PokerWrapper object, holds the game information
               bot -> a class object. part of the Discord API, the context of the message
        """
        while True:
            has_raised = False
            blind = False
            i = 0
            raise_amt = 0
            raise_round = 0
            while True:
                called_action = False
                if (game.competing[0].get_action() == "raise"
                        and game.competing[0].in_pot == raise_amt) or i == len(game.competing):
                    for player in game.competing:
                        player.set_action(0)
                    return
                if game.competing[0].get_action() == "blind":
                    blind = True
                    raise_amt = game.competing[0].in_pot
                    raise_round = game.competing[0].in_pot
                    game.competing[0].set_action("called blind")
                    i = 0
                    temp = game.competing.pop(0)
                    game.competing.append(temp)
                    continue
                if game.competing[0].get_action() == "called blind":
                    blind = False
                await self.announcer_ui.show_player(ctx, game)
                await self.announcer_ui.ask_move(ctx, "<@"+str(game.competing[0].user.id)+">",
                                                 has_raised, blind)

                def verify(message):
                    return game.competing[0].user == message.author

                try:
                    afk = False
                    msg = await bot.wait_for('message', check=verify, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send("Sorry, you took too long to type your decision")
                    afk = True

                format_msg = []
                if afk:
                    if has_raised:
                        format_msg[0] = "fold"
                    else:
                        format_msg[0] = "check"
                else:
                    format_msg = msg.content.lower().strip().split()

                game.competing[0].set_action(format_msg)
                if format_msg[0] == "raise":
                    if not format_msg[1].isdigit():
                        await self.announcer_ui.value_not_digit(ctx, game.competing[0].user)
                        continue

                    raise_round = int(format_msg[1])
                    if raise_round > game.competing[0].game_balance - game.competing[0].in_pot:

                        await self.announcer_ui.above_balance(ctx, game.competing[0].user)
                        continue
                    await self.announcer_ui.report_raise(ctx, game.competing[0].get_username(),
                                                         format_msg[1])
                    has_raised = True
                    game.competing[0].in_pot += raise_round
                    game.current_pot += raise_round
                    raise_amt = game.competing[0].in_pot
                    called_action = True
                    temp = game.competing.pop(0)
                    game.competing.append(temp)
                    i = 0
                elif format_msg[0] == "call":
                    await self.announcer_ui.report_call(ctx, game.competing[0].get_username())
                    game.current_pot += (raise_amt - game.competing[0].in_pot)
                    game.competing[0].in_pot = raise_amt
                    temp = game.competing.pop(0)
                    game.competing.append(temp)
                    called_action = True
                elif format_msg[0] == "check":
                    await self.announcer_ui.report_check(ctx, game.competing[0].get_username())
                    temp = game.competing.pop(0)
                    game.competing.append(temp)
                    called_action = True
                elif format_msg[0] == "fold":
                    await self.announcer_ui.report_fold(ctx, game.competing[0].get_username())
                    game.competing.pop(0)
                    if len(game.competing) == 1:
                        return
                else:
                    continue
                if called_action:
                    i += 1

    async def turn(self, ctx, game):
        """
        This method reveals the fourth card in the community deck.
        input: ctx -> a class object. part of Discord API, the context of the message
               game -> a PokerWrapper object, holds the game information
        """
        game.add_card_to_comm()
        comm_deck = game.community_deck
        await game.poker_ui.show_comm_cards(ctx, comm_deck)
        for player in game.participants:
            comm_and_hand = comm_deck + player.hand
            eval = EvaluateHand(comm_and_hand)
            player.win_condition = eval.evaluate()
            await player.user.send(player.get_win_cond())

    async def river(self, ctx, game):
        """
        This method reveals the fifth card in the community deck.
        input: ctx -> a class object. part of Discord API, the context of the message
               game -> a PokerWrapper object, holds the game information
        """
        game.add_card_to_comm()
        comm_deck = game.community_deck
        await game.poker_ui.show_comm_cards(ctx, comm_deck)
        for player in game.participants:
            comm_and_hand = comm_deck + player.hand
            eval = EvaluateHand(comm_and_hand)
            player.win_condition = eval.evaluate()
            await player.user.send(player.get_win_cond())

    async def find_winner(self, ctx, game):
        """
        This method finds the winner out of all the players hand.
        input: ctx -> a class object. part of Discord API, the context of the message
               game -> a PokerWrapper object, holds the game information
        """
        for player in game.competing:
            await ctx.send("**" + player.get_username() + "'s Hand:**")
            await self.announcer_ui.show_cards(ctx, player.hand)
        winners = game.find_winner()  # needs to return a list of winners
        for player in winners:
            embed = discord.Embed(
                title="WINNER: " + player.username,
                description=player.get_win_cond(), color=discord.Color.green())
            embed.set_image(url=player.user.avatar_url)
            await ctx.send(embed=embed)
            player.game_balance += int(game.current_pot / len(winners))

    async def reset_round(self, ctx, game, bot):
        """
        This method resets the round after the initial round has finished.
        input: ctx -> a class object. part of Discord API, the context of the message
               game -> a PokerWrapper object, holds the game information
               bot -> a class object. part of Discord API, the bot information
        """
        game.reset_round()
        await self.announcer_ui.show_balances(ctx, game.participants)
        await self.announcer_ui.ask_leave(ctx)
        await asyncio.sleep(10)
        await game.leave_game(ctx, self.players, True)
        await game.add_players(ctx, self.players)
        if len(game.participants) < 2:
            for player in game.participants:
                game.leave_queue.append(player)
            await ctx.send("Not enough players! Terminating game")
            await game.leave_game(ctx, self.players, False)
            del self.games[ctx.message.channel.id]
            return
        await self.announcer_ui.reset_game(ctx)
        await self.redo_game(ctx, game, bot)
