from xmlrpc.client import ServerProxy

if __name__ == "__main__":
    
    server = ServerProxy("http://localhost:8000", allow_none=True)

    chave = 'calculos'

    primeiro_num = 1 # float(input(print("Digite o primeiro número: ")))
    segundo_num = 1 # float(input(print("Digite o segundo número: ")))

    tupla = (chave, primeiro_num, segundo_num)
    print(server.write(tupla)['data'])
