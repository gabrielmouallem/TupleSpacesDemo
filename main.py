from tuplespace import TupleSpace

t = ('teste1', 10, 'string2', {'chave': 1})
tu = ['teste1', 1, 2]

tupla = TupleSpace()
tupla.write(t)
print(tupla.getTupleSpaceLength())
print(tupla.take(t))
print(tupla.getTupleSpaceLength())