from PIL import Image
from io import BytesIO
from discord import Embed, utils
from datetime import datetime

import rosebud_configs
import random
import os
import copy
import sys
import pickle
import requests
import bidict
import re

trans = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

settings = rosebud_configs.settings

elid = '181057933654622208'
wishid = '304080356900995092'
    
class Profile():
    '''
    Class containing profile card info.
    Object Variables:
    id
    profileurl
    '''
    currency_name = 'kisses'
    currency_symbol = '₪'
    daily_range = (10, 15)
    
    def __init__(self, user):
        self.id = user.id
        self.name = user.name.translate(trans)
        self.info = {}
        self.load_profile(user, int(settings.suppress_loading_messages))
        
    def load_profile(self, user, suppress_messages = False):
        self.profileurl = user.avatar_url if user.avatar_url != '' else user.default_avatar_url
        self.info = copy.deepcopy(load_user_info(self.id))
        self.info['marriages'] = bidict.readmarriages()[self.id] if self.id in bidict.readmarriages() else None
        self.info['wishimarriages'] = bidict.readwmarriages()[self.id] if self.id in bidict.readwmarriages() else 0
        if not suppress_messages:
            print('successfully loaded user profile {} from file'.format(self.id))

    def save_profile(self, message = None, suppress_messages = False):
        save_user_info(self.id, self.info)
        if not suppress_messages:
            print('successfully saved user profile {} to file'.format(self.id) if message == None else message)

    async def daily(self):
        lasttime = datetime.now()-self.info['lastdaily']
        if self.id != wishid and lasttime.days < 1 and lasttime.seconds / 3600.0 < 20:
           raise TooSoonError(self.info['lastdaily'], datetime.now())
        amount = random.randrange(self.daily_range[0], self.daily_range[1])
        self.amend_currency(amount)
        self.info['lastdaily'] = datetime.now()
        self.save_profile('Reset daily for {}'.format(self.id))
        return amount
        
    def amend_currency(self, amount):
        self.info[self.currency_name] += amount
        self.save_profile()
            
    async def get_card_plaintext(self, client):
        if self.info['marriages'] == None:
            marriages = 'nobody'
        else:
            marriages = await client.get_user_info(self.info['marriages'])

        if self.id == '304080356900995092':
            wishimarriages = 0
            mars = bidict.readwmarriages()
            for i in mars:
                if i == 'lucky':
                    continue
                #print(mars[i]['marriages'])
                wishimarriages += int(mars[i]['marriages'])
        elif type(self.info['wishimarriages']) == type(1):
            wishimarriages = self.info['wishimarriages']
        
        else:
            wishimarriages = '{} since {}'.format(self.info['wishimarriages']['marriages'], self.info['wishimarriages']['anniversary'].strftime("%Y-%m-%d"))
            #wishimarriages = '{} since {}'.format(self.info['wishimarriages']['marriages'], self.info['wishimarriages']['anniversary'].strftime("%Y-%m-%d")) if self.info['wishimarriages'] != 0 else 0
        emb = Embed(title=self.name, color=0xffd1dc)
        emb.set_thumbnail(url=self.profileurl)
        emb.add_field(name='Stickers', value=re.sub('\[\]\,\'', '', str([self.info['stickers'][i]['symbol'] for i in self.info['stickers']])), inline=False)
        emb.add_field(name='Married to:', value=marriages, inline=False)
        emb.add_field(name='Wishi Marriages:', value=wishimarriages, inline=False)
        emb.add_field(name='Inventory', value=self.info['inventory'], inline=False)
        emb.add_field(name=self.currency_name, value='{} {}'.format(self.currency_symbol,self.info[self.currency_name]), inline=False)
        return emb
    
    def get_card(self):
        profile_canvas = Image.open('{}/profile_canvas.png'.format(settings.home_dir))
        profile = load_image_from_url(self.profileurl)
        profile.thumbnail(profile_size, Image.ANTIALIAS)

    def set_value(self, key, value):
        self.info[key] = value
        self.save_info()
        
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type == None:
            save_profile()

    '''
    profile card dimensions
    '''

    profile_size = (50, 50)
    profile_leftcoord = 0
    profile_topcoord = 0

    stickers_size = (50, 50)
    stickers_leftcoord = 0
    stickers_topcoord = 0

    marriages_size = (50, 50)
    marriages_leftcoord = 0
    marriages_topcoord = 0

    names_size = (50, 50)
    names_leftcoord = 0
    names_topcoord = 0

    inventory_size = (50, 50)
    inventory_leftcoord = 0
    inventory_topcoord = 0

class Stickers():
    '''
    sticker list
    '''
    stickers = {'Married':{'desc':'Married to a special someone!',
                         'symbol':'<:chains:467852423508262912>'},
              'WishiMarried':{'desc':'Married without consent to Queen Wishi!',
                              'symbol':'<:eyes:467853189887164436>'},
              'Divorced':{'desc':'Separated from a special someone!',
                         'symbol':'<:free:467854340363911178>'},
              'Merchant':{'desc':'Sold an item on the market.',
                         'symbol':'<:money_with_wings:467854731264655383>'},
              'SecretHunter':{'desc':'Found a secret command',
                             'symbol':'<:question:467856326823903234>'}
              }


    async def award(id, tag):
        profile = load_user_info(id)
        try:
            profile['stickers'][tag] = Stickers.stickers[tag]
            save_user_info(id, profile)
        except KeyError:
            print('No sticker found with that tag!')

    async def unaward(id, tag):
        profile = load_user_info(id)
        try:
            del profile['stickers'][tag]
            save_user_info(id, profile)
        except KeyError:
            print('No sticker found with that tag!')
        
def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def load_user_info(id, suppress_messages = False):
    info=0
    with open('{}/userlist.pk'.format(settings.home_dir),'rb') as f:
        try:
            return pickle.load(f)[id]
        except KeyError:
            info = {'stickers': {},
                    #'marriages': bidict.readmarriages()[id] if id in bidict.readmarriages() else None,
                    #'wishimarriages': bidict.readwmarriages()[id] if id in bidict.readwmarriages() else 0,
                    'inventory': {},
                    Profile.currency_name: 0,
                    'lastdaily': datetime.min
                    }
    save_user_info(id, info)
    if not suppress_messages:
        print('successfully created user profile for {}'.format(id))
    return info

def save_user_info(id, entry):
    userlist = ''
    with open('{}/userlist.pk'.format(settings.home_dir),'rb') as f:
        userlist = pickle.load(f)

    with open('{}/userlist.pk'.format(settings.home_dir),'wb') as f:
        userlist[id] = entry
        pickle.dump(userlist, f)

class TooSoonError(Exception):
     def __init__(self, current, goal):
         self.waittime =  current - goal
