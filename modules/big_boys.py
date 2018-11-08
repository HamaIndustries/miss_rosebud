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
        await client.send_message(message.channel, 'The bouncers have been notified. {}{} has been escorted accordingly.'.format(message.mentions[0].name, ' and company' if len(message.mentions) > 1 else ''))
    except AssertionError:
        await client.send_message(message.channel, 'This command is only authorized for admins against people with roles lower than mine.')
    except discord.Forbidden:
        await client.send_message(message.channel, 'You haven\'t given me that power. Command only authorized for admins against people with roles lower than mine.')

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

