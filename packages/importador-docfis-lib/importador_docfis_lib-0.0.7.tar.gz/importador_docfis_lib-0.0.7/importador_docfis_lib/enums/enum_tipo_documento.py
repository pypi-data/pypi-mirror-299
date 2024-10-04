from enum import Enum


class EnumTipoDocumento(Enum):
    """
    Enumerado para guardar os tipos de documentos suportados
    """
    NFCE = "NFCE"
    CTE = "CTE"
    NFSE = "NFSE"
    SAT = "SAT"
    CONV11503 = "CONV11503"  # Convenio 115/2003
    NFE = "NFE" # Nota Fiscal, modelo 55
