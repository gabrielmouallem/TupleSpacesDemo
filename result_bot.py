from xmlrpc.client import ServerProxy
import time

def soma(num1, num2):
    return float(num1 + num2)

def subtrai(num1, num2):
    return float(num1 - num2)

def multiplica(num1, num2):
    return float(num1 * num2)

def divisao(num1, num2):
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
            print("Tupla não encontrada ou já foi escrita.")
            pass
        else:
            print(numeros_cliente)
            primeiro_numero = numeros_cliente['data'][1]
            segundo_numero = numeros_cliente['data'][2]

            soma_numeros = soma(primeiro_numero, segundo_numero)
            sub_numeros = subtrai(primeiro_numero, segundo_numero)
            mult_numeros = multiplica(primeiro_numero, segundo_numero)
            div_numeros = divisao(primeiro_numero, segundo_numero)

            temp_tupla_resposta = (chave_resultado_ops, float(), float(), float(), float())
            tupla_resposta = (chave_resultado_ops, soma_numeros, sub_numeros, mult_numeros, div_numeros)

            take_tupla_resposta = server.take(temp_tupla_resposta)

            if take_tupla_resposta['data'] != -1:
                print("Tupla ja existia, escrevendo nela")
                server.write(tupla_resposta)
            else:
                if tupla_resposta != take_tupla_resposta['data'] or take_tupla_resposta['data'] == -1:
                    server.write(tupla_resposta)
                    print("Tupla resposta escrita!")
