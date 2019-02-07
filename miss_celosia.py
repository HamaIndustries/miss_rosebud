import roseworks, rosebud_configs
#from full_house import miss_celosia
from backend import rp
from modules import lady_luck_casino

import discord, re, traceback, sys, asyncio
import threading

client = discord.Client()
trans = rosebud_configs.trans
prefix = rosebud_configs.settings.prefix

#current main settings in case I change config categories later
settings = rosebud_configs.settings

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name.translate(trans))
    print(client.user.id)
    await client.change_presence(game=discord.Game(name='Serving Lady Luck Casino!'))
    #print('starting rp...')
    #threading.Thread(target=roleplay, args=(client,)).start()
    print('------')

def safety(func):
    async def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('Uncaught exception {}, ignoring...'.format(repr(e)))
    return decorator

@safety
@client.event
async def on_message(message):
    if message.channel.id == '467294482854051841':
        return
    
#----- commands -----
    
    if message.content.startswith(prefix):
        command = message.content.split()[0].replace(',,','')

        availcommands = dict(roseworks.casinocommands_dict)

        if command in availcommands:
            try:
                await availcommands[command]['command'](client, message)
            except IndexError:
                print('user {} {} unsuccessfully executed command {}:'.format(message.author.name.translate(trans), message.author.id, command))
                print('attempted {}'.format(message.content.translate(trans)))
                await client.send_message(message.channel, 'usage: {}{}'.format(prefix, availcommands[command]['help']))
            except:
                print('user {} {} fatally executed command {}:'.format(message.author.name.translate(trans), message.author.id, command))
                print('attempted {}'.format(message.content.translate(trans)))
                traceback.print_exc()
                await client.send_message(message.channel, 'usage: {}{}'.format(prefix, availcommands[command]['help']))
            if len(message.attachments) > 0 or re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content):
                try:
                    await client.delete_message(message)
                except:
                    traceback.print_exc()
            
async def astart():
    start()
         
def start(leader):
    try:
        setattr(client, 'boss_lady', leader)
        threading.Thread(target=client.run, args=(settings.setting['celosia_token'],)).start() #allows me to dynamically access/modify code
        rp.rolep(client, asyncio.get_event_loop())
    except discord.errors.LoginFailure:
        if '--debuglogin' or '--dl' in sys.argv:
            raise
        else:
            print('config.cfg created, change login token\nIf you recieve this message after changing it, try running the program with argument --debuglogin')

def th(loop, coro, *args, **kwargs):
    asyncio.run_coroutine_threadsafe(coro(args, kwargs), loop).result()

if __name__ == '__main__':
        rp.rolep(client, asyncio.get_event_loop())
