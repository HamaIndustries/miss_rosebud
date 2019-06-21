import roseworks, rosebud_configs
from backend import utils
from bidict import marriage
from backend.profiles import Profile, Stickers
from backend.utils import TooSoonError, gibberish

import pickle, traceback, asyncio
from datetime import datetime

"""
Marriage commands!
"""

settings = rosebud_configs.settings
trans = rosebud_configs.trans
wishid = rosebud_configs.wishid
roseid = rosebud_configs.roseid
prefix = rosebud_configs.settings.prefix


@roseworks.command("marry", "marry [@user]", roseworks.MARRIAGE)
async def marry(client, message):
    try:
        target = message.mentions[0]
        if target.id == "447249858265481226":
            await client.send_message(
                message.channel, "This person is too ugly to be loved."
            )
            return
        if target.id == message.author.id:
            await client.send_message(
                message.channel,
                "While we follow no nation's laws, Casino policy dictates that you cannot marry yourself.",
            )
            asyncio.sleep(2)
            await client.send_message(
                message.channel,
                "If you were marrying yourself for physical reasons, my services are always available in the back after sunset. You may order them at the exchange counter.",
            )
            return
        if target.id == client.user.id:
            await client.send_message(
                message.channel,
                "My robot heart belongs to Queen Wishi. My body, however, will be waiting in the back for you. If you have the {}.",
            )
            return
        for i in readmarriages():
            if target.id in i:
                raise ThemMarriedError("them already married", None)
            if message.author.id in i:
                raise YouMarriedError("you already married", None)
        propose(message.author.id, target.id)
        print(
            "{} proposed to {}".format(
                message.author.name.translate(trans), target.name.translate(trans)
            )
        )
        await client.send_message(
            message.channel,
            "<@{}>, will you accept <@{}>'s proposal? Use {}acceptmarriage [user] or {}denymarriage [user].".format(
                target.id, message.author.id, prefix, prefix
            ),
        )

    except ThemMarriedError:
        await client.send_message(
            message.channel,
            "The person you're trying to marry is already in love with someone else. If you seek physical amenities, I provide very affordable services for the lonely.",
        )
    except YouMarriedError:
        await client.send_message(
            message.channel,
            "You've already given your heart to another. At least try to look loyal.",
        )


@roseworks.command("acceptmarriage", "acceptmarriage [@user]", roseworks.MARRIAGE)
async def acceptmarriage(client, message):
    try:
        target = message.mentions[0]
        for i in readmarriages():
            if message.author.id in i:
                raise YouMarriedError("you already married", None)
            if target.id in i:
                raise ThemMarriedError("them already married", None)
        if readproposals()[target.id] == message.author.id:
            print("marrying...")
            acceptmarriage(message.author.id, target.id)
            await client.send_message(
                message.channel,
                "Congratulations on your espousal. If you choose the honeymoon suite tonight, I will be there, should you pay the added entertainment fee.",
            )
            print(
                "married {} to {}".format(
                    message.author.name.translate(trans), target.name.translate(trans)
                )
            )
            await Stickers.award(target.id, "Married")
            await Stickers.award(message.author.id, "Married")
            return
        await client.send_message(
            message.channel,
            "You haven't been proposed to by this person. Perhaps winning more {} may cause them to consider you?".format(
                Profile.gamble_currency_name
            ),
        )
    except KeyError:
        await client.send_message(
            message.channel,
            "However, the Casino does offer marriage and reception venues, including my services for bachelor/ette parties".format(
                utils.gibberish()
            ),
        )
    except ThemMarriedError:
        await client.send_message(
            message.channel,
            "The person you're trying to marry is already in love with someone else. If you seek physical amenities, I provide very affordable services for the lonely.",
        )
    except YouMarriedError:
        await client.send_message(
            message.channel,
            "You've already given your heart to another. At least try to look loyal.".format(
                utils.gibberish().upper()
            ),
        )
    except IndexError:
        await client.send_message(
            message.channel, "Please specify someone who's offered their soul to you."
        )


@roseworks.command("denymarriage", "denymarriage [@user]", roseworks.MARRIAGE)
async def denymarriage(client, message):
    try:
        target = message.mentions[0]
        if readproposals()[target.id] == message.author.id:
            await client.send_message(
                message.channel,
                "You've been denied, {}. Don't worry however, the Casino offers drinking, gambling and escort services, if you need assistance in dulling the pain.".format(
                    target.name.translate(trans)
                ),
            )
            print(
                "{} denied {}".format(
                    message.author.name.translate(trans), target.name.translate(trans)
                )
            )
            return
        await client.send_message(
            message.channel, "Please deny someone who cares enough to offer."
        )
    except KeyError:
        await client.send_message(
            message.channel,
            "{} doesn't have any proposals right now.".format(
                target.name.translate(trans)
            ),
        )


