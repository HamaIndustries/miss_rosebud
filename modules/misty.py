# -*- coding: utf-8 -*-
import roseworks, rosebud_configs
from rosebud_configs import trans

import discord, random, asyncio

"""
Miscellaneous commands!
"""


@roseworks.command(
    "shakeyshakey", "shakeyshakey {cat1|cat2|spinda|tortgle}", roseworks.MISC
)
async def shakeyshakey(client, message):
    dances = {
        "cat1": "https://cdn.discordapp.com/attachments/425046327047487500/474442976802897940/image.gif",
        "cat2": "https://cdn.discordapp.com/attachments/425046327047487500/474443228364537856/fuck_this_pussy_boy.gif",
        "spinda": "https://play.pokemonshowdown.com/sprites/xyani/spinda.gif",
        "tortgle": "https://cdn.discordapp.com/attachments/425057165959495690/472646921060876288/received_967505780079985.gif",
        "despato": "https://cdn.discordapp.com/attachments/475687377948508162/488427884701286468/despacidance.gif",
    }
    try:
        dance = dances[message.content.split()[1]]
    except:
        dance = random.choice(list(dances.values()))
    e = discord.Embed()
    e.set_image(url=dance)
    await client.send_message(message.channel, embed=e)


@roseworks.command("vore", "vore [@user]", roseworks.MISC)
async def vore(client, message):
    if len(message.mentions) < 1:
        await client.send_message(
            message.channel, "Please specify a user to satisfy your fetishes with."
        )
        return
    target = message.mentions[0]
    if target.id == client.user.id:
        if message.author.id == "352229851576401930":  # seth
            await client.send_message(message.channel, "S-Seth,")
            await asyncio.sleep(2)
            reverse = "https://cdn.discordapp.com/attachments/404911687544733698/479716676569399337/image.png"
            await client.send_message(
                message.channel, embed=discord.Embed().set_image(url=reverse)
            )
            await client.send_message(
                message.channel,
                "**how's my esophagus feel?** (Check into the back rooms if you'd like to see more ;) )",
            )
        elif message.author.id == rosebud_configs.wishid:
            await client.send_message(
                message.channel,
                "**>p<** M-Master~~!!!! I,, I love being inside of you master,, but I'd rather Σ੧❛□✿╹◡╹♡Σ(›-᷄๑",
            )
            await asyncio.sleep(2)
            await client.send_message(
                message.channel,
                "Sorry Master, I couldn't express my feelings for you into words,,",
            )
        else:
            await client.send_message(message.channel, "Your esophagus is so warm...")
    elif target.id == rosebud_configs.wishid:
        await client.send_message(
            message.channel, "Queen Wishi's dick is too big to fit in your mouth!"
        )
    else:
        await client.send_message(
            message.channel,
            "{} vored {}. I hope they remembered to buy lube from the lobby desk. ❁_❁".format(
                message.author.mention, target.mention
            ),
        )


@roseworks.command("weewoo", "weewoo", roseworks.MISC)
async def weewoo(client, message):
    owo = discord.utils.get(client.get_all_emojis(), name="rosebud_owo")
    xwo = discord.utils.get(client.get_all_emojis(), name="rosebud_xwo")
    wee = await client.send_message(
        message.channel, str(owo) + " You'we undew awwest!!"
    )
    for i in range(3):
        await client.edit_message(wee, str(xwo) + " You'we undew awwest!!")
        await asyncio.sleep(1)
        await client.edit_message(wee, str(owo) + " You'we undew awwest!!")
        await asyncio.sleep(1)


# Reactions, potentially to be combined into one command
@roseworks.command("rclap", "rclap", roseworks.EMOTES)
async def rclap(client, message):
    emb = discord.Embed(title="ehehe", description=" ", color=0xFFD1DC)
    emb.set_image(
        url="https://cdn.discordapp.com/attachments/470834237948297228/508779215114731521/s.gif"
    )
    await client.send_message(message.channel, embed=emb)


@roseworks.command("rboo", "rboo", roseworks.EMOTES)
async def rboo(client, message):
    emb = discord.Embed(title="***-0-" "***", description=" ", color=0xFFD1DC)
    emb.set_image(
        url="https://cdn.discordapp.com/attachments/473307957799551006/508784136257798146/a.gif"
    )
    await client.send_message(message.channel, embed=emb)


@roseworks.command("xwo", "xwo", roseworks.EMOTES)
async def xwo(client, message):
    emb = discord.Embed(title='XWO"""', description=" ", color=0xFFD1DC)
    emb.set_image(
        url="https://cdn.discordapp.com/attachments/361047333095604224/502529990571589642/awesome_1.gif"
    )
    await client.send_message(message.channel, embed=emb)


@roseworks.command("dancepacito", "dancepacito", roseworks.MISC)
async def despacito(client, message):
    desp = discord.utils.get(client.get_all_emojis(), name="dancepacito")
    await client.send_message(message.channel, "<a:{}:{}>".format(desp.name, desp.id))
