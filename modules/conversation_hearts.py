import roseworks, rosebud_configs
from backend import utils

import discord, random, re

'''
Conversations!
'''

wishid = rosebud_configs.wishid
elid = rosebud_configs.elid
trans = rosebud_configs.trans
prefix = rosebud_configs.settings.prefix

@roseworks.conversation()
async def c_wishitell(client, message):
    if message.channel.is_private and message.author.id == wishid:
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
        e = discord.Embed(title=message.author.name.translate(trans), description=message.content)
        if len(message.attachments)>0:
            e.set_image(url=message.attachments[0]['url'])
        elif len(links)>0:
            e.set_image(url=links[0])
        await client.send_message(discord.utils.get(client.get_all_channels(), id='475034267928363019'), embed=e)
        print('wishi to server: {}'.format(message.content.translate(trans)))

@roseworks.command('tellwishi', 'tellwishi {{message}}', 'misc')
async def tellwishi(client, message):
    if message.content.startswith('{}tellwishi'.format(prefix)) and not wishid in [i.id for i in message.server.members]:
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
        e = discord.Embed(title=message.author.name.translate(trans), description=message.content.replace('{}tellwishi'.format(prefix), ''))
        if len(message.attachments)>0:
            e.set_image(url=message.attachments[0]['url'])
        elif len(links)>0:
            e.set_image(url=links[0])
        await client.send_message(await client.get_user_info(elid), embed=e)
        print('{} to wishi: {}'.format(message.author.name.translate(trans), message.content.translate(trans).replace('{}tellwishi'.format(prefix), '')))
    else:
        await client.send_message(message.channel, 'This command only available in servers Queen Wishi is not in! (aka bad servers xvo)')

@roseworks.conversation()
async def converse(client, message):
    if ('WHO\'S YOUR DADDY' in message.content.upper() or 'WHO\'S YOUR BIG DADDY' in message.content.upper()) and message.author.id == wishid:
        await client.send_message(message.channel, "Hoshi!")

    elif message.content.upper().startswith('I MADE') or message.content.upper().startswith('TODAY I'):
        await client.send_message(message.channel, random.choice(['Ooh', utils.gibberish()]))

    elif 'SEX' in message.content.upper() or 'EAR RAPE' in message.content.upper():
        await client.send_message(message.channel, discord.utils.get(client.get_all_emojis(), name='repent'))

    elif 'LOL' in message.content.upper().replace(' ',''):
        await client.add_reaction(message, discord.utils.get(client.get_all_emojis(), name='despacito'))

