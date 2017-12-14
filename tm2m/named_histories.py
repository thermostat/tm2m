

"""
Managed history lists
"""

import json

def get_serializer():
    return json

def strn_trunc(strn, limit=80):
    if len(strn) > limit:
        return strn[:limit-3]+"..."
    return strn

class HistoryItem(object):

    @staticmethod
    def load(obj):
        return HistoryItem(**obj)

    def __init__(self, cmd, shortname=None):
        self.cmd = cmd
        self.shortname = shortname

    def __eq__(self, other):
        return self.cmd == other.cmd

    def startswith(self, prefix):
        return self.cmd.startswith(prefix)

    def serialize(self):
        return vars(self)

    def __repr__(self):
        return strn_trunc(self.cmd, 20)


class History(object):
    def __init__(self, name, fname=None, max_cnt=100):
        self.name = name
        self.lst = []
        self.fname = fname

    def add_item(self, cmd, shortname=None):
        hi = HistoryItem(cmd, shortname)
        self.lst.append(hi)

    def remove_item(self, cmd=None):
        if cmd:
            s = self.search(cmd)
            if len(s):
                self.lst.remove(s[0])
        else:
            self.lst.remove(self._select_victim())

    def _select_victim(self):
        return self.lst[-1]

    def search(self, prefix):
        return [x for x in self.lst if x.startswith(prefix)]

    def save(self):
        if self.fname:
            serial = get_serializer()
            fd = open(self.fname, 'w')
            serial.dump([x.serialize() for x in self.lst], fd)

    def load(self):
        if self.fname:
            serial = get_serializer()
            fd = open(self.fname, 'r')
            self.lst = [ HistoryItem.load(x) for x in 
                         serial.load(fd) ]

class HistoryMap(object):
    def __init__(self, history_save_dir=None):
        self.save_dir = history_save_dir
        
