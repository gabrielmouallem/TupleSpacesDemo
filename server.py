from xmlrpc.server import SimpleXMLRPCServer
from tuplespace import TupleSpace


class Server:
    _server_methods = [
        'hello_world',
        'write',
        'read',
        'take',
        'getAllTuples',
    ]

    def __init__(self, address):
        self._server = SimpleXMLRPCServer(address, allow_none=True)
        self.tuple_space = TupleSpace()

        for method in self._server_methods:
            self._server.register_function(getattr(self, method))

    def hello_world(self):
        return "hello world"

    def write(self, t):
        return self.tuple_space.write(t)

    def read(self, t):
        return self.tuple_space.read(t)

    def take(self, t):
        return self.tuple_space.take(t)

    def getAllTuples(self):
        self.tuple_space.getAllTuples()

    def init_server(self):
        self._server.serve_forever()

if __name__ == '__main__':
    server = Server(('', 8000))
    print("Server started.")
    server.init_server()