import roseworks
from backend.profiles import Profile
from backend import utils
from rosebud_configs import wishid, trans

import discord



@roseworks.command('daily', 'daily', 'money')
async def daily(client, message):
    target = Profile(message.author)
    try:
        if message.author.id == wishid:
            await client.send_message(message.channel, 'Added {} {} to your account, my Queen. Feel free to ask for more. xwu'.format(await target.daily(), Profile.currency_name))
            return
        await client.send_message(message.channel, 'Added {} {} to your account for today!'.format(await target.daily(), Profile.currency_name))
    except utils.TooSoonError as e:
        await client.send_message(message.channel, 'Please wait {:.2f} hours before begging for more {}.'.format(e.waittime.seconds / 3600.0, Profile.currency_name))

@roseworks.command('pay', 'pay [@user]', 'money')
async def pay(client, message):
        payer = Profile(message.author)
        recipient = Profile(message.mentions[0])
        amount = int(message.content.split()[2])
        if payer.id == wishid:
            recipient.amend_currency(amount)
            await client.send_message(message.channel, 'Queen Wishi has amended {}\'s balance by {}{}.'.format(message.author.mention, message.mentions[0].mention, Profile.currency_symbol, amount))
        elif amount <= 0:
            await client.send_message(message.channel, 'You can\'t pay {} idiot {}.'.format(amount, utils.gibberish()))
            return
        elif payer.id == recipient.id:
            await client.send_message(message.channel, 'Trying to defraud me? Nice try idiot.')
            return
        elif message.mentions[0].bot:
            await client.send_message(message.channel, 'You can\'t even buy a bot\'s love, small dick energy cuck.')
            return
        elif payer.get_balance() >= amount:
            payer.amend_currency(-amount)
            recipient.amend_currency(amount)
            await client.send_message(message.channel, '{} has paid {} {}{}'.format(message.author.mention, message.mentions[0].mention, Profile.currency_symbol, amount))
        else:
            await client.send_message(message.channel, 'Insufficient funds, ya broke cuck.')

@roseworks.command('bal', 'bal', 'money')
async def bal(client, message):
    e = discord.Embed(title='{}\'s balance'.format(message.author.name.translate(trans)), description='{}{}'.format(Profile.currency_symbol, Profile(message.author).get_balance()))
    await client.send_message(message.channel, embed=e)
