class Leaderboard:
    
    def __init__(self):
        self.players=[]
        self.playerdata={}
        
    async def printLeaderboard(self, ctx):
        sort_byvalue=sorted(self.playerdata.items(),key=lambda x:x[1],reverse=True)
        for i in sort_byvalue:
            await ctx.send((i[0],i[1]))

    def addplayer(self,name):
        self.players.append(name)
        self.playerdata[name]=3000

    def updateplayer(self,name,number):
        self.playerdata[name]+=number

