
from . import raw_tmux
import os

NAME_APP_MAP = {
    "bash" : lambda x: ShellWindow(x, shell="bash")
    "zsh"  : lambda x: ShellWindow(x, shell="zsh")
    "emacs": lambda x: EmacsWindow(x)
    }

class AppWindow(object):
    def __init__(self):
        pass

    def pwd_to_buffer(self):
        raw_tmux.tmux_set_buffer(os.environ['PWD'])

class ShellWindow(AppWindow):
    def __init__(self, window, name=None, shell="bash"):
        self.window = window
        self.name = name if name else shell
        self.shell = shell

class EmacsWindow(AppWindow):
    def __init__(self, window):
        self.window = window
        self.name = 'emacs'
        
