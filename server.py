from xmlrpc.server import SimpleXMLRPCServer
import SimpleTS


class Server:
    _server_methods = [
        'hello_world',
        'tuple_space_rt',
        'tuple_space_rd',
        'tuple_space_out',
        'tuple_space_all',
        'tuple_space_ref_in',
        'tuple_space_ref_rd',
        'tuple_space_ref_out',
        'tuple_space_ref_eval',
        'provide_tuple_space',
    ]

    def __init__(self, address):
        self._server = SimpleXMLRPCServer(address, allow_none=True)
        self.tuple_space = SimpleTS.TupleSpace()

        for method in self._server_methods:
            self._server.register_function(getattr(self, method))

    def hello_world(self):
        return "Hello World"

    def tuple_space_rt(self, template=()):
        return (str(self.tuple_space.rt(template)))

    def tuple_space_rd(self, template=()):
        return "teste" + str(self.tuple_space.rd(template))

    def tuple_space_out(self, t):
        try:
            self.tuple_space.out(t)
            return t
        except Exception as e:
            return str(e)

    def tuple_space_all(self):
        return self.tuple_space.all()

    def tuple_space_ref_in(self, ts, template=()):
        SimpleTS.TupleSpaceRef(ts).rt(template)

    def tuple_space_ref_rd(self, ts, template=()):
        SimpleTS.TupleSpaceRef(ts).rd(template)

    def tuple_space_ref_out(self, ts, t):
        SimpleTS.TupleSpaceRef(ts).out(t)

    def tuple_space_ref_eval(self, ts, pre_tuple, func, args, post_tuple=()):
        SimpleTS.TupleSpaceRef(ts).eval(pre_tuple, func, args, post_tuple)

    def provide_tuple_space(self, ts):
        """Host a named tuple space in this process"""
        ts = SimpleTS.TupleSpace()
        # pyrocomm.provide_object(ts, _tsName2PyroName(tsName))
        SimpleTS.TupleSpaceRef(ts)

    def init_server(self):
        self._server.serve_forever()

if __name__ == '__main__':
    server = Server(('', 20064))
    print("Server started.")
    server.init_server()