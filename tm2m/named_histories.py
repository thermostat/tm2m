

"""
Managed history lists
"""

import json
import re, os, os.path
import pick

def get_serializer():
    return json

def get_serial_ext():
    return ".json"

def strn_trunc(strn, limit=80):
    if len(strn) > limit:
        return strn[:limit-3]+"..."
    return strn

######################################################################
# Commands
######################################################################

def add_fd(name, fd, remove_prefix):
    hm = HistoryMap(os.path.join(os.environ['HOME'], '.tm2m'))
    hm.load()
    history = hm[name]
    for line in fd:
        if remove_prefix:
            line = re.sub(r'^(\s*\d+\*?\s+)(.*?)\n', r'\2', line)
        history.add_item(line)
    history.save()

def search(name, search_strn):
    hm = HistoryMap(os.path.join(os.environ['HOME'], '.tm2m'))
    hm.load()
    history = hm[name]
    sr = history.search(search_strn)
    if len(sr):
        print(str(sr[-1]))

def pick_cmd(name, limit=40):
    hm = HistoryMap(os.path.join(os.environ['HOME'], '.tm2m'))    
    history = hm[name]
    history.load()
    lst = [x.cmd for x in history.lst[:limit]]
    cmd,_ = pick.pick(lst, "Command:")
    return cmd

######################################################################
# Objects
######################################################################
    
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

    def __str__(self):
        return self.cmd


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
            loaded = serial.load(fd)
            self.lst = [ HistoryItem.load(x) for x in 
                         loaded ]

class HistoryMap(object):
    def __init__(self, history_save_dir=None):
        self.save_dir = history_save_dir
        self._map = {}
        
    def load(self):
        assert self.save_dir
        ext = get_serial_ext()
        prex = "history."
        for f in os.listdir(self.save_dir):
            if not f.endswith(ext) or not f.startswith(prex):
                continue
            full_f = os.path.join(self.save_dir, f)
            name = f.strip(prex).strip(ext)
            hist = History(name, full_f)
            hist.load()
            self._map[name] = hist
        print(list(self._map.keys()))

    def save(self):
        for hist in self._map.values():
            hist.save()

    def __getitem__(self, key):
        if key in self._map:
            return self._map[key]
        else:
            fname = os.path.join(self.save_dir, "history."+key+get_serial_ext())
            new_history = History(key, fname)
            self._map[key] = new_history
            return new_history
