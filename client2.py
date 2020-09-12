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
    
    server = ServerProxy("https://c9c13e8e4232.ngrok.io/", allow_none=True)

    chave_cliente = 'calculos'
    chave_resultado_ops = 'resultados'

    numeros_cliente = server.take(chave_cliente, float, float)

    if numeros_cliente == -1:
        print("Tupla não encontrada!")
    else:
        primeiro_numero = numeros_cliente[1]
        segundo_numero = numeros_cliente[2]

        soma_numeros = soma(primeiro_numero, segundo_numero)
        sub_numeros = subtrai(primeiro_numero, segundo_numero)
        mult_numeros = multiplica(primeiro_numero, segundo_numero)
        div_numeros = divisao(primeiro_numero, segundo_numero)

        tupla_resposta = tuple(chave_resultado_ops, soma_numeros, sub_numeros, mult_numeros, div_numeros)

        server.tuple_space.write(tupla_resposta)