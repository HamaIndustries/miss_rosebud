import sys
import pyCardDeck
import asyncio
from typing import List
from pyCardDeck.cards import PokerCard

import roseworks
from backend import profiles
from backend.profiles import Profile

@roseworks.command('exchange', 'exchange [{}/{}] [amount]'.format(Profile.gamble_currency_name, Profile.currency_name), roseworks.CASINO)
async def exchange(client, message):
    userprof = Profile(message.author)
    currency = message.content.split()[1]
    amount = int(message.content.split()[2])

    if amount > userprof.info[currency]:
        await client.send_message(message.channel,
                            'While Lady Luck welcomes all to the Casino, we must insist that--'
                            )
        await client.boss_lady.send_message(message.channel,
                            'YOU\'RE FUCKING POOR LMAO'
                            )
        await asyncio.sleep(2)
        await client.send_message(message.channel,
                            '...'
                            )
        await asyncio.sleep(2)
        await client.send_message(message.channel,
                            'As I was saying, you don\'t have enough {} for that. Your current balance is {}.'.format(currency, userprof.info[currency])
                            )
        return
    if currency == Profile.currency_name:
        if amount < 20:
            client.send_message(message.channel, 'The exchange rate for Lady Luck LLC. chips is 20 kisses : chip, no fractions, minimum 20. Please remember this next time you make use of our facilities.')
            return
        userprof.amend_currency(-(amount-(amount % 20)))
        userprof.amend_currency(amount//20, Profile.gamble_currency_name)
        await client.send_message(message.channel, 'You\'ve exchanged {} {} for {} {}. Have a nice day, and please check back when the tables are opened.'.format(
            amount-(amount%20),
            Profile.currency_name,
            amount//20,
            Profile.gamble_currency_name
            ))
    if currency == Profile.gamble_currency_name:
        userprof.amend_currency(amount*20)
        userprof.amend_currency(-amount, Profile.gamble_currency_name)
        await client.send_message(message.channel, 'You\'ve exchanged {} {} for {} {}. Have a nice day.'.format(
            amount,
            Profile.gamble_currency_name,
            amount*20,
            Profile.currency_name
            ))

class Player:

    def __init__(self, name: str):
        self.hand = []
        self.name = name

    def __str__(self):
        return self.name

class BlackjackGame:
    def __init__(self, players: List[Player], client):
        self.deck = pyCardDeck.Deck()
        self.deck.load_standard_deck()
        self.players = players
        self.scores = {}
        print("Created a game with {} players.".format(len(self.players)))

    def blackjack(self):
        """
        The main blackjack game sequence.
        Each player takes an entire turn before moving on.
        If each player gets a turn and no one has won, the player or players
        with the highest score below 21 are declared the winner.
        """
        print("Setting up...")
        print("Shuffling...")
        self.deck.shuffle()
        print("All shuffled!")
        print("Dealing...")
        self.deal()
        print("\nLet's play!")
        for player in self.players:
            print("{}'s turn...".format(player.name))
            self.play(player)
        else:
            print("That's the last turn. Determining the winner...")
            self.find_winner()

    def deal(self):
        """
        Deals two cards to each player.
        """
        for _ in range(2):
            for p in self.players:
                newcard = self.deck.draw()
                p.hand.append(newcard)
                print("Dealt {} the {}.".format(p.name, str(newcard)))

    def find_winner(self):
        """
        Finds the highest score, then finds which player(s) have that score,
        and reports them as the winner.
        """
        winners = []
        try:
            win_score = max(self.scores.values())
            for key in self.scores.keys():
                if self.scores[key] == win_score:
                    winners.append(key)
                else:
                    pass
            winstring = " & ".join(winners)
            print("And the winner is...{}!".format(winstring))
        except ValueError:
            print("Whoops! Everybody lost!")

    def hit(self, player):
        """
        Adds a card to the player's hand and states which card was drawn.
        """
        newcard = self.deck.draw()
        player.hand.append(newcard)
        print("   Drew the {}.".format(str(newcard)))

    def play(self, player):
        """
        An individual player's turn.
        If the player's cards are an ace and a ten or court card,
        the player has a blackjack and wins.
        If a player's cards total more than 21, the player loses.
        Otherwise, it takes the sum of their cards and determines whether
        to hit or stand based on their current score.
        """
        while True:
            points = sum_hand(player.hand)
            if points < 17:
                print("   Hit.")
                self.hit(player)
            elif points == 21:
                print("   {} wins!".format(player.name))
                sys.exit(0) # End if someone wins
            elif points > 21:
                print("   Bust!")
                break
            else:  # Stand if between 17 and 20 (inclusive)
                print("   Standing at {} points.".format(str(points)))
                self.scores[player.name] = points
                break

def sum_hand(hand: list):
    """
    Converts ranks of cards into point values for scoring purposes.
    'K', 'Q', and 'J' are converted to 10.
    'A' is converted to 1 (for simplicity), but if the first hand is an ace
    and a 10-valued card, the player wins with a blackjack.
    """
    vals = [card.rank for card in hand]
    intvals = []
    while len(vals) > 0:
        value = vals.pop()
        try:
            intvals.append(int(value))
        except ValueError:
            if value in ['K', 'Q', 'J']:
                intvals.append(10)
            elif value == 'A':
                intvals.append(1)  # Keep it simple for the sake of example
    if intvals == [1, 10] or intvals == [10, 1]:
        print("   Blackjack!")
        return(21)
    else:
        points = sum(intvals)
        print("   Current score: {}".format(str(points)))
        return(points)

@roseworks.command('blackjack', 'blackjack [chips]', roseworks.CASINO)
def blackjack(client, message):
    client.send_message(message.channel, 'Check back tomorrow for when I open the tables.')





