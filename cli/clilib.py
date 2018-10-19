import argparse


class Subcommand(object):
    def __init__(self, *args, **kargs):
        self._kargs = kargs
        self._args = args
        self._callback = None

    def register(self, subparsers: argparse._SubParsersAction):
        parser = subparsers.add_parser(*self._args, **self._kargs)
        self.init(parser)

    def init(self, parser: argparse.ArgumentParser):
        if self._callback is not None:
            self._callback(parser)
        else:
            pass


class Command(object):
    def __init__(self, *args, **kargs):
        self._parser = argparse.ArgumentParser(*args, **kargs)
        self.subparsers = self._parser.add_subparsers(dest='cmd')

    def run(self, args):
        parsed = vars(self._parser.parse_args(args))
        if 'func' in parsed:
            return parsed['func'](parsed)
        else:
            self._parser.print_usage()
            return ""

    def add(self, *subcmds):
        for subcmd in subcmds:
            subcmd.register(self.subparsers)

    def subcommand(self, *args, **kargs):
        def subcommand_decorator(func: callable):
            subcmd = Subcommand(*args, **kargs)
            subcmd._callback = func
            self.add(subcmd)

        return subcommand_decorator
