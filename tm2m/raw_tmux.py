
"""
"""

SESSION_LIST = """tmux list-s -F "#{session_name},#{session_id},#{session_attached}" """
SESSION_COLS = ['session_name', 'session_id', 'session_attached']
WINDOW_LIST  = """tmux list-windows -a -F "#{session_name},#{window_name},#{window_id}" """
WINDOW_COLS  = ['session_name', 'window_name', 'window_id']
PANE_LIST    = """tmux list-panes -a -F "#{session_name},#{window_name},#{pane_id},#{pane_active}" """
PANE_COLS    = ['session_name', 'window_name', 'pane_id', 'pane_active']

import csv
import subprocess
import shlex
import io


def tmux_cmd_csv(cmd, cols):
    cmd_list = shlex.split(cmd)
    output = subprocess.check_output(cmd_list)
    return list(csv.DictReader(io.StringIO(output.decode('utf-8')),  
                               cols))



class TMux(object):
    def __init__(self):
        self.sessions = []


class Session(object):
    def __init__(self, tmux=None):
        self.windows = []
        self.tmux = tmux


class Windows(object):
    def __init__(self, session=None):
        self.name = None
        self.session = session
        self.id = None

class Pane(object):
    def __init__(self, window):
        self.name =None
        self.window=window




if __name__ == '__main__':
    print(tmux_cmd_csv(SESSION_LIST, SESSION_COLS))
    print(tmux_cmd_csv(WINDOW_LIST, WINDOW_COLS))
    print(tmux_cmd_csv(PANE_LIST, PANE_COLS))
