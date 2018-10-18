import json
import socket
import unicodedata
from contextlib import contextmanager

SERVER_ADDRESS = '/tmp/mpvsocket'


class UnixDomainSocket(object):
    def __init__(self, address):
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._addr = address

    def connect(self):
        self._socket.connect(self._addr)

    def close(self):
        self._socket.close()

    def send_recv(self, raw):
        """Send bytes to the mpv socket, and return the bytes of the
        recved feedback.

        :param bytes raw: the given raw
        :rtypes: bytes

        """
        try:
            self._socket.sendall(b''.join([raw, b'\n']))
            recved = []
            while True:
                got = self._socket.recv(1024)
                recved.append(got)
                if got.rfind(b'\n') != -1:
                    break
            data = b''.join(recved).rstrip(b'\n')

        except Exception as e:
            raise e

        return data


class MessageSocket(UnixDomainSocket):
    def __init__(self, address):
        UnixDomainSocket.__init__(self, address)

    def send_recv_message(self, message):
        """Send a string to the mpv socket, and return the feedback in str.

        :param str message: the given message
        :rtypes: str

        """
        feedback = self.send_recv(message.encode()).decode("utf-8")
        return unicodedata.normalize("NFKC", feedback)


class JsonSocket(MessageSocket):
    def __init__(self, address):
        MessageSocket.__init__(self, address)

    def send_recv_json(self, jsn):
        """Send a json to the mpv socket, and return the feedback as a json.

        :param dict jsn: an json being sent
        :rtypes: dict

        """
        return json.loads(self.send_recv_message(json.dumps(jsn)))


class CommandSocket(JsonSocket):
    """Docstring for CommandSocket. """

    def __init__(self, address):
        JsonSocket.__init__(self, address)

    def do_command(self, *argv):
        """Send the command args to mpv, and return the feedback.

        :param argv: a list of command args
        """
        result = self.send_recv_json({"command": argv})
        if result["error"] == "success":
            return True, result["data"] if "data" in result else None
        else:
            return False, None


@contextmanager
def cmdsocket(address):
    skt = CommandSocket(address)
    try:
        skt.connect()
        yield skt
    finally:
        skt.close()
