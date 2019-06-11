from tkinter import *
import threading, discord, traceback, asyncio, time

fields = "id", "message"


trans = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xFFFD)


class bot_info:
    client = ""


def fetch(entries):
    dic = {}
    for entry in entries:
        dic[entry[0]] = entry[1].get()
    spoo(bot_info.bot_info.client, "{} {}".format(dic["id"].strip(), dic["message"]))
    try:
        print(
            "==={} to {}( {} ): {}".format(
                bot_info.user.name,
                discord.utils.get(
                    bot_info.client.get_all_members(), id=dic["id"]
                ).name.translate(trans),
                dic["id"],
                dic["message"],
            )
        )
    except AttributeError:
        print(
            "==={} to {}( {} ): {}".format(
                bot_info.user.name,
                discord.utils.get(
                    bot_info.client.get_all_channels(), id=dic["id"]
                ).name.translate(trans),
                dic["id"],
                dic["message"],
            )
        )
    global root
    entries[1][1].delete(0, "end")


def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor="w")
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries


def spoo(client, inp):
    try:
        target = discord.utils.get(
            client.get_all_members(), id=inp.split(" ", maxsplit=1)[0]
        )
        if target == None:
            target = discord.utils.get(
                client.get_all_channels(), id=inp.split(" ", maxsplit=1)[0]
            )  # theres definitely a more elegant way to do this but I haven't slept in ~24 hours
            if target == None:
                print("channel or user not found")
                return
        asyncio.run_coroutine_threadsafe(
            client.send_message(target, inp.split(" ", maxsplit=1)[1]), client.loop
        ).result()
    except (IndexError, discord.errors.HTTPException):
        print("you forgot a message dummy")
    except:
        print("spook issue: vvv--------------------------- vvv")
        traceback.print_exc()


def rolep(cli, loop):
    asyncio.run_coroutine_threadsafe(cli.wait_until_ready(), loop).result()
    root = Tk()
    ents = makeform(root, fields)
    root.bind("<Return>", (lambda event, e=ents: fetch(e)))
    b1 = Button(root, text="Send", command=(lambda e=ents: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    root.title(cli.user.name)
    bot_info.client = cli
    threading.Thread(target=root.mainloop).start()
