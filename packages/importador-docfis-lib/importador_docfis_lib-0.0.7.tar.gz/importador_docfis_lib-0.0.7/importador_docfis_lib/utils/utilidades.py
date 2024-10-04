from datetime import datetime
from pytz import timezone

def now_brazil():
    return datetime.now(timezone("America/Sao_Paulo")).strftime("%Y-%m-%d %H:%M:%S")

def elemento_mais_comum(lista: list[str]) -> str:
    """
    Retorna o elemento que mais se repete na lista
    :param lista: lista a ser analisada
    :return: o elemento mais comum
    """
    if not lista:
        return None
    return max(set(lista), key=lista.count)

def preencher_objeto(registro: dict, classeRetorno) -> object:
    """
    Preenche um objeto a partir de um dict retornado de uma query
    """
    objeto = classeRetorno()
    for chave, valor in registro.items():
        if hasattr(objeto, chave):
            setattr(objeto, chave, valor)
    return objeto