# -*- coding: utf-8 -*-
import roseworks, rosebud_configs
from rosebud_configs import trans

import discord, random, asyncio

'''
Miscellaneous commands!
'''
@roseworks.command('shakeyshakey', 'shakeyshakey {cat1|cat2|spinda|tortgle}', roseworks.MISC)
async def shakeyshakey(client, message):
    dances = {
            'cat1': 'https://cdn.discordapp.com/attachments/425046327047487500/474442976802897940/image.gif',
            'cat2': 'https://cdn.discordapp.com/attachments/425046327047487500/474443228364537856/fuck_this_pussy_boy.gif',
            'spinda': 'https://play.pokemonshowdown.com/sprites/xyani/spinda.gif',
            'tortgle': 'https://cdn.discordapp.com/attachments/425057165959495690/472646921060876288/received_967505780079985.gif',
            'despato': 'https://cdn.discordapp.com/attachments/425046327047487500/482027890574360576/Untitled.gif'
            }
    try:
        dance = dances[message.content.split()[1]]
    except:
        dance = random.choice(list(dances.values()))
    e = discord.Embed()
    e.set_image(url=dance)
    await client.send_message(message.channel, embed=e)

@roseworks.command('vore', 'vore [@user]', roseworks.MISC)
async def vore(client, message):
    if len(message.mentions) < 1:
        await client.send_message(message.channel, 'please specify a user to vore! ***xvo***')
        return
    target = message.mentions[0]
    if target.id == client.user.id:
        if message.author.id == '352229851576401930': #seth
            await client.send_message(message.channel, '>p<` S-Seth,,')
            await asyncio.sleep(2)
            reverse = 'https://cdn.discordapp.com/attachments/404911687544733698/479716676569399337/image.png'
            await client.send_message(message.channel, embed=discord.Embed().set_image(url=reverse))
            await client.send_message(message.channel, '**how\'s my esophagus feel?**')
        elif message.author.id == rosebud_configs.wishid:
            await client.send_message(message.channel, '**>p<** M-Master~~!!!! I,, I love being inside of you master,, but I\'d rather')
            await asyncio.sleep(2)
            await client.send_message(message.channel, 'Sorry Master, I couldn\'t express my feelings for you into words,,')
        else:
            await client.send_message(message.channel, '>p< Your esophagus is so warm,,')
    else:
        await client.send_message(message.channel, '{} vored {}! I hope they lubed up first. X_O'.format(message.author.mention, target.mention))

@roseworks.command('dancepacito', 'dancepacito', roseworks.MISC)
async def despacito(client, message):
    desp = discord.utils.get(client.get_all_emojis(), name='dancepacito')
    await client.send_message(message.channel, '<a:{}:{}>'.format(desp.name, desp.id))
