from tkinter import *
import threading, discord, traceback, asyncio
import rosebud_configs
fields = 'id', 'message'

client = ''

def fetch(entries):
    dic = {}
    for entry in entries:
        dic[entry[0]] = entry[1].get()
    spoo(client, '{} {}'.format(dic['id'].strip(), dic['message']))
    try:
        print('===Rosebud to {}( {} ): {}'.format(discord.utils.get(client.get_all_members(), id=dic['id']).name.translate(rosebud_configs.trans),dic['id'], dic['message']))
    except AttributeError:
        print('===Rosebud to {}( {} ): {}'.format(discord.utils.get(client.get_all_channels(), id=dic['id']).name.translate(rosebud_configs.trans),dic['id'], dic['message']))
    global root
    entries[1][1].delete(0, 'end')

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

root = Tk()
ents = makeform(root, fields)
root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
b1 = Button(root, text='Send',
      command=(lambda e=ents: fetch(e)))
b1.pack(side=LEFT, padx=5, pady=5)

def spoo(client, inp):
    try:
        target = discord.utils.get(client.get_all_members(), id=inp.split(' ', maxsplit=1)[0])
        if target == None:
            target = discord.utils.get(client.get_all_channels(), id=inp.split(' ', maxsplit=1)[0]) # theres definitely a more elegant way to do this but I haven't slept in ~24 hours
            if target == None:
                print('channel or user not found')
                return
        asyncio.run_coroutine_threadsafe(client.send_message(target, inp.split(' ', maxsplit=1)[1]), client.loop).result()
    except (IndexError, discord.errors.HTTPException):
        print('you forgot a message dummy')
    except:
        print('spook issue: vvv--------------------------- vvv')
        traceback.print_exc()

def rolep(cli):
    global client
    client = cli
    threading.Thread(target=root.mainloop).start()