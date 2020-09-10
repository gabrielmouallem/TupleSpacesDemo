from xmlrpc.client import ServerProxy

server = ServerProxy("https://0dd2c1843cf6.ngrok.io", allow_none=True)

print(server.hello_world())
print(server.write(("teste", 1, 2, 3)))

# response = server.tuple_space_rd()
# print(response)