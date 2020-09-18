import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import server as sv

class MainView():

    def __init__(self, mainTk):
        self.serverOn = False
        self.mainTk = mainTk
        self.mainTk.title("Trabalho SD")
        self.mainTk.geometry('400x430')
        
        self.menubar = tk.Menu(self.mainTk, bg='#366998')
        self.blankmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="".ljust(83), menu=self.blankmenu, activebackground="#366998")
        self.helpMenu = tk.Menu(self.menubar, bg='#E66C63')
        self.menubar.add_cascade(label="Ajuda", menu=self.helpMenu, foreground="white", activebackground="#366998")
        self.mainTk.config(menu=self.menubar)

        self.frameTitle = tk.Frame(self.mainTk)
        self.frameServer = tk.Frame(self.mainTk)
        self.frameReturn = tk.Frame(self.mainTk)
        self.frameInput = tk.Frame(self.mainTk, width=40)
        self.frameTable = tk.Frame(self.mainTk)
        self.frameTitle.pack()
        self.frameServer.pack()
        self.frameReturn.pack()
        self.frameInput.pack()
        self.frameTable.pack()

        self.labelGUI = tk.Label(self.frameTitle, text="Tuple Spaces Demo", font=(None, 18))
        self.labelGUI.pack(pady=(10, 0))

        self.labelServer = tk.Label(self.frameServer, text="Server:", bg="#232323", fg="#329C28", width=47)
        self.labelServer.pack(pady=(10, 0))

        self.labelResponseString = tk.StringVar(value="resposta do server aqui")
        self.labelResponse = tk.Label(self.frameReturn, textvariable=self.labelResponseString, bg="#232323", fg="#329C28", width=47, height=3)
        self.labelResponse.pack(pady=(0, 10))

        self.inputParameters = tk.Entry(self.frameInput, width=25)
        self.inputParameters.pack(side="left", padx=(0, 5))

        self.buttonSubmit = tk.Button(self.frameInput, text="Ok", width=5)
        self.buttonSubmit.pack(side="right")
        self.buttonSubmit.bind("<Button-1>", lambda event, arg=self.inputParameters: self.okClick(event, self.inputParameters))

        self.operation = tk.StringVar()
        self.combobox = ttk.Combobox(self.frameInput, width = 10 , textvariable = self.operation)
        self.combobox.pack(side="right", padx=(0,5))
        self.operationsList = ["read", "write", "take"]
        self.combobox['values'] = self.operationsList
        self.combobox.bind("<<ComboboxSelected>>", lambda event, arg=self.operation: self.operationClick(event, self.operation))

        self.listForTable = [("Class", "Description"),
                            ("bool", "boolean value"),
                            ("int", "integer (arbitrary magnitude)"),
                            ("float", "floating-point number"),
                            ("list", "mutable sequence of objects"),
                            ("tuple", "immutable sequence of objects"),
                            ("str", "character string"),
                            ("set", "unordered set of distinct objects"),
                            ("frozenset", "immutable form of set class"),
                            ("dict", "associative mapping (aka dictionary)")
                        ]
        totalRows = len(self.listForTable) 
        totalColumns = len(self.listForTable[0]) 

        for i in range(totalRows):
            for j in range(totalColumns):
                if(j == 0):
                    if(i == 0):
                        self.entry = tk.Entry(self.frameTable, width=13, font=("Calibri", 9, "bold"))
                    else:
                        self.entry = tk.Entry(self.frameTable, width=13, font=("Calibri", 9))
                else:
                    if(i == 0):
                        self.entry = tk.Entry(self.frameTable, width=33, font=("Calibri", 9, "bold"))
                    else:
                        self.entry = tk.Entry(self.frameTable, width=33, font=("Calibri", 9))
                if(i == 0):
                    self.entry.grid(row=i, column=j, pady=(10, 0))
                else:
                    self.entry.grid(row=i, column=j)
                self.entry.insert(0, self.listForTable[i][j])
            
    def helpClick(self):
        pass

    def operationClick(self, event, operation):
        self.operation = operation.get()
    
    def initializeServer(self):
        self.server = sv.Server()
        self.serverOn = True

    def okClick(self, event, parameters):
        parameters = parameters.get()

        if(parameters == ""):
            self.serverResponse("Digite os parâmetros.")
            return

        if(self.serverOn == False):
            responseString = self.initializeServer(('', 8000))

        if(self.operation == "read"):
            responseString = self.server.read()

        elif(self.operation == "write"):
            responseString = self.server.write()

        elif(self.operation == "take"):
            responseString = self.server.take()

        else: 
            self.serverResponse("Escolha um tipo de operação válido.")
            return

        self.serverResponse(responseString)
    
    def serverResponse(self, responseString):
        self.labelResponseString.set(responseString)
