import functools
import sys
import pyCardDeck
import asyncio
import discord
import random
from typing import List

from PIL import Image
from pyCardDeck.cards import PokerCard

import roseworks
from backend import profiles
from backend.profiles import Profile
from backend.utils import send_image

symbols = ["❤", "♣", "♠", "♦", "♢", "♤", "♧", "♡"]


def rsym():
    return random.choice(symbols)


class Pot:
    def __init__(self):
        self.pot = 0

    def jack(self, mon=None):
        if not mon:
            ret = self.pot
            self.pot = 0
            return ret
        self.pot += mon / 2
        return mon / 2


@roseworks.command(
    "exchange",
    "exchange [{}/{}] [amount]".format(
        Profile.gamble_currency_name, Profile.currency_name
    ),
    roseworks.CASINO,
)
async def exchange(client, message):
    userprof = Profile(message.author)
    currency = message.content.split()[1]
    amount = int(message.content.split()[2])

    if amount > userprof.info[currency]:
        await client.send_message(
            message.channel,
            "While Lady Luck welcomes all to the Casino, we must insist that--",
        )
        await client.boss_lady.send_message(message.channel, "YOU'RE FUCKING POOR LMAO")
        await asyncio.sleep(2)
        await client.send_message(message.channel, "...")
        await asyncio.sleep(2)
        await client.send_message(
            message.channel,
            "As I was saying, you don't have enough {} for that. Your current balance is {}.".format(
                currency, userprof.info[currency]
            ),
        )
        return
    if currency == Profile.currency_name:
        if amount < 20:
            client.send_message(
                message.channel,
                "The exchange rate for Lady Luck LLC. chips is 20 kisses : chip, no fractions, minimum 20. Please remember this next time you make use of our facilities.",
            )
            return
        userprof.amend_currency(-(amount - (amount % 20)))
        userprof.amend_currency(amount // 20, Profile.gamble_currency_name)
        await client.send_message(
            message.channel,
            "You've exchanged {} {} for {} {}. Have a nice day, and please check back when the tables are opened.".format(
                amount - (amount % 20),
                Profile.currency_name,
                amount // 20,
                Profile.gamble_currency_name,
            ),
        )
    if currency == Profile.gamble_currency_name:
        userprof.amend_currency(amount * 20)
        userprof.amend_currency(-amount, Profile.gamble_currency_name)
        await client.send_message(
            message.channel,
            "You've exchanged {} {} for {} {}. Have a nice day.".format(
                amount, Profile.gamble_currency_name, amount * 20, Profile.currency_name
            ),
        )


class Machine:
    offset_mid = 191
    offset_right = 191 * 2

    def __init__(self):
        self.pot = Pot()
        # I'm bad at statistics, Lady Luck forgive me
        self.modifiers = {
            "flower": (range(1, 300), self.pot.jack, "Better luck next time."),
            "cherry": (range(300, 450), lambda x: x * 1, "Your money's safe at least."),
            "blueberry": (range(450, 650), lambda x: x * 2, "Double or nothing!"),
            "raspberry": (range(650, 672), lambda x: x * 8, "8x 🎉🎉🎉"),
            "strawberry": (range(672, 678), lambda x: x * 16, "16x? Two 8s. xwo"),
            "peach": (
                range(678, 680),
                lambda x: x * 78,
                "Peach time??? X_O I- Uh, let me count that out again...",
            ),
            "tada": (
                range(680, 681),
                lambda x: self.pot.jack(),
                "Jackpot! feel free to pick up the second half of your prize in the back rooms. ;3€",
            ),
        }

    def run_odds(self, cost):
        roll = int(random.random() * 800)
        for symbol, (odds, func, reaction) in self.modifiers.items():
            if roll in odds:
                return symbol, int(func(cost)), reaction
        return None, 0, "Lady Luck's not around it seems, care to try again?"


mach = Machine()


@roseworks.command("slots", "slots [amount]", roseworks.CASINO)
async def slots(client, message):
    userprof = Profile(message.author)

    # TODO in 2.0: auto check/withdraw in user class.
    bet_amount = int(message.content.split()[1])
    if bet_amount > userprof.info[Profile.gamble_currency_name]:
        await client.send_message(
            message.channel,
            "I'm afraid you haven't that many {} to spend. Feel free to exchange with me if you must supplement your enjoyment.".format(
                Profile.gamble_currency_name
            ),
        )
        return
    elif bet_amount <= 0:
        await client.send_message(
            message.channel,
            "Not to be rude, but all possible attempts to defraud the Casino are reported directly to Queen wishi",
        )
        return

    userprof.amend_currency(-bet_amount, typ=Profile.gamble_currency_name)
    symbol, ret_amount, resp = mach.run_odds(bet_amount)

    if symbol:
        symbols = [f"resources/slots/{symbol}.png" for _ in range(3)]
        userprof.amend_currency(ret_amount, typ=Profile.gamble_currency_name)
    else:
        rand_syms = list(mach.modifiers.keys())
        symbols = [f"resources/slots/{random.choice(rand_syms)}.png" for _ in range(3)]

    im = await asyncio.get_event_loop().run_in_executor(
        None, functools.partial(render_slots, symbols)
    )
    await client.send_message(message.channel, f"{resp}\n(won {ret_amount} chips)")
    await send_image(im, client, message.channel)


def render_slots(symbols):
    with Image.open("resources/slots/machine.png") as backg:
        for i in range(3):
            with Image.open(symbols[i]) as symbol:
                new_l = Image.new("RGBA", symbol.size)
                new_l.paste(symbol, (195 * i, 0), symbol)
                # symbol = symbol.transform(symbol.size, Image.AFFINE, ())
                backg = Image.alpha_composite(backg, new_l)
                # backg.paste(symbol, (195 * i, 0), symbol)
        return backg.copy()

    # userprof.amend_currency(amount)


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
                sys.exit(0)  # End if someone wins
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
            if value in ["K", "Q", "J"]:
                intvals.append(10)
            elif value == "A":
                intvals.append(1)  # Keep it simple for the sake of example
    if intvals == [1, 10] or intvals == [10, 1]:
        print("   Blackjack!")
        return 21
    else:
        points = sum(intvals)
        print("   Current score: {}".format(str(points)))
        return points


"""
@roseworks.command('blackjack', 'blackjack [chips]', roseworks.CASINO)
def blackjack(client, message):
    client.send_message(message.channel, 'later for when I open the tables.')

"""