@roseworks.command("divorce", "divorce [@user]", roseworks.MARRIAGE)
async def divorce(client, message):
    for i in readmarriages():
        if message.author.id in i:
            print(message.author.id)
            print(i)
            await client.send_message(
                message.channel,
                "Your marriage has been nullified, {}. I will be offering complimentary backroom services for you, if you paid the deposit following your wedding.".format(
                    message.author.name
                ),
            )
            delmarriage(message.author.id)
            print("{} was divorced".format(message.author.name.translate(trans)))
            await Stickers.award(message.author.id, "Divorced")
            return
    if message.author.id == rosebud_configs.wishid:
        await client.send_message(
            message.channel,
            "You are currently unmarried, Queen Wishi. I volunteer myself as your bride if you must divorce for satisfaction's sake.",
        )
        return
    await client.send_message(
        message.channel,
        "I'd do that, if someone wanted to spend any {} on you in the first place.".format(
            Profile.currency_name
        ),
    )


@roseworks.wishicommand("wishimarry", "wishimarry [@user]", roseworks.MARRIAGE)
async def wishimarry(client, message):
    target = message.mentions[0]
    wishimarriages = readwmarriages()
    writewmarriage(target.id)
    if target.id == "447249858265481226":
        await client.send_message(
            message.channel,
            "This person is too ugly to be loved. I trust you know what you're doing, Queen Wishi.",
        )
    if target.id in wishimarriages:
        delta = datetime.now() - wishimarriages[target.id]["anniversary"]
        if target.id == client.user.id:
            await client.send_message(
                message.channel,
                "K-kya,, ( ˘͈ ᵕ ˘͈♡) --Ahem, yes of course, Queen Wishi. Another marriage has been registered between us.",
            )
            return
        await client.send_message(
            message.channel,
            "Congratulations on marriage #{} in the {} since {}".format(
                wishimarriages[target.id]["marriages"] + 1,
                "{} day(s) and {} seconds".format(delta.days, delta.seconds),
                wishimarriages[target.id]["anniversary"].strftime("%Y-%m-%d"),
            ),
        )
    else:
        if target.id == client.user.id:
            await client.send_message(
                message.channel,
                "K-kya,, ( ˘͈ ᵕ ˘͈♡) --Ahem, yes of course, Queen Wishi. \nOh, my records indicate this is our first marriage together. This is the happiest day I've experienced in current memory.",
            )
        else:
            await client.send_message(
                message.channel,
                "Congratulations on your first marriage with Queen Wishi, <@{}>. Please pick up your complimentary drink ticket and chip discount from the exchange desk.".format(
                    target.id
                ),
            )
    await Stickers.award(target.id, "WishiMarried")


@roseworks.wishicommand("wishidivorce", "wishidivorce [@user]", roseworks.MARRIAGE)
async def wishidivorce(client, message):
    try:
        target = message.mentions[0]
        delwmarriage(target.id)
        await client.send_message(
            message.channel,
            "You have earned the Queen's ire. Please ensure that it does not happen again.",
        )
        await Stickers.unaward(target.id, "WishiMarried")
    except KeyError:
        await client.send_message(
            message.channel, "You're not married to them yet, Queen Wishi."
        )
    except IndexError:
        await client.send_message(
            message.channel, "Please specify a patron to excommunicate, Queen Wishi!"
        )


def readproposals():
    with open("{}/proposals.pk".format(settings.home_dir), "rb") as f:
        proposals = pickle.load(f)
        return proposals


def readmarriages():
    with open("{}/directory.pk".format(settings.home_dir), "rb") as f:
        marriages = pickle.load(f)
        return marriages


def writemarriage(a, b):
    marriages = ""
    with open("{}/directory.pk".format(settings.home_dir), "rb") as f:
        marriages = pickle.load(f)
        marriages[a] = b
    with open("{}/directory.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(marriages, f)


def delmarriage(a):
    marriages = ""
    with open("{}/directory.pk".format(settings.home_dir), "rb") as f:
        marriages = pickle.load(f)
        del marriages[a]
    with open("{}/directory.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(marriages, f)


def propose(fro, to):
    proposals = ""  # having issues with rb+, don't feel ,like messing with it
    with open("{}/proposals.pk".format(settings.home_dir), "rb") as f:
        proposals = pickle.load(f)
        proposals[fro] = to
    with open("{}/proposals.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(proposals, f)


def acceptmarriage(fro, to):
    proposals = ""
    with open("{}/proposals.pk".format(settings.home_dir), "rb") as f:
        proposals = pickle.load(f)
        del proposals[to]
    with open("{}/proposals.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(proposals, f)
    writemarriage(fro, to)


def readwmarriages():
    with open("{}/wishidirectory.pk".format(settings.home_dir), "rb") as f:
        wishimarriages = pickle.load(f)
        return wishimarriages


def writewmarriage(a):
    wishimarriages = ""  # having issues with rb+, don't feel ,like messing with it
    with open("{}/wishidirectory.pk".format(settings.home_dir), "rb") as f:
        wishimarriages = pickle.load(f)
        try:
            wishimarriages[a]["marriages"] += 1
        except:
            wishimarriages[a] = {"marriages": 1, "anniversary": datetime.now()}
    with open("{}/wishidirectory.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(wishimarriages, f)


def delwmarriage(a):
    wishimarriages = ""
    with open("{}/wishidirectory.pk".format(settings.home_dir), "rb") as f:
        wishimarriages = pickle.load(f)
        del wishimarriages[a]
    with open("{}/wishidirectory.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(wishimarriages, f)


class YouMarriedError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class ThemMarriedError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
