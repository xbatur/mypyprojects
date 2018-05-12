from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import getpass,os
from pathlib import Path
import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
ipadress = get_ip_address()
username = getpass.getuser()
homefolder = str(Path.home())
authorizer = DummyAuthorizer()
authorizer.add_user("xboomer", "12345", homefolder, perm="elradfmwM")
authorizer.add_anonymous(homefolder, perm="r")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer((ipadress, 1026), handler)
server.serve_forever()
