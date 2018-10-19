from os.path import split

from cli import Subcommand
from mpv import Mpv


class GetPlayListSubcommand(Subcommand):
    def __init__(self):
        Subcommand.__init__(self, "list", help="list the playing filenames")

    def init(self, parser):
        parser.set_defaults(func=self._action)

    def _action(self, args):
        items = []
        for index, item in enumerate(Mpv(args["socket"]).get_playlist()):
            current = "current" in item
            playing = current and "playing" in item
            output = {
                "uid": index,
                "title": split(item["filename"])[1],
                "arg": item["filename"],
                "variables": {
                    "index": index
                }
            }
            if current:
                output["subtitle"] = "playing" if playing else "pause"
                items.insert(0, output)
            else:
                items.append(output)
        return {"items": items}


class SetIndexSubcommand(Subcommand):
    def __init__(self):
        Subcommand.__init__(
            self,
            "set-index",
            help="play the file indexed with the given number"
        )

    def init(self, parser):
        parser.set_defaults(func=self._action)
        parser.add_argument(
            "index",
            metavar="INDEX",
            help="the index of the file wished to play",
            type=int
        )

    def _action(self, args):
        if not Mpv(args["socket"]).set_index(args["index"]):
            return "failed"
        return " ".join([
            "playing:",
            split(Mpv(args["socket"]).get_filename())[1]
        ])
