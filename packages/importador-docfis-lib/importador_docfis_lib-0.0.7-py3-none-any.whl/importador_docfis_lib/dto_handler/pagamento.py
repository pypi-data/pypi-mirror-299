class Pagamento:
    """ Classe de Domínio de Pagamento """

    def __init__(self):
        self.__indPag = 0
        self.__tPag = 0
        self.__vPag = 0.0
    
    @property
    def tPag(self) -> int:
        """ Tipo de Pagamento """
        return self.__tPag
    
    @tPag.setter
    def tPag(self, value: int):
        self.__tPag = value

    @property
    def indPag(self) -> int:
        """ Indicador de Pagamento """
        return self.__indPag
    
    @indPag.setter
    def indPag(self, value: int):
        self.__indPag = value

    @property
    def vPag(self) -> float:
        """ Valor do Pagamento """
        return self.__vPag
    
    @vPag.setter
    def vPag(self, value: float):
        self.__vPag = value