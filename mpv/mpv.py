from .socketlib import cmdsocket


class Mpv(object):
    def __init__(self, address):
        self._addr = address

    def _wrappercall(self, *args):
        with cmdsocket(self._addr) as s:
            status, output = s.do_command(*args)
        return status, output

    def get_playlist(self):
        status, output = self._wrappercall("get_property", "playlist")
        if not status:
            return []
        else:
            return output

    def get_index(self):
        status, output = self._wrappercall("get_property", "playlist-pos")
        if not status:
            return -1
        else:
            return output

    def set_index(self, index):
        status, _ = self._wrappercall("set_property", "playlist-pos", index)
        return status

    def dispatch(self, func, *args):
        return getattr(self, func)(*args)

    def get_filename(self):
        status, filename = self._wrappercall("get_property", "filename/no-ext")
        if not status:
            return None
        else:
            return filename

    def is_playing(self):
        status, pause = self._wrappercall("get_property", "pause")
        if not status:
            return True
        return not pause

    def toggle_playing(self):
        status, _ = self._wrappercall("cycle", "pause")
        return status
