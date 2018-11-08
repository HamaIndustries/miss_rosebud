import roseworks
from rosebud_configs import trans

import shlex, discord
'''
Admin commands!
'''

kicked = []

@roseworks.admincommand('kick', 'kick [@user]', roseworks.ADMIN)
async def kick(client, message):
    try:
        assert message.channel.permissions_for(message.author).administrator
        for i in message.mentions:
            await client.kick(i)
            kicked.append(i.id)
        await client.send_message(message.channel, 'Butts kicked.')
    except AssertionError:
        await client.send_message(message.channel, 'Command only authorized for admins against people with roles lower than mine! smh cmh')
    except discord.Forbidden:
        await client.send_message(message.channel, 'You haven\'t given me that power. Command only authorized for admins against people with roles lower than mine. ( xmu)')

@roseworks.admincommand('getroleusers', 'getroleusers [role] {roles...} (Use quotes for multi-word arguments)', roseworks.ADMIN)
async def getroles(client, message):
    users = {}
    for item in shlex.split(message.content)[1:]:
        users[item] = []
        for member in message.server.members:
            for role in member.roles: 
                if role.name == item or role.id == item:
                    users[item].append(member.name.translate(trans))
        if users[item]:
            users[item].sort()
        else:
            await client.send_message(message.channel, 'Role {} not found'.format(item))
            del users[item]
    if not users:
        return
    e = discord.Embed(title='Role users:')
    for item in users:
        e.add_field(name=item, value='\n'.join(users[item]), inline=False)
    await client.send_message(message.channel, embed=e)
