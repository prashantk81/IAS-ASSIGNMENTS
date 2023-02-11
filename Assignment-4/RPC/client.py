from rpc_client import *
HOSTNAME = '127.0.0.1'
PORTNUMBER = 12346
client = connectToServer(HOSTNAME, PORTNUMBER)
print(client.foo(23))
print(client.bar(11, "Ashish"))
print(client.random_rating())
