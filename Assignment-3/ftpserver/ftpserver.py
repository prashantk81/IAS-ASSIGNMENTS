from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

addr = ('127.0.0.1', 3000)
authorizer = DummyAuthorizer()
authorizer.add_user('admin', 'adminpass', '..', perm='elradfmw')
handler = FTPHandler
handler.authorizer = authorizer
server = FTPServer(addr, handler)
server.max_cons = 10
server.max_cons_per_ip = 10
server.serve_forever()
