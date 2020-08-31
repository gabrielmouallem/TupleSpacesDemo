"""
Test program for SimpleTS.

Author :        John Markus Bjorndalen <johnm@cs.uit.no>
Version:        1.1
"""
import SimpleTS
import time

TupleSpace = SimpleTS.TupleSpace()
time.sleep(1)


def test():
    print("**** test function, 'computing' for a while")
    time.sleep(3)
    print("**** test function ready to return")
    return "this is a test"


TupleSpaceRef = SimpleTS.TupleSpaceRef(TupleSpace)

# Add something to the tuple space using eval
TupleSpaceRef.eval((1, 2), test, (), (3, 4))

# Wait for it, first with rd
print("--- Client trying to read returned value")
ret = TupleSpaceRef.rd()
print("--- Rd returned", ret)
ret = TupleSpaceRef._in((1, 2, SimpleTS.MatchAny(), 3))
print("--- In returned", ret)
