"""
ANNOUNCER
"""
import asyncio
import discord

class Announcer:
    """
    The Announcer class is the interface of Poker Bot,
    and the class that will be interacting with the
    user the most. All the information stored inside
    the other classes will be communicated through the
    Announcer class.
    """

    async def initiate_game(self, ctx):
        """
        initiate_bet outputs the announcing message that begins the Poker Game.
        input: ctx (part of Discord API, the context of the message)
        output: none
        """
        await ctx.send("WELCOME TO POKER BOT!")
        await ctx.send("If this is your first time with Poker Bot," +
                       " please type \'.create\'. Please type \'.help\' for the rules" +
                       " and betting system.")


    async def ask_bet(self, ctx):
        """
        This methods ask_bet outputs the announcing message that asks users for Bets
        in the beginning of the game.
        input: ctx -> part of Discord API, the context of the message
        """
        await ctx.send("What is the big blind (minimum bet) amount?")


    async def announce_winner(self, ctx, sorted_players, com_deck, current_pot):
        """
        This method announce_winner outputs the announcing
        message that reveals the winner of the game.
        input: ctx -> part of Discord API, the context of the message
            sorted_players -> a sorted list of players, the winner
                                at the beginning of list
        output: none
        """
        winner = sorted_players[0].get_username()
        self.show_comm_cards(ctx, com_deck)
        await ctx.send(winner + " has won, receiving " + str(current_pot))


    async def ask_move(self, ctx, member, has_raised, blind):
        """
        This method ask_move outputs the announcing
        message that asks participants for their next move.
        input: ctx -> a class object. part of
                Discord API, the context of the message
                member -> a class object. part of Discord
                    API, the information about the Discord User
                hasRaised -> a boolean that checks if the
                    previous user has increased bet
                blind -> a boolean that checks if the
                    blind has been set
                bot -> a class object. part of Discord API,
                    the bot information
        """
        if has_raised or blind:
            await ctx.send("{}, Would you like to call, raise, or fold?".format(member))
        else:
            await ctx.send("{}, Would you like to check, raise, or fold?".format(member))


    async def ask_balance(self, ctx):
        """
        This method ask_balance outputs the announcing message
            that asks participant for the starting balance
            for the game.
        input: ctx -> part of Discord API, the context of the message
        """
        await ctx.send("What should be the starting game balance of all players?")


    async def join_timer(self, ctx):
        """
        This method join_timer limits the time
        given for someone to join the game. the timer is
        30 seconds long.
        input: ctx -> part of Discord API, the context of the message
        """
        time = 30
        while time != 0:
            if time == 5:
                await ctx.send("Entries close in 5 seconds.")
            time -= 1
            await asyncio.sleep(1)


    async def join_queue(self, ctx):
        """
        This method join_queue outputs the announcing
        message that opens the game for people to join.
        input: ctx -> a class object. part of Discord API, the context of the message
        """
        await ctx.send("Please click on the green checkmark to join the game!")
        await ctx.send("A timer will begin now. You will have 60 seconds to join the game.")
        await self.join_timer(ctx)
        await ctx.send("Time is up. The game will be starting shortly...")


    async def show_cards(self, ctx, hand):
        """
        This method show_cards reveals all the cards in a hand.
        outputs the message into the game channel.
        input: ctx -> a class object. part of Discord API, the context of the message
                hand -> an array of the Card object
        """
        cards = ""
        for card in hand:
            cards += card.show()
        await ctx.send(cards)


    async def show_comm_cards(self, ctx, comm_deck):
        """
        This method show_comm_cards reveals the community deck.
        outputs the mesasge into the game channel.
        input: ctx -> a class object. part of Discord API, the context of the message
                comm_deck -> an array of the Card object, ideally where the community deck is stored
        """
        await ctx.send("**CURRENT COMMUNITY DECK**")
        comm_cards = ""
        i = 0
        for card in comm_deck:
            comm_cards += card.show()
            i += 1
        for j in range(5-i):
            comm_cards += "<:back:867926963061411871>"
            j += 1
        await ctx.send(comm_cards)

    async def report_raise(self, ctx, name, amount):
        """
        This method report_raise outputs the announcing message
        that someone has raised the bet amount.
        input: ctx -> a class object. part of Discord API, the context of the message
                name -> the string of the player's name
                amount -> the string of the raise amount
        """
        await ctx.send(name + " has raised to " + amount + " <:chips:865450470671646760>!")


    async def report_call(self, ctx, name):
        """
        This method report_call outputs the announcing
        message that someone has called.
        input: ctx -> a class object. part of Discord API, the context of the message
                name -> the string of the player name
        """
        await ctx.send(name + " has called!")


    async def report_fold(self, ctx, name):
        """
        This method report_fold outputs the announcing message that someone has folded.
        input: ctx -> a class object. part of Discord API, the context of the message
                name -> the string of the player name
        """
        await ctx.send(name + " has folded!")


    async def report_check(self, ctx, name):
        """
        This method announces that a certain player has checked for their move.
        input: ctx -> a class object. part of Discord API, the context of the message
                name -> the string of the player name
        """
        await ctx.send(name + " has checked!")


    async def show_balances(self, ctx, pkr_players):
        """
        This method show_balances outputs the balances of all the participating poker players.
        input: ctx -> a class object. part of Discord API, the context of the message
                pkr_players -> a list of Poker Player objects. a list of all the particpants
        """
        await ctx.send("CURRENT BALANCES:")
        for player in pkr_players:
            await ctx.send(player.get_username() + ": " +
                           str(player.get_game_balance()) + " <:chips:865450470671646760>")


    async def show_player(self, ctx, game):
        """
        show_player outputs the formatted player profile.
        input: ctx -> a class object. part of Discord API, the context of the message
                game -> a PokerWrapper object. the current game information
        """
        embed = discord.Embed(title=game.competing[0].get_username(),
                              description="Balance: "+str(game.competing[0].get_game_balance()) +
                              " <:chips:865450470671646760>" +
                              """\nIn Pot: """ + str(game.competing[0].in_pot) +
                              """ <:chips:865450470671646760> \nCurrent Pot: """ +
                              str(game.current_pot), color=discord.Color.green())
        embed.set_thumbnail(url=game.competing[0].user.avatar_url)
        await ctx.send(embed=embed)


    async def ask_leave(self, ctx):
        """
        ask_leave outputs the announcing message that requests
        if anyone would like to leave the poker game.
        input: ctx -> a class object. part of Discord API, the context of the message
        """
        await ctx.send("If you would like to leave the game, type the command .leave")


    async def reset_game(self, ctx):
        """
        reset_game outputs the announcing message that a game has restarted.
        input: ctx -> a class object. part of Discord API, the context of the message
        """
        await ctx.send("\n\n**A NEW GAME HAS STARTED**")


    async def game_already_in_progress(self, ctx):
        """
        game_already_in_progress outputs the error message that
        a game is already ongoing in the current channel.
        input: ctx -> a class object. part of Discord API, the context of the message
        """
        await ctx.send("Cannot create game: Game is already in progress in this channel!")


    async def no_account(self, ctx, user):
        """
        no_account outputs the error message that
        the player does not have a profile created.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} You do not have an account! " +
                       "Use the command .create to create an account!")


    async def player_already_in_game(self, ctx, user):
        """
        player_already_in_game outputs the error message that
        a player tried to join a game that they are already in.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} You are already in game! " +
                       "Use the .leave command to exit your current game to join a new one!")


    async def no_game(self, ctx):
        """
        no_game outputs the error message that there is no ongoing game.
        input: ctx -> a class object. part of Discord API, the context of the message
        """
        await ctx.send(f"There is no game currently running in this channel")


    async def added_to_join_queue(self, ctx, user):
        """
        added_to_join_queue outputs the announcing message that
        a player will join the game the next round.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} You have been added to the join queue! "+
                       "You will be in the next game once the round is over.")


    async def added_to_leave_queue(self, ctx, user):
        """
        added_to_leave_queue outputs the announcing message that
        a player will leave the game the next round.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} You have been added to the leave queue! " +
                       "You will exit the game once the round is over.")


    async def player_has_joined(self, ctx, user):
        """
        player_has_joined outputs the announcing message that
        the player has joined the game for the new round.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} has joined the game!")


    async def player_has_left(self, ctx, user):
        """
        player_has_left outputs the announcing message that
        the player has left for the new round.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} has left the game!")


    async def player_kicked(self, ctx, user):
        """
        player_kicked outputs the announcing message that
        the player has been kicked when there are not enough
        participants.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API the user information
        """
        await ctx.send(f"{user.mention} You have been removed from the game as " +
                       "there are not enough players")


    async def not_in_game(self, ctx, user):
        """
        not_in_game outputs the error message that a user in the
        current channel are typing in commands in a game
        they are not participating in.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} You are not in this game! " +
                       "Use the .join command to join the game")


    async def already_in_leave_queue(self, ctx, user):
        """
        already_in_leave_queue outputs the error message that a participant
        has already requested to leave the game.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} You are already in the leave queue! " +
                       "You will be removed from the game after this round")


    async def already_in_join_queue(self, ctx, user):
        """
        already_in_join_queue outputs the error message that a participant
        has already requested to join the game.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} You are already in the join queue! " +
                       "You will be added to the game after this round")


    async def game_is_full(self, ctx, user):
        """
        game_is_full outputs the error message that the game is currently full
        and that the user will be added to the join queue.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} Game is currently full. " +
                       "You will be added to the join queue.")


    async def above_balance(self, ctx, user):
        """
        above_balance outputs the error message that a particpant
        has wagered an amount higher than their game balance.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} You exceeded your game balance. " +
                       "Please wager a new amount.")


    async def value_not_digit(self, ctx, user):
        """
        value_not_digit outputs the error message that a particpant
        has wagered an amount that is not a number.
        input: ctx -> a class object. part of Discord API, the context of the message
                user -> a class object. part of the Discord API, the user information
        """
        await ctx.send(f"{user.mention} Please raise a numerical value.")
