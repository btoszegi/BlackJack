from collections import namedtuple
from itertools import product
from random import shuffle

Card = namedtuple('Card', ('rank', 'suit'))


class Deck:
    card_ranks = []
    card_suits = []

    def __init__(self):
        self.cards = []
        self.refresh_deck()

    def refresh_deck(self):
        self.cards = list(map(lambda x: Card(x[0],x[1]), product(self.card_ranks, self.card_suits)))

    def shuffle(self):
        shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()


class FrenchDeck(Deck):
    card_ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    card_suits = ['♥', '♠', '♣', '♦']


class BlackjackGame:
    def __init__(self, deck: FrenchDeck, balance):
        self.deck = deck
        self.balance = balance
        self.player_cards = []
        self.bank_cards = []
        self.player_dealt_cards = 0


    def card_value(self, card, current_hand_value):
        if card.rank == "Ace":
            if current_hand_value + 11 <= 21:
                return 11
            else:
                return 1
        elif card.rank in ["J","Q","K"]:
            return 10
        else:
            return int(card.rank)


    def hand_value(self, hand):
        current_hand_value = 0
        if type(hand) == Card:
            return self.card_value(hand, current_hand_value)
        else:
            for card in hand:
                current_hand_value += self.card_value(card, current_hand_value)
            return current_hand_value


    def deal_card_to_player(self):
        self.deck.shuffle()
        self.player_cards.append(self.deck.draw_card())
        self.player_dealt_cards += 1


    def deal_card_to_bank(self):
        self.deck.shuffle()
        self.bank_cards.append(self.deck.draw_card())


    def show_hand(self, cards):
        hand = ""
        if type(cards) == Card:
            return cards.rank + cards.suit
        else:
            for card in cards:
                hand += card.rank+card.suit+" "
            return hand


    def evaluate(self, bet):
        self.bank_play()

        if self.player_dealt_cards >= 5 and self.hand_value(self.player_cards) <= 21:
            prize = 1.5*bet
            self.balance += prize
            print("Congratulations, you won!")
            print(f"You won: {prize} credit, your balance is now: {self.balance} credit.")
        elif self.hand_value(self.bank_cards) > 21 and self.hand_value(self.player_cards) <= 21:
            prize = 2 * bet
            self.balance += prize
            print("Congratulations, you won!")
            print(f"You won: {prize} credit, your balance is now: {self.balance} credit.")

        elif (self.hand_value(self.player_cards) > 21 or (self.hand_value(self.bank_cards) > self.hand_value(self.player_cards) and self.hand_value(self.bank_cards) <= 21)):
            print("You lost!")
            print(f"Your balance is now: {self.balance} credit.")
        else:
            self.balance+=bet
            print(f"It's a tie! You get your bet back.")
            print(f"Your balance is now: {self.balance} credit.")



    def player_play(self):
        while (self.hand_value(self.player_cards) < 21 and self.player_dealt_cards < 5 and input("Do you want to see the next card? (Y/N)").lower() == "y"):
            self.deal_card_to_player()
            print(f"Your new card: {self.player_cards[-1].rank}{self.player_cards[-1].suit}")
            print(f"Your cards: {self.show_hand(self.player_cards)} Value of your cards: {self.hand_value(self.player_cards)}")


    def bank_play(self):
        print(f"Bank's hand': {self.show_hand(self.bank_cards)} Value of the cards: {self.hand_value(self.bank_cards)}")
        while (self.hand_value(self.bank_cards) < self.hand_value(self.player_cards) and self.hand_value(self.bank_cards) <= 21):
            self.deal_card_to_bank()
            print(f"Bank draw: {self.show_hand(self.bank_cards[-1])}")
        print(f"Bank's hand': {self.show_hand(self.bank_cards)} Value of the cards: {self.hand_value(self.bank_cards)}")
        return self.hand_value(self.bank_cards)


    def replay(self):
        choice = input("New game? (Y/N)").lower()
        if choice == "y":
            return True
        else:
            return False

    def play(self):
        rematch = True
        print("Welcome!")
        while(rematch == True):

            self.deck.refresh_deck()
            self.deck.shuffle()
            self.player_cards = []
            self.bank_cards = []
            self.player_dealt_cards = 0


            print(f"Balance: {self.balance} credit")
            bet = int(input("Place your bet: "))
            while(self.balance - bet < 0):
                print("You don't have enough credit.")
                bet = int(input("Place your bet: "))
            self.balance -= bet
            print("Dealing cards...")
            self.deal_card_to_player()
            self.deal_card_to_bank()
            self.deal_card_to_player()
            self.deal_card_to_bank()

            print(f"Bank's first card: {self.show_hand(self.bank_cards[0])} Card's value: {self.hand_value(self.bank_cards[0])}")
            print(f"Your cards: {self.show_hand(self.player_cards)} Value of your cards: {self.hand_value(self.player_cards)}")
            if self.hand_value(self.player_cards) == 21:
                print("BLACKJACK!! Congratulation!")
                prize = 2.5 * bet
                self.balance += prize
                print(f"You won: {prize} credit, your balance is now: {self.balance} credit.")
            elif self.hand_value(self.bank_cards) == 21:
                print("Bank got BlackJack, you lost.")
                print(f"Bank's first two cards: {self.show_hand(self.bank_cards[0])} Value of the cards: {self.hand_value(self.bank_cards[0])}")
            else:
                self.player_play()
                self.evaluate(bet)

            if self.balance == 0:
                print("You don't have any credit left.")
                rematch = False
            else:
                rematch = self.replay()
        print(f"Balance: {self.balance}")
        print("Thank you for the game!")

if __name__ == "__main__":
    game = BlackjackGame(FrenchDeck(), 1000)
    game.play()
