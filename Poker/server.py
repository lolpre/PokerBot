from Poker.player import Player
from Poker.announcer import Announcer
from Poker.pokerwrapper import PokerWrapper

class Server:
    def __init__(self):
        self.players = {}
        self.resets = 0
        self.announcer = Announcer()
        self.pokerWrapper = PokerWrapper()
    
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
        
    def nextTurns(self, pool, message): 
        while len(pool) != 0:
            hasRaised = False
            i = 0
            for i in range(len(pool)):
                self.announcer.askMove(pool[i].getHand(), hasRaised)
                format_msg = message.content.lower().strip().split()
                pool[i].setAction(format_msg)
                if format_msg == "raise":
                    self.announcer.reportRaise(pool[i].username, format_msg[1]) 
                    hasRaised = True
                    temp = pool.pop(i)
                    pool.append(temp)
                if format_msg == "call": 
                    self.announcer.reportCall(pool[i].username)
                    i += 1
                if format_msg == "check":
                    self.announcer.reportCheck(pool[i].username)
                    i += 1
                if format_msg == "fold":
                    self.announcer.reportFold(pool[i].username)
                    self.pokerWrapper.removePlayer(message.author.id)
                    pool.pop(i)
                
                
                
                

