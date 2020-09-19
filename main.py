from tuplespace import TupleSpace
import tkinter as tk
from PIL import ImageTk, Image
from views import MainView as mv
# from views import OffilineMainView as mv

### Online version ###
mainTk = tk.Tk()
mainTk.resizable(width=False, height=False)
mv.MainView(mainTk) 
mainTk.mainloop()

### Offline Testing version ###
# mainTk = tk.Tk()
# mainTk.resizable(width=False, height=False)
# mv.MainView(mainTk) 
# mainTk.mainloop()