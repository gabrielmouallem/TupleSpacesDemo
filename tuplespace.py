import threading


# def syncronized(func):
#     def sync(self, *args, **kws):
#
#         self.blocked.acquire()
#
#         try:
#             return func(self, *args, **kws)
#         finally:
#             self.blocked.release()
#
#     return sync


class TupleSpace:

    def __init__(self):
        # self.blocked = threading.Condition()
        self.length = 0
        self.tuples = []

    # insere a tupla no espaço de tuplas
    # @syncronized
    def write(self, t):

        # será inserida no final de uma lista (representando o espaço de tuplas)
        # sem afetar as tuplas que já foram inseridas
        if self.verifyTuple(t):
            self.tuples.append(t)
            self.length += 1
            # self.blocked.notify_all()
            return {
                "data": t,
                "response": "Tupla " + str(t) + " escrita com sucesso!",
                "status": "OK"
            }
        else:
            return {
                "data": -1,
                "response": "Erro ao escrever tupla " + str(t) + ".",
                "status": "ERROR"
            }

    # lê uma tupla do espaço de tuplas
    def read(self, t):

        if self.verifyTuple(t):
            # irá procurar por uma tupla no espaço e retorná-la
            tuple_found = self.getTuple(t)

            # tupla não encontrada ou espaço de tuplas está vazio
            if tuple_found == -1:
                return {
                    "data": -1,
                    "response": "Tupla " + str(t) + " não encontrada.",
                    "status": "ERROR"
                }

            return {
                "data": t,
                "response": "Tupla " + str(t) + " encontrada.",
                "status": "OK"
            }
        else:
            return {
                "data": -1,
                "response": "Por favor insira uma tupla!",
                "status": "ERROR"
            }

    # lê uma tupla do espaço de tuplas
    def take(self, t):

        if self.verifyTuple(t):
            # irá procurar por uma tupla, retornar e removê-la do espaço
            tuple_found = self.getTuple(t)

            # tupla não encontrada ou espaço de tuplas está vazio
            if tuple_found == -1:
                return {
                    "data": -1,
                    "response": "Tupla " + str(t) + " não encontrada.",
                    "status": "ERROR"
                }

            # remove a tupla do espaço de tuplas
            self.removeTuple(tuple_found)

            return {
                "data": t,
                "response": "Tupla " + str(t) + " encontrada.",
                "status": "OK"
            }
        else:
            return {
                "data": -1,
                "response": "Por favor insira uma tupla!",
                "status": "ERROR"
            }

    def removeTuple(self, t):

        try:
            # remove a tupla do espaço e decrementa o tamanho do espaço
            self.tuples.remove(t)
            self.length -= 1

            return {
                "data": t,
                "response": "Tupla" + str(t) + "removida com sucesso!",
                "status": "OK"
            }


        except Exception as ex:
            return {
                "data": -1,
                "response": "Não foi possível remover a tupla. " + str(ex),
                "status": "ERROR"
            }

    # irá procurar por uma tupla e retorná-la
    # @syncronized
    def getTuple(self, t):

        # self.blocked.wait()
        found = True

        # espaço de tuplas está vazio
        if self.length == 0:
            return {
                "data": -1,
                "response": "Não foi possível remover a tupla.",
                "status": "ERROR"
            }

        # não foi passado nenhum parâmetro
        # retorna todas as tuplas
        if len(t) == 0:
            self.getAllTuples()

        else:
            # procura a tupla no espaço
            for tup in self.tuples:

                current_tuple = tup

                for index in range(len(t)):

                    # verfica se os valores e os tipos das tuplas são iguais
                    if t[index] == current_tuple[index] and type(t[index]) == type(current_tuple[index]):
                        continue

                    found = False
                    break

                # se encontrou uma tupla, retorna ela
                if found:
                    return {
                        "data": current_tuple,
                        "response": "Tupla encontrada" + str(current_tuple) + ".",
                        "status": "OK"
                    }

            return {
                "data": -1,
                "response": "Tupla não foi encontrada.",
                "status": "ERROR"
            }

        # notifica todos os outros computadores que o espaço não tá mais bloqueado
        # self.blocked.notifyAll()

    # retorna todas as tuplas que foram inseridas no espaço
    def getAllTuples(self):
        try:
            return {
                "data": self.tuples,
                "response": "Tuplas: " + str(self.tuples),
                "status": "OK"
            }

        except Exception as ex:
            return {
                "data": -1,
                "response": "Ocorreu um problema ao pegar todas as tuplas. " + str(ex),
                "status": "ERROR"
            }

    # retorna a quantidade de tuplas inseridas no espaço
    def getTupleSpaceLength(self):
        return self.length

    # verifica se a variável é uma tupla
    def verifyTuple(self, t):

        if type(t) != tuple:
            return False

        return True