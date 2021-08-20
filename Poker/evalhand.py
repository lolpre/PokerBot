from Poker.card import Card
from Poker.pokerplayer import PokerPlayer



class EvaluateHand:
    '''
    EvaluateHand

    This is the EvaluateHand class. This class's sole purpose is to
    evaluate the given hand. It runs an algorithm that checks to see
    what is the best combination for the hand. Such combinations are
    a Royal Flush, Two Pair, Straight Flush, Four of a Kind, etc.

    '''

    def __init__(self, hand):
        """Constructor to Evaluate Hand. Sets hand to all_cards List."""
        self.all_cards = hand
    
    def print_hand(self):
        """Prints the cards in all_cards."""
        for x in self.all_cards:
            print(str(x.val) +str(x.suit) )

    def add_card(self, card):
        """Adds card to all_cards List."""
        self.all_cards.append(card)

    def num_cards(self):
        """Returns the amount of cards in all_cards."""
        return len(self.hand)

    def sort_by_rank(self):
        """Sorts the all_cards list by card rank."""
        self.all_cards.sort(key = lambda x:x.get_num_val())
    
    def sort_by_suit(self):
        """Sorts the all_cards list by card suit."""
        self.all_cards.sort(key = lambda x:x.get_num_suit())
    
    def sort_by_suit_then_rank(self):
        """Sorts the all_cards list by card suit then by card rank."""
        self.all_cards.sort(key = lambda x:x.get_num_suit())
        self.all_cards.sort(key = lambda x:x.get_num_val())

    def sort_by_rank_then_suit(self):
        """Sorts the all_cards list by card rank then by card suit."""
        self.all_cards.sort(key = lambda x:x.get_num_val())
        self.all_cards.sort(key = lambda x:x.get_num_suit())

    def evaluate(self):
        """Evaluates all_cards to find all its possible winning conditions."""

        #Count the ranks and suits in all_cards
        rank_counter = {}
        suit_counter = {}

        for x in range(13):
            rank_counter[x] = []

        for x in range(4):
            suit_counter[x] = []

        for x in self.all_cards:
            rank_counter[x.get_num_val()].append(x)
            suit_counter[x.get_num_suit()].append(x)

        self.sort_by_rank_then_suit()

        hand_result = []
        #Evaluate if hand has Royal Flush
        hand_result = self.evaluate_royal(rank_counter,suit_counter)      

        #Evaluate if hand has Straight Flush
        if len(hand_result) == 0:
            hand_result = self.evaluate_straight_flush(suit_counter)      
    
        #Evaluate if hand has Four of a Kind
        if len(hand_result) == 0:
            hand_result = self.evaluate_four_of_a_kind(rank_counter)        
        
        #Evaluate if hand has Full House
        if len(hand_result) == 0:
            hand_result = self.evaluate_full_house(rank_counter)           

        #Evaluate if hand has Flush
        if len(hand_result) == 0:
            hand_result = self.evaluate_flush(suit_counter)              

        #Evaluate if hand has Straight
        if len(hand_result) == 0:
            hand_result = self.evaluate_straight(rank_counter)           

        #Evaluate if hand has Three of a Kind
        if len(hand_result) == 0:
            hand_result = self.evaluate_three_of_a_kind(rank_counter)       
        
        #Evaluate if hand has Two Pair
        if len(hand_result) == 0:
            hand_result = self.evaluate_two_pair(rank_counter)            

        #Evaluate if hand has One Pair
        if len(hand_result) == 0:
            hand_result = self.evaluate_one_pair(rank_counter)            

        #Evaluate if hand's High Card
        if len(hand_result) == 0:
            hand_result = self.evaluate_high_card(rank_counter)           
        
        #Returns result of evaluated hand
        return hand_result            
    
    def evaluate_royal(self, rank_counter, suit_counter):
        """Evaluate if hand has Royal Flush."""

        result = []
        #Checks if hand has 10, J, Q, K, A
        if ((len(rank_counter[9]) >= 1 and len(rank_counter[10]) >= 1 and         
            len(rank_counter[11]) >= 1 and len(rank_counter[12]) >= 1 and
            len(rank_counter[0]) >= 1)
            and #Checks for flush
            (len(suit_counter[0]) > 4 or len(suit_counter[1]) > 4 or              
            len(suit_counter[2]) > 4 or len(suit_counter[3]) > 4)):
            #Finds where in hand has Royal Flush
            for i in range(3):
                if (self.all_cards[i].get_num_val() == 0):
                    for j in range(1,4-i):
                        if (self.all_cards[i+j].get_num_val() == 9 and 
                            self.all_cards[i+j+1].get_num_val() == 10 and  
                            self.all_cards[i+j+2].get_num_val() == 11 and 
                            self.all_cards[i+j+3].get_num_val() == 12
                            and
                            self.all_cards[i].get_num_suit() == 
                            self.all_cards[i+j].get_num_suit() and
                            self.all_cards[i].get_num_suit() == 
                            self.all_cards[i+j+1].get_num_suit() and
                            self.all_cards[i].get_num_suit() == 
                            self.all_cards[i+j+2].get_num_suit() and
                            self.all_cards[i].get_num_suit() == 
                            self.all_cards[i+j+3].get_num_suit()):
                            #Sets result to 10 to represent Royal Flush
                            result = [10]                                     
                            break
        return result

    
    def evaluate_straight_flush(self, suit_counter):
        """Evaluate if hand has Straight Flush."""

        result = []
        #Checks for Flush
        if (len(suit_counter[0]) > 4 or len(suit_counter[1]) > 4 or               
            len(suit_counter[2]) > 4 or len(suit_counter[3]) > 4):
            #Checks for Straight
            for i in range(len(self.all_cards)-1, 3, -1):                    
                if ((self.all_cards[i].get_num_val()-1 == 
                    self.all_cards[i-1].get_num_val() and   
                    self.all_cards[i].get_num_val()-2 == 
                    self.all_cards[i-2].get_num_val() and
                    self.all_cards[i].get_num_val()-3 == 
                    self.all_cards[i-3].get_num_val() and
                    self.all_cards[i].get_num_val()-4 == 
                    self.all_cards[i-4].get_num_val())
                    and
                    (self.all_cards[i].get_num_suit() == 
                    self.all_cards[i-1].get_num_suit() and
                    self.all_cards[i].get_num_suit() == 
                    self.all_cards[i-2].get_num_suit() and
                    self.all_cards[i].get_num_suit() == 
                    self.all_cards[i-3].get_num_suit() and
                    self.all_cards[i].get_num_suit() == 
                    self.all_cards[i-4].get_num_suit())):
                    #Sets result to 9 to represent Straight Flush and 
                    # highest card rank in straight
                    result = [9,self.all_cards[i].get_num_val()]                 
        return result

    def evaluate_four_of_a_kind(self, rank_counter):
        """Evaluate if hand has Four of a Kind."""

        result = []
        #Checks for Four of a Kind
        for i in range(13):                             
            if len(rank_counter[i]) == 4:
                #Sets result to 8 to represent Four of a Kind 
                #and the rank value
                result = [8,i]
                #Adds Ace rank to result if highest 
                # card outside four of a kind                            
                if len(rank_counter[0]) > 0 and i != 0:      
                    result.append(0)
                    break
                #Adds card rank outside four of a kind to result 
                for j in range(len(rank_counter),0,-1):  
                    if len(rank_counter[j-1]) > 0 and j != i:
                        result.append(j)
                        break
                break
        return result        

    def evaluate_full_house(self, rank_counter):
        """Evaluate if hand has Full House."""

        result = []
        three_of_kind =- 1
        two_of_kind =- 1
        #Checks for Three of a kind and two of a kind
        for i in range(len(rank_counter), 0, -1):    
            if three_of_kind < 0 or two_of_kind < 0:
                if len(rank_counter[i-1]) > 2:
                    three_of_kind = i-1
                elif len(rank_counter[i-1]) > 1:
                    two_of_kind = i-1
            else:
                break
        #Checks if Three of a kind and pair exists
        if three_of_kind >=0 and two_of_kind >=0:       
            #Sets result to 7 to represent Full house 
            #and rank values of three and two of a kind.
            result = [7,three_of_kind,two_of_kind]        
            
        return result     

    def evaluate_flush(self, suit_counter):
        """Evaluate if hand has Flush."""

        result = []
        #Checks if hand has flush
        if (len(suit_counter[0]) > 4 or len(suit_counter[1]) > 4 or       
            len(suit_counter[2]) > 4 or len(suit_counter[3]) > 4):
            for i in range(len(self.all_cards)-1, 3, -1):
                if (self.all_cards[i].get_num_suit() == 
                    self.all_cards[i-1].get_num_suit() and
                    self.all_cards[i].get_num_suit() == 
                    self.all_cards[i-2].get_num_suit() and
                    self.all_cards[i].get_num_suit() == 
                    self.all_cards[i-3].get_num_suit() and
                    self.all_cards[i].get_num_suit() == 
                    self.all_cards[i-4].get_num_suit()):
                    #Sets result to 6 to represent Flush and all card ranks
                    #inside the flush
                    result = [6, self.all_cards[i].get_num_val(),
                        self.all_cards[i-1].get_num_val(),                                 
                        self.all_cards[i-2].get_num_val(),
                        self.all_cards[i-3].get_num_val(),
                        self.all_cards[i-4].get_num_val()]      
                    if self.all_cards[i-4].get_num_val() ==0:
                        result.pop()
                        result.insert(1,0)
                    break

        return result

    def evaluate_straight(self, rank_counter):
        """Evaluate if hand has Straight."""

        result = []
        #Checks for straight with Ace as high
        if (len(rank_counter[0]) > 0 and len(rank_counter[12]) > 0 and            
            len(rank_counter[11]) > 0 and len(rank_counter[10]) > 0 and
            len(rank_counter[9]) > 0):
            #Sets result to 5 to represent straight and 0 
            #to represent ace as high
            result = [5, 0]                                                   
            return result
        for i in range(len(rank_counter), 4, -1):
            #Checks for straight in hand
            if (len(rank_counter[i-1]) > 0 and len(rank_counter[i-2]) > 0 and     
                len(rank_counter[i-3]) > 0 and len(rank_counter[i-4]) > 0 and
                len(rank_counter[i-5]) > 0):
                #Sets result to 5 to represent straight and 
                #highest rank in straight
                result = [5,i-1]                                              

        return result

    def evaluate_three_of_a_kind(self, rank_counter):
        """Evaluate if hand has Three of a kind."""

        result = []

        for i in range(len(rank_counter),0,-1):
            #Checks for Three of a Kind
            if len(rank_counter[i-1]) > 2:      
                #Sets result to 4 to represent three of a kind               
                result =[4, i-1]                            
                count = 0
                if (len(rank_counter[0]) > 0 and i != 0 ):
                    #If ace is present, adds to result
                    result.append(0)                        
                    count+=1
                for j in range(len(rank_counter),0,-1):
                    if (len(rank_counter[j-1]) > 0 and 
                        (j-1) != i and count != 2):
                        #Adds highest ranking cards outside of three of a kind 
                        #to result
                        result.append(j-1)                  
                        count+=1
                break
        return result

    def evaluate_two_pair(self, rank_counter):
        """Evaluate if hand has Three of a kind."""

        result = []

        pair_one =- 1
        pair_two =- 1

        #Finds pairs in hand
        for i in range(len(rank_counter),0,-1):              
            if pair_one < 0 or pair_two < 0:
                if len(rank_counter[i-1]) > 1 and pair_one < 0:
                    pair_one = i-1
                elif len(rank_counter[i-1]) > 1:
                    pair_two = i-1
            else:
                break
        #Finds if two pairs exist            
        if pair_one >= 0 and pair_two >= 0:                      
            if (pair_two == 0):
                #Sets result to 3 to represent two pair
                result = [3, pair_two, pair_one]                
            else:                                
                #Sets the higher pair first to result and second pair next           
                result = [3, pair_one, pair_two]

            if (len(rank_counter[0]) > 0 and 
                pair_one != 0 and pair_two != 0):
                    #Adds ace if not in two pair to result
                    result.append(0)                        
                    return result
            for j in range(len(rank_counter),0,-1):
                if (len(rank_counter[j-1]) > 0 and 
                    (j-1) != pair_one and (j-1) != pair_two):
                    #Adds highest ranking card outside the two pairs to result
                    result.append(j-1)                      
                    break
        return result

    def evaluate_one_pair(self, rank_counter):
        """Evaluate if hand has One Pair."""

        result = []
        #Finds if hand has one pair
        for i in range(len(rank_counter),0,-1):              
            if len(rank_counter[i-1]) > 1:
                #Sets result to 2 to represent one pair and ranking of pair
                result = [2, i-1]                             
                count = 0
                #Adds highest ranking cards outside of pair to result
                if (len(rank_counter[0]) > 0 and i != 0):          
                    result.append(0)
                    count+=1
                for j in range(len(rank_counter),0,-1):
                    if (len(rank_counter[j-1]) > 0 and 
                        (j-1) != i and count != 3):
                        result.append(j-1)
                        count+=1
                break
        return result

    def evaluate_high_card(self, rank_counter):
        """Evaluate hand's high card."""

        #Sets result to 1 to represent high card
        result = [1]                                      
        count = 0
        #Adds highest ranking four cards next
        if len(rank_counter[0]) > 0:                       
            result.append(0)
            count+=1

        for i in range(len(rank_counter),0,-1):          
            if len(rank_counter[i-1]) > 0 and count != 5:
                result.append(i-1)
                count+=1

        return result
    

    def winning(self, competing, win_cond):
        """Finds the winner(s) of competing poker players with specific 
        tie breaker rules."""
        winners = []
        winners_2 = []
        winners_3 = []

        #If only one player has the highest win condition, 
        #then just return the player
        if len(competing) == 1:                                           
            return competing                
        #Royal Flush
        if win_cond == 10:           
            #Returns all competing players, as there are no tiebreakers 
            #for Royal Flush                                      
            return competing         

        #Straight Flush
        elif win_cond == 9:                 
            #Finds winner by higher card in straight flush                               
            max_val = max(x.win_condition[1] for x in competing)         
            for x in competing:
                if x.win_condition[1] == max_val:
                    winners.append(x)
        #Four of a Kind
        elif win_cond == 8:                                                
            if (min(x.win_condition[1] for x in competing) == 0):         
                max_val = 0
            else:
                max_val = max(x.win_condition[1] for x in competing)

            #Finds winner by whoever has the higher four of a kind
            for x in competing:
                if x.win_condition[1] == max_val:                        
                    winners.append(x)
            #If there's a tie for highest four of a kind, then checks for 
            #highest card outside.
            if len(winners) > 1:                                          
                if (min(x.win_condition[2] for x in winners) == 0):       
                    max_val = 0
                else:
                    max_val = max(x.win_condition[2] for x in winners)
                for x in winners:
                    if x.win_condition[2] == max_val:
                        winners_2.append(x)
                return winners_2
                
        #Full House
        elif win_cond == 7:                                                
            if (min(x.win_condition[1] for x in competing) == 0): 
                max_val = 0
            else:
                max_val = max(x.win_condition[1] for x in competing)
                
            for x in competing:
                #Finds winner by whoever has the higher three of a kind
                if x.win_condition[1] == max_val:                        
                    winners.append(x)
            #If there's a tie for highest three of a kind, then checks for 
            #highest pair
            if len(winners) > 1:                                          
                if (min(x.win_condition[2] for x in winners) == 0): 
                    max_val = 0
                else:
                    max_val = max(x.win_condition[2] for x in winners)
                for x in winners:
                    if x.win_condition[2] == max_val:
                        winners_2.append(x)
                return winners_2
        #Flush
        elif win_cond == 6:                                                
            if (min(x.win_condition[1] for x in competing) == 0): 
                max_val = 0
            else:
                max_val = max(x.win_condition[1] for x in competing)

            #Finds winner by whoever has the cards in flush
            for x in competing:
                if x.win_condition[1] == max_val:                          
                    winners.append(x)
            #If there's a tie for highest card, then it will check the next 
            #highest cards, continuously until the last card.
            if len(winners) > 1:                                        
                max_val = max(x.win_condition[2] for x in winners)      
                for x in winners:
                    if x.win_condition[2] == max_val:
                        winners_2.append(x)
                if len(winners_2) == 1:
                    return winners_2
                else:
                    max_val = max(x.win_condition[3] for x in winners_2)
                    for x in winners_2:
                        if x.win_condition[3] == max_val:
                            winners_3.append(x)
                    if len(winners_3) == 1:
                        return winners_3
                    else:
                        winners.clear()
                        max_val = max(x.win_condition[4] for x in winners_3)
                        for x in winners_3:
                            if x.win_condition[4] == max_val:
                                winners.append(x)
                        if len(winners) == 1:
                            return winners
                        else:     
                            winners_2.clear()
                            max_val = max(x.win_condition[5] for x in winners)
                            for x in winners:
                                if x.win_condition[5] == max_val:
                                    winners_2.append(x)
                            return winners_2        
        #Straight
        elif win_cond == 5:                                                
            if (min(x.win_condition[1] for x in competing) == 0): 
                max_val = 0
            else:
                max_val = max(x.win_condition[1] for x in competing)            

            #Finds winner by whoever has the higher straight
            for x in competing:
                if x.win_condition[1] == max_val:                          
                    winners.append(x)

        #Three of a Kind
        elif win_cond == 4:                                               
            if (min(x.win_condition[1] for x in competing) == 0): 
                max_val = 0
            else:
                max_val = max(x.win_condition[1] for x in competing)

            #Finds winner by whoever has the higher three of a kind
            for x in competing:
                if x.win_condition[1] == max_val:                          
                    winners.append(x)
            #If there's a tie for highest three of a kind, checks remaining 
            #cards for higher ranks
            if len(winners) > 1:                                         
                if (min(x.win_condition[2] for x in winners) == 0): 
                    max_val = 0
                else:
                    max_val = max(x.win_condition[2] for x in winners)
                for x in winners:
                    if x.win_condition[2] == max_val:
                        winners_2.append(x)
                if len(winners_2) == 1:
                    return winners_2
                else:
                    max_val = max(x.win_condition[3] for x in winners_2)
                    for x in winners_2:
                        if x.win_condition[3] == max_val:
                            winners_3.append(x)
                    return winners_3
        #Two Pair
        elif win_cond == 3:                                                
            
            if (min(x.win_condition[1] for x in competing) == 0): 
                max_val = 0
            else:
                max_val = max(x.win_condition[1] for x in competing)

            #Finds winner by whoever has the higher first pair
            for x in competing:
                if x.win_condition[1] == max_val:                          
                    winners.append(x)
            #If tied, finds winner by whoever has the higher second pair
            if len(winners) > 1:
                max_val = max(x.win_condition[2] for x in winners)       
                for x in winners:
                    if x.win_condition[2] == max_val:
                        winners_2.append(x)
                #If tied again, finds winner by whoever has the highest 
                # remaining card
                if len(winners_2) == 1:                                    
                    return winners_2
                else:
                    if (min(x.win_condition[3] for x in winners_2) == 0): 
                        max_val = 0
                    else:
                        max_val = max(x.win_condition[3] for x in winners_2)
                    for x in winners_2:
                        if x.win_condition[3] == max_val:
                            winners_3.append(x)
                    return winners_3
        #One Pair
        elif win_cond == 2:                                                
            if (min(x.win_condition[1] for x in competing) == 0): 
                max_val = 0
            else:
                max_val = max(x.win_condition[1] for x in competing)

            #Finds winner by whoever has the higher pair
            for x in competing:
                if x.win_condition[1] == max_val:                          
                    winners.append(x)
            #If there's a tie for highest pair, then it will check the next 
            # highest cards, continuously until the last card.
            if len(winners) > 1:                                         
                if (min(x.win_condition[2] for x in winners) == 0): 
                    max_val = 0
                else:
                    max_val = max(x.win_condition[2] for x in winners)
                for x in winners:
                    if x.win_condition[2] == max_val:
                        winners_2.append(x)
                if len(winners_2) == 1:
                    return winners_2
                else:
                    max_val = max(x.win_condition[3] for x in winners_2)
                    for x in winners_2:
                        if x.win_condition[3] == max_val:
                            winners_3.append(x)
                    if len(winners_3) == 1:
                        return winners_3
                    else:
                        winners.clear()
                        max_val = max(x.win_condition[4] for x in winners_3)
                        for x in winners_3:
                            if x.win_condition[4] == max_val:
                                winners.append(x)    
        #High Card
        elif win_cond == 1:                                            
            if (min(x.win_condition[1] for x in competing) == 0): 
                max_val = 0
            else:
                max_val = max(x.win_condition[1] for x in competing)

            #Finds winner by whoever has the highest card, if tied continuously 
            # check the next highest card
            for x in competing:
                if x.win_condition[1] == max_val:                      
                    winners.append(x)               
            
            if len(winners) > 1:
                max_val = max(x.win_condition[2] for x in winners)
                for x in winners:
                    if x.win_condition[2] == max_val:
                        winners_2.append(x)
                if len(winners_2) == 1:
                    return winners_2
                else:
                    max_val = max(x.win_condition[3] for x in winners_2)
                    for x in winners_2:
                        if x.win_condition[3] == max_val:
                            winners_3.append(x)
                    if len(winners_3) == 1:
                        return winners_3
                    else:
                        winners.clear()
                        max_val = max(x.win_condition[4] for x in winners_3)
                        for x in winners_3:
                            if x.win_condition[4] == max_val:
                                winners.append(x)
                        if len(winners) == 1:
                            return winners
                        else:     
                            winners_2.clear()
                            max_val = max(x.win_condition[5] for x in winners)
                            for x in winners:
                                if x.win_condition[5] == max_val:
                                    winners_2.append(x)
                            return winners_2                      
        return winners