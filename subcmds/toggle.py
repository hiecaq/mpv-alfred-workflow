from os.path import split

from cli import Subcommand
from mpv import Mpv


class TogglePlayingSubcommand(Subcommand):
    def __init__(self):
        Subcommand.__init__(
            self, "toggle", help="toggle whether playing the current file"
        )

    def init(self, parser):
        parser.set_defaults(func=self._action)

    def _playing(self, args):
        pass

    def _action(self, args):
        playing = Mpv(args["socket"]).is_playing()
        if not Mpv(args["socket"]).toggle_playing():
            return "failed"
        return " ".join([
            "playing:" if not playing else "paused:",
            split(Mpv(args["socket"]).get_filename())[1]
        ])
