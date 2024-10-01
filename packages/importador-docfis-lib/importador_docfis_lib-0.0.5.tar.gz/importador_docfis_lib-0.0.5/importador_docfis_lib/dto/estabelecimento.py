from typing import List
from uuid import UUID

from importador_docfis_lib.dto.cfop import CFOP
from importador_docfis_lib.dto.cliente import Cliente
from importador_docfis_lib.dto_handler.nfce import NFCE
from importador_docfis_lib.dto.operacao_cfop_slot import OperacaoCfopSlot
from importador_docfis_lib.dto.produto import Produto
from importador_docfis_lib.dto.servico import Servico
from importador_docfis_lib.dto.unidade import Unidade


class Estabelecimento:
    """Classe de Dominio para Estabelecimento"""

    def __init__(self):
        self.__id = None
        self.__conjunto_produtos = None
        self.__conjunto_clientes = None
        self.__conjunto_servicos = None
        self.__cnpj = None
        self.__codigo = None
        self.__inscricao_estadual = None
        self.__cadastro = None
        self.__produtos = dict()
        self.__clientes = dict()
        self.__servicos = dict()
        self.__produtosNovos = dict()
        self.__clientesNovos = dict()
        self.__servicosNovos = dict()
        self.__cfopsNovos = dict()
        self.__unidades = dict()
        self.__nfces = dict()
        self.__listaNFSE = dict()
        self.__listaCTE = dict()
        self.__listaNFSE = dict()
        self.__listaChavesImportadas = set()
        self.__cfops = dict()
        self.__operacoes = list()
        self.__id_figuratributaria = ""
        self.__id_localdeestoque = ""
        self.__id_operacao = ""
        self.__completo = False
        self.__uf = "RJ"
        self.__lanc_ipi = 0
        self.__id_empresa = None
        self.ibge = ""
        self.__listaSAT = dict()
        self.estabelecimento_multinota = None
        self.tenant_multinotas = None

    @property
    def id(self) -> UUID:
        return self.__id

    @id.setter
    def id(self, value: UUID):
        self.__id = value

    @property
    def cnpj(self) -> str:
        if self.__cnpj is None:
            return ""
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, value: str):
        self.__cnpj = "".join([v for v in value if v.isdigit()])

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, value: str):
        self.__codigo = value

    @property
    def uf(self) -> str:
        return self.__uf

    @uf.setter
    def uf(self, value: str):
        self.__uf = value

    @property
    def lanc_ipi(self) -> str:
        return self.__lanc_ipi

    @lanc_ipi.setter
    def lanc_ipi(self, value: str):
        self.__lanc_ipi = value

    @property
    def inscricao_estadual(self) -> str:
        if self.__inscricao_estadual is None:
            return ""
        return self.__inscricao_estadual

    @inscricao_estadual.setter
    def inscricao_estadual(self, value: str):
        self.__inscricao_estadual = "".join([v for v in value if v.isdigit()])

    @property
    def conjunto_produtos(self) -> UUID:
        return self.__conjunto_produtos

    @conjunto_produtos.setter
    def conjunto_produtos(self, value: UUID):
        self.__conjunto_produtos = value

    @property
    def conjunto_clientes(self) -> UUID:
        return self.__conjunto_clientes

    @conjunto_clientes.setter
    def conjunto_clientes(self, value: UUID):
        self.__conjunto_clientes = value

    @property
    def conjunto_servicos(self) -> UUID:
        return self.__conjunto_servicos

    @conjunto_servicos.setter
    def conjunto_servicos(self, value: UUID):
        self.__conjunto_servicos = value

    @property
    def cadastro(self) -> UUID:
        """Ligado ao Grupo Empresarial"""
        return self.__cadastro

    @cadastro.setter
    def cadastro(self, value: UUID):
        self.__cadastro = value

    @property
    def produtos(self) -> dict[Produto]:
        """Lista dos itens (estoque.itens) do Estabelecimento"""
        return self.__produtos

    @produtos.setter
    def produtos(self, value: dict):
        self.__produtos = value

    @property
    def clientes(self) -> dict[Cliente]:
        """Lista dos itens (ns.pessoas) do Estabelecimento"""
        return self.__clientes

    @clientes.setter
    def clientes(self, value: List[Cliente]):
        self.__clientes = value

    # @property
    # def servicos(self) -> Dict[str, Servico]:
    #     """ Lista dos servicos do Estabelecimento """
    #     self.completarDados()
    #     return self.__servicos

    # @servicos.setter
    # def servicos(self, value: List[Servico]):
    #     self.__servicos = value

    @property
    def cfops(self) -> dict[str,CFOP]:
        """Lista dos cfops (ns.cfops) do Estabelecimento"""
        return self.__cfops

    @cfops.setter
    def cfops(self, value: dict[str,CFOP]):
        self.__cfops = value

    @property
    def operacoes(self) -> List[OperacaoCfopSlot]:
        """Lista dos cfops (ns.cfops) do Estabelecimento"""
        return self.__operacoes

    @operacoes.setter
    def operacoes(self, value: List[OperacaoCfopSlot]):
        self.__operacoes = value

    @property
    def identificador(self) -> str:
        """Identificador unico do Estabeleciemto no sistema: CNPJ + IE"""
        return self.cnpj + "_" + self.inscricao_estadual

    @property
    def produtosNovos(self) -> dict:
        """ Lista de Produtos que estao sendo adicionados (criados ou \
        associados) ao Estabelecimento """
        return self.__produtosNovos

    @produtosNovos.setter
    def produtosNovos(self, value: dict):
        self.__produtosNovos = value

    @property
    def clientesNovos(self) -> List[Cliente]:
        """ Lista de Clientes que estão sendo adicionados (criados ou \
        associados) ao Estabelecimento """
        return self.__clientesNovos

    @clientesNovos.setter
    def clientesNovos(self, value: List[Cliente]):
        self.__clientesNovos = value

    @property
    def servicosNovos(self) -> List[Servico]:
        """ Lista de Servicos que estao sendo adicionados (criados ou \
        associados) ao Estabelecimento """
        return self.__servicosNovos

    @servicosNovos.setter
    def servicosNovos(self, value: List[Servico]):
        self.__servicosNovos = value

    @property
    def cfopsNovos(self) -> List[Servico]:
        """ Lista de Servicos que estao sendo adicionados (criados ou \
        associados) ao Estabelecimento """
        return self.__cfopsNovos

    @cfopsNovos.setter
    def cfopsNovos(self, value: List[Servico]):
        self.__cfopsNovos = value

    @property
    def unidades(self) -> List[Unidade]:
        """ Lista de Unidades que estao sendo adicionados (criados ou \
        associados) ao Estabelecimento """
        return self.__unidades

    @unidades.setter
    def unidades(self, value: List[Unidade]):
        self.__unidades = value

    @property
    def nfces(self) -> dict[NFCE]:
        """ Lista de NFCe que estao sendo adicionados (criados ou \
        associados) ao Estabelecimento """
        return self.__nfces

    @nfces.setter
    def nfces(self, value: dict[NFCE]):
        self.__nfces = value

    # @property
    # def listaSAT(self) -> List[SAT]:
    #     """ Lista de SAT que estao sendo adicionados (criados ou \
    #     associados) ao Estabelecimento """
    #     self.completarDados()
    #     return self.__listaSAT

    # @listaSAT.setter
    # def listaSAT(self, value: List[SAT]):
    #     self.__listaSAT = value

    # @property
    # def listaCTE(self) -> Dict:
    #     """ Lista de CTE do Estabelecimento """
    #     self.completarDados()
    #     return self.__listaCTE

    # @listaCTE.setter
    # def listaCTE(self, value: Dict):
    #     self.__listaCTE = value

    # @property
    # def listaNFSE(self) -> Dict:
    #     """ Lista de NFSE do Estabelecimento """
    #     self.completarDados()
    #     return self.__listaNFSE

    # @listaNFSE.setter
    # def listaNFSE(self, value: Dict):
    #     self.__listaNFSE = value

    @property
    def id_figuratributaria(self) -> UUID:
        return self.__id_figuratributaria

    @id_figuratributaria.setter
    def id_figuratributaria(self, value):
        self.__id_figuratributaria = value

    @property
    def id_localdeestoque(self) -> UUID:
        return self.__id_localdeestoque

    @id_localdeestoque.setter
    def id_localdeestoque(self, value):
        self.__id_localdeestoque = value

    @property
    def id_operacao(self) -> UUID:
        return self.__id_operacao

    @id_operacao.setter
    def id_operacao(self, value):
        self.__id_operacao = value

    @property
    def id_empresa(self) -> UUID:
        return self.__id_empresa

    @id_empresa.setter
    def id_empresa(self, value):
        self.__id_empresa = value

    @property
    def listaChavesImportadas(self) -> set:
        """ Lista das Chaves de acesso das notas que foram importadas nesta \
        instancia do importador """
        return self.__listaChavesImportadas

    @property
    def completo(self) -> bool:
        return self.__completo

    @completo.setter
    def completo(self, value: bool):
        self.__completo = value

    def retornar_operacao_cfop(self, CFOP: str) -> OperacaoCfopSlot:
        if (self.id_operacao is not None) and (type(self.id_operacao) is UUID):
            operacoesCfop = [
                operacao
                for operacao in self.operacoes
                if (operacao.operacao == self.id_operacao)
            ]
        else:
            operacoesCfop = [
                operacao for operacao in self.operacoes if (operacao.cfop == CFOP)
            ]
        return operacoesCfop[0] if operacoesCfop else None

    def __repr__(self):
        return self.identificador

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) is str:
            return self.identificador == other
        return self.identificador == other.identificador

    def __ne__(self, other):
        if other is None:
            return True
        if type(other) is str:
            return self.identificador != other
        return self.identificador != other.identificador

    def __hash__(self):
        return hash(self.identificador)

    def __str__(self):
        return "CNPJ: " + self.cnpj + " - IE: " + self.inscricao_estadual
