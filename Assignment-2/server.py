from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

addr = ('127.0.0.1', 3000)
authorizer = DummyAuthorizer()
authorizer.add_user('prashant', 'prashant', '.', perm='elradfmw')
authorizer.add_user('ujjwal', 'ujjwal', '.', perm='elradfmw')
authorizer.add_user('raghav', 'raghav', '.', perm='elradfmw')
authorizer.add_user('rishabh', 'rishabh', '.', perm='elradfmw')
authorizer.add_user('priyank', 'priyank', '.', perm='elradfmw')

handler = FTPHandler
handler.authorizer = authorizer
server = FTPServer(addr, handler)
server.serve_forever()
