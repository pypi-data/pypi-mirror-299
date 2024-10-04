class PIS:
    """
        Classe de Domínio de PIS
    """
    def __init__(self):
        self.__CST = "1"
        self.__vBC = 0
        self.__pPIS = 0
        self.__vPIS = 0  


    @property
    def CST(self) -> str:
        """ CST do PIS """
        return self.__CST
    
    @CST.setter
    def CST(self, value: str):
        self.__CST = value


    @property
    def vBC(self) -> float:
        """ Valor da Base de Cálculo do PIS (Não utilizado atualmente)"""
        return self.__vBC
    
    @vBC.setter
    def vBC(self, value: float):
        self.__vBC = float(value)
    

    @property
    def pPIS(self) -> float:
        """ Alíquota do PIS (Não utilizado atualmente)"""
        return self.__pPIS
    
    @pPIS.setter
    def pPIS(self, value: float):
        self.__pPIS = float(value)
    

    @property
    def vPIS(self) -> float:
        """ Valor do PIS """
        return self.__vPIS

    @vPIS.setter
    def vPIS(self, value: float):
        self.__vPIS = float(value)