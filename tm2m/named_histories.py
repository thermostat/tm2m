

"""
Managed history lists
"""

ZSH_FUNCTION = """
zshaddhistory() {
  tm2m --name zsh --add-one "$1"
}
"""

CMD_BIASES = {
    "gcc"            : .25,
    "make"           : .25,
    "git"            : .1,
    "ls"             :-.25,
    "pwd"            :-.25,
    "echo"           :-.2,
    "sed"            : .1,
    "awk"            : .1,
    "grep"           :0.0,
    "tm2m"           :-.25,
    "tm2m_pick"      :-.4
    }

import json
import re, os, os.path, time
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

def add_command(name, command):
    hm = HistoryMap(os.path.join(os.environ['HOME'], '.tm2m'))
    hm.load()
    history = hm[name]
    history.add_item(command)
    history.save()

def add_fd(name, fd, remove_prefix=True, history_dir=None):
    if history_dir == None:
        history_dir = os.path.join(os.environ['HOME'], '.tm2m')
    hm = HistoryMap(history_dir)
    hm.load()
    history = hm[name]
    for line in fd:
        if remove_prefix:
            line = re.sub(r'^(\s*\d+\*?\s+)(.*?)\n', r'\2', line)
        history.add_item(line)
    history.save()
    return history

def search(name, search_strn):
    hm = HistoryMap(os.path.join(os.environ['HOME'], '.tm2m'))
    hm.load()
    history = hm[name]
    sr = history.search(search_strn)
    if len(sr):
        print(str(sr[-1]))

def pick_cmd(name, limit=100):
    hm = HistoryMap(os.path.join(os.environ['HOME'], '.tm2m'))    
    history = hm[name]
    history.load()
    lst = [x.cmd.strip('\n') for x in history.lst[:limit]]
    title = "Command using {} ({}):".format(name,
                                            history.fname)
    cmd,_ = pick.pick(lst, title)
    return cmd

######################################################################
# Objects
######################################################################
    
class HistoryItem(object):

    @staticmethod
    def load(obj):
        return HistoryItem(**obj)

    def __init__(self, cmd, shortname=None,
                 timestamp=None,
                 score=0.5,
                 uses=1):
        self.cmd = cmd
        self.shortname = shortname
        if timestamp is None:
            self.timestamp = time.time()
        self.score = score
        self.uses = uses

    def __eq__(self, other):
        return self.cmd == other.cmd

    def startswith(self, prefix):
        return self.cmd.startswith(prefix)

    def serialize(self):
        return vars(self)

    def score_cmd(self):
        cmd_name = os.path.basename(shlex.split(self.cmd)[0])
        self.score += CMD_BIASES.get(cmd_name, .05)
    
    def __repr__(self):
        return strn_trunc(self.cmd, 20)

    def __str__(self):
        return self.cmd


class History(object):
    def __init__(self, name, fname=None, max_cnt=100):
        self.name = name
        self.lst = []
        self.fname = fname
        self.max_cnt = max_cnt

    def add_item(self, cmd, shortname=None):
        hi = HistoryItem(cmd, shortname)
        if len(self.lst) + 1 > self.max_cnt:
            self.remove_item()
        self.lst.append(hi)

    def remove_item(self, cmd=None):
        if cmd:
            s = self.search(cmd)
            if len(s):
                self.lst.remove(s[0])
        else:
            self.lst.remove(self._select_victim())

    def _select_victim(self):
        return self.lst[0]

    def __len__(self):
        return len(self.lst)

    def search(self, prefix):
        return [x for x in self.lst if x.startswith(prefix)]

    def save(self):
        if self.fname:
            serial = get_serializer()
            fd = open(self.fname, 'w')
            serial.dump([x.serialize() for x in self.lst], fd)
            fd.close()

    def load(self):
        if self.fname:
            serial = get_serializer()
            fd = open(self.fname, 'r')
            loaded = serial.load(fd)
            self.lst = [ HistoryItem.load(x) for x in 
                         loaded ]
            fd.close()

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
            #name = f.strip(prex).strip(ext)
            name = f[len(prex):-len(ext)]
            hist = History(name, full_f)
            hist.load()
            self._map[name] = hist

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
