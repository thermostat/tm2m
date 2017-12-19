
from . import raw_tmux

class AppWindow(object):
    def __init__(self):
        pass

class ShellWindow(AppWindow):
    def __init__(self, window, name=None, shell="bash"):
        self.window = window
        self.name = name if name else shell
        self.shell = shell

class EmacsWindow(AppWindow):
    def __init__(self, window):
        self.window = window
        self.name = 'emacs'
