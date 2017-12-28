
"""
__init__ placeholder
"""

from . import raw_tmux
from . import cmdline


__version__ = cmdline.__version__
Session = raw_tmux.Session
TMux = raw_tmux.TMux
get_tmux = raw_tmux.get_tmux

commandline = cmdline.commandline
