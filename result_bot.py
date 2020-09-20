from xmlrpc.client import ServerProxy
import time

def soma(num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    return float(num1 + num2)

def subtrai(num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    return float(num1 - num2)

def multiplica(num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    return float(num1 * num2)

def divisao(num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    try:
        divisao = num1/num2
        return float(divisao)
    except ZeroDivisionError:
        return float(0)

if __name__ == "__main__":
    
    server = ServerProxy("http://localhost:8000", allow_none=True)

    while(True):

        chave_cliente = 'calculos'
        chave_resultado_ops = 'resultados'

        numeros_cliente = server.read((chave_cliente, int(), int()))

        if numeros_cliente['data'] == -1:
            print("Não achou a tupla calculos.")
            pass
        else:
            print("Tupla calculos encontrada.")
            primeiro_numero = numeros_cliente['data'][1]
            segundo_numero = numeros_cliente['data'][2]

            soma_numeros = soma(primeiro_numero, segundo_numero)
            sub_numeros = subtrai(primeiro_numero, segundo_numero)
            mult_numeros = multiplica(primeiro_numero, segundo_numero)
            div_numeros = divisao(primeiro_numero, segundo_numero)

            tupla_resposta = (chave_resultado_ops, soma_numeros, sub_numeros, mult_numeros, div_numeros)

            read_tupla_resposta = server.read(tupla_resposta)

            if read_tupla_resposta['data'] == -1:
                print("Tupla resposta não existia, resposta escrita!")
                server.write(tupla_resposta)
            else:
                if tupla_resposta != tuple(read_tupla_resposta['data']):
                    server.take(tupla_resposta)
                    server.write(tupla_resposta)
                    print("Tupla já existia, resposta escrita!")
                else:
                    print("Resposta não mudou, nada a fazer...")
