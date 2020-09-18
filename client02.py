from xmlrpc.client import ServerProxy

if __name__ == "__main__":
    
    server = ServerProxy("http://localhost:8000", allow_none=True)

    chave = 'calculos'
    chave_resposta = 'resultados'

    primeiro_num = 99 # float(input(print("Digite o primeiro número: ")))
    segundo_num = 99 # float(input(print("Digite o segundo número: ")))

    temp_tupla = (chave, int(), int())
    print(server.take(temp_tupla)['data'])

    tupla = (chave, primeiro_num, segundo_num)
    print(server.write(tupla)['data'])
