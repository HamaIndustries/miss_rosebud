import roseworks, rosebud_configs
from backend import rp
from modules import big_boys, conversation_hearts, general, kissy, marriage_owo, misty, xwu_nud35

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
    client.change_presence(game=discord.Game(name='in the 8 Isles!'))
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

@client.event
async def on_member_remove(member):
    farewell = 'Cya {} lmao.'
    if member.server.id == rosebud_configs.settings.setting['main_server_id']:
        if member.id in big_boys.kicked:
            big_boys.kicked.remove(member.id)
            farewell = '{} bye bitch.'
        await client.send_message(client.get_channel(rosebud_configs.settings.setting['entry_channel_id']), farewell.format(member.mention))

@safety
@client.event
async def on_message(message):
    if message.channel.id == '467294482854051841':
        return

    '''
    if message.content.startswith('{}updatestatus'.format(prefix)) and message.author.id in (rosebud_config.elid, rosebud_config.wishid):
        await client.change_presence(game=discord.Game(name=message.content.split(' ',1)[1]))
        return

    elif message.content.startswith('{}makepickles'.format(prefix)) and message.author.id == rosebud_configs.elid:
        await client.send_message(message.channel, 'Pickles created!')
        with open('{}/directory.pk'.format(settings.home_dir), 'wb+') as f:
            marriages = marriage()
            marriages['lucky'] = 'dante'
            pickle.dump(marriages, f)
        with open('{}/proposals.pk'.format(settings.home_dir), 'wb+') as f:
            proposals = {'lucky':'dante'}
            pickle.dump(proposals, f)
        return

    elif message.content.startswith('{}makewmar'.format(prefix)) and message.author.id == rosebud_configs.elid:
        await client.send_message(message.channel, 'Wishi flavored pickles created!')
        with open('{}/wishidirectory.pk'.format(settings.home_dir), 'wb+') as f:
            marriages = dict()
            marriages['lucky'] = 'dante'
            pickle.dump(marriages, f)
        return

    elif message.content.startswith('{}makeprofiles'.format(prefix)) and message.author.id == rosebud_configs.elid:
        with open('{}/userlist.pk'.format(settings.home_dir), 'wb+') as f:
            profiles = dict()
            #profiles['lucky'] = 'dante'
            pickle.dump(profiles, f)
        
        await client.send_message(message.channel, 'profiles created!')
        return
    '''
#----- commands -----
    
    if message.content.startswith(prefix):
        command = message.content.split()[0].replace(',,','')

        availcommands = dict(roseworks.commands_dict)
        if message.author.id == rosebud_configs.wishid:
            availcommands.update(roseworks.wishicommands_dict)
        if message.channel.permissions_for(message.author).administrator:
            availcommands.update(roseworks.admincommands_dict)

        if command == 'help':
            try:
                await client.send_message(message.channel, 'usage: {}{}'.format(prefix, availcommands[message.content.split()[1]]['help']))
            except:
                send = discord.Embed(title='٩( ᐛ )و  Commands!', color=0xffd1dc)
                send.set_author(name='Miss Rosebud', icon_url=client.user.avatar_url)
                organized = {}
                for i in availcommands:
                    if not availcommands[i]['category'] in organized:
                        organized[availcommands[i]['category']] = {}
                    organized[availcommands[i]['category']][i] = availcommands[i]

                for i in organized:
                    send.add_field(name='✿ {} ✿'.format(i),value='```{}```'.format(re.sub('[\[\]\']', '', str(list(organized[i])))), inline=False)
                
                #send.add_field(name='✿ marriage commands ✿',value='```{}```'.format(), inline=False)
                #send.add_field(name='✿ miscellaneous ✿', value='```{}```'.format(re.sub('[\[\]\']', '', str(list(misccommands.keys())))), inline=False)
                #send = '٩( ᐛ )و  Commands!\n✿ marriage commands ✿\n{}\n\n✿ miscellaneous ✿\n{}\n\nMore to come. ;3c'.format(
                #    re.sub('[\[\]\']', '', str(list(commands.keys()))), re.sub('[\[\]\']', '', str(list(misccommands.keys()))))
                await client.send_message(message.channel, embed=send)

        
        elif command in availcommands or command in roseworks.secretcommands_dict:
            availcommands.update(roseworks.secretcommands_dict)
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
                    client.delete_message(message)
                except:
                    traceback.print_exc()
    else:
        for i in roseworks.conversations:
            await i(client, message)
            
async def astart():
    start()
         
def start():
    try:
        client.run(settings.token)
    except discord.errors.LoginFailure:
        if '--debuglogin' or '--dl' in sys.argv:
            raise
        else:
            print('config.cfg created, change login token\nIf you recieve this message after changing it, try running the program with argument --debuglogin')

def th(loop, coro, *args, **kwargs):
    asyncio.run_coroutine_threadsafe(coro(args, kwargs), loop).result()

if __name__ == '__main__':
    threading.Thread(target=client.run, args=(settings.token,)).start() #allows me to dynamically access/modify code
    rp.rolep(client, asyncio.get_event_loop())
