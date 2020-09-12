from xmlrpc.server import SimpleXMLRPCServer
from tuplespace import TupleSpace

class Server:
    _server_methods = [
        'hello_world',
        'write',
        'read',
        'take',
        'get_all_tuples',
    ]

    def __init__(self, address):
        self._server = SimpleXMLRPCServer(address, allow_none=True)
        self.tuple_space = TupleSpace()

        for method in self._server_methods:
            self._server.register_function(getattr(self, method))

    def write(self, t):
        t = tuple(t)
        return self.tuple_space.write(t)

    def read(self, t):
        t = tuple(t)
        return self.tuple_space.read(t)

    def take(self, t):
        t = tuple(t)
        return self.tuple_space.take(t)

    def get_all_tuples(self):
        self.tuple_space.getAllTuples()

    def init_server(self):
        self._server.serve_forever()

if __name__ == '__main__':
    server = Server(('', 8000))
    print("Server started.")
    server.init_server()