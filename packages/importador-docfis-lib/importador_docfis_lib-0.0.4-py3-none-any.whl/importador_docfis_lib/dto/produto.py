import uuid
from uuid import UUID

from nasajon.dto_handler.item_nota import ItemNota

class Produto:
    """
    Classe de Domínio de Produtos
    """
    def __init__(self):
        self.__id = None
        self.__item = ""
        self.__grupoinventario = None
        self.__especificacao = ""
        self.__estabelecimento = None
        self.__dados = None 
        self.__cadastro = None   
        self.__conjunto = None
        self.__somenteConjunto = False
        self.__id_produto = None
    

    @property
    def id(self) -> UUID:
        return self.__id
    
    @id.setter
    def id(self, value: UUID):
        self.__id = value


    @property
    def item(self) -> str:
        return self.__item
    
    @item.setter
    def item(self, value: str):
        self.__item = value


    @property
    def grupoinventario(self) -> str:
        return self.__grupoinventario

    @grupoinventario.setter
    def grupoinventario(self, value: str):
        self.__grupoinventario = value


    @property
    def especificacao(self) -> str:
        return self.__especificacao      
    
    @especificacao.setter
    def especificacao(self, value: str):
        self.__especificacao = value


    @property
    def estabelecimento(self) -> UUID:
        return self.__estabelecimento
    
    @estabelecimento.setter
    def estabelecimento(self, value: UUID):
        self.__estabelecimento = value


    @property
    def identificador(self) -> str:
        """ Identificador único do produto por estabelecimento no sistema\
        (código do item) """
        return self.item
    

    @property
    def dados(self) -> ItemNota:
        """ Dados do Item na NFCe de origem """
        return self.__dados

    @dados.setter
    def dados(self, value: ItemNota):
        self.__dados = value
    

    @property
    def cadastro(self) -> UUID:
        """ Ligado ao Grupo Empresarial """
        return self.__cadastro
    
    @cadastro.setter
    def cadastro(self, value: UUID):
        self.__cadastro = value


    @property
    def conjunto(self) -> UUID:
        return self.__conjunto
    
    @conjunto.setter
    def conjunto(self, value: UUID):
        self.__conjunto = value


    @property
    def somenteConjunto(self) -> UUID:
        """ Flag para indicar que o produto já existe e precisa ser associado\
        ao conjunto do Estabelecimento """
        return self.__somenteConjunto
    
    @somenteConjunto.setter
    def somenteConjunto(self, value: UUID):
        self.__somenteConjunto = value
        
    @property
    def id_produto(self) -> uuid:
        """Identificado do produto"""
        return self.__id_produto
    
    @id_produto.setter
    def id_produto(self, value: uuid):
        self.__id_produto = value
    
    def __str__(self) -> str:
        return "Código: " + self.item + ' - Descrição: ' + self.especificacao


    def __repr__(self) -> str:
        return self.identificador


    def __hash__(self) -> int:
        return hash(self.identificador)