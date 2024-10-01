class ICMS:
    """
    Classe de Domínio de ICMS
    """

    def __init__(self):
        self.__CST = ""
        self.__vBC = 0
        self.__pICMS = 0.00
        self.__vICMS = 0
        self.__orig = None
        self.__modBC = None
        self.__vBCFCP = 0
        self.__pFCP = 0
        self.__vFCP = 0
        self.__vICMSDeson = 0
        self.__vBCST = 0
        self.__vST = 0
        self.__vFCPST = 0
        self.__vFCPSTRet = 0
        self.__vBCOutraUF = 0
        self.__pICMSOutraUF = 0.00
        self.__vICMSOutraUF = 0
        self.__vBCSTRet = 0
        self.__pICMSSTRet = 0.00
        self.__vICMSSTRet = 0
        self.__pRedBC = 0.0000
        self.__motDesICMS = "00"
        self.__indSN = 0
        self.calcularTotal = True

    @property
    def orig(self) -> int:
        """Origem do Produto"""
        if self.__orig is None:
            return 0
        return self.__orig

    @orig.setter
    def orig(self, value):
        if value == "":
            self.__orig = 0
        else:
            self.__orig = int(value)

    @property
    def modBC(self) -> str:
        """Modo de definição da base de cálculo do ICMS (Não utilizado atualmente)"""
        if self.__modBC is None:
            return ""
        return self.__modBC

    @modBC.setter
    def modBC(self, value):
        self.__modBC = value

    @property
    def motDesICMS(self) -> str:
        """Motiovo de Desoneração da base de cálculo do ICMS"""
        if self.__motDesICMS is None:
            return ""
        return self.__motDesICMS

    @motDesICMS.setter
    def motDesICMS(self, value):
        self.__motDesICMS = value

    @property
    def CST(self) -> str:
        """CST do ICMS"""
        return self.__CST

    @CST.setter
    def CST(self, value: str):
        self.__CST = value

    @property
    def vBC(self) -> float:
        """Valor da Base de Cálculo do ICMS"""
        return self.__vBC

    @vBC.setter
    def vBC(self, value: float):
        self.__vBC = float(value)

    @property
    def vBCOutraUF(self) -> float:
        """Valor da Base de Cálculo do ICMS de Outra UF"""
        return self.__vBCOutraUF

    @vBCOutraUF.setter
    def vBCOutraUF(self, value: float):
        self.__vBCOutraUF = float(value)

    @property
    def vBCSTRet(self) -> float:
        """Valor da Base de Cálculo do ICMS Retido"""
        return self.__vBCSTRet

    @vBCSTRet.setter
    def vBCSTRet(self, value: float):
        self.__vBCSTRet = float(value)

    @property
    def pICMS(self) -> float:
        """Alíquota do ICMS"""
        return self.__pICMS

    @pICMS.setter
    def pICMS(self, value: float):
        self.__pICMS = float(value)

    @property
    def pICMSOutraUF(self) -> float:
        """Alíquota do ICMS de Outra UF"""
        return self.__pICMSOutraUF

    @pICMSOutraUF.setter
    def pICMSOutraUF(self, value: float):
        self.__pICMSOutraUF = float(value)

    @property
    def pICMSSTRet(self) -> float:
        """Alíquota do ICMS Retido"""
        return self.__pICMSSTRet

    @pICMSSTRet.setter
    def pICMSSTRet(self, value: float):
        self.__pICMSSTRet = float(value)

    @property
    def vICMS(self) -> float:
        """Valor do ICMS"""
        return self.__vICMS

    @vICMS.setter
    def vICMS(self, value: float):
        self.__vICMS = float(value)

    @property
    def vICMSOutraUF(self) -> float:
        """Valor do ICMS de Outra UF"""
        return self.__vICMSOutraUF

    @vICMSOutraUF.setter
    def vICMSOutraUF(self, value: float):
        self.__vICMSOutraUF = float(value)

    @property
    def vICMSSTRet(self) -> float:
        """Valor do ICMS Retido"""
        return self.__vICMSSTRet

    @vICMSSTRet.setter
    def vICMSSTRet(self, value: float):
        self.__vICMSSTRet = float(value)

    @property
    def pFCP(self) -> float:
        """Alíquota do FCP"""
        return self.__pFCP

    @pFCP.setter
    def pFCP(self, value: float):
        self.__pFCP = float(value)

    @property
    def vBCFCP(self) -> float:
        """Base de Cálculo do FCP"""
        return self.__vBCFCP

    @vBCFCP.setter
    def vBCFCP(self, value: float):
        self.__vBCFCP = float(value)

    @property
    def vFCP(self) -> float:
        """Valor do FCP"""
        return self.__vFCP

    @vFCP.setter
    def vFCP(self, value: float):
        self.__vFCP = float(value)

    @property
    def vICMSDeson(self) -> float:
        """Valor do ICMS Desonerado"""
        return self.__vICMSDeson

    @vICMSDeson.setter
    def vICMSDeson(self, value: float):
        self.__vICMSDeson = float(value)

    @property
    def vBCST(self) -> float:
        """Valor da Base de Cálculo da ST (Não utilizado atualmente)"""
        return self.__vBCST

    @vBCST.setter
    def vBCST(self, value: float):
        self.__vBCST = float(value)

    @property
    def vST(self) -> float:
        """Valor da ST (Não utilizado atualmente)"""
        return self.__vST

    @vST.setter
    def vST(self, value: float):
        self.__vST = float(value)

    @property
    def vFCPST(self) -> float:
        """Valor do FCP da ST (Não utilizado atualmente)"""
        return self.__vFCPST

    @vFCPST.setter
    def vFCPST(self, value: float):
        self.__vFCPST = float(value)

    @property
    def vFCPSTRet(self) -> float:
        """Valor do FCP ST Retido (Não utilizado atualmente)"""
        return self.__vFCPSTRet

    @vFCPSTRet.setter
    def vFCPSTRet(self, value: float):
        self.__vFCPSTRet = float(value)

    @property
    def pRedBC(self) -> float:
        """Percentual da Redução de Base do ICMS"""
        return self.__pRedBC

    @pRedBC.setter
    def pRedBC(self, value: float):
        self.__pRedBC = float(value)

    @property
    def indSN(self) -> int:
        """Indicador se é simples nacional"""
        return int(self.__indSN)

    @indSN.setter
    def indSN(self, value: str):
        self.__indSN = value

    @property
    def aliquotaICMSTotal(self) -> float:
        """Alíquota do ICMS total da Nota (ICMS + FCP)"""
        if self.calcularTotal:
            return self.pICMS + self.pFCP
        else:
            return self.pICMS

    @property
    def valorICMSTotal(self) -> float:
        """Valor do ICMS total da Nota (ICMS + FCP)"""
        if self.calcularTotal:
            return self.vICMS + self.vFCP
        else:
            return self.vICMS

    def retornarValorReducao(self, valorContabil: float) -> float:
        """Valor da parcela Isenta de ICMS"""
        valor = 0
        aliquota = self.pRedBC / 100.0000
        if aliquota > 0.0000:
            valor = round(valorContabil * aliquota, 2)
        return valor if self.CST == "20" else 0

    def retornar_outras_icms(self, valorContabil: float) -> float:
        """Valor de Outras ICMS"""
        return valorContabil if self.CST in ("10", "51", "60", "70", "90") else 0
        # else (self.vICMSDeson - self.retornarValorDesoneracao())\
        # if self.CST in ('20') else 0  # Se já retorna a desoneração como desconto, não pode colocar no Outras

    def retornarIsentasICMS(self, valorContabil: float) -> float:
        """Valor de Isentas ICMS"""
        valor = valorContabil - (self.vBC + self.retornar_outras_icms(valorContabil))
        return valor if valor > 0 else 0

    def retornarValorDesoneracao(self, icms_desonerado_desconto=False) -> float:
        return self.vICMSDeson if icms_desonerado_desconto else 0

    def retornarBaseNaoTributada(self, valorItem: float) -> float:
        """Retorna o valor não tributado"""
        return valorItem if self.CST in ("60", "70") else 0
