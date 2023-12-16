import random

# Card class
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

# Deck class
class Deck:
    def __init__(self):
        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.cards = [Card(suit, value) for suit in suits for value in range(1, 14)]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

# Hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += 11 if card.value == 1 else min(card.value, 10)
        self.aces += 1 if card.value == 1 else 0

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def is_bust(self):
        return self.value > 21

    def is_blackjack(self):
        return self.value == 21 and len(self.cards) == 2

# Game class
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def show_initial_cards(self):
        print("Dealer's Hand:")
        print(" <card hidden>")
        print('', self.dealer_hand.cards[1])
        print("\nPlayer's Hand:", *self.player_hand.cards, sep='\n ')

    def player_turn(self):
        while True:
            choice = input("Would you like to Hit or Stand? (h/s): ").lower()
            if choice == 'h':
                self.player_hand.add_card(self.deck.deal())
                self.player_hand.adjust_for_ace()
                print("\nPlayer's Hand:", *self.player_hand.cards, sep='\n ')
                if self.player_hand.is_bust():
                    print("Player busts! Dealer wins.")
                    return False
            elif choice == 's':
                print("Player stands. Dealer's turn.")
                return True

    def dealer_turn(self):
        print("\nDealer's Hand:", *self.dealer_hand.cards, sep='\n ')
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal())
            self.dealer_hand.adjust_for_ace()
            print('', self.dealer_hand.cards[-1])
            if self.dealer_hand.is_bust():
                print("Dealer busts! Player wins.")
                return

        print("Dealer's final hand:", *self.dealer_hand.cards, sep='\n ')

    def compare_hands(self):
        if self.player_hand.value > self.dealer_hand.value:
            print("Player wins!")
        elif self.player_hand.value < self.dealer_hand.value:
            print("Dealer wins!")
        else:
            print("It's a tie!")

    def play(self):
        while True:
            self.player_hand = Hand()
            self.dealer_hand = Hand()
            self.deck = Deck()
            self.deck.shuffle()

            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())

            if self.player_hand.is_blackjack():
                print("Blackjack! Player wins!")
                continue

            self.show_initial_cards()

            if not self.player_turn():
                continue

            self.dealer_turn()

            if not self.dealer_hand.is_bust():
                self.compare_hands()

            play_again = input("\nWould you like to play again? (yes/no): ").lower()
            if play_again != "yes":
                print("Thank you for playing!")
                break

# Run the game
game = BlackjackGame()
game.play()
