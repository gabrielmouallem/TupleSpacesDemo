from tuplespace import TupleSpace
import tkinter as tk
from PIL import ImageTk, Image
from views import MainView as mv

mainTk = tk.Tk()
mainTk.resizable(width=False, height=False)
mv.MainView(mainTk) 
mainTk.mainloop()

# t = ('teste1', 10, 'string2', {'chave': 1})
# tu = ['teste1', 1, 2]

# tupla = TupleSpace()
# tupla.write(t)
# print(tupla.getTupleSpaceLength())
# print(tupla.take(t))
# print(tupla.getTupleSpaceLength())