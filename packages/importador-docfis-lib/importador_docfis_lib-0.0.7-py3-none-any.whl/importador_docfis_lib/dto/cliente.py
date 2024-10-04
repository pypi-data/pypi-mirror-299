from uuid import UUID


class Cliente:
    """
    Classe DTO de Clientes
    """

    def __init__(self):
        self.__id = None
        self.__cnpj = ""
        self.__nome = ""
        self.__estabelecimento = None

    @property
    def id(self) -> UUID:
        """
        Identificador no Banco de Dados (ns.pessoas)
        """
        return self.__id

    @id.setter
    def id(self, value: UUID):
        self.__id = value

    @property
    def cnpj(self) -> str:
        """
        CNPJ ou CPF da pessoa
        """
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, value: str):
        self.__cnpj = value

    @property
    def nome(self) -> str:
        """
        Nome da Pessoa
        """
        return self.__nome

    @nome.setter
    def nome(self, value: str):
        self.__nome = value

    @property
    def estabelecimento(self) -> UUID:
        """
        Identificador do Estabelecimento no banco de dados \
        (ns.estabelecimentos)
        """
        return self.__estabelecimento

    @estabelecimento.setter
    def estabelecimento(self, value: UUID):
        self.__estabelecimento = value

    @property
    def identificador(self) -> str:
        """
        Identificador único da pessoa no sistema (CPF/CNPJ)
        """
        return self.cnpj

    def __str__(self) -> str:
        return "CPF: " + self.cnpj + ' - Nome: ' + self.nome

    def __repr__(self) -> str:
        return self.identificador

    def __hash__(self) -> int:
        return hash(self.identificador)
