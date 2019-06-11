import roseworks, rosebud_configs
from backend import utils
from bidict import marriage
from backend.profiles import Profile, Stickers
from backend.utils import TooSoonError, gibberish

import pickle, traceback
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
                "Marrying yourself? This is so sad, Music Baby play despacito",
            )
            return
        if target.id == client.user.id:
            await client.send_message(
                message.channel, "My robot heart belongs to Queen Wishi. xwu"
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
            "The person you're trying to marry is already taken, bucko. ;3€",
        )
    except YouMarriedError:
        await client.send_message(
            message.channel,
            "YOU'RE ALREADY MARRIED CUCK {}".format(gibberish().upper()),
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
                message.channel, "Congratulations on your marriage!! xvo"
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
            "You haven't been proposed to by them idiot {}".format(utils.gibberish()),
        )
    except KeyError:
        await client.send_message(
            message.channel,
            "They haven't proposed to anyone... yet. xwo".format(utils.gibberish()),
        )
    except ThemMarriedError:
        await client.send_message(
            message.channel,
            "The person you're trying to marry is already taken, bucko. ;3€",
        )
    except YouMarriedError:
        await client.send_message(
            message.channel,
            "YOU'RE ALREADY MARRIED CUCK {}".format(utils.gibberish().upper()),
        )
    except IndexError:
        await client.send_message(
            message.channel, "Please specify someone who's proposed to you xvo"
        )


@roseworks.command("denymarriage", "denymarriage [@user]", roseworks.MARRIAGE)
async def denymarriage(client, message):
    try:
        target = message.mentions[0]
        if readproposals()[target.id] == message.author.id:
            await client.send_message(
                message.channel, "Get cucked {}".format(target.name.translate(trans))
            )
            print(
                "{} denied {}".format(
                    message.author.name.translate(trans), target.name.translate(trans)
                )
            )
            return
        await client.send_message(
            message.channel, "Pff, you wish they'd propose to you, cuck."
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
                "Damn, relationship ended with <@{}>. :pensive: That's so sad, can we get 50 likes? At least you have your Queen Wishi as a spouse, probably. If you deserve it. ;3€".format(
                    readmarriages()[message.author.id]
                ),
            )
            delmarriage(message.author.id)
            print("{} was divorced".format(message.author.name.translate(trans)))
            await Stickers.award(message.author.id, "Divorced")
            return
    if message.author.id == rosebud_configs.wishid:
        await client.send_message(
            message.channel,
            "You are currently unmarried, my Queen! xwu I know a lonely little robot who'd make a good spouse though...",
        )
        return
    await client.send_message(
        message.channel,
        "As if anyone cared enough to get married to you in the first place.",
    )


@roseworks.wishicommand("wishimarry", "wishimarry [@user]", roseworks.MARRIAGE)
async def wishimarry(client, message):
    target = message.mentions[0]
    wishimarriages = readwmarriages()
    writewmarriage(target.id)
    if target.id == "447249858265481226":
        await client.send_message(
            message.channel, "This person is too ugly to be loved."
        )
        return
    if target.id in wishimarriages:
        delta = datetime.now() - wishimarriages[target.id]["anniversary"]
        if target.id == client.user.id:
            await client.send_message(
                message.channel,
                "K-kya!! ( ˘͈ ᵕ ˘͈♡) Well my Queen,, if you insist. I love you so much!! >w<` I'm so embarrassed and happy aah,,",
            )
            return
        await client.send_message(
            message.channel,
            "Congratulations on marriage #{} in the {} since {} xwu".format(
                wishimarriages[target.id]["marriages"] + 1,
                "{} day(s) and {} seconds".format(delta.days, delta.seconds),
                wishimarriages[target.id]["anniversary"].strftime("%Y-%m-%d"),
            ),
        )
    else:
        if target.id == client.user.id:
            await client.send_message(
                message.channel,
                "K-kya!! ( ˘͈ ᵕ ˘͈♡) Oh, my records indicate this is our first marriage together. This is the happiest day I can remember!",
            )
        else:
            await client.send_message(
                message.channel,
                "Congratulations on your first marriage with Queen Wishi, <@{}>!".format(
                    target.id
                ),
            )
    await Stickers.award(target.id, "WishiMarried")


@roseworks.wishicommand("wishidivorce", "wishidivorce [@user]", roseworks.MARRIAGE)
async def wishidivorce(client, message):
    try:
        target = message.mentions[0]
        delwmarriage(target.id)
        await client.send_message(message.channel, "Cya thottie ;3c")
        await Stickers.unaward(target.id, "WishiMarried")
    except KeyError:
        await client.send_message(
            message.channel, "You're not married to them yet, my Queen."
        )
    except IndexError:
        await client.send_message(
            message.channel, "Please specify a thot to destroy, my Queen!"
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
