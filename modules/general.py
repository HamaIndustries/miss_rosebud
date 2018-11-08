import roseworks, rosebud_configs
from backend.profiles import Profile, Stickers
from backend import utils
from rosebud_configs import trans, elid, wishid

import discord

prefix = rosebud_configs.settings.prefix

@roseworks.command('profile', 'profile {@user}', roseworks.GENERAL)
async def profile(client, message):
    if len(message.mentions) > 0:
        target = message.mentions[0]
    else:
        target = message.author

    await client.send_message(message.channel, embed=await Profile(target).get_card_plaintext(client))

@roseworks.command('invite', 'invite', roseworks.GENERAL)
async def invite(client, message):
    info = await client.application_info()
    await client.send_message(message.channel, discord.utils.oauth_url(info.id, permissions=discord.Permissions(permissions=388163)))

@roseworks.secretcommand('bitch')
async def baka(client, message):
    with open('watashipasta.txt', 'r') as f:
        await client.send_message(message.channel, f.read())

@roseworks.secretcommand('test')
async def test(client, message):
    await client.send_message(message.channel, 'hi')
    await Stickers.award(message.author.id, 'SecretHunter')

@roseworks.secretcommand('bitter?')
async def bitter(client, message):
    await client.send_message(message.channel, random.choice('It doesn\'t matter.|No I\'m fine xvu'.split('|')))
    await Stickers.award(message.author.id, 'SecretHunter')

@roseworks.secretcommand('gibberish')
async def gibberish(client, message):
    await client.send_message(message.channel, utils.gibberish())
    await Stickers.award(message.author.id, 'SecretHunter')

@roseworks.secretcommand('miss')
async def miss(client, message):
    await client.send_message(message.channel, 'I miss {} :\'('.format(message.content.split(maxsplit=1)[1]))
    await Stickers.award(message.author.id, 'SecretHunter')

@roseworks.secretcommand('pokemon')
async def pokemon(client, message):
    #https://cdn.discordapp.com/attachments/467397772044271617/471404564365705236/1532444999442.png
    emb = discord.Embed(title='A wild pokémon has appeared!',description='Guess the pokémom and type p!catch <pokémon> to catch it!', color=0xffd1dc)
    emb.set_image(url='https://cdn.discordapp.com/attachments/467397772044271617/471404564365705236/1532444999442.png')
    await client.send_message(message.channel, embed=emb)
    await Stickers.award(message.author.id, 'SecretHunter')

@roseworks.secretcommand('catch wishi')
async def pokecatch(client, message):
    await client.send_message(message.channel, 'Congratulations {}! You caught a level 78 Wishi!'.format(message.author.mention))

@roseworks.secretcommand('nayth')
async def nayth(client, message):
    if not message.author.id == elid and not message.author.id == wishid:
        return
    for member in message.server.members:
        try:
            await client.change_nickname(member, 'nayth')
            print('--------- {}'.format(member.name.translate(trans)))
        except:
            print('skipped {}'.format(member.name.translate(trans)))

@roseworks.secretcommand('nay')
async def nay(client, message):
    if not message.author.id == elid and not message.author.id == wishid:
        return
    for member in message.server.members:
        if member.bot:
            try:
                await client.change_nickname(member, None)
                print('--------- {}'.format(member.name.translate(trans)))
            except:
                print('skipped {}'.format(member.name.translate(trans)))
