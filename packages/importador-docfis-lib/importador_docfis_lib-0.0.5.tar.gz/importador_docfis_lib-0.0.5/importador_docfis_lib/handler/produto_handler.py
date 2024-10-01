
import xml.sax

from importador_docfis_lib.dto.estabelecimento import Estabelecimento
from importador_docfis_lib.dto_handler.item_nota import ItemNota
from importador_docfis_lib.enums.enum_tipo_documento import EnumTipoDocumento
from importador_docfis_lib.handler.cofins_handler import COFINSHandler
from importador_docfis_lib.handler.icms_handler import ICMSHandler
from importador_docfis_lib.handler.pis_handler import PISHandler

class ProdutoHandler(xml.sax.ContentHandler):
    """
    Classe responsável por tratar os eventos disparados pelo Sax Parser \
    relativos a um Item de Nota
    """
    def __init__(
        self, 
        parser, 
        handler_anterior, 
        estabelecimento: Estabelecimento,
        tipo_documento: EnumTipoDocumento|str
    ):
        self.__estabelecimento = estabelecimento
        self.__handler_anterior = handler_anterior
        self.__parser = parser
        self.__item_nota = ItemNota()
        self.__tag_atual = ""
        self.__conteudo = ""
        self.__tipoDocumento = tipo_documento


    @property
    def produto(self) -> ItemNota:
        return self.__item_nota


    def startElement(self, name, attrs):
        """
        Evento de abertura de tag
        """
        if (name == "PIS"):
            pis_handler = PISHandler(self.__parser, self)
            self.__parser.setContentHandler(pis_handler)            
        elif (name == "COFINS"):
            cofins_handler = COFINSHandler(self.__parser, self)
            self.__parser.setContentHandler(cofins_handler)
        elif (name == "ICMS"):
            icms_handler = ICMSHandler(self.__parser, self)
            self.__parser.setContentHandler(icms_handler)           
        else:
            self.__tag_atual = name
        self.__conteudo = ""


    def characters(self, content):
        """
        Evento de conteúdo de tag
        """
        #logging.debug(str(type(self)) + " > " + self.__tag_atual + " : "  + content)
        if (not hasattr(self.__item_nota, self.__tag_atual)):
            return
        self.__conteudo = self.__conteudo + content
        setattr(self.__item_nota, self.__tag_atual, str(self.__conteudo))


    def endElement(self, name):
        """
        Evento de fechamento de tag
        """
        #logging.debug("Valor do Atributo > " + self.__tag_atual + " : "  + self.__conteudo)
        if (name == "det"):
            if (
                    (self.__estabelecimento is not None)
                and (self.__item_nota.cProd in self.__estabelecimento.produtos)
            ):
                self.__item_nota.id_produto = self.__estabelecimento.produtos[
                                                    self.__item_nota.cProd
                                                ].id
                if ((self.__estabelecimento.produtos[self.__item_nota.cProd].grupoinventario) == self.__item_nota.giGorjeta()):
                    self.__item_nota.item_gorjeta = True
            if self.__tipoDocumento == EnumTipoDocumento.NFCE or self.__tipoDocumento == EnumTipoDocumento.NFCE.value:
                self.__handler_anterior.nfce.lista_itens.append(self.__item_nota)
            # elif (self.__tipoDocumento == EnumTipoDocumento.SAT.value):
            #     self.__handler_anterior.sat.listaItens.append(self.__itemNota)
            # elif (self.__tipoDocumento == EnumTipoDocumento.NFE.value):
            #     self.__handler_anterior.nfe.listaItens.append(self.__itemNota)
            
            self.__parser.setContentHandler(self.__handler_anterior)
        self.__tag_atual = ""
        self.__conteudo = ""