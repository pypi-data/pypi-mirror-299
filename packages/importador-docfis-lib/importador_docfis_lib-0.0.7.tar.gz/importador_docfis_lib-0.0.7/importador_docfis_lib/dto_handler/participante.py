import uuid

class Participante:
    """
    Classe de Domínio de Destinatários de NFCe
    """
    def __init__(self):
        self.__id = None
        self.__CPF = ""
        self.__CNPJ = ""
        self.__xNome = ""
        self.__IE = ""
        self.__id_estabelecimento = None
        self.__id_endereco = None
        self.__conjunto = None
        self.__xLgr = ""
        self.__nro = ""
        self.__xBairro = ""
        self.__xCpl = ""
        self.__cMun = ""
        self.__xMun = ""
        self.__CEP = ""
        self.__UF = ""
        self.__email = ""
        # Para NFSE que não é um xml, então não precisa de funcoes de property 
        self.tipo_logradouro = ""
        self.IM = ""

    @property
    def id(self) -> uuid.UUID:
        """ Identificador no Banco de Dados (ns.pessoas) """
        return self.__id
    
    @id.setter
    def id(self, value: uuid.UUID):
        self.__id = value


    @property
    def CPF(self) -> str:
        return self.__CPF
    
    @CPF.setter
    def CPF(self, value: str):
        self.__CPF = value
        
    @property
    def CNPJ(self) -> str:
        return self.__CNPJ
    
    @CNPJ.setter
    def CNPJ(self, value: str):
        self.__CNPJ = value


    @property
    def xNome(self) -> str:
        """ Nome da Pessoa """
        return self.__xNome
    
    @xNome.setter
    def xNome(self, value:str):
        self.__xNome = value
        
    @property
    def nome(self) -> str:
        """ Nome da Pessoa """
        return self.__xNome
    
    @nome.setter
    def nome(self, value:str):
        self.__xNome = value
        
    @property
    def IE(self) -> str:
        """ Inscrição Estadual """
        return self.__IE
    
    @IE.setter
    def IE(self, value:str):
        self.__IE = value
        
    @property
    def xLgr(self) -> str:
        """ Logradouro """
        return self.__xLgr
    
    @xLgr.setter
    def xLgr(self, value:str):
        self.__xLgr = value
        
    @property
    def logradouro(self) -> str:
        """ Logradouro """
        return self.__xLgr
    
    @logradouro.setter
    def logradouro(self, value:str):
        self.__xLgr = value
        
    @property
    def nro(self) -> str:
        """ Número do logradouro """
        return self.__nro
    
    @nro.setter
    def nro(self, value:str):
        self.__nro = value
        
    @property
    def numero(self) -> str:
        """ Número do logradouro """
        return self.__nro
    
    @numero.setter
    def numero(self, value:str):
        self.__nro = value
        
    @property
    def xBairro(self) -> str:
        """ Bairro """
        return self.__xBairro
    
    @xBairro.setter
    def xBairro(self, value:str):
        self.__xBairro = value
        
    @property
    def bairro(self) -> str:
        """ Bairro """
        return self.__xBairro
    
    @bairro.setter
    def bairro(self, value:str):
        self.__xBairro = value
        
    @property
    def xCpl(self) -> str:
        """ Complemento """
        return self.__xCpl
    
    @xCpl.setter
    def xCpl(self, value:str):
        self.__xCpl = value
        
    @property
    def complemento(self) -> str:
        """ Complemento """
        return self.__xCpl
    
    @complemento.setter
    def complemento(self, value:str):
        self.__xCpl = value
        
    @property
    def cMun(self) -> str:
        """ IBGE """
        return self.__cMun
    
    @cMun.setter
    def cMun(self, value:str):
        self.__cMun = value
        
    @property
    def ibge(self) -> str:
        """ IBGE """
        return self.__cMun
    
    @ibge.setter
    def ibge(self, value:str):
        self.__cMun = value
        
    @property
    def xMun(self) -> str:
        """ Cidade """
        return self.__xMun
    
    @xMun.setter
    def xMun(self, value:str):
        self.__xMun = value
        
    @property
    def cidade(self) -> str:
        """ Cidade """
        return self.__xMun
    
    @cidade.setter
    def cidade(self, value:str):
        self.__xMun = value
    
    @property
    def CEP(self) -> str:
        """ CEP """
        return self.__CEP
    
    @CEP.setter
    def CEP(self, value:str):
        self.__CEP = value
        
    @property
    def UF(self) -> str:
        """ UF """
        return self.__UF
    
    @UF.setter
    def UF(self, value:str):
        self.__UF = value
        
    @property
    def email(self) -> str:
        """ email """
        return self.__email
    
    @email.setter
    def email(self, value:str):
        self.__email = value

    @property
    def id_estabelecimento(self) -> uuid.UUID:
        return self.__id_estabelecimento
    
    @id_estabelecimento.setter
    def id_estabelecimento(self, value: uuid.UUID):
        self.__id_estabelecimento = value
    
    @property
    def id_endereco(self) -> uuid.UUID:
        return self.__id_endereco
    
    @id_endereco.setter
    def id_endereco(self, value: uuid.UUID):
        self.__id_endereco = value

    @property
    def conjunto(self) -> uuid.UUID:
        return self.__conjunto
    
    @conjunto.setter
    def conjunto(self, value: uuid.UUID):
        self.__conjunto = value


    @property
    def identificador(self) -> str:
        """ Identificador único da pessoa no sistema (CPF ou CNPJ) """
        return (self.CPF if self.CPF else self.CNPJ).replace(".","").replace("-","").replace("/","")
    

    def __str__(self) -> str:
        return (("CPF: " + self.CPF ) if self.CPF else ("CNPJ: " + self.CNPJ )) + ' - Nome: ' + self.xNome


    def __repr__(self) -> str:
        return self.identificador


    def __hash__(self) -> int:
        return hash(self.identificador)
    
    @property
    def Cnpj(self) -> str:
        """ Cnpj """
        return self.__CNPJ
    
    @Cnpj.setter
    def Cnpj(self, value:str):
        self.__CNPJ = value
        
    @property
    def Cpf(self) -> str:
        """ Cpf """
        return self.__CPF
    
    @Cpf.setter
    def Cpf(self, value:str):
        self.__CPF = value
        
    @property
    def InscricaoMunicipal(self) -> str:
        """ IM """
        return self.IM
    
    @InscricaoMunicipal.setter
    def InscricaoMunicipal(self, value:str):
        self.IM = value
        
    @property
    def RazaoSocial(self) -> str:
        """ RazaoSocial """
        return self.__xNome
    
    @RazaoSocial.setter
    def RazaoSocial(self, value:str):
        self.__xNome = value
        
    @property
    def Endereco(self) -> str:
        """ Endereco """
        return self.__xLgr
    
    @Endereco.setter
    def Endereco(self, value:str):
        self.__xLgr = value
        
    @property
    def Numero(self) -> str:
        """ Numero """
        return self.__nro
    
    @Numero.setter
    def Numero(self, value:str):
        self.__nro = value
        
    @property
    def Complemento(self) -> str:
        """ Complemento """
        return self.__xCpl
    
    @Complemento.setter
    def Complemento(self, value:str):
        self.__xCpl = value
        
    @property
    def Bairro(self) -> str:
        """ Bairro """
        return self.__xBairro
    
    @Bairro.setter
    def Bairro(self, value:str):
        self.__xBairro = value
        
    @property
    def CodigoMunicipio(self) -> str:
        """ CodigoMunicipio """
        return self.ibge
    
    @CodigoMunicipio.setter
    def CodigoMunicipio(self, value:str):
        self.ibge = value
        
    @property
    def Uf(self) -> str:
        """ Uf """
        return self.__UF
    
    @Uf.setter
    def Uf(self, value:str):
        self.__UF = value
        
    @property
    def Cep(self) -> str:
        """ Cep """
        return self.__CEP
    
    @Cep.setter
    def Cep(self, value:str):
        self.__CEP = value
    
    @property
    def Email(self) -> str:
        """ email """
        return self.__email
    
    @Email.setter
    def Email(self, value:str):
        self.__email = value