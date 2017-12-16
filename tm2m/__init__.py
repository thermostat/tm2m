
"""
__init__ placeholder
"""

from . import raw_tmux
from . import cmdline


__version__ = cmdline.__version__
Session = raw_tmux.Session
TMux = raw_tmux.TMux

commandline = cmdline.commandline
