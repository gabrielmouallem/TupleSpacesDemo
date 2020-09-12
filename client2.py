from xmlrpc.client import ServerProxy

def soma(num1, num2):
    return num1 + num2

def subtrai(num1, num2):
    return num1 - num2

def multiplica(num1, num2):
    return num1 * num2

def divisao(num1, num2):
    try:
        divisao = num1/num2
        return divisao
    except ZeroDivisionError:
        return 0

if __name__ == "__main__":
    
    server = ServerProxy("http://localhost:8000", allow_none=True)

    while(True):

        chave_cliente = 'calculos'
        chave_resultado_ops = 'resultados'

        numeros_cliente = server.take((chave_cliente, 0, 0))

        print(numeros_cliente)

        if numeros_cliente['data'] == -1:
            print("Tupla não encontrada!")
        else:
            primeiro_numero = numeros_cliente['data'][1]
            segundo_numero = numeros_cliente['data'][2]

            soma_numeros = soma(primeiro_numero, segundo_numero)
            sub_numeros = subtrai(primeiro_numero, segundo_numero)
            mult_numeros = multiplica(primeiro_numero, segundo_numero)
            div_numeros = divisao(primeiro_numero, segundo_numero)

            tupla_resposta = (chave_resultado_ops, soma_numeros, sub_numeros, mult_numeros, div_numeros)
            resposta = tuple(server.read(tupla_resposta)['data'])

            print(tupla_resposta, resposta)
            if tupla_resposta != resposta:
                server.write(tupla_resposta)
                print("Tupla resposta escrita!")