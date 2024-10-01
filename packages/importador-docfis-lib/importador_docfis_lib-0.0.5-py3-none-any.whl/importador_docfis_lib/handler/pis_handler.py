import xml.sax

from importador_docfis_lib.dto_handler.pis import PIS
from importador_docfis_lib.handler.nfce_handler import NFCeHandler


class PISHandler(xml.sax.ContentHandler):
    """
    Classe responsável por tratar os eventos disparados pelo Sax Parser \
    relativos ao PIS de um Item de Nota
    """
    def __init__(self, parser, handler_anterior):
        self.__parser = parser
        self.__handler_anterior = handler_anterior
        self.__pis = PIS()
        self.__tag_atual = ""
        self.__conteudo = ""

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
        #logging.debug(str(type(self)) + " > " + self.__tag_atual + " : "  + content)
        if (not hasattr(self.__pis, self.__tag_atual)):
            return
        self.__conteudo = self.__conteudo + content
        setattr(self.__pis, self.__tag_atual, str(self.__conteudo))
    
    def endElement(self, name):
        """
        Evento de fechamento de tag
        """        
        if (name == "PIS"):
            if (self.__handler_anterior is NFCeHandler):
                self.__handler_anterior.nfce.pis = self.__pis
            else:
                self.__handler_anterior.produto.pis = self.__pis
            self.__parser.setContentHandler(self.__handler_anterior)
        else:
            self.__tag_atual = ""
        self.__conteudo = ""
