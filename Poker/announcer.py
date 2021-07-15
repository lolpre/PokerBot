class Announcer():
    def initiateGame():
        print("WELCOME TO POKER BOT!")
        print("If this is your first time with Poker Bot," + 
        "please type \'.create\'. Please type \'.help\' for the rules" + 
        "and betting system.")
    
    def askBet():
        print("What is the big blind (minimum bet) amount?")
    
    def announceWinner(sorted_players, com_deck, currentPot):
        #printing community hands
        print("CURRENT COMMUNITY DECK")

        com_str = ""
        winner = sorted_players[0]
        for card in com_deck:
            com_str += card.show + ", "
        print(com_str)    
        print(winner + " has won, receiving " + currentPot)
            
    def askMove(hand):
        print("Here is your hand:")
        hand_str = ""
        for card in hand:
            hand_str += card.str + ", "
        print(hand_str)
        print("Would you like to call, raise, or fold?")

    def showCards(seat, pkr_players):
        play_hand = pkr_players[seat].getHand()
        hand_str = ""
        print("Your current hand:")
        for card in play_hand:
            hand_str += card.show + ", "
        print(hand_str)

    def reportRaise(seat, pkr_players):
        print(pkr_players[seat].username + " has raised!")

    def reportCall(seat, pkr_players):
        print(pkr_players[seat].username + " has called!")

    def reportFold(seat, pkr_players):
        print(pkr_players[seat].username + " has folded!")

    def showBalances(pkr_players):
        print("CURRENT BALANCES:")
        for player in pkr_players:
            print(player.username + ": " + player.getGameBalance())
