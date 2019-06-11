from collections.abc import MutableMapping
import rosebud_configs
import os, pickle


settings = rosebud_configs.settings


class marriage(MutableMapping):
    """
    Mutable Dictionary-Set hybrid that treats keys as values and vice versa.
    """

    def __init__(self, *args, **kw):
        self._storage = dict(*args, **kw)

    def __getitem__(self, key):
        if key in self._storage:
            return self._storage[key]
        for i in self._storage:
            if self._storage[i] == key:
                return i
        raise KeyError

    def __setitem__(self, key, val):
        for i in self._storage:
            if self._storage[i] == key:
                del self._storage[i]
                continue
        self._storage[key] = val

    def __delitem__(self, key):
        if key in self._storage:
            del self._storage[key]
            return
        if key in self._storage.values():
            del self._storage[next(k for k, v in self._storage.items() if v == key)]
            return
        raise KeyError

    def __iter__(self):
        # creates a list to be iterated
        a = [(key, value) for key, value in self._storage.items()]
        return iter(a)

    def __len__(self):
        return len(self._storage)

    def __str__(self):
        return str([a for a in self])


async def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        print("error removing")
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


"""
duplicate code from miss_rosebud for upkeep/testing purposes. May become main code if I separate modules.
"""


def readproposals():
    with open("{}/proposals.pk".format(settings.home_dir), "rb") as f:
        proposals = pickle.load(f)
        return proposals


def readmarriages():
    with open("{}/directory.pk".format(settings.home_dir), "rb") as f:
        marriages = pickle.load(f)
        return marriages


def writemarriage(a, b):
    marriages = ""
    with open("{}/directory.pk".format(settings.home_dir), "rb") as f:
        marriages = pickle.load(f)
        marriages[a] = b
    with open("{}/directory.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(marriages, f)


def delmarriage(a):
    marriages = ""
    with open("{}/directory.pk".format(settings.home_dir), "rb") as f:
        marriages = pickle.load(f)
        del marriages[a]
    with open("{}/directory.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(marriages, f)


def propose(fro, to):
    proposals = ""  # having issues with rb+, don't feel ,like messing with it
    with open("{}/proposals.pk".format(settings.home_dir), "rb") as f:
        proposals = pickle.load(f)
        proposals[fro] = to
    with open("{}/proposals.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(proposals, f)


def acceptmarriage(fro, to):
    proposals = ""
    with open("{}/proposals.pk".format(settings.home_dir), "rb") as f:
        proposals = pickle.load(f)
        del proposals[to]
    with open("{}/proposals.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(proposals, f)
    writemarriage(fro, to)


def readwmarriages():
    with open("{}/wishidirectory.pk".format(settings.home_dir), "rb") as f:
        wishimarriages = pickle.load(f)
        return wishimarriages


def writewmarriage(a):
    wishimarriages = ""  # having issues with rb+, don't feel ,like messing with it
    with open("{}/wishidirectory.pk".format(settings.home_dir), "rb") as f:
        wishimarriages = pickle.load(f)
        try:
            wishimarriages[a]["marriages"] += 1
        except:
            wishimarriages[a] = {"marriages": 1, "anniversary": datetime.now()}
    with open("{}/wishidirectory.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(wishimarriages, f)


def delwmarriage(a):
    wishimarriages = ""
    with open("{}/wishidirectory.pk".format(settings.home_dir), "rb") as f:
        wishimarriages = pickle.load(f)
        del wishimarriages[a]
    with open("{}/wishidirectory.pk".format(settings.home_dir), "wb") as f:
        pickle.dump(wishimarriages, f)


"""
with open('directory.pk', 'rb') as f:
    proposals = pickle.load(f)
    print(proposals)
"""
"""
a = marriage()
a['b'] = 'c'
del a['c']
"""
"""
a = marriage()
a["wishi"] = 'Eli'
a["russ"] = 'Blur'

if 'russ' in a:
    print('true')"""
