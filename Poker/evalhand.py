from Poker.card import Card
from Poker.pokerplayer import PokerPlayer

'''

This is the EvaluateHand class. This class's sole purpose is to
evaluate the given hand. It runs an algorithm that checks to see
what is the best combination for the hand. Such combinations are
a Royal Flush, Two Pair, Straight Flush, Four of a Kind, etc.

'''

class EvaluateHand:
    #Constructor to Evaluate Hand. Sets hand to allCards List
    def __init__(self, hand):
        self.allCards= hand
        # print(self.allCards)
    
    #Prints the cards in allCards
    def printHand(self):
        for x in self.allCards:
            print(str(x.val) +str(x.suit) )

    #Adds card to allCards List
    def addCard(self, card):
        self.allCards.append(card)

    #Returns the amount of cards in allCards
    def numCards(self):
        return len(self.hand)

    #Sorts the allCards list by card rank
    def sortByRank(self):
        self.allCards.sort(key=lambda x:x.getNumVal())
    
    #Sorts the allCards list by card suit
    def sortBySuit(self):
        self.allCards.sort(key=lambda x:x.getNumSuit())
    
    #Sorts the allCards list by card suit then by card rank
    def sortBySuitThenRank(self):
        self.allCards.sort(key=lambda x:x.getNumSuit())
        self.allCards.sort(key=lambda x:x.getNumVal())

    #Sorts the allCards list by card rank then by card suit
    def sortByRankThenSuit(self):
        self.allCards.sort(key=lambda x:x.getNumVal())
        self.allCards.sort(key=lambda x:x.getNumSuit())

    #Evaluates allCards to find all its possible winning conditions
    def evaluate(self):
        #Count the ranks and suits in allCards
        rankCounter = {}
        suitCounter = {}

        for x in range(13):
            rankCounter[x]=[]

        for x in range(4):
            suitCounter[x]=[]

        for x in self.allCards:
            rankCounter[x.getNumVal()].append(x)
            suitCounter[x.getNumSuit()].append(x)

        self.sortByRankThenSuit()

        handResult=[]
        handResult=self.evaluateRoyal(rankCounter,suitCounter)      #Evaluate if hand has Royal Flush

        if len(handResult)==0:
            handResult=self.evaluateStraightFlush(suitCounter)      #Evaluate if hand has Straight Flush
    
        if len(handResult)==0:
            handResult=self.evaluateFourOfAKind(rankCounter)        #Evaluate if hand has Four of a Kind

        if len(handResult)==0:
            handResult=self.evaluateFullHouse(rankCounter)          #Evaluate if hand has Full House 

        if len(handResult)==0:
            handResult=self.evaluateFlush(suitCounter)              #Evaluate if hand has Flush

        if len(handResult)==0:
            handResult=self.evaluateStraight(rankCounter)           #Evaluate if hand has Straight

        if len(handResult)==0:
            handResult=self.evaluateThreeOfAKind(rankCounter)       #Evaluate if hand has Three of a Kind

        if len(handResult)==0:
            handResult=self.evaluateTwoPair(rankCounter)            #Evaluate if hand has Two Pair

        if len(handResult)==0:
            handResult=self.evaluateOnePair(rankCounter)            #Evaluate if hand has One Pair

        if len(handResult)==0:
            handResult=self.evaluateHighCard(rankCounter)           #Evaluate if hand's High Card
        
        return handResult                                           #Returns result of evaluated hand
    
    #Evaluate if hand has Royal Flush
    def evaluateRoyal(self, rankCounter, suitCounter):
        result=[]
        if ((len(rankCounter[9])>=1 and len(rankCounter[10])>=1 and         #Checks if hand has 10, J, Q, K, A
            len(rankCounter[11])>=1 and len(rankCounter[12])>=1 and
            len(rankCounter[0])>=1)
            and 
            (len(suitCounter[0])>4 or len(suitCounter[1])>4 or              #Checks for flush
            len(suitCounter[2])>4 or len(suitCounter[3])>4)):
            for i in range(3):                                              #Finds where in hand has Royal Flush
                if (self.allCards[i].getNumVal()==0):
                    for j in range(1,4-i):
                        if (self.allCards[i+j].getNumVal()==9 and self.allCards[i+j+1].getNumVal()==10 and  
                            self.allCards[i+j+2].getNumVal()==11 and self.allCards[i+j+3].getNumVal()==12
                            and
                            self.allCards[i].getNumSuit() == self.allCards[i+j].getNumSuit() and
                            self.allCards[i].getNumSuit() == self.allCards[i+j+1].getNumSuit() and
                            self.allCards[i].getNumSuit() == self.allCards[i+j+2].getNumSuit() and
                            self.allCards[i].getNumSuit() == self.allCards[i+j+3].getNumSuit()):
                            result=[10]                                     #Sets result to 10 to represent Royal Flush
                            break
        return result

    #Evaluate if hand has Straight Flush
    def evaluateStraightFlush(self, suitCounter):
        result=[]
        if (len(suitCounter[0])>4 or len(suitCounter[1])>4 or               #Checks for Flush
            len(suitCounter[2])>4 or len(suitCounter[3])>4):
            for i in range(len(self.allCards)-1, 3, -1):                    #Checks for Straight
                if ((self.allCards[i].getNumVal()-1 == self.allCards[i-1].getNumVal() and   
                    self.allCards[i].getNumVal()-2 == self.allCards[i-2].getNumVal() and
                    self.allCards[i].getNumVal()-3 == self.allCards[i-3].getNumVal() and
                    self.allCards[i].getNumVal()-4 == self.allCards[i-4].getNumVal())
                    and
                    (self.allCards[i].getNumSuit() == self.allCards[i-1].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-2].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-3].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-4].getNumSuit())):
                    result=[9,self.allCards[i].getNumVal()]                 #Sets result to 9 to represent Straight Flush and highest card rank in straight
        return result

    #Evaluate if hand has Four of a Kind
    def evaluateFourOfAKind(self, rankCounter):
        result=[]
        for i in range(13):                             #Checks for Four of a Kind
            if len(rankCounter[i])==4:
                result=[8,i]                            #Sets result to 8 to represent Four of a Kind and the rank value
                if len(rankCounter[0])>0 and i!=0:      #Adds Ace rank to result if highest card outside four of a kind
                    result.append(0)
                    break
                for j in range(len(rankCounter),0,-1):  #Adds card rank outside four of a kind to result 
                    if len(rankCounter[j-1])>0 and j!=i:
                        result.append(j)
                        break
                break
        return result        

    #Evaluate if hand has Full House
    def evaluateFullHouse(self, rankCounter):
        result=[]
        threeOfKind=-1
        twoOfKind=-1

        for i in range(len(rankCounter), 0, -1):    #Checks for Three of a kind and two of a kind
            if threeOfKind<0 or twoOfKind<0:
                if len(rankCounter[i-1])>2:
                    threeOfKind=i-1
                elif len(rankCounter[i-1])>1:
                    twoOfKind=i-1
            else:
                break
        if threeOfKind >=0 and twoOfKind >=0:       #Checks if Three of a kind and pair exists
            result=[7,threeOfKind,twoOfKind]        #Sets result to 7 to represent Full house and rank values of three and two of a kind.
            
        return result     

    #Evaluate if hand has Flush
    def evaluateFlush(self, suitCounter):
        result=[]

        if (len(suitCounter[0])>4 or len(suitCounter[1])>4 or       #Checks if hand has flush
            len(suitCounter[2])>4 or len(suitCounter[3])>4):
            for i in range(len(self.allCards)-1, 3, -1):
                if (self.allCards[i].getNumSuit() == self.allCards[i-1].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-2].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-3].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-4].getNumSuit()):
                    result=[6, self.allCards[i].getNumVal(),self.allCards[i-1].getNumVal(),                                 #Sets result to 6 to represent Flush and all card ranks
                        self.allCards[i-2].getNumVal(),self.allCards[i-3].getNumVal() ,self.allCards[i-4].getNumVal()]      #inside the flush
                    if self.allCards[i-4].getNumVal()==0:
                        result.pop()
                        result.insert(1,0)
                    break

        return result

    #Evaluate if hand has Straight
    def evaluateStraight(self, rankCounter):
        result=[]
        if (len(rankCounter[0])>0 and len(rankCounter[12])>0 and            #Checks for straight with Ace as high
            len(rankCounter[11])>0 and len(rankCounter[10])>0 and
            len(rankCounter[9])>0):
            result=[5, 0]                                                   #Sets result to 5 to represent straight and 0 to represent ace as high
            return result
        for i in range(len(rankCounter), 4, -1):
            if (len(rankCounter[i-1])>0 and len(rankCounter[i-2])>0 and     #Checks for straight in hand
                len(rankCounter[i-3])>0 and len(rankCounter[i-4])>0 and
                len(rankCounter[i-5])>0):
                result=[5,i-1]                                              #Sets result to 5 to represent straight and highest rank in straight

        return result

    #Evaluate if hand has Three of a kind
    def evaluateThreeOfAKind(self, rankCounter):
        result=[]

        for i in range(len(rankCounter),0,-1):
            if len(rankCounter[i-1])>2:                     #Checks for Three of a Kind
                result =[4, i-1]                            #Sets result to 4 to represent three of a kind
                count=0
                if len(rankCounter[0])>0 and i!=0:
                    result.append(0)                        #If ace is present, adds to result
                    count+=1
                for j in range(len(rankCounter),0,-1):
                    if len(rankCounter[j-1])>0 and (j-1)!=i and count!=2:
                        result.append(j-1)                  #Adds highest ranking cards outside of three of a kind to result
                        count+=1
                break
        return result

    #Evaluate if hand has Three of a kind
    def evaluateTwoPair(self, rankCounter):
        result=[]

        pairOne=-1
        pairTwo=-1

        for i in range(len(rankCounter),0,-1):              #Finds pairs in hand
            if pairOne<0 or pairTwo<0:
                if len(rankCounter[i-1])>1 and pairOne < 0:
                    pairOne=i-1
                elif len(rankCounter[i-1])>1:
                    pairTwo=i-1
            else:
                break

        if pairOne>=0 and pairTwo >=0:                      #Finds if two pairs exist
            if (pairTwo==0):
                result=[3, pairTwo, pairOne]                #Sets result to 3 to represent two pair
            else:                                           #Sets the higher pair first to result and second pair next
                result=[3, pairOne, pairTwo]

            if (len(rankCounter[0])>0 and pairOne!=0 and pairTwo!=0):
                    result.append(0)                        #Adds ace if not in two pair to result
                    return result
            for j in range(len(rankCounter),0,-1):
                if len(rankCounter[j-1])>0 and (j-1)!=pairOne and (j-1)!=pairTwo:
                    result.append(j-1)                      #Adds highest ranking card outside the two pairs to result
                    break
        return result

    #Evaluate if hand has One Pair
    def evaluateOnePair(self, rankCounter):
        result=[]

        for i in range(len(rankCounter),0,-1):              #Finds if hand has one pair
            if len(rankCounter[i-1])>1:
                result=[2, i-1]                             #Sets result to 2 to represent one pair and ranking of pair
                count=0
                if len(rankCounter[0])>0 and i!=0:          #Adds highest ranking cards outside of pair to result
                    result.append(0)
                    count+=1
                for j in range(len(rankCounter),0,-1):
                    if len(rankCounter[j-1])>0 and (j-1)!=i and count!=3:
                        result.append(j-1)
                        count+=1
                break
        return result

    #Evaluate hand's high card
    def evaluateHighCard(self, rankCounter):
        result=[1]                                      #Sets result to 1 to represent high card
        count=0
        if len(rankCounter[0])>0:                       #Adds highest ranking four cards next
            result.append(0)
            count+=1

        for i in range(len(rankCounter),0,-1):          
            if len(rankCounter[i-1])>0 and count!=5:
                result.append(i-1)
                count+=1

        return result
    
    #Finds the winner(s) of competing poker players with specific tie breaker rules.
    def winning(self, competing, winCond):
        winners=[]
        winners2=[]
        winners3=[]

        if len(competing)==1:                                           #If only one player has the highest win condition, then just return the player
            return competing                

        if winCond==10:                                                 #Royal Flush
            return competing                                            #Returns all competing players, as there are no tiebreakers for Royal Flush

        elif winCond==9:                                                #Straight Flush
            maxVal = max(x._winCondition[1] for x in competing)         #Finds winner by higher card in straight flush
            for x in competing:
                if x._winCondition[1] == maxVal:
                    winners.append(x)

        elif winCond==8:                                                #Four of a Kind
            if (min(x._winCondition[1] for x in competing)==0):         
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)
            
            for x in competing:
                if x._winCondition[1] == maxVal:                        #Finds winner by whoever has the higher four of a kind
                    winners.append(x)
            if len(winners)>1:                                          #If there's a tie for highest four of a kind, then checks for highest card outside.
                if (min(x._winCondition[2] for x in winners)==0):       
                    maxVal=0
                else:
                    maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                return winners2
                
        elif winCond==7:                                                #Full House
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)
                
            for x in competing:
                if x._winCondition[1] == maxVal:                        #Finds winner by whoever has the higher three of a kind
                    winners.append(x)
            if len(winners)>1:                                          #If there's a tie for highest three of a kind, then checks for highest pair
                if (min(x._winCondition[2] for x in winners)==0): 
                    maxVal=0
                else:
                    maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                return winners2

        elif winCond==6:                                                #Flush
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)

            for x in competing:
                if x._winCondition[1]==maxVal:                          #Finds winner by whoever has the cards in flush
                    winners.append(x)
            
            if len(winners) >1:                                         #If there's a tie for highest card, then it will check the next highest cards, continuously until the last card.
                maxVal = max(x._winCondition[2] for x in winners)      
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                if len(winners2)==1:
                    return winners2
                else:
                    maxVal = max(x._winCondition[3] for x in winners2)
                    for x in winners2:
                        if x._winCondition[3] == maxVal:
                            winners3.append(x)
                    if len(winners3)==1:
                        return winners3
                    else:
                        winners.clear()
                        maxVal = max(x._winCondition[4] for x in winners3)
                        for x in winners3:
                            if x._winCondition[4] == maxVal:
                                winners.append(x)
                        if len(winners)==1:
                            return winners
                        else:     
                            winners2.clear()
                            maxVal = max(x._winCondition[5] for x in winners)
                            for x in winners:
                                if x._winCondition[5] == maxVal:
                                    winners2.append(x)
                            return winners2        

        elif winCond==5:                                                #Straight
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)            

            for x in competing:
                if x._winCondition[1]==maxVal:                          #Finds winner by whoever has the higher straight
                    winners.append(x)
        
        elif winCond==4:                                                #Three of a Kind
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)

            for x in competing:
                if x._winCondition[1]==maxVal:                          #Finds winner by whoever has the higher three of a kind
                    winners.append(x)
            
            if len(winners) >1:                                         #If there's a tie for highest three of a kind, checks remaining cards for higher ranks
                if (min(x._winCondition[2] for x in winners)==0): 
                    maxVal=0
                else:
                    maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                if len(winners2)==1:
                    return winners2
                else:
                    maxVal = max(x._winCondition[3] for x in winners2)
                    for x in winners2:
                        if x._winCondition[3] == maxVal:
                            winners3.append(x)
                    return winners3

        elif winCond==3:                                                #Two Pair
            
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)

            for x in competing:
                if x._winCondition[1]==maxVal:                          #Finds winner by whoever has the higher first pair
                    winners.append(x)
            
            if len(winners) >1:
                maxVal = max(x._winCondition[2] for x in winners)       #If tied, finds winner by whoever has the higher second pair
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                if len(winners2)==1:                                    #If tied again, finds winner by whoever has the highest remaining card
                    return winners2
                else:
                    if (min(x._winCondition[3] for x in winners2)==0): 
                        maxVal=0
                    else:
                        maxVal = max(x._winCondition[3] for x in winners2)
                    for x in winners2:
                        if x._winCondition[3] == maxVal:
                            winners3.append(x)
                    return winners3

        elif winCond==2:                                                #One Pair
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)

            for x in competing:
                if x._winCondition[1]==maxVal:                          #Finds winner by whoever has the higher pair
                    winners.append(x)
            
            if len(winners) >1:                                         #If there's a tie for highest pair, then it will check the next highest cards, continuously until the last card.
                if (min(x._winCondition[2] for x in winners)==0): 
                    maxVal=0
                else:
                    maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                if len(winners2)==1:
                    return winners2
                else:
                    maxVal = max(x._winCondition[3] for x in winners2)
                    for x in winners2:
                        if x._winCondition[3] == maxVal:
                            winners3.append(x)
                    if len(winners3)==1:
                        return winners3
                    else:
                        winners.clear()
                        maxVal = max(x._winCondition[4] for x in winners3)
                        for x in winners3:
                            if x._winCondition[4] == maxVal:
                                winners.append(x)    

        elif winCond==1:                                            #High Card
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)

            for x in competing:
                if x._winCondition[1]==maxVal:                      #Finds winner by whoever has the highest card, if tied continuously check the next highest card
                    winners.append(x)               
            
            if len(winners) >1:
                maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                if len(winners2)==1:
                    return winners2
                else:
                    maxVal = max(x._winCondition[3] for x in winners2)
                    for x in winners2:
                        if x._winCondition[3] == maxVal:
                            winners3.append(x)
                    if len(winners3)==1:
                        return winners3
                    else:
                        winners.clear()
                        maxVal = max(x._winCondition[4] for x in winners3)
                        for x in winners3:
                            if x._winCondition[4] == maxVal:
                                winners.append(x)
                        if len(winners)==1:
                            return winners
                        else:     
                            winners2.clear()
                            maxVal = max(x._winCondition[5] for x in winners)
                            for x in winners:
                                if x._winCondition[5] == maxVal:
                                    winners2.append(x)
                            return winners2                      
        return winners