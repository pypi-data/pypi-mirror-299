import xml.sax

from nasajon.dto.estabelecimento import Estabelecimento
from nasajon.dto_handler.nfce import NFCE


class EventoHandler(xml.sax.ContentHandler):
    """
    Classe responsável por tratar os eventos disparados pelo Sax Parser \
    relativos aos Eventos de uma NFCe
    """

    def __init__(
        self,
        parser,
        handler_anterior,
        estabelecimentos: dict[str, Estabelecimento] = None,
        estabelecimento: Estabelecimento = None,
    ):
        self.__parser = parser
        self.__handler_anterior = handler_anterior
        self.__nfce = NFCE()
        self.__tag_atual = ""
        self.__conteudo = ""
        self.__estabelecimentos = estabelecimentos
        self.__estabelecimento = estabelecimento

    def startElement(self, name, attrs):
        """
        Evento de abertura de tag
        """
        self.__tag_atual = name
        self.__conteudo = ""

    def characters(self, content):
        """
        Evento de conteúdo de tag
        """
        if not hasattr(self.__nfce, self.__tag_atual):
            if self.__tag_atual == "xMotivo":
                if "INUTILIZACAO" in str(content).upper():
                    self.__conteudo = self.__conteudo + content
                    setattr(self.__nfce, "descEvento", str(self.__conteudo))
            elif self.__tag_atual == "dhRecbto":
                self.__conteudo = self.__conteudo + content
                setattr(self.__nfce, "dhEmi", str(self.__conteudo))
            else:
                return
        elif self.__tag_atual == "CNPJ":
            self.__conteudo = self.__conteudo + content
            setattr(self.__nfce, self.__tag_atual, str(self.__conteudo))

            if "INUTILIZACAO" in str(self.__nfce.descEvento).upper():
                if self.__estabelecimento is None:
                    for estabelecimento in self.__estabelecimentos:
                        cnpj, separador, inscricao_estadual = estabelecimento.partition(
                            "_"
                        )
                        if cnpj == self.__nfce.CNPJ:
                            self.__estabelecimento = self.__estabelecimentos[
                                estabelecimento
                            ]
                setattr(self.__nfce, "id_emitente", self.__estabelecimento.id)
                setattr(
                    self.__nfce,
                    "codigo_emitente",
                    self.__estabelecimento.codigo,
                )
        else:
            self.__conteudo = self.__conteudo + content
            setattr(self.__nfce, self.__tag_atual, str(self.__conteudo))

    def endElement(self, name):
        """
        Evento de fechamento de tag
        """
        if (name == "procEventoNFe") or (name == "retInutNFe"):
            self.__handler_anterior.nfce = self.__nfce
            self.__parser.setContentHandler(self.__handler_anterior)
        else:
            self.__tag_atual = ""
        self.__conteudo = ""
