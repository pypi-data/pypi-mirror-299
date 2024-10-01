from typing import List
from uuid import UUID, uuid4

class OperacaoCfopSlot:

    def __init__(self):
        self.__operacao = None
        self.__codigo = ""
        self.__descricao = "" 
        self.__sinal = 0
        self.__afetacustodosprodutos = False
        self.__cfop = ""
        self.__slots = set()
        self.__id_estabelecimento = None
    

    @property
    def operacao(self) -> UUID:
        if (self.__operacao is None):
            self.__operacao = uuid4()
        return self.__operacao
    
    @operacao.setter
    def operacao(self, value):
        self.__operacao = value
    

    @property
    def codigo (self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, value):
        self.__codigo = value
    

    @property
    def descricao(self) -> str:
        return self.__descricao
    
    @descricao.setter
    def descricao(self, value):
        self.__descricao = value
    

    @property
    def sinal(self) -> int:
        return self.__sinal
    
    @sinal.setter
    def sinal(self, value):
        self.__sinal = value
    

    @property
    def afetacustodosprodutos(self) -> bool:
        return self.__afetacustodosprodutos
    
    @afetacustodosprodutos.setter
    def afetacustodosprodutos(self, value):
        self.__afetacustodosprodutos = value
    

    @property
    def cfop(self) -> str:
        return self.__cfop
    
    @cfop.setter
    def cfop(self, value):
        self.__cfop = value
    

    @property
    def slots(self) -> List[str]:
        return self.__slots
    
    @slots.setter
    def slots(self, value):
        self.__slots = set(value.split(',')) if (type(value) is str) else value
    

    @property
    def id_estabelecimento(self) -> UUID:
        if (self.__id_estabelecimento is None):
            self.__id_estabelecimento = uuid4()
        return self.__id_estabelecimento
    
    @id_estabelecimento.setter
    def id_estabelecimento(self, value):
        self.__id_estabelecimento = value