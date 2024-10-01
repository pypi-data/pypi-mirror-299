import xml.sax

from nasajon.dto.estabelecimento import Estabelecimento
from nasajon.dto_handler.participante import Participante
from nasajon.enums.enum_tipo_documento import EnumTipoDocumento


class DestinatarioHandler(xml.sax.ContentHandler):
    """
    Classe responsável por tratar os eventos disparados pelo Sax Parser \
    relativos a um Destinatario de Nota
    """

    def __init__(
        self,
        parser,
        handler_anterior,
        estabelecimento: Estabelecimento,
        tipo_documento: EnumTipoDocumento | str,
    ):
        self.__estabelecimento = estabelecimento
        self.__handler_anterior = handler_anterior
        self.__parser = parser
        self.__destinatario = Participante()
        self.__tag_atual = ""
        self.__conteudo = ""
        self.__tipoDocumento = tipo_documento

    @property
    def cliente(self) -> Participante:
        return self.__destinatario

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
        if not hasattr(self.__destinatario, self.__tag_atual):
            return
        self.__conteudo = self.__conteudo + content
        setattr(self.__destinatario, self.__tag_atual, str(self.__conteudo))

    def endElement(self, name):
        """
        Evento de fechamento de tag
        """
        self.__tag_atual = ""
        if (name == "dest") or (name == "CNPJ"):
            if (
                self.__destinatario.CPF is not None
                and len(self.__destinatario.CPF) == 11
            ) or (self.__tipoDocumento == EnumTipoDocumento.NFE.value):
                if (
                    self.__estabelecimento is not None
                    and self.__destinatario.identificador
                    in self.__estabelecimento.clientes
                ):
                    self.__destinatario.id = self.__estabelecimento.clientes[
                        self.__destinatario.identificador
                    ].id

                if self.__tipoDocumento == EnumTipoDocumento.SAT.value:
                    self.__handler_anterior.sat.destinatario = self.__destinatario
                elif self.__tipoDocumento == EnumTipoDocumento.NFE.value:
                    self.__handler_anterior.nfe.destinatario = self.__destinatario
                else:
                    self.__handler_anterior.nfce.destinatario = self.__destinatario

            self.__parser.setContentHandler(self.__handler_anterior)
            self.__conteudo = ""
