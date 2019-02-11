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

''' temporarily taken out
@roseworks.conversation()
async def c_wishitell(client, message):
    if message.channel.is_private and message.author.id == wishid:
        await client.send_message(client.get_channel('475034267928363019'), embed=embed_message(message))
        print('wishi to server: {}'.format(message.content.translate(trans)))
'''


'''for independent rosebud interaction
@roseworks.conversation()
async def c_dm(client, message):
    if message.channel.is_private and not message.author.bot:
        if len(message.attachments)>0:
            await client.send_message(discord.utils.get(client.get_all_members(), id=elid), content='{} sent {}'.format(message.author.name.translate(trans), message.attachments[0]['url']))
        print('==={}( {} ): {}'.format(message.author.name.translate(trans),message.author.id, '[image]' if message.content == '' else message.content.translate(trans)))
'''

dmchannel = '542545218780528640'
moonlit_casino = '527951672903729154'
moonlit_output = '542571277454671875'
general_convo = '542600309134852096'

class Channellistener:
    listen_channel = ''

def is_error(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        return False
    except:
        return True

@roseworks.conversation()
async def c_communicate(client, message):
    async def display_message(channelid, message_type = 'Message'):
        e = discord.Embed()
        e.set_author(name=message.author.name, icon_url = message.author.avatar_url if not message.author.avatar_url == "" else message.author.default_avatar_url)
        e.add_field(name=message_type, value='[image]' if message.content == '' else message.content)

        if len(message.attachments)>0:
            e.set_image(url=message.attachments[0]['url'])
        await client.send_message(client.get_channel(channelid), content=message.author.id, embed=e)

    async def reply_message(inp):
        reply = inp.split(' ', maxsplit=1)
        target = discord.utils.get(client.get_all_members(), id=reply[0])
        if target == None:
            target = discord.utils.get(client.get_all_channels(), id=reply[0])
            if target == None:
                raise AttributeError
        await client.send_message(target, content=reply[1])
        print('==='+client.user.name+' to {} ( {} ): '.format(target.name.translate(trans), reply[0])+reply[1])

    if message.channel.is_private and not message.author.bot:
        await display_message(dmchannel)
        print('==={}( {} ): {}'.format(message.author.name.translate(trans), message.author.id, '[image]' if message.content == '' else message.content.translate(trans)))

    elif message.channel.id == moonlit_output and not message.author.bot:
        await reply_message(moonlit_casino + " " + message.content)

    elif (message.channel.id == general_convo or message.channel.id == dmchannel) and not message.author.bot:
        try:
            await reply_message(message.content)
            await client.delete_message(message)
            reply = message.content.split(' ', maxsplit=1)
            e = discord.Embed()
            e.set_author(name = client.user.name, icon_url = client.user.avatar_url)
            e.add_field(name='Message to {}'.format(client.get_user_info(reply[0]).name), value=reply[1])
            await client.send_message(message.channel, embed=e)
        except AttributeError:
            ...

    elif message.channel.id == Channellistener.listen_channel and not message.author.bot:
        await display_message(general_convo)

@roseworks.secretcommand(name='setlisten')
async def setlisten(client, message):
    Channellistener.listen_channel = message.content.split(' ')[1]

@roseworks.command('tellwishi', 'tellwishi {message}', roseworks.MISC)
async def tellwishi(client, message):
    if message.content.startswith('{}tellwishi'.format(prefix)) and not wishid in [i.id for i in message.server.members]:
        await client.send_message(await client.get_user_info(wishid), embed=embed_message(message))
        print('{} to wishi: {}'.format(message.author.name.translate(trans), message.content.translate(trans).replace('{}tellwishi'.format(prefix), '')))
    else:
        await client.send_message(message.channel, 'This command is only available in servers Queen Wishi is not in.')

@roseworks.conversation()
async def converse(client, message):
    if ('WHO\'S YOUR DADDY' in message.content.upper() or 'WHO\'S YOUR BIG DADDY' in message.content.upper()) and message.author.id == wishid:
        await client.send_message(message.channel, "Queen Wishi.")

    elif message.content.upper().startswith('I MADE') or message.content.upper().startswith('TODAY I'):
        await client.send_message(message.channel, random.choice(['How interesting.', 'I see.', 'Fascinating.']))

    elif 'LOL' in message.content.upper().replace(' ',''):
        await client.add_reaction(message, discord.utils.get(client.get_all_emojis(), name='despacito'))

    elif re.search(">KISS.+ROSEBUD", message.content.upper()):
        await client.send_message(message.channel, '>kiss '+message.author.mention)


def embed_message(message):
    links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
    e = discord.Embed(title=message.author.name.translate(trans), description=message.content)
    if len(message.attachments)>0:
        e.set_image(url=message.attachments[0]['url'])
    elif len(links)>0:
        e.set_image(url=links[0])
    return e

