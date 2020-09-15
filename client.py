from xmlrpc.client import ServerProxy

if __name__ == "__main__":
    
    server = ServerProxy("http://localhost:8000", allow_none=True)

    chave = 'calculos'
    chave_resposta = 'resultados'

    primeiro_num = 12 # float(input(print("Digite o primeiro número: ")))
    segundo_num = 12 # float(input(print("Digite o segundo número: ")))

    tupla = (chave, primeiro_num, segundo_num)
    server.write(tupla)

    # resultados = server.take((chave_resposta))
    #
    # if resultados == -1:
    #     print("Tupla não encontrada!")
    # else:
    #     print(primeiro_num + " + " + segundo_num + " = " + resultados(1))
    #     print(primeiro_num + " - " + segundo_num + " = " + resultados(2))
    #     print(primeiro_num + " * " + segundo_num + " = " + resultados(3))
    #     print(primeiro_num + " / " + segundo_num + " = " + resultados(4))
