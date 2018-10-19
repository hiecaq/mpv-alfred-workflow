#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
import inspect
import json
import sys

from cli import Command, Subcommand


class MpvCommand(Command):
    def __init__(self):
        Command.__init__(
            self,
            description="mpv ipc call cmdline wrapper",
            allow_abbrev=False
        )
        self._parser.add_argument(
            "-s",
            "--socket",
            metavar="SOCKET",
            help="the socket location",
            type=str,
            default="/tmp/mpvsocket"
        )


def main(args):
    c = MpvCommand()

    subcmds = [
        v() for _, v in vars(importlib.import_module("subcmds")).items()
        if inspect.isclass(v) and issubclass(v, Subcommand)
    ]

    c.add(*subcmds)
    output = c.run(args)
    if isinstance(output, str):
        print(output)
    else:
        print(json.dumps(output))


if __name__ == "__main__":
    main(sys.argv[1:])
