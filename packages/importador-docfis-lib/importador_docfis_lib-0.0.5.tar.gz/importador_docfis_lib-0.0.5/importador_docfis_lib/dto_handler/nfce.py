import uuid
from datetime import date, datetime
from typing import List

from importador_docfis_lib.dto.estabelecimento import Estabelecimento
from importador_docfis_lib.dto.produto import Produto
from importador_docfis_lib.dto_handler.cofins import COFINS
from importador_docfis_lib.dto_handler.item_nota import ItemNota
from importador_docfis_lib.dto_handler.participante import Participante
from importador_docfis_lib.dto_handler.pis import PIS
from importador_docfis_lib.utils import utilidades
from importador_docfis_lib.utils.lanfis import Lanfis


class NFCE:
    """
    Classe de Domínio de NFCe
    """

    def __init__(self):
        self.__mod = None
        self.__serie = ""
        self.__nNF = ""
        self.__dhEmi = None
        self.__tpNF = None
        self.__infCpl = ""
        self.__CNPJ = None
        self.__IE = None
        self.__cUF = None
        self.__id_emitente = None
        self.__codigo_emitente = None
        self.__lista_itens = list()
        self.__destinatario = None
        self.__chNFe = None
        self.__id = None
        self.__cMunFG = ""
        self.__pis = None
        self.__cofins = None
        self.__vNF = 0.00
        self.__xml = ""
        self.__vFrete = 0.00
        self.__vSeg = 0.00
        self.__vDesc = 0.00
        self.__vProd = 0.00
        self.__vOutro = 0.00
        self.__listaPagamentos = list()
        self.__vTroco = 0.0
        self.__lanfis = None
        self.__nomeArquivo = ""
        self.__operacaoCfopSlot = None
        self.__descEvento = ""
        self.__outrasIcms = 0.00
        self.__vICMSDeson = 0.00
        self.__nNFIni = None
        self.__nNFFin = None
        self.cfop = ""

    @property
    def mod(self) -> str:
        """Modelo da Nota"""
        if self.__mod is None:
            return ""
        return self.__mod

    @mod.setter
    def mod(self, value: str):
        self.__mod = value

    @property
    def cUF(self) -> str:
        """Codigo da UF"""
        return self.__cUF

    @cUF.setter
    def cUF(self, value: str):
        self.__cUF = value

    @property
    def serie(self) -> str:
        """Série da Nota"""
        return self.__serie

    @serie.setter
    def serie(self, value: str):
        self.__serie = value

    @property
    def nNF(self) -> str:
        """Número da Nota"""
        return "%09.f" % float(self.__nNF)

    @nNF.setter
    def nNF(self, value: str):
        self.__nNF = value

    @property
    def dhEmi(self) -> date:
        """Data de Emissão da Nota"""
        if self.__dhEmi is None:
            return date(1889, 12, 31)
        return self.__dhEmi

    @dhEmi.setter
    def dhEmi(self, value: str):
        self.__dhEmi = datetime.strptime(value[0:19], "%Y-%m-%dT%H:%M:%S")

    @property
    def emissao(self) -> date:
        """Data de Emissão da Nota"""
        if self.__dhEmi is None:
            return date(1889, 12, 31)
        return self.__dhEmi

    @emissao.setter
    def emissao(self, value: date):
        self.__dhEmi = value

    @property
    def tpNF(self) -> str:
        """Tipo de Nota Fiscal"""
        if self.__tpNF is None:
            return ""
        return self.__tpNF

    @tpNF.setter
    def tpNF(self, value: str):
        """Definidor de valor para o Tipo da Nota"""
        self.__tpNF = value

    @property
    def infCpl(self) -> str:
        """Informações Complementares da Nota"""
        return self.__infCpl

    @infCpl.setter
    def infCpl(self, value: str):
        self.__infCpl = value

    @property
    def chNFe(self) -> str:
        """Chave de Acesso Eletrônica da Nota"""
        if self.__chNFe is None:
            return ""
        return self.__chNFe

    @chNFe.setter
    def chNFe(self, value: str):
        self.__chNFe = value

    @property
    def CNPJ(self) -> str:
        """CNPJ do Emitente"""
        if self.__CNPJ is None:
            return ""
        return self.__CNPJ

    @CNPJ.setter
    def CNPJ(self, value: str):
        self.__CNPJ = "".join([v for v in value if v.isdigit()])

    @property
    def IE(self) -> str:
        """Inscrição Estadual do Emitente"""
        if (self.__IE is not None) and (self.__cUF is not None):
            if (self.__cUF == "33") and (
                len(self.__IE.valor) > 8
            ):  # No Rio de Janeiro, utilize apenas os ultimos 8 digitos
                return self.__IE[-8:]
        if self.__IE is None:
            return ""
        return self.__IE

    @IE.setter
    def IE(self, value: str):
        self.__IE = "".join([v for v in value if v.isdigit()])

    @property
    def id_emitente(self) -> uuid:
        """Identificador do Emitente no banco de dados"""
        return self.__id_emitente

    @id_emitente.setter
    def id_emitente(self, value: uuid):
        self.__id_emitente = value

    @property
    def codigo_emitente(self) -> str:
        """Código do Emitente no banco de dados"""
        return self.__codigo_emitente

    @codigo_emitente.setter
    def codigo_emitente(self, value: str):
        self.__codigo_emitente = value

    @property
    def lista_itens(self) -> List[ItemNota]:
        """Lista de Itens da Nota"""
        return self.__lista_itens

    @property
    def destinatario(self) -> Participante:
        """Destinatário da Nota"""
        if self.__destinatario is None:
            return Participante()
        return self.__destinatario

    @destinatario.setter
    def destinatario(self, value: Participante):
        self.__destinatario = value

    @property
    def id(self) -> uuid:
        """Identificador da Nota no banco de dados"""
        return self.__id

    @id.setter
    def id(self, value: uuid):
        self.__id = value

    @property
    def cMunFG(self):
        """Código IBGE do Município do Fato Gerador"""
        return self.__cMunFG

    @cMunFG.setter
    def cMunFG(self, value: str):
        self.__cMunFG = value

    @property
    def pis(self) -> PIS:
        """Contém as informações de PIS do produto"""
        if self.__pis is None:
            return PIS()
        return self.__pis

    @pis.setter
    def pis(self, value: PIS):
        self.__pis = value

    @property
    def cofins(self) -> COFINS:
        """Contém as informações de COFINS do produto"""
        if self.__cofins is None:
            return COFINS()
        return self.__cofins

    @cofins.setter
    def cofins(self, value: COFINS):
        self.__cofins = value

    @property
    def vNF(self):
        """Valor Declarado da Nota Fiscal"""
        return self.__vNF

    @vNF.setter
    def vNF(self, value):
        self.__vNF = value

    @property
    def vICMSDeson(self):
        """Valor Desonerado de ICMS da Nota Fiscal"""
        return self.__vICMSDeson

    @vICMSDeson.setter
    def vICMSDeson(self, value):
        self.__vICMSDeson = value

    @property
    def xml(self):
        """XML original da Nota"""
        return self.__xml

    @xml.setter
    def xml(self, value: str):
        self.__xml = value

    @property
    def vFrete(self):
        """Valor do Frete"""
        return float(self.__vFrete)

    @vFrete.setter
    def vFrete(self, value: float):
        self.__vFrete = value

    @property
    def vSeg(self):
        """Valor do Seguro"""
        return float(self.__vSeg)

    @vSeg.setter
    def vSeg(self, value: float):
        self.__vSeg = value

    @property
    def vDesc(self):
        """Valor do Desconto"""
        return float(self.__vDesc)

    @vDesc.setter
    def vDesc(self, value: float):
        self.__vDesc = value

    @property
    def outras_icms(self):
        """Valor do outrasIcms"""
        return float(self.__outrasIcms)

    @outras_icms.setter
    def outras_icms(self, value: float):
        self.__outrasIcms = value

    @property
    def vProd(self):
        """
        Valor das Mercadorias
        Note:   Na NFe 3.1 esse campo não era informado, para compatibilidade\
        utilize o método retornarValorMercadorias()
        """
        return float(self.__vProd)

    @vProd.setter
    def vProd(self, value: float):
        self.__vProd = value

    @property
    def vOutro(self):
        """Valor de Outras"""
        return float(self.__vOutro)

    @vOutro.setter
    def vOutro(self, value: float):
        self.__vOutro = value

    @property
    def vTroco(self):
        """Valor do Troco"""
        return float(self.__vTroco)

    @vTroco.setter
    def vTroco(self, value: float):
        self.__vTroco = value

    @property
    def listaPagamentos(self):
        """Lista de Pagamentos da Nota"""
        return self.__listaPagamentos

    @listaPagamentos.setter
    def listaPagamentos(self, value: list):
        self.__listaPagamentos = value

    @property
    def nomeArquivo(self) -> str:
        return self.__nomeArquivo

    @nomeArquivo.setter
    def nomeArquivo(self, value: str):
        self.__nomeArquivo = value

    @property
    def operacaoCfopSlot(self) -> uuid.UUID:
        return self.__operacaoCfopSlot

    @operacaoCfopSlot.setter
    def operacaoCfopSlot(self, value):
        self.__operacaoCfopSlot = value

    @property
    def identificadorEmitente(self) -> str:
        """Retorna o identificador único do Emitente (CNPJ + IE)"""
        return (
            self.CNPJ + "_" + self.IE if ((self.CNPJ != "") and (self.IE != "")) else ""
        )

    @property
    def descEvento(self) -> str:
        """Evento da Nota"""
        return self.__descEvento

    @descEvento.setter
    def descEvento(self, value: str):
        self.__descEvento = value

    def estaCancelada(self) -> bool:
        """Retorna se a Nota está ou não cancelada"""
        return self.__descEvento == "Cancelamento"

    def obterLancamentosFiscais(self) -> dict:
        """Retorna uma lista (chave:id) com os lançamentos fiscais da nota"""
        if self.__lanfis is None:
            self.__lanfis = Lanfis().obterLancamentosNFCe(self).items()
        return self.__lanfis

    def retornarListaCFOP(self) -> List[str]:
        """Retorna os CFOP dos itens da Nota"""
        return [item.CFOP for item in self.lista_itens]

    def retornarListaIdCFOP(self) -> List[str]:
        """Retorna os Ids dos CFOP dos itens da Nota"""
        return [str(item.id_cfop) for item in self.lista_itens]

    def existeCFOPDiferente(self) -> bool:
        """Retorna se há, ou não, itens com CFOP diferentes"""
        return len(set(self.lista_itens)) > 1

    def calcular_cfop(self) -> str:
        """Retorna o CFOP da Nota (o mais comum nos itens)"""
        return str(utilidades.elemento_mais_comum(self.retornarListaCFOP()))

    def retornarIdCFOP(self) -> str:
        """Retorna o CFOP da Nota (o mais comum nos itens)"""
        return str(utilidades.elemento_mais_comum(self.retornarListaIdCFOP()))

    def retornarValorMercadorias(self) -> float:
        """Retorna o valor das Mercadorias da Nota"""
        return (
            self.vProd
            if (self.vProd > 0)
            else sum([item.vProd for item in self.lista_itens])
        )

    def retornarBaseICMS(self) -> float:
        """Valor da Base do ICMS"""
        return sum([item.icms.vBC for item in self.lista_itens])

    def retornarValorICMS(self) -> float:
        """Valor do ICMS"""
        return sum([item.icms.vICMS for item in self.lista_itens])

    def retornarIsentasICMS(self) -> float:
        """Valor Isento do ICMS"""
        isentas = sum(
            item.valorContabil
            for item in self.lista_itens
            if item.icms.CST in ("40", "41")
        )
        return (
            sum(
                [
                    item.icms.retornarIsentasICMS(item.valorContabil)
                    for item in self.lista_itens
                ]
            )
            + isentas
        )

    @property
    def identificador(self):
        """Identificador da Nota (Chave NFe)"""
        return self.chNFe

    @identificador.setter
    def identificador(self, value):
        self.chNFe = value

    @property
    def nNFIni(self) -> str:
        """Início do número de notas marcadas para Inutilização"""
        return self.__nNFIni

    @nNFIni.setter
    def nNFIni(self, value: str):
        self.__nNFIni = value

    @property
    def nNFFin(self) -> str:
        """Fim do número de notas marcadas para Inutilização"""
        return self.__nNFFin

    @nNFFin.setter
    def nNFFin(self, value: str):
        self.__nNFFin = value

    def gorjetaCFOP(self, value):
        """Retorna o CFOP com a terminação de gorjeta"""
        return str(value) + ".GJT"

    def __str__(self) -> str:
        return (
            self.chNFe
            if self.chNFe is not None
            else "{} > mod: {} ser: {} num: {} - {}".format(
                self.chNFe, self.mod, self.serie, self.nNF, str(self.dhEmi)
            )
        )

    def __repr__(self):
        return self.identificador

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        return self.identificador == other.identificador

    def __ne__(self, other) -> bool:
        if other is None:
            return True
        return self.identificador != other.identificador

    def __hash__(self):
        return hash(self.identificador)  

    def retornar_produtos_novos(
        self, estabelecimento: Estabelecimento
    ) -> dict[str, Produto]:
        """
        Método para retornar os produtos da nota que não existem no estabelecimento informado
        Args:
            estabelecimento: Estabelecimento ao qual a NFCe pertence
        """
        produtos_novos: dict[str, Produto] = {}
        for item in self.lista_itens:
            if item.CFOP == "" and self.cfop != "":
                item.CFOP = self.cfop

            if item.CFOP in estabelecimento.cfops:
                item.id_cfop = estabelecimento.cfops[item.CFOP].id
                if item.item_gorjeta is True:
                    item.CFOP = self.gorjetaCFOP(item.CFOP)
            else:
                raise Exception(f"CFOP {item.CFOP} não existente no estabelecimento")
            item.idLocalDeEstoque = estabelecimento.id_localdeestoque
            item.idFiguraTributaria = estabelecimento.id_figuratributaria
            if item.id_produto is not None:
                continue
            if item.cProd in produtos_novos:
                item.id_produto = produtos_novos[item.cProd].id
            else:
                produto_novo = Produto()
                produto_novo.estabelecimento = estabelecimento.id

                produto_novo.id = uuid.uuid4()
                produto_novo.item = item.cProd
                produto_novo.especificacao = item.xProd
                produto_novo.cadastro = estabelecimento.cadastro
                if item.uCom in estabelecimento.unidades:
                    item.id_unidade = estabelecimento.unidades[item.uCom].id
                elif "UN" in estabelecimento.unidades:
                    item.id_unidade = estabelecimento.unidades["UN"].id
                else:
                    for unidade in estabelecimento.unidades.values():
                        item.id_unidade = unidade.id
                        break
                if item.uTrib in estabelecimento.unidades:
                    item.id_unidade_trib = estabelecimento.unidades[item.uCom].id
                elif "UN" in estabelecimento.unidades:
                    item.id_unidade_trib = estabelecimento.unidades["UN"].id
                else:
                    for unidade in estabelecimento.unidades.values():
                        item.id_unidade_trib = unidade.id
                        break
                produto_novo.dados = item

                item.id_produto = produto_novo.id
                produto_novo.conjunto = estabelecimento.conjunto_produtos
                if produto_novo.conjunto is None:
                    raise Exception("Estabelecimento não possui Conjuntos de Produtos")

                produtos_novos[produto_novo.identificador] = produto_novo

        return produtos_novos

    def retornarDescontoTotal(self, icms_desonerado_desconto) -> float:
        """Retorna o valor total de descontos da NF"""
        desoneracao = self.vICMSDeson if icms_desonerado_desconto else 0
        return float(self.vDesc) + float(desoneracao)
