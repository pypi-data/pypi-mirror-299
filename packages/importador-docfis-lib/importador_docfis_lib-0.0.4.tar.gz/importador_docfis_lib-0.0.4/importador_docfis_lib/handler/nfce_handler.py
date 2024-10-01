import xml.sax
from xml.sax.xmlreader import XMLReader

from nasajon.dto.estabelecimento import Estabelecimento
from nasajon.dto_handler.nfce import NFCE
from nasajon.dto_handler.pagamento import Pagamento
from nasajon.enums.enum_tipo_documento import EnumTipoDocumento
from nasajon.handler.cofins_handler import COFINSHandler
from nasajon.handler.destinatario_handler import DestinatarioHandler
from nasajon.handler.evento_handler import EventoHandler
from nasajon.handler.icms_handler import ICMSHandler
from nasajon.handler.pis_handler import PISHandler
from nasajon.handler.produto_handler import ProdutoHandler


class NFCeHandler(xml.sax.ContentHandler):
    """
    Classe responsavel por tratar os eventos disparados pelo Sax Parser \
    relativos a uma NFCe
    """

    def __init__(
        self,
        parser: XMLReader,
        estabelecimentos: dict[str, Estabelecimento] = None,
        estabelecimento: Estabelecimento = None,
    ):
        self.__conteudo = ""
        self.__parser = parser
        self.__nfce = None
        self.reiniciarNFCe()
        self.__tag_atual = ""
        self.__estabelecimentos = estabelecimentos
        self.__estabelecimento = estabelecimento

    @property
    def nfce(self) -> NFCE:
        return self.__nfce

    @nfce.setter
    def nfce(self, value: NFCE):
        self.__nfce = value

    def reiniciarNFCe(self):
        self.__nfce = NFCE()
        self.__estabelecimento = None

    def startElement(self, name, attrs):
        """
        Evento de abertura de tag
        """
        if name == "CTe" or name == "Nfse" or name == "CFe":
            raise Exception("Nota informada não é NFCE")
        elif name == "det":
            if self.__estabelecimento is None:
                raise Exception("Produto encontrado antes do Estabelecimento")
            produto_handler = ProdutoHandler(
                self.__parser, self, self.__estabelecimento, EnumTipoDocumento.NFCE
            )
            self.__parser.setContentHandler(produto_handler)
        elif name == "ICMS":
            icms_handler = ICMSHandler(self.__parser, self, EnumTipoDocumento.NFCE)
            self.__parser.setContentHandler(icms_handler)
        elif name == "PIS":
            pis_handler = PISHandler(self.__parser, self)
            self.__parser.setContentHandler(pis_handler)
        elif name == "COFINS":
            cofins_handler = COFINSHandler(self.__parser, self)
            self.__parser.setContentHandler(cofins_handler)
        elif name == "dest":
            destinatario_handler = DestinatarioHandler(
                self.__parser, self, self.__estabelecimento, EnumTipoDocumento.NFCE
            )
            self.__parser.setContentHandler(destinatario_handler)
        elif name == "detPag":
            self.nfce.listaPagamentos.append(Pagamento())
        elif name == "procEventoNFe" or name == "retInutNFe":
            evento_handler = EventoHandler(
                self.__parser,
                self,
                estabelecimentos=self.__estabelecimentos,
                estabelecimento=self.__estabelecimento,
            )
            self.__parser.setContentHandler(evento_handler)
        else:
            self.__tag_atual = name
        self.__conteudo = ""

    def characters(self, content):
        """
        Evento de conteudo de tag
        """

        self.__conteudo = self.__conteudo + content
        if (self.__tag_atual == "mod") and (self.__conteudo != "65"):
            raise ValueError("Nota importada não é NFCE")
        if hasattr(self.__nfce, self.__tag_atual) and getattr(self.__nfce, self.__tag_atual):
            setattr(self.__nfce, self.__tag_atual, str(self.__conteudo))
        elif (len(self.__nfce.listaPagamentos) > 0) and (
            hasattr(self.__nfce.listaPagamentos[-1], self.__tag_atual)
        ):
            setattr(
                self.__nfce.listaPagamentos[-1], self.__tag_atual, str(self.__conteudo)
            )
        else:
            return

        if (
            self.__estabelecimento is None
            and len(self.__nfce.CNPJ) > 1
            and len(self.__nfce.IE) > 1
        ):
            if self.__nfce.identificadorEmitente not in self.__estabelecimentos:
                raise Exception(
                    f"CNPJ/IE do emitente nao corresponde a nenhum estabelecimento cadastrado: cnpj={self.__nfce.CNPJ} IE={self.__nfce.IE}"
                )
            else:
                self.__estabelecimento = self.__estabelecimentos[
                    self.__nfce.identificadorEmitente
                ]

    def endElement(self, name):
        """
        Evento de fechamento de tag
        """
        self.__tag_atual = ""
        self.__conteudo = ""
