import configparser
import os
import copy

def get_config(category):
    cfg = configparser.ConfigParser({
        'home_dir':os.path.dirname(os.path.abspath(__file__)),
        'suppress_loading_messages':'0',
        'token':'CHANGEME',
        'main_server_id':'425046326275866626',
        'entry_channel_id':'425057127632207902'
        })

    if not os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.cfg')):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.cfg'), 'w') as f:
            cfg.write(f)
        
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.cfg'), 'r') as f:
            cfg.read_file(f)
            
    return cfg[category]

class settings():
    '''
    Formalized container class for grabbing settings regardless of category

    Redundant, but useful if/when we scale Rosebud
    '''

    # defaults
    cfg_default = dict(get_config('DEFAULT'))
    suppress_loading_messages = int(cfg_default['suppress_loading_messages'])
    home_dir = cfg_default['home_dir']
    token = cfg_default['token']

    #all vals
    setting = copy.deepcopy(cfg_default)
