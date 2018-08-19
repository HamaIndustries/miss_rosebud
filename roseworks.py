from backend.profiles import Profile

GENERAL = 'info/general'
MARRIAGE = 'marriage commands'
IMAGES = 'photoshop fun'
MONEY = Profile.currency_name
MISC = 'miscellaneous'
ADMIN = 'administration'

commands_dict = {}
def command(name, help='', category='misc'): #misc, general, money, marriage, image
    def real_command_hehe(func):
        commands_dict[name]={
                            'command':func,
                            'help':help,
                            'category':category
                            }
        return func
    return real_command_hehe

wishicommands_dict = {}
def wishicommand(name, help='', category = 'misc'):
    def real_command_hehe(func):
        wishicommands_dict[name]={
                            'command':func,
                            'help':help,
                            'category':category
                            }
        return func
    return real_command_hehe

admincommands_dict = {}
def admincommand(name, help='', category='misc'): # all including admin
    def real_command_hehe(func):
        admincommands_dict[name]={
                            'command':func,
                            'help':help,
                            'category':category
                            }
        return func
    return real_command_hehe

secretcommands_dict = {}
def secretcommand(name):
    def real_command_hehe(func):
        secretcommands_dict[name]={
                            'command':func,
                            'help':'',
                            'category':'secret'
                            }
        return func
    return real_command_hehe

conversations = []
def conversation(): #function for consistency
    def real_command_hehe(func):
        conversations.append(func)
        return func
    return real_command_hehe

if __name__ == '__main__':
    @command('test', help='hehe')
    def test():
        return 1
