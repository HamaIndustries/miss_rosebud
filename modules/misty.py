import roseworks

import discord, random

'''
Miscellaneous commands!
'''
@roseworks.command('shakeyshakey', 'shakeyshakey {{cat1|cat2|spinda|tortgle}}', 'misc')
async def shakeyshakey(client, message):
    dances = {
            'cat1': 'https://cdn.discordapp.com/attachments/425046327047487500/474442976802897940/image.gif',
            'cat2': 'https://cdn.discordapp.com/attachments/425046327047487500/474443228364537856/fuck_this_pussy_boy.gif',
            'spinda': 'https://play.pokemonshowdown.com/sprites/xyani/spinda.gif',
            'tortgle': 'https://cdn.discordapp.com/attachments/425057165959495690/472646921060876288/received_967505780079985.gif'
            }
    try:
        dance = dances[message.content.split()[1]]
    except:
        dance = random.choice(list(dances.values()))

    e = discord.Embed()
    e.set_image(url=dance)
    await client.send_message(message.channel, embed=e)
