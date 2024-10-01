import xml.sax

from nasajon.dto_handler.icms import ICMS
from nasajon.enums.enum_tipo_documento import EnumTipoDocumento
from nasajon.handler.nfce_handler import NFCeHandler


class ICMSHandler(xml.sax.ContentHandler):
    """
    Classe responsável por tratar os eventos disparados pelo Sax Parser \
    relativos ao ICMS de um Item de Nota
    """

    def __init__(self, parser, handler_anterior, tipo_documento: EnumTipoDocumento|str):
        self.__parser = parser
        self.__handler_anterior = handler_anterior
        self.__icms = ICMS()
        self.__tag_atual = ""
        self.__conteudo = ""
        self.__tipoDocumento = tipo_documento

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
        # logging.debug(str(type(self)) + " > " + self.__tag_atual + " : "  + content)
        if not hasattr(self.__icms, self.__tag_atual):
            return
        self.__conteudo = self.__conteudo + content
        setattr(self.__icms, self.__tag_atual, str(self.__conteudo))

    def endElement(self, name):
        """
        Evento de fechamento de tag
        """
        if name == "ICMS":
            if self.__tipoDocumento == EnumTipoDocumento.NFCE or self.__tipoDocumento == EnumTipoDocumento.NFCE.value:
                if self.__handler_anterior is NFCeHandler:
                    self.__handler_anterior.nfce.icms = self.__icms
                else:
                    self.__handler_anterior.produto.icms = self.__icms
            # elif( self.__tipoDocumento == EnumTipoDocumento.CTE.value ):
            #     self.__handler_anterior.cte.icms = self.__icms
            # elif (self.__tipoDocumento == EnumTipoDocumento.SAT.value):
            #     if (self.__handler_anterior is NFCeHandler):
            #         self.__handler_anterior.sat.icms = self.__icms
            #     else:
            #         self.__handler_anterior.produto.icms = self.__icms
            # elif( self.__tipoDocumento == EnumTipoDocumento.NFE.value ):
            #     if self.__handler_anterior is NFeHandler or self.__handler_anterior is NFeEntradaHandler:
            #         self.__handler_anterior.nfe.icms = self.__icms
            #     else:
            #         self.__handler_anterior.produto.icms = self.__icms

            self.__parser.setContentHandler(self.__handler_anterior)
        self.__tag_atual = ""
        self.__conteudo = ""
