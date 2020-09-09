from xmlrpc.client import ServerProxy

server = ServerProxy("http://ff9c2de17b3a.ngrok.io:8000", allow_none=True)

temp_tuple = ("teste", 1, 2)

print(server.write(temp_tuple))

# response = server.tuple_space_rd()
# print(response)