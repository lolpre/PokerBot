from player import Player
class Leaderboard:
    
    def __init__(self):
        self.players=[]
        
        
    def printLeaderboard(self):
        sortplayers=sorted(self.players,key=lambda x:x.balance,reverse=True)
        for i in sortplayers:
            print(i.id,i.balance)

    def addplayer(self,name):
        self.players.append(name)

    def updateplayer(self,player,number):
        for i in self.players:
            if i.id==player:
                i.setBalance(number)
      
