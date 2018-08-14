import roseworks, rosebud_configs
from backend.utils import unmultiply, premultiply, send_image
from backend import wishify

import requests, traceback, discord
from io import BytesIO
from PIL import Image

'''
Image commands!
'''

settings = rosebud_configs.settings

@roseworks.command('wishify', 'wishify {{url}} {{color hex}}', 'image')
async def wishif(client, message):
    print(message.author.id)
    arg = message.content.strip().split(' ')
    color = 'ffd1dc'
    imurl = ''
    
    if len(message.attachments)>0:
        imurl = message.attachments[0]['url']
        try:
            color = arg[1].strip('#')
        except:
            color = 'ffd1dc'
        print(imurl)
    elif len(arg)>1:
        imurl = arg[1]
        try:
            color = arg[2]
        except:
            color = 'ffd1dc'
        print(imurl)
    else:
        await client.send_message(message.channel, 'Please specify an image to wishify! xwu\"')
        return

    #open and convert to PNG
    response = requests.get(imurl)
    top = Image.open(BytesIO(response.content))
    im = Image.new('RGBA', top.size)
    im.paste(top, (0,0))

    #im = Image.open(BytesIO(response.content))
    colored = ''
    try:
        colored = wishify.colorify(im, color)
    except MemoryError:
        await client.send_message(message.channel, 'It\'s too big for me! \_(´ཀ`」 ∠)')
    except Exception as e:
        print('colorify exception: {}'.format(repr(e)))
    
    #colored.show()

    await send_image(colored, client, message.channel)

    #await client.send_message(message.channel, message.embeds[0].image.url)

@roseworks.command('dlemoji', 'dlemoji [emoji]', 'image')
async def dlemoji(client, message):
    response = requests.get(discord.utils.get(client.get_all_emojis(), name = message.content.split(':')[1]).url)
    await send_image(Image.open(BytesIO(response.content)), client, message.channel)

@roseworks.command('dlprofile', 'dlprofile {{@user}}', 'image')
async def dlprofile(client, message):
    if len(message.mentions) > 0:
        target = message.mentions[0]
    else:
        target = message.author
    
    response = requests.get(target.avatar_url if message.author.avatar_url != '' else target.default_avatar_url)
    profile = Image.open(BytesIO(response.content))

    await send_image(profile, client, message.channel)

@roseworks.command('gay', 'gay {{@user|url}}', 'image')
async def gay(client, message):
    if len(message.mentions) > 0:
        target = message.mentions[0]
    else:
        target = message.author

    try:
        if len(message.attachments)>0:
            imurl = message.attachments[0]['url']
        else:
            imurl = message.content.split()[1]
        response = requests.get(imurl)
    except:
        response = requests.get(target.avatar_url if message.author.avatar_url != '' else target.default_avatar_url)
        
    profile = Image.open(BytesIO(response.content))

    overlay = Image.open('{}/pretty.png'.format(settings.home_dir))
    if profile.size[0] > overlay.size[0]:
        profile.thumbnail(overlay.size, Image.ANTIALIAS)
    else:
        premultiply(overlay)
        overlay.thumbnail(profile.size, Image.ANTIALIAS)
        unmultiply(overlay)
    profile.paste(overlay, (0,0), overlay)
    
    await send_image(profile, client, message.channel)

@roseworks.command('nikki', 'nikki {{@user|url}}', 'image')
async def nikki(client, message):
    if len(message.mentions) > 0:
        target = message.mentions[0]
    else:
        target = message.author

    try:
        if len(message.attachments)>0:
            imurl = message.attachments[0]['url']
        else:
            imurl = message.content.split()[1]
        response = requests.get(imurl)
    except:
        response = requests.get(target.avatar_url if message.author.avatar_url != '' else target.default_avatar_url)

    profile = Image.open(BytesIO(response.content))
    overlay = Image.open('{}/nikki.png'.format(settings.home_dir))
    canvas = Image.new('RGB', overlay.size, (255, 255, 255))

    
    if profile.size[1] > 200:
        profile.thumbnail((1000, 200), Image.ANTIALIAS)
    else:
        profile = profile.resize((200, profile.size[0]//profile.size[1]*200), Image.BICUBIC)
    
    canvas.paste(profile, (0,200))
    canvas.paste(overlay, (0,0), overlay)
    
    await send_image(canvas, client, message.channel)

@roseworks.command('hotel', 'hotel {{@user|url}}', 'image')
async def hotel(client, message):
    if len(message.mentions) > 0:
        target = message.mentions[0]
    else:
        target = message.author

    try:
        if len(message.attachments)>0:
            imurl = message.attachments[0]['url']
        else:
            imurl = message.content.split()[1]
        response = requests.get(imurl)
    except:
        response = requests.get(target.avatar_url if message.author.avatar_url != '' else target.default_avatar_url)
        
    profile = Image.open(BytesIO(response.content))

    overlay = Image.open('{}/mario.png'.format(settings.home_dir))
    if profile.size[0] > overlay.size[0]:
        profile.thumbnail(overlay.size, Image.ANTIALIAS)
    else:
        premultiply(overlay)
        overlay.thumbnail(profile.size, Image.ANTIALIAS)
        unmultiply(overlay)
    profile.paste(overlay, (0,profile.size[1]-overlay.size[1]), overlay)
    
    await send_image(profile, client, message.channel)



