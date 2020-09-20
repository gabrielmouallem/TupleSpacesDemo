import threading

# Único possível problema de implementação: como saber que um usuário (e qual usuário) deu take em uma tupla para previnir que outros usuários dêem write numa tupla com a mesa chave?
# O getTuple bugava antes de ter o goToTypeChecks porque se ele trombasse uma tupla que o primeiro elemento fosse diferente da tupla de comparativo ele dava break e já saia

class TupleSpace:

    def __init__(self):
        self.blocked = threading.Lock()
        self.tuples = []

    # insere a tupla no espaço de tuplas
    def write(self, t):

        # será inserida no final de uma lista (representando o espaço de tuplas)
        # sem afetar as tuplas que já foram inseridas
        if self.verifyTuple(t):
            # print("write(): este object realmente é uma tupla.")
            tuple_found = self.getTuple(t)
            if tuple_found == -1:
                self.tuples.append(t)
                # print("write(): tupla adicionada ao espaço de tuplas.")
                return {
                    "data": t,
                    "response": "Tupla " + str(t) + "\nescrita com sucesso!",
                    "status": "OK"
                }
            else:
                return {
                    "data": -1,
                    "response": "Tupla " + str("("+str(t[0])+", ...)") + "\njá existe, você precisa obtê-la antes de escrevê-la.",
                    "status": "ERROR"
                }

        else:
            # print("write(): este object não é uma tupla, erro.")
            return {
                "data": -1,
                "response": "Erro ao escrever tupla\n" + str(t) + ".",
                "status": "ERROR"
            }

    # lê uma tupla do espaço de tuplas
    def read(self, t):

        if self.verifyTuple(t):
            # print("read(): este object realmente é uma tupla.")
            # irá procurar por uma tupla no espaço e retorná-la
            self.blocked.acquire()
            tuple_found = self.getTuple(t)
            self.blocked.release()

            # tupla não encontrada ou espaço de tuplas está vazio
            if tuple_found == -1:
                # print("read(): a tupla não foi encontrada.")
                return {
                    "data": -1,
                    "response": "Tupla " + str("("+str(t[0])+", ...)") + "\nnão foi lida.",
                    "status": "ERROR"
                }
            # print("read(): a tupla foi encontrada e foi lida.")
            return {
                "data": tuple_found,
                "response": "Tupla " + str(tuple_found) + "\nfoi lida.",
                "status": "OK"
            }
        else:
            # print("read(): este object não é uma tupla, erro.")
            return {
                "data": -1,
                "response": "Tupla em uso ou não existe.",
                "status": "ERROR"
            }

    # lê uma tupla do espaço de tuplas
    def take(self, t):
        if self.verifyTuple(t):
            # print("take(): este object realmente é uma tupla.")
            # irá procurar por uma tupla, retornar e removê-la do espaço
            self.blocked.acquire()
            tuple_found = self.getTuple(t)
            self.blocked.release()

            # tupla não encontrada ou espaço de tuplas está vazio
            if tuple_found == -1:
                # print("take(): a tupla não foi encontrada.")
                return {
                    "data": -1,
                    "response": "Tupla " + str(t) + "\nnão foi obtida.",
                    "status": "ERROR"
                }

            # remove a tupla do espaço de tuplas
            self.removeTuple(tuple_found)
            # print("take(): a tupla foi encontrada e foi removida.")
            return {
                "data": tuple_found,
                "response": "Tupla " + str(tuple_found) + "\nfoi obtida.",
                "status": "OK"
            }
        else:
            # print("take(): este object não é uma tupla, erro.")
            return {
                "data": -1,
                "response": "Tupla em uso ou não existe.",
                "status": "ERROR"
            }

    def removeTuple(self, t):

        try:
            # remove a tupla do espaço e decrementa o tamanho do espaço
            self.tuples.remove(t)
            # print("removeTuple(): Removida com sucesso!")
            return t


        except Exception as ex:
            # print("removeTuple(): Erro ao remover, talvez a tupla não exista.")
            return -1

    # irá procurar por uma tupla e retorná-la
    def getTuple(self, t):

        goToTypeChecks = False
        found = True

        # espaço de tuplas está vazio
        if len(self.tuples) == 0:
            # print("getTuple(): Espaço de tuplas vazio.")
            return -1

        # não foi passado nenhum parâmetro
        # retorna todas as tuplas
        if len(t) == 0:
            return self.getAllTuples()

        else:
            # procura a tupla no espaço
            for _, current_tuple in enumerate(self.tuples):

                for index in range(len(t)):
                    if index == 0:
                        # verifica se o primeiro valor é igual
                        if t[index] == current_tuple[index]:
                            goToTypeChecks = True
                            continue
                        else:
                            # print("getTuple(): Primeiro elemento da tupla não bate. " + str(t[index]) + " " + str(current_tuple[index]))
                            found = False
                            break
                    else:
                        if type(t[index]) == type(current_tuple[index]) and goToTypeChecks:
                            found = True
                            continue
                        else:
                            # print("getTuple(): Os tipos da tupla não batem.")
                            found = False
                            break
                # se encontrou uma tupla, retorna ela
                if found:
                    # print("getTuple(): Tupla encontrada.")
                    return current_tuple

            return -1

    # retorna todas as tuplas que foram inseridas no espaço
    def getAllTuples(self):
        try:
            return self.tuples

        except Exception as ex:
            return -1

    # retorna a quantidade de tuplas inseridas no espaço
    def getTupleSpaceLength(self):
        return len(self.tuples)

    # verifica se a variável é uma tupla
    def verifyTuple(self, t):

        if type(t) != tuple:
            return False

        return True