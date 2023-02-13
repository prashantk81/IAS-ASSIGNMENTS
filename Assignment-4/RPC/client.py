from rpc_client import *
HOSTNAME = '127.0.0.1'
PORTNUMBER = 1238
client = connectToServer(HOSTNAME, PORTNUMBER)
print(client.foo(500))
print(client.bar(21, "Ashish"))
print(client.random_rating())
