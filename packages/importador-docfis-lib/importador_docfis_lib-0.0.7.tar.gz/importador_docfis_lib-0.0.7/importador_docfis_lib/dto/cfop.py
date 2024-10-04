from datetime import datetime
from uuid import UUID, uuid4


class CFOP:
    
    def __init__(self):
        self.__tipo = 0
        self.__cfop = ""
        self.__grupo = 0
        self.__descricao = ""
        self.__retorno = False
        self.__statusicms = 0
        self.__statusipi = 0
        self.__rapis = 0
        self.__remas = 0
        self.__tipomov = 0
        self.__soposse = False
        self.__transporte = False
        self.__cnae = ""
        self.__codserv = ""
        self.__cpsrb = ""
        self.__observacao = ""
        self.__discriminacaorps = ""
        self.__retempis = False
        self.__retemcofins = False
        self.__retemcsll = False
        self.__retemirrf = False
        self.__ibptaxa = 0.0
        self.__id = None, 
        self.__aliquotaiss = 0.0
        self.__cfopservico = False
        self.__reducaobase = 0.0
        self.__ibptaxamunicipal = 0.0
        self.__ibptaxafederal = 0.0
        self.__incluirdeducoes = True
        self.__afeta_customedio = False
        self.__custo_nota_origem = False
        self.__id_cfop_lcp_116_2003 = None, 
        self.__tipotributacaoservico = 0
        self.__codigobeneficiofiscal = ""
        self.__sugerirtipotributacaoservico = False
        self.__lastupdate = datetime.now()
        self.__tenant = 0
    

    @property
    def tipo (self) -> int:
        return self.__tipo
    
    @tipo.setter
    def tipo (self, value):
        self.__tipo = value

    @property
    def cfop (self) -> str:
        return self.__cfop
    
    @cfop.setter
    def cfop (self, value):
        self.__cfop = value

    @property
    def grupo (self) -> int:
        return self.__grupo
    
    @grupo.setter
    def grupo (self, value):
        self.__grupo = value

    @property
    def descricao (self) -> str:
        return self.__descricao
    
    @descricao.setter
    def descricao (self, value):
        self.__descricao = value

    @property
    def retorno (self) -> bool:
        return self.__retorno
    
    @retorno.setter
    def retorno (self, value):
        self.__retorno = value

    @property
    def statusicms (self) -> int:
        return self.__statusicms
    
    @statusicms.setter
    def statusicms (self, value):
        self.__statusicms = value

    @property
    def statusipi (self) -> int:
        return self.__statusipi

    @statusipi.setter
    def statusipi (self, value):
        self.__statusipi = value

    @property
    def rapis (self) -> int:
        return self.__rapis
    
    @rapis.setter
    def rapis (self, value):
        self.__rapis = value

    @property
    def remas (self) -> int:
        return self.__remas
    
    @remas.setter
    def remas (self, value):
        self.__remas = value

    @property
    def tipomov (self) -> int:
        return self.__tipomov
    
    @tipomov.setter
    def tipomov (self, value):
        self.__tipomov = value

    @property
    def soposse (self) -> bool:
        return self.__soposse
    
    @soposse.setter
    def soposse (self, value):
        self.__soposse = value

    @property
    def transporte (self) -> bool:
        return self.__transporte
    
    @transporte.setter
    def transporte (self, value):
        self.__transporte = value

    @property
    def codserv (self) -> str:
        return self.__codserv
    
    @codserv.setter
    def codserv (self, value):
        self.__codserv = value

    @property
    def cnae (self) -> str:
        return self.__cnae
    
    @cnae.setter
    def cnae (self, value):
        self.__cnae = value

    @property
    def cpsrb (self) -> str:
        return self.__cpsrb
    
    @cpsrb.setter
    def cpsrb (self, value):
        self.__cpsrb = value

    @property
    def observacao (self) -> str:
        return self.__observacao
    
    @observacao.setter
    def observacao (self, value):
        self.__observacao = value

    @property
    def discriminacaorps (self) -> str:
        return self.__discriminacaorps
    
    @discriminacaorps.setter
    def discriminacaorps (self, value):
        self.__discriminacaorps = value

    @property
    def retempis (self) -> bool:
        return self.__retempis
    
    @retempis.setter
    def retempis (self, value):
        self.__retempis = value

    @property
    def retemcofins (self) -> bool:
        return self.__retemcofins
    
    @retemcofins.setter
    def retemcofins (self, value):
        self.__retemcofins = value

    @property
    def retemcsll (self) -> bool:
        return self.__retemcsll
    
    @retemcsll.setter
    def retemcsll (self, value):
        self.__retemcsll = value

    @property
    def retemirrf (self) -> bool:
        return self.__retemirrf
    
    @retemirrf.setter
    def retemirrf (self, value):
        self.__retemirrf = value

    @property
    def ibptaxa (self) -> float:
        return self.__ibptaxa
    
    @ibptaxa.setter
    def ibptaxa (self, value):
        self.__ibptaxa = value

    @property
    def id (self) -> UUID:
        if (self.__id is None):
            self.__id = uuid4()
        return self.__id
    
    @id.setter
    def id (self, value):
        self.__id = value

    @property
    def aliquotaiss (self) -> float:
        return self.__aliquotaiss
    
    @aliquotaiss.setter
    def aliquotaiss (self, value):
        self.__aliquotaiss = value

    @property
    def cfopservico (self) -> bool:
        return self.__cfopservico
    
    @cfopservico.setter
    def cfopservico (self, value):
        self.__cfopservico = value

    @property
    def reducaobase (self) -> float:
        return self.__reducaobase
    
    @reducaobase.setter
    def reducaobase (self, value):
        self.__reducaobase = value

    @property
    def ibptaxamunicipal (self) -> float:
        return self.__ibptaxamunicipal
    
    @ibptaxamunicipal.setter
    def ibptaxamunicipal (self, value):
        self.__ibptaxamunicipal = value

    @property
    def ibptaxafederal (self) -> float:
        return self.__ibptaxafederal
    
    @ibptaxafederal.setter
    def ibptaxafederal (self, value):
        self.__ibptaxafederal = value

    @property
    def incluirdeducoes (self) -> bool:
        return self.__incluirdeducoes
    
    @incluirdeducoes.setter
    def incluirdeducoes (self, value):
        self.__incluirdeducoes = value

    @property
    def afeta_customedio (self) -> bool:
        return self.__afeta_customedio
    
    @afeta_customedio.setter
    def afeta_customedio (self, value):
        self.__afeta_customedio = value

    @property
    def custo_nota_origem (self) -> bool:
        return self.__custo_nota_origem
    
    @custo_nota_origem.setter
    def custo_nota_origem (self, value):
        self.__custo_nota_origem = value

    @property
    def id_cfop_lcp_116_2003 (self) -> UUID:
        return self.__id_cfop_lcp_116_2003
    
    @id_cfop_lcp_116_2003.setter
    def id_cfop_lcp_116_2003 (self, value):
        self.__id_cfop_lcp_116_2003 = value

    @property
    def tipotributacaoservico (self) -> int:
        return self.__tipotributacaoservico
    
    @tipotributacaoservico.setter
    def tipotributacaoservico (self, value):
        self.__tipotributacaoservico = value

    @property
    def codigobeneficiofiscal (self) -> str:
        return self.__codigobeneficiofiscal

    @codigobeneficiofiscal.setter
    def codigobeneficiofiscal (self, value):
        self.__codigobeneficiofiscal = value

    @property
    def sugerirtipotributacaoservico (self) -> bool:
        return self.__sugerirtipotributacaoservico
    
    @sugerirtipotributacaoservico.setter
    def sugerirtipotributacaoservico (self, value):
        self.__sugerirtipotributacaoservico = value

    @property
    def lastupdate (self) -> datetime:
        return self.__lastupdate

    @lastupdate.setter
    def lastupdate (self, value):
        self.__lastupdate = value

    @property
    def tenant (self) -> int:
        return self.__tenant
    
    @tenant.setter
    def tenant (self, value):
        self.__tenant = value

    @property
    def identificador(self):
        """ Identificador do CFOP (Código) """
        return self.cfop

    @property
    def identificadorNFSE(self):
        """ Identificador do CFOP (tipo(ibge) + Código) """
        return str(self.tipo) + '_' + self.cfop

    def __str__(self) -> str:
        return self.identificador


    def __repr__(self):
        return self.identificador


    def __eq__(self, other) -> bool:
        if (other is None):
            return False
        return (self.identificador == other.identificador)


    def __ne__(self, other) -> bool:
        if (other is None):
            return True
        return (self.identificador != other.identificador)
    

    def __hash__(self):
        return hash(self.identificador)
    