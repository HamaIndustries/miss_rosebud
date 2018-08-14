import roseworks


'''
Admin commands!
'''

kicked = []

@roseworks.admincommand('kick', 'kick [@user]', 'admin')
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
