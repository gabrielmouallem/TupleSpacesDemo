from xmlrpc.client import ServerProxy

if __name__ == "__main__":
    
    server = ServerProxy("https://c9c13e8e4232.ngrok.io/", allow_none=True)

    chave = 'calculos'
    chave_resposta = 'resultados'

    primeiro_num = float(input(print("Digite o primeiro número: ")))
    segundo_num = float(input(print("Digite o segundo número: ")))

    tupla = tuple(chave, primeiro_num, segundo_num)
    server.tuple_space.write(tupla)

    resultados = server.tuple_space.take(tuple(chave_resposta))

    if resultados == -1:
        print("Tupla não encontrada!")
    else:
        print(primeiro_num + " + " + segundo_num + " = " + resultados(1))
        print(primeiro_num + " - " + segundo_num + " = " + resultados(2))
        print(primeiro_num + " * " + segundo_num + " = " + resultados(3))
        print(primeiro_num + " / " + segundo_num + " = " + resultados(4))
