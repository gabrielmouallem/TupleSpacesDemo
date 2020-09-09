import threading

class TupleSpace:

    def __init__(self):
        self.new_tuple = threading.Condition()
        self.blocked = threading.Condition()
        self.length = 0
        self.tuples = []

    #insere a tupla no espaço de tuplas
    def write(self, t):

        #será inserida no final de uma lista (representando o espaço de tuplas)
        #sem afetar as tuplas que já foram inseridas
        if self.verifyTuple(t):
            self.tuples.append(t)
            self.length += 1
            
            #notifica todos os computadores de que uma nova tupla foi inserida
            #self.new_tuple.notifyAll()
        else:
            raise ValueError("Por favor, insira uma tupla!")

    #lê uma tupla do espaço de tuplas
    def read(self, t):

        if self.verifyTuple(t):
            #irá procurar por uma tupla no espaço e retorná-la
            tuple_found = self.getTuple(t)

            #tupla não encontrada ou espaço de tuplas está vazio
            if tuple_found == -1:
                return -1

            return tuple_found
        else:
            raise ValueError("Por favor, insira uma tupla!")

    #lê uma tupla do espaço de tuplas
    def take(self, t):

        if self.verifyTuple(t):
            #irá procurar por uma tupla, retornar e removê-la do espaço
            tuple_found = self.getTuple(t)

            #tupla não encontrada ou espaço de tuplas está vazio
            if tuple_found == -1:
                return -1

            #remove a tupla do espaço de tuplas
            self.removeTuple(tuple_found)

            return tuple_found
        else:
            raise ValueError("Por favor, insira uma tupla!")
    
    def removeTuple(self, t):

        #remove a tupla do espaço e decrementa o tamanho do espaço
        self.tuples.remove(t)
        self.length -= 1

    #irá procurar por uma tupla e retorná-la
    def getTuple(self, t):

        #self.blocked.wait()
        found = True

        #espaço de tuplas está vazio
        if self.length == 0:
            return -1

        #não foi passado nenhum parâmetro
        #retorna todas as tuplas
        if len(t) == 0:
            self.getAllTuples()

        else:
            #procura a tupla no espaço
            for tup in self.tuples:
    
                current_tuple = tup

                for index in range(len(t)):

                    #verfica se os valores e os tipos das tuplas são iguais
                    if t[index] == current_tuple[index] and type(t[index]) == type(current_tuple[index]):
                        continue

                    found = False
                    break

                #se encontrou uma tupla, retorna ela
                if found:
                    return current_tuple

            return -1
        
        #notifica todos os outros computadores que o espaço não tá mais bloqueado
        #self.blocked.notifyAll()

    #retorna todas as tuplas que foram inseridas no espaço
    def getAllTuples(self):
        return self.tuples
    
    #retorna a quantidade de tuplas inseridas no espaço
    def getTupleSpaceLength(self):
        return self.length

    #verifica se a variável é uma tupla
    def verifyTuple(self, t):

        if type(t) != tuple:
            return False
        
        return True