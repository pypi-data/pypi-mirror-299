from uuid import UUID

import re

from importador_docfis_lib.dto_handler.cofins import COFINS
from importador_docfis_lib.dto_handler.icms import ICMS
from importador_docfis_lib.dto_handler.pis import PIS


class ItemNota:
    """
    Classe de Dominio de Itens de Nota
    """

    def __init__(self):
        self.__cProd = ""
        self.__xProd = ""
        self.__NCM = ""
        self.__CFOP = ""
        self.__uCom = ""
        self.__qCom = 0
        self.__vUnCom = 0
        self.__vProd = 0
        self.__uTrib = ""
        self.__CEST = ""
        self.__qTrib = 0
        self.__vUnTrib = 0
        self.__indTot = True
        self.__icms = None
        self.__id_produto = None
        self.__cEAN = None
        self.__cEANTrib = None
        self.__id_unidade = None
        self.__id_unidade_trib = None
        self.__ordem = 0
        self.__id = None
        self.__pis = None
        self.__cofins = None
        self.__id_cfop = None
        self.__idFiguraTributaria = None
        self.__idLocalDeEstoque = None
        self.__vDesc = 0
        self.__vOutro = 0
        self.__cBenef = ""
        self.__id_lanfis = None
        self.__itemGorjeta = None
        self.__df_linha = None
        self.numero = ""

    @property
    def pis(self) -> PIS:
        """Contem as informacoes de PIS do produto"""
        if self.__pis is None:
            return PIS()
        return self.__pis

    @pis.setter
    def pis(self, value: PIS):
        self.__pis = value

    @property
    def cofins(self) -> COFINS:
        """Contem as informacoes de COFINS do produto"""
        if self.__cofins is None:
            return COFINS()
        return self.__cofins

    @cofins.setter
    def cofins(self, value: COFINS):
        self.__cofins = value

    @property
    def ordem(self) -> int:
        """Ordem do Item na Nota"""
        return self.__ordem

    @ordem.setter
    def ordem(self, value: int):
        self.__ordem = int(value)

    @property
    def cProd(self) -> str:
        """Codigo do produto"""
        return self.__cProd

    @cProd.setter
    def cProd(self, value: str):
        self.__cProd = value

    @property
    def cEAN(self) -> str:
        """Codigo de Barras (EAN-13, UPC-12 ou GTIN-8) do produto"""
        if self.__cEAN is None:
            return ""
        return self.__cEAN.valor

    @cEAN.setter
    def cEAN(self, value: str):
        self.__cEAN = value

    @property
    def xProd(self) -> str:
        """Descricao do produto"""
        return self.__xProd

    @xProd.setter
    def xProd(self, value: str):
        self.__xProd = re.sub(r"[^\x00-\x7F]+", "", value)

    @property
    def cBenef(self) -> str:
        """Codigo do Beneficio do ICMS do produto"""
        return self.__cBenef

    @cBenef.setter
    def cBenef(self, value: str):
        self.__cBenef = value

    @property
    def nBenef(self) -> str:
        """Codigo do Beneficio do ICMS do produto"""
        import re

        regex = re.sub("[^0-9]", "", self.cBenef)
        if len(regex) <= 6:
            return regex

    @nBenef.setter
    def nBenef(self, value: str):
        raise Exception("Nao e possivel definir este valor")

    @property
    def NCM(self) -> str:
        """Numero Comum do Mercosul do produto"""
        return self.__NCM

    @NCM.setter
    def NCM(self, value: str):
        self.__NCM = value

    @property
    def CEST(self) -> str:
        """Codigo Especificador da Substituicao Tributaria do produto"""
        return self.__CEST

    @CEST.setter
    def CEST(self, value: str):
        self.__CEST = value

    @property
    def CFOP(self) -> str:
        """CFOP do produto"""
        return self.__CFOP

    @CFOP.setter
    def CFOP(self, value: str):
        self.__CFOP = value

    @property
    def id_cfop(self) -> UUID:
        """Id do CFOP do produto"""
        return self.__id_cfop

    @id_cfop.setter
    def id_cfop(self, value: UUID):
        self.__id_cfop = value

    @property
    def id_lanfis(self) -> UUID:
        """Id do CFOP do produto"""
        return self.__id_lanfis

    @id_lanfis.setter
    def id_lanfis(self, value: UUID):
        self.__id_lanfis = value

    @property
    def df_linha(self) -> UUID:
        """Id da linha do produto"""
        return self.__df_linha

    @df_linha.setter
    def df_linha(self, value: UUID):
        self.__df_linha = value

    @property
    def uCom(self) -> str:
        """Unidade Comercial do produto"""
        return self.__uCom

    @uCom.setter
    def uCom(self, value: str):
        self.__uCom = value

    @property
    def qCom(self) -> float:
        """Quantidade do produto na Unidade Comercial"""
        return float(self.__qCom)

    @qCom.setter
    def qCom(self, value: float):
        self.__qCom = value

    @property
    def vUnCom(self) -> float:
        """Valor Unitario do produto na Unidade Comercial"""
        return float(self.__vUnCom)

    @vUnCom.setter
    def vUnCom(self, value: float):
        self.__vUnCom = value

    @property
    def vProd(self) -> float:
        """Valor Total do produto"""
        return float(self.__vProd)

    @vProd.setter
    def vProd(self, value: float):
        self.__vProd = float(value)

    @property
    def vDesc(self) -> float:
        """Valor de Desconto"""
        return float(self.__vDesc)

    @vDesc.setter
    def vDesc(self, value: float):
        self.__vDesc = float(value)

    @property
    def vOutro(self) -> float:
        """Valor de Outras Despesas"""
        return float(self.__vOutro)

    @vOutro.setter
    def vOutro(self, value: float):
        self.__vOutro = float(value)

    @property
    def valorContabil(self) -> float:
        return self.vProd - self.retornarDescontoTotal() + self.vOutro

    @property
    def cEANTrib(self) -> str:
        """Codigo de Barras (EAN-13, UPC-12 ou GTIN-8) do produto Tributavel (Nao utilizado atualmente)"""
        if self.__cEANTrib is None:
            return ""
        return self.__cEANTrib.valor

    @cEANTrib.setter
    def cEANTrib(self, value: str):
        self.__cEANTrib = value

    @property
    def uTrib(self) -> str:
        """Unidade Tributavel do produto"""
        return self.__uTrib

    @uTrib.setter
    def uTrib(self, value: str):
        self.__uTrib = value

    @property
    def qTrib(self) -> float:
        """Quantidade do produto na Unidade Tributavel (Nao utilizado atualmente)"""
        return float(self.__qTrib)

    @qTrib.setter
    def qTrib(self, value: float):
        self.__qTrib = value

    @property
    def vUnTrib(self) -> float:
        """Valor do produto na Unidade Trbutavel (Nao utilizado atualmente)"""
        return float(self.__vUnTrib)

    @vUnTrib.setter
    def vUnTrib(self, value: float):
        self.__vUnTrib = value

    @property
    def indTot(self) -> bool:
        """ Indica se o valor do produto deve ou nao ser somado ao valor total\
        da nota (Nao utilizado atualmente)"""
        return self.__indTot

    @indTot.setter
    def indTot(self, value: str):
        self.__indTot = value

    @property
    def icms(self) -> ICMS:
        """Contem as informacoes de ICMS do produto"""
        return self.__icms

    @icms.setter
    def icms(self, value: ICMS):
        self.__icms = value

    @property
    def id_produto(self) -> UUID:
        """Identificador do produto no banco de dados (estoque.itens)"""
        return self.__id_produto

    @id_produto.setter
    def id_produto(self, value: UUID):
        self.__id_produto = value

    @property
    def id(self) -> UUID:
        """Identificador do Item da Nota no banco de dados (ns.df_itens)"""
        return self.__id

    @id.setter
    def id(self, value: UUID):
        self.__id = value

    @property
    def id_unidade(self) -> UUID:
        """Identificador da Unidade Comercial no Banco de Dados"""
        return self.__id_unidade

    @id_unidade.setter
    def id_unidade(self, value: UUID):
        self.__id_unidade = value

    @property
    def id_unidade_trib(self) -> UUID:
        """Identificador da Unidade Tributada no Banco de Dados"""
        return self.__id_unidade_trib

    @id_unidade_trib.setter
    def id_unidade_trib(self, value: UUID):
        self.__id_unidade_trib = value

    @property
    def idLocalDeEstoque(self) -> UUID:
        return self.__idLocalDeEstoque

    @idLocalDeEstoque.setter
    def idLocalDeEstoque(self, value):
        self.__idLocalDeEstoque = value

    @property
    def idFiguraTributaria(self) -> UUID:
        return self.__idFiguraTributaria

    @idFiguraTributaria.setter
    def idFiguraTributaria(self, value):
        self.__idFiguraTributaria = value

    @property
    def item_gorjeta(self):
        return self.__itemGorjeta

    @item_gorjeta.setter
    def item_gorjeta(self, value: bool):
        self.__itemGorjeta = value

    def retornarDescontoTotal(self, icms_desonerado_desconto=False) -> float:
        """Retorna o valor total de descontos da NF"""
        desoneracao = self.icms.vICMSDeson if icms_desonerado_desconto else 0
        return self.vDesc + desoneracao

    def giGorjeta(self):
        """Retorna a constante padrao para grupo de inventario GORJETA"""
        return 98
