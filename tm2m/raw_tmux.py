#!/usr/bin/env python3

"""

"""

SESSION_LIST = """tmux list-s -F "#{session_name},#{session_id},#{session_attached}" """
SESSION_COLS = ['session_name', 'session_id', 'session_attached']
WINDOW_LIST  = """tmux list-windows -a -F "#{session_id},#{window_name},#{window_id}" """
WINDOW_COLS  = ['session_id', 'window_name', 'window_id']
PANE_LIST    = """tmux list-panes -a -F "#{session_id},#{window_id},#{pane_id},#{pane_active},#{pane_title}" """
PANE_COLS    = ['session_id', 'window_id', 'pane_id', 'pane_active', 'pane_title']

CREATE_WINDOW_FMT = '"#{session_id},#{window_name},#{window_id},#{pane_id},#{pane_title}"'
CREATE_WINDOW = """tmux new-window -d -P -F {fmt}  -n {name} -t {session_name} {cmd}"""
SET_BUFFER = """tmux set-buffer "{value}" """
SEND_KEYS = """tmux send-keys -t {window_id} {value}"""

import csv
import subprocess
import shlex
import io
import os


def tmux_cmd_csv(cmd, cols):
    cmd_list = shlex.split(cmd)
    output = subprocess.check_output(cmd_list)
    return list(csv.DictReader(io.StringIO(output.decode('utf-8')),  
                               cols))

def tmux_set_buffer(value):
    cmd = SET_BUFFER.format(value=value)
    cmd_list = shlex.split(cmd)
    subprocess.check_output(cmd_list)

TMUX_OBJ = None
def get_tmux():
    global TMUX_OBJ
    if TMUX_OBJ == None:
        TMUX_OBJ = TMux()
    return TMUX_OBJ


class TMux(object):
    def __init__(self):
        self.sessions = []
        self.raw_lists = {}
        self.this_pane = os.environ.get('TMUX_PANE', None)
        self._load()

    def _load(self):
        self.raw_lists['sessions'] = tmux_cmd_csv(SESSION_LIST, SESSION_COLS)
        self.raw_lists['windows'] = tmux_cmd_csv(WINDOW_LIST, WINDOW_COLS)
        self.raw_lists['panes'] = tmux_cmd_csv(PANE_LIST, PANE_COLS)
        for session_dict in self.raw_lists['sessions']:
            session = Session(tmux=self, info=session_dict)
            self.sessions.append(session)
        for window_dict in self.raw_lists['windows']:
            session = self.find_session_by_id(window_dict['session_id'])
            window = Window(session)
            window.update_info(window_dict)
            session.add_window(window)
        for pane_dict in self.raw_lists['panes']:
            session = self.find_session_by_id(pane_dict['session_id'])
            window = session.find_window_by_id(pane_dict['window_id'])
            pane = Pane(window)
            pane.update_info(pane_dict)
            window.add_pane(pane)

    def find_session_by_id(self, idn):
        for session in self.sessions:
            if idn == session.id:
                return session
        return None

    def current_session(self):
        for session in self.sessions:
            if session.current_window():
                return session

    def __repr__(self):
        return "TMux [{} sessions]".format(len(self.sessions))


class Session(object):
    def __init__(self, tmux=None, info=None):
        self.windows = []
        self.tmux = tmux
        self.name = None
        self.id = None
        self.attached = None
        if info:
            self.update_info(info)

    def update_info(self, d):
        self.name = d['session_name']
        self.id = d['session_id']
        self.attached = d['session_attached']

    def create_window(self, name=None, cmd='bash'):
        if name==None:
            name = os.path.basename(shlex.split(cmd)[0])
        cw = CREATE_WINDOW.format(name=name, session_name=self.name,
                                  fmt=CREATE_WINDOW_FMT, cmd=cmd)
        d = tmux_cmd_csv(cw, ['session_id','window_name','window_id','pane_id', 'pane_title'])[0]
        window = Window(self)
        window.update_info(d)
        pane = Pane(window)
        pane.update_info(d)
        window.add_pane(pane)
        self.add_window(window)

    def add_window(self, win):
        self.windows.append(win)
        
    def find_window_by_id(self, idn):
        for window in self.windows:
            if window.id == idn:
                return window
        return None

    def current_window(self):
        for window in self.windows:
            if window.current_pane():
                return window
        return None

    def __repr__(self):
        return "Session {} [{} windows]".format(self.name,
                                                len(self.windows))

class Window(object):
    def __init__(self, session=None):
        self.name = None
        self.session = session
        self.id = None
        self.panes = []

    def update_info(self, d):
        self.name = d['window_name']
        self.id = d['window_id']

    def add_pane(self, pane):
        self.panes.append(pane)

    def send_keys(self, keys):
        cmd = SEND_KEYS.format(window_id=self.id, value=keys)
        cmd_list = shlex.split(cmd)
        subprocess.check_output(cmd_list)

    def current_pane(self):
        for pane in self.panes:
            if pane.is_current_pane():
                return pane
        return None

    def __repr__(self):
        return "Window {} [{}]".format(self.name,
                                       self.id)

class Pane(object):
    def __init__(self, window=None):
        self.name =None
        self.window=window
        self.id = None

    def update_info(self, d):
        self.name = d['pane_title']
        self.id = d['pane_id']

    def is_current_pane(self):
        if self.id == self.window.session.tmux.this_pane:
            return True
        return False


if __name__ == '__main__':
    tmux = TMux()

    sess = tmux.current_session()
    sess.create_window(name="Test1", cmd="zsh")

    for session in tmux.sessions:
        print("Session {}".format(session.name))
        for window in session.windows:
            print("  Window {}".format(window.name))
            for pane in window.panes:
                print("    Pane {}".format(pane.name))
    cw = tmux.current_session().current_window()
    print("Currently {}.{}".format(cw.session.name,
                                   cw.name))
