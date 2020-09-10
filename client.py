from xmlrpc.client import ServerProxy

if __name__ == '__main__':
    server = ServerProxy("https://0dd2c1843cf6.ngrok.io", allow_none=True)

    print(server.hello_world())
    temp_tuple = ('teste', 1, 2, 3)
    print(server.write(temp_tuple))
