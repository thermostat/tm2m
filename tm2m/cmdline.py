

import argparse
import sys
from . import named_histories
from . import raw_tmux

__version__ = '0.1'

def default_commandline():
    TM2MCL().commandline()

class Commandline(object):

    def commandline(self):
        self.main(self.generate_args())

    def main(self, args):
        raise NotImplementedError()

    def generate_args(self, in_args=None):
        parser = argparse.ArgumentParser()
        self._add_args(parser)
        return parser.parse_args(in_args)
        
    def _add_args(self, parser):
        raise NotImplementedError()        

class TM2MCL(Commandline):

    def _add_args(self, parser):
        add_arg = parser.add_argument
        add_arg('--version', action='store_true')
        add_arg('--history', action='store_true')
        add_arg('--add-stdin', action='store_true')
        add_arg('--search', nargs=1)
        add_arg('--name', nargs=1)
        add_arg('--nbr-prefix', action='store_true', default=False)

    def main(self, args):
        if args.version:
            print("tm2m version {}".format(__version__))
            sys.exit(0)
        if args.add_stdin:
            named_histories.add_fd(args.name[0],
                                   sys.stdin, args.nbr_prefix)
        elif len(args.search):
            named_histories.search(args.name[0], args.search[0])

class InsertHistoryItem(Commandline):
    def _add_args(self, parser):
        add_arg = parser.add_argument        
        add_arg('--app-name', nargs=1, default=[None])

    def main(self, args):
        if args.app_name[0] == None:
            app_name = raw_tmux.get_tmux().current_session().current_window().name
        else:
            app_name = args.app_name[0]
        print(named_histories.pick_cmd(app_name))

def history_add_cmd(args):
    pass
