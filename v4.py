
# We start off by importing the random module in order to generate random cards for our hands.
import random

# We then create our first class, the cards we're going to use for our BlackJack game.
class Card:
    def __init__(self, suit, value) -> None:
        self.suit = suit
        self.value = value

# Since we want our end users to see the actual numerical values of the cards we call the repr() function to translate our Python objects to end-user friendly output.
    
    def __repr__(self) -> str:
        return (f"{self.value} of the suit of {self.suit}")

# Now that we have the very basic sketch of the framework for our cards, we're going to move on and make our second class, the Player class.
class Player:
    def __init__(self, name, money=100) -> None:
        # I'm setting the players starting chips (the default value) to equal $100.00. I want to keep things simple so it's easier for us to wrap our brains around the core concepts.
        self.name = name
        self.money = money
        self.cards = []
        self.bet = 0
    
# For our next step, we're going to set up our Method to place bets.
    def place_bet(self):
        # We're going to make a very basic While Loop that will hold our program to the basic betting rules.
        while True:
            bet = int(input(f"{self.name}, you currently have ${self.money} left. How much are you willing to bet?"))
            if bet > self.money:
                print(f"Unforutnately, you simply can't bet more than you have.")
            else:
                self.bet = bet
                self.money -= bet
                break
    
    # Here we're setting up a very basic method to deal cards for all parties involved.
    def add_card(self, card):
        self.cards.append(card)
    
    # Here we're setting up the logic to calculate the final scores of the cards we work with.
    def calculate_score(self):
        aces = 0
        score = 0
        for card in self.cards:
            if card.value.isnumeric():
                score += int(card.value)
            elif card.value in ['Jack', 'Queen', 'King']:
                score += 10
            elif card.value == 'Ace':
                aces += 1
                score += 11
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score
    # The toughest bit has been in comping up with how to handle an Ace, but we set up a rudimentary While loop to handle that.

    def __repr__(self) -> str:
        return (f"{self.name} currently has ${self.money} remaining.")

# The dirty, filthy little secret to setting up our Dealer is that we simply make the Dealer Class a child that inherits all of the attributes and methods of the parent Player Class.
class Dealer(Player):
    def __init__(self) -> None:
        super().__init__("Dealer", 0)
        # Since the dealer is a faceless, nameless entity we can ignore the restrictions and therefore the parameters that the Player has. The super() funciton here is simply used to call the methods and access the properties of the Parent Player Class.

# Now that we're done making the required classes we'll write the logic for the actual game of BlackJack.
def blackjack_game():
    suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    # The most basic setup of both, all available suits and number values in a standard deck of playing cards

    deck = [Card(suit, value) for suit in suits for value in values]
    random.shuffle(deck)

    # We've come to a difficult fork in our programming path, how to program more than a single human player. Let's start off by simply prinitng interaction with our human players in the Terminal.
    dealer = Dealer()
    players = [Player(input(f"Please, enter your name Player 1:"))]
    if input(f"Is there another player? (yay/nay)").lower() == 'yay':
        players.append(Player(input(f"Please, enter your name Player 2:")))
    
    for player in players:
        player.place_bet()
        player.add_card(deck.pop())
        player.add_card(deck.pop())
    # The pop()function takes the last card in our shuffle deck and presents it to us. It's destructive, and modifies our original deck o' cards.
    
    dealer.add_card(deck.pop())
    dealer.add_card(deck.pop())

    for player in players:
        while True:
            print(f"{player.name} it's currently your turn my dear friend. Your cards are {player.cards}. Just so you're aware your cards currently add up to {player.calculate_score()}")
            if player.calculate_score() == 21:
                player.money += 2 * player.bet
                print(f"Huzzah! You hit the fabled, mythical BlackJack! You've done it bud, you won! Enjoy your {player.money}")
                return
            elif player.calculate_score() > 21:
                print(f"Oh no! You BUSTED! YOU LOSE!")
                return
            elif input(f"Do you wish to hit or stay? (hit/stay): ").lower() == 'hit':
                player.add_card(deck.pop())
            else:
                break
    
    while dealer.calculate_score() <= 16:
        dealer.add_card(deck.pop())
    
    print(f"The Dealer currently holds these cards: {dealer.cards}. Their current score is a grand total of: {dealer.calculate_score()}")
    if dealer.calculate_score() > 21:
        print(f"What's it feel like? Knowing you just made a grown man cry? Because you just beat the Dealer, the Dealer busts YOU WIN!")
        for player in players:
            player.money += 2 * player.bet
            print(f"And your total winnigns are: {player.money}")

    else:
        for player in players:
            if player.calculate_score() > dealer.calculate_score() and player.calculate_score() <= 21:
                print(f"{player.name} wins!")
                player.money += 2 * player.bet
                print(f"And your total winnigns are: {player.money}")
            else:
                print(f"{player.name} loses! Thank you for playing, try again!")

blackjack_game()