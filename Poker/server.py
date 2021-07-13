import player

class Server:
    def __init__(self):
        self.players = []
        self.resets = 0
    
    def addPlayer(self, player):
        self.players.append(player)
    
    def reset(self):
        for player in self.players:
            player.setBalance(3000)
        self.resets += 1
    
    async def help(self, ctx):
        await ctx.send("List of commands")
        await ctx.send(".create - Create your profile for the server")
        await ctx.send(".p - Create and play a game of Texas Hold'Em Poker")
        await ctx.send(".balance - Check to see how many chips you have")
        await ctx.send(".top - Check the leaderboards to see who is on top")
        await ctx.send(".join - Join an already existing Poker game")
        await ctx.send("(Mods Only) .reset - Reset the balances of everyone in the server")
