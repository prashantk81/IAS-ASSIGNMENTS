from rpc_client import *
HOSTNAME = '127.0.0.1'
PORTNUMBER = 1234
client = connectToServer(HOSTNAME, PORTNUMBER)
print(client.foo(2323))
print(client.bar(2, "Ashish"))
print(client.random_rating())
