# Name: Roberto Hong Xu Kuang
# Class: CS 375-01
# Date: 10/28/2014

# Blackjack Program
# This program will allow the player to play a blackjack game.
# Special note : Ace will be an 11 unless there is already another Ace,
# at that point, the second ace will have a value of 1.
# If the total of the hand goes over 21 with an Ace, then that ace will become 1 also.

#Using random to randomly get the card to the player and the dealer.
import random

#Global variables.
money = 100
bet = 0
player = [] #Will store the player cards.
dealer = [] #Will store the dealer cards.

#Class card
# A Card has a name, which is A, J, Q, K, and 2-10.
# Value is the numerical value, which is 1/11 for Aces, 2-10 for cards 2 through K
# Hidden is just for the very beginning, to hide the dealer card.
class card:
    def __init__(self,name,value,hidden):
        self.name = name
        self.value = value
        self.hidden = hidden
    #Change the hidden attribute.
    def toggleHide(self):
        if self.hidden == 0:
            self.hidden = 1;
        else:
            self.hidden = 0;
        return self
    #Change the value.
    def setValue(self, value):
        self.value = value
    #If the card is hidde, it will show a question mark, otherwise the name.
    def printCard(self):
        if self.hidden == 1:
            return "?"
        else:
            return self.name
        
# method hasAce
# This will check if the hand contains an Ace. Will return the index if found.
def hasAce(hand):
    for loop in range(0,len(hand)):
        if hand[loop].value == 11:
            return loop;
    return -1

# method play
# Asks the player to input the amount to bet.
def play():
    global bet
    #Will continue until valid number.
    while bet < 1 or bet > money:
        #This makes sure that the entered value is an int.
        try:
            bet = int(input("Enter amount to bet:"))
        except ValueError:
            print("Not an integer")
            
        if bet < 1 or bet > money:
            print("Bet invalid.")

# method drawCard
# This will give the hand a correct card.
def drawCard(hand):
    #Using the random library to get a card.
    num = random.randrange(0,52)%13
    #Since it goes from 0 to 51, I add 1 for better values.
    num += 1

    #Aces start off as 11, and J-K start as 10.
    if num == 1:
        name = "A"
        num = 11
    elif num == 11:
        name = "J"
        num = 10
    elif num == 12:
        name = "Q"
        num = 10
    elif num == 13:
        name = "K"
        num = 10
    else:
        name = num

    #For more than 1 Ace, the second+ aces are values of 1
    if name == "A" and hasAce(hand) >= 0:
        num = 1

    #Adds the card to the hand list.
    hand.append(card(name,num,0))

# method totalVal
# Calculates the total of the hand.
def totalVal(hand):
    total = 0
    for loop in range(0,len(hand)):
        if hand[loop].hidden == 0:
            total += hand[loop].value;
    return total

# method printCards
# Will print out and calculate the cards of both hands.
def printCards():
    pString = ""
    dString = ""
    for loop in range(0,len(player)):
        pString += str(player[loop].printCard()) + " "
    for loop in range(0,len(dealer)):
        dString += str(dealer[loop].printCard()) + " "

    print("Player Cards: " + pString + "(" + str(totalVal(player)) +")")
    print("Dealer Cards: " + dString + "(" + str(totalVal(dealer)) +")")
    print("")

# method playerDeal
# Allows the player to either hit or stand.
def playerDeal():
    choice = 0
    while choice != 2 and totalVal(player) < 21:
        print("1. Hit")
        print("2. Stand")
        #Checks for correct integer input.
        try:
            choice = int(input("Choice: "))
        except ValueError:
            print("Not an integer")

        if choice == 1:
            #Adds a card.
            drawCard(player)
            #This is to change any Aces to 1 if they're over 21.
            if totalVal(player) > 21 and hasAce(player) >= 0:
               player[hasAce(player)].setValue(1)
            printCards()
            
# method dealerDeal
# Like the playerDeal method, but automated for the dealer.
def dealerDeal():
    #The dealer will hit anything below 17.
    while totalVal(dealer) < 17:
        drawCard(dealer)
        #Like the playerDeal method, this will change Aces.
        if totalVal(dealer) > 21 and hasAce(dealer) >= 0:
           dealer[hasAce(dealer)].changeValue(1)
        printCards()

# method GameOver
# Once the round has ended, it will calculate the two hands
# and give the proper bet back to the player.
def gameOver():
    global bet
    global money
    
    playerTotal = totalVal(player)
    dealerTotal = totalVal(dealer)
    #If the player lost,
    if (playerTotal > 21 and dealerTotal <= 21) or (playerTotal < dealerTotal and dealerTotal <= 21):
        money -= bet
        print("Sorry, you lost the round and " + str(bet) + " coins.")
    #if the player won.
    elif (playerTotal <= 21 and dealerTotal > 21) or (playerTotal > dealerTotal and playerTotal <= 21):
        money += bet
        print("Congratulations! You won the round and " + str(bet) + " coins!")

# method startRound
# This is the main driver of the program.
# This resets all the global variables for the rounds,
# And calls the other methods, and begins the round.
def startRound():
    print("Now starting new round of BlackJack")
    #Resetting
    global player
    global dealer
    global bet
    player = []
    dealer = []
    bet = 0
    #Calls the play method.
    play()
    print("Bet wagered: ",bet)
    #Initial cards.
    drawCard(player)
    drawCard(player)
    drawCard(dealer)
    drawCard(dealer)
    #Hide the dealer's second card.
    dealer[1].toggleHide()
    #Print out the cards.
    printCards()
    #Player goes first.
    playerDeal()
    print("Player turn over!")
    #Unhide the dealer's card.
    dealer[1].toggleHide()
    #Show the cards.
    printCards()
    #dealer's turn.
    dealerDeal()
    #Run the game over method.
    gameOver()

# method printMenu
# This is a menu that will be shown every time a round ends.
def printMenu():
    choice = 0
    while choice != 3 and money > 0:
        print("Menu")
        print("1: Start new round")
        print("2: Check coins")
        print("3: Exit")
        #check for integer input.
        try:
            choice = int(input("Choice: "))
        except ValueError:
            print("Not an integer")
            
        if choice == 1:
            startRound()
        elif choice == 2:
            print("Current coins: ", money)
        elif choice == 3:
            print("Thanks for playing!")
        print("")
    print("Looks like you're all out of money! Sorry, try again!")


#The very beginning introduction, and calling menu for the first time
print("Hello, welcome to Blackjack. You start off with 100 coins.")
print("Aces count as 1 or 11. Jack, Queen, and King all equal to 10.")
print("Dealer must hit below 17. You get 2x the bet if you win.")
print("Now, lets start!")
printMenu()
