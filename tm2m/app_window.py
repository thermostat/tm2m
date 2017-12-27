
from . import raw_tmux
import os

NAME_APP_MAP = {
    "bash" : lambda x: ShellWindow(x, shell="bash"),
    "zsh"  : lambda x: ShellWindow(x, shell="zsh"),
    "emacs": lambda x: EmacsWindow(x),
    "ipy"  : lambda x: PythonWindow(x),
    }

class AppWindow(object):
    def __init__(self):
        self.tmux = raw_tmux.get_tmux()
        if self.window == None:
            self.window = self.tmux.current_session().current_window()

    def pwd_to_buffer(self):
        raw_tmux.tmux_set_buffer(os.environ['PWD'])

class ShellWindow(AppWindow):
    def __init__(self, window=None, name=None, shell="bash"):
        self.window = window
        self.name = name if name else shell
        self.shell = shell

class EmacsWindow(AppWindow):
    def __init__(self, window=None):
        self.window = window
        self.name = 'emacs'
        super().__init__()        

class PythonWindow(AppWindow):
    def __init__(self, window=None):
        self.window = window
        self.name = 'ipy'
        super().__init__()


