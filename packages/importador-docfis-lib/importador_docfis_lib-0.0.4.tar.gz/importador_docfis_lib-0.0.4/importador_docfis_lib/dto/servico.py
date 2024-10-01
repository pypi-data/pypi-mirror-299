class Servico:
    """
    Classe de Domínio de Servico
    """    
    def __init__(self):
        
        self.codigo = ""
        self.tipo = 1
        self.id = None
        self.descricao = ""
        self.lcp = ""
        
    @property
    def identificador(self):
        """ Descrição do Servico """
        return self.codigo
        
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