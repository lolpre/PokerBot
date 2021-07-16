from Poker.player import Player

class Server:
    def __init__(self):
        self.players = {}
        self.resets = 0
    
    def addPlayer(self, ctx):
        player = Player(ctx.author.name, 3000)
        self.players[ctx.author.id] = player
    
    async def getBalance(self, ctx):
        if ctx.author.id not in self.players:
            await ctx.send("You do not have an account! Use the .create command to create an account!")
        else:
            player = self.players[ctx.author.id]
            await ctx.send("You currently have " + str(player.getBalance()) + " chips!")
    
    def reset(self):
        for player in self.players:
            player.setBalance(3000)
        self.resets += 1
    
    async def help(self, ctx):
        await ctx.send("```List of commands\n\
.create - Create your profile for the server\n\
.p - Create and play a game of Texas Hold'Em Poker\n\
.balance - Check to see how many chips you have\n\
.top - Check the leaderboards to see who is on top\n\
.join - Join an already existing Poker game\n\
(Mods Only) .reset - Reset the balances of everyone in the server```")

