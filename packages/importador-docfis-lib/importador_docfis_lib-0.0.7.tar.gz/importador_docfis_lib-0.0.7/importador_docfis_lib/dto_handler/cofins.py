class COFINS:
    """
    Classe de Modelo de COFINS
    """
    def __init__(self):
        self.__CST = ""
        self.__vBC = 0
        self.__pCOFINS = 0
        self.__vCOFINS = 0
    

    @property
    def CST(self) -> str:
        """ CST do COFINS (Não utilizado atualmente)"""
        return self.__CST
    
    @CST.setter
    def CST(self, value: str):
        self.__CST = value


    @property
    def vBC(self) -> float:
        """ Valor da Base de Cálculo do COFINS (Não utilizado atualmente)"""
        return self.__vBC
    
    @vBC.setter
    def vBC(self, value: float):
        self.__vBC = float(value)
    

    @property
    def pCOFINS(self) -> float:
        """ Alíquota do COFINS (Não utilizado atualmente)"""
        return self.__pCOFINS
    
    @pCOFINS.setter
    def pCOFINS(self, value: float):
        self.__pCOFINS = float(value)
    

    @property
    def vCOFINS(self) -> float:
        """ Valor do COFINS """
        return self.__vCOFINS

    @vCOFINS.setter
    def vCOFINS(self, value: float):
        self.__vCOFINS = float(value)