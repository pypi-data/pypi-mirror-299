from uuid import UUID

class Unidade:
    """
    Classe Domínio de Unidades
    """

    def __init__(self):
        self.__codigo = ""
        self.__id = None
        self.__cadastro = None
    

    @property
    def codigo(self) -> str:
        return self.__codigo
    
    @codigo.setter
    def codigo(self, value: str):
        self.__codigo = value
    

    @property
    def id(self) -> UUID:
        """ Identificador da Unidade no banco de dados (estoque.unidades) """
        return self.__id
    
    @id.setter
    def id (self, value: UUID):
        self.__id = value


    @property
    def cadastro(self) -> UUID:
        """ ligado ao Grupo Empresarial """
        return self.__cadastro
    
    @cadastro.setter
    def cadastro(self, value: UUID):
        self.__cadastro = value


    @property
    def identificador(self) -> str:
        """ Identificador único da Unidade por Estabelecimento no sistema\
        (código) """
        return self.codigo
    

    def __str__(self) -> str:
        return "Unidade: " + self.codigo


    def __repr__(self) -> str:
        return self.identificador


    def __hash__(self) -> int:
        return hash(self.identificador)


    def __eq__(self, other):
        if (other is None):
            return False
        return (self.identificador.upper() == other.identificador.upper())