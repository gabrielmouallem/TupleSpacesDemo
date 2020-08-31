"""
SimpleTS - a simplified TupleSpace implementation using Pyro (Python Remote Objects). 

Author :        John Markus Bjorndalen <johnm@cs.uit.no>
Version:        1.1
"""
import types
import threading
import copy


class MatchAny:
    """Used to indicate a wildcard in tuple templates for In and Rd"""
    pass


def synchronized(func):
    """Decorator for creating java-like monitor functions"""

    def _call(self, *args, **kwargs):
        self._cond.acquire()
        try:
            return func(self, *args, **kwargs)
        finally:
            self._cond.release()

    return _call


class TupleSpace:
    def __init__(self):
        self._tuples = []
        self._cond = threading.Condition()

    def rt(self, template=()):
        """Retrieve a tuple matching 'template' (default () = 'ANY') from the tuple space."""
        return self._get_tuple(template, True)

    def rd(self, template=()):
        """Read a tuple matching 'template' (default () = 'ANY') from the tuple space."""
        return self._get_tuple(template, False)

    @synchronized
    def out(self, t):
        """Add a tuple 't' to the tuple space."""
        self._tuples.append(t)
        # wake up readers to allow them to search for matching tuples again
        self._cond.notifyAll()

    def all(self):
        """Searches for a matching tuple in the tuple space. The search pattern can
        be shorter than the matched tuple. (TODO: should have a more regex-like match)."""
        tuples = []
        for idx in range(len(self._tuples)):
            tuples.append(self._tuples[idx])
        return tuples


    @synchronized
    def _get_tuple(self, t, remove):
        """Retrieves a tuple from the tuple space. Removes the tuple from the tuplespace if
        'remove' is true. Blocks if there is no matching tuple."""
        idx = self._match_tuple(t)
        while idx < 0:
            self._cond.wait()
            idx = self._match_tuple(t)
        ret = self._tuples[idx]
        if remove:
            del self._tuples[idx]
        return ret

    def _match_tuple(self, t):
        """Searches for a matching tuple in the tuple space. The search pattern can
        be shorter than the matched tuple. (TODO: should have a more regex-like match)."""
        for idx in range(len(self._tuples)):
            c = self._tuples[idx]  # candidate tuple
            if len(c) < len(t):
                continue  # candidate too short
            found = True
            for i in range(len(t)):
                if isinstance(t[i], MatchAny):
                    continue
                if t[i] == c[i]:
                    continue
                # didn't match this idx, so fail this index
                found = False
                break
            if found:
                return idx
        return -1  # nothing found so far


class TupleSpaceRef:
    """This class is instantiated locally in the client and takes care
    of thread safety issues with Pyro Proxy objects, as well as
    Eval. The copy.copy method is per suggestion from the Pyro
    documentation. A cleaner way than the TupleSpaceRef class is left
    for future work."""

    def __init__(self, ts):
        self._ts = ts

    def _get_safe_ref(self):
        """Returns a 'thread-safe' reference to the object (for now, a copy if it's a proxy object, self if we have a
        reference to the real tuple space"""
        if isinstance(self._ts, TupleSpace):
            return self._ts
        return copy.copy(self._ts)

    def rt(self, template=()):
        """Retrieve a tuple matching 'template' (default () = 'ANY') from the tuple space."""
        return self._get_safe_ref()._in(template)

    def rd(self, template=()):
        """Read a tuple matching 'template' (default () = 'ANY') from the tuple space."""
        return self._get_safe_ref().rd(template)

    def out(self, t):
        return self._get_safe_ref().out(t)

    def eval(self, pre_tuple, func, args, post_tuple=()):
        """Fires off a thread that executes the given function. The returned value is stored as a tuple.
        NB: this function will be evaluated locally, not in the ts-hosting process. A 'remote-execute'
        parameter is on the todo-list"""
        # The typechecking code and the idea to use post and pre tuples comes from PyBrenda
        if type(pre_tuple) != tuple:
            raise ValueError("not a tuple: " + repr(pre_tuple))

        elif type(func) != types.BuiltinFunctionType and type(func) != types.FunctionType:
            raise ValueError("not a function:  " + repr(func))

        elif type(args) != tuple:
            raise ValueError("not a tuple: " + repr(args))

        elif type(post_tuple) != tuple:
            raise ValueError("not a tuple: " + repr(post_tuple))

        def do_fun(ts, func, args):
            ret = func(*args)
            ts.out(pre_tuple + (ret,) + post_tuple)

        th = threading.Thread(target=do_fun, args=[self, func, args],
                              name="Tuple Space Eval() thread (%s,%s,%s)" % (self, func, args))
        th.setDaemon(True)
        th.start()
