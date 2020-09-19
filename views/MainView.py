import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from xmlrpc.client import ServerProxy

class MainView():

    def __init__(self, mainTk):
        self.server = ServerProxy("http://localhost:8000", allow_none=True)

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

        self.labelResponseString = tk.StringVar(value="")
        self.labelResponse = tk.Label(self.frameReturn, textvariable=self.labelResponseString, bg="#232323", fg="#329C28", width=47, height=3)
        self.labelResponse.pack(pady=(0, 10))

        self.inputParameters = tk.Entry(self.frameInput, width=25)
        self.inputParameters.pack(side="left", padx=(0, 5))

        self.buttonSubmit = tk.Button(self.frameInput, text="Ok", width=5)
        self.buttonSubmit.pack(side="right")
        self.buttonSubmit.bind("<Button-1>", lambda event, arg=self.inputParameters: self.okClick(event, self.inputParameters))

        self.operation = tk.StringVar()
        self.selectedOption = None
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
        self.selectedOption = operation.get()
    
    def okClick(self, event, parameters):
        parameters = parameters.get()
        tupleItemsWithType = parameters.split("&&")
        items = []
        for index, item in enumerate(tupleItemsWithType):
            itemValue = item.split("::")[0]
            itemType = item.split("::")[1]

            if itemType == "string":
                if itemValue == "":
                    itemValue = str("")
                else:
                    itemValue = str(itemValue)

            elif itemType == "int":
                if itemValue == "":
                    itemValue = int(0)
                else:
                    itemValue = int(itemValue)

            elif itemType == "bool":
                if itemValue == "":
                    itemValue = bool(True)
                if(itemValue == "False"):
                    itemValue = False
                elif(itemValue == "True"):
                    itemValue = True

            elif itemType == "float":
                if itemValue == "":
                    itemValue = float(0.00)
                else:
                    itemValue = float(itemValue)

            elif itemType == "list":
                if itemValue == "":
                    itemValue = list([])
                else:
                    itemValue = list(itemValue)

            elif itemType == "tuple":
                if itemValue == "":
                    itemValue = tuple(())
                else:
                    itemValue = tuple(itemValue)

            elif itemType == "dict":
                if itemValue == "":
                    itemValue = dict({})
                else:
                    itemValue = eval(itemValue)        

            items.append(itemValue)
        
        inputTuple = tuple(items)
        print(inputTuple)

        if(parameters == ""):
            self.serverResponse("Digite os parâmetros.", "ERROR")
            return

        if(self.selectedOption == "read"):
            server_return = self.server.read(inputTuple)
            responseString = server_return['response']
            responseStatus = server_return['status']

        elif(self.selectedOption == "write"):
            server_return = self.server.write(inputTuple)
            responseString = server_return['response']
            responseStatus = server_return['status']

        elif(self.selectedOption == "take"):
            server_return = self.server.take(inputTuple)
            responseString = server_return['response']
            responseStatus = server_return['status']

        else: 
            self.serverResponse("Escolha um tipo de operação válido.", "ERROR")
            return

        self.serverResponse(responseString, responseStatus)
    
    def serverResponse(self, responseString, responseStatus):
        self.labelResponseString.set(responseString)

        if(responseStatus == "ERROR"):
            self.labelResponse.configure(fg="red")
        else:
            self.labelResponse.configure(fg="#329C28")

