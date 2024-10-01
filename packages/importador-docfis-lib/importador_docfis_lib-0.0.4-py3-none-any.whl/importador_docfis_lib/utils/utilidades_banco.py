from typing import List

from nasajon.utils import utilidades
from nasajon.utils.conexao_postgres_adapter import ConexaoPostgresAdapter


class UtilidadesBanco:
    """
    Classe utilizada para centralizar as operações com o banco de dados.
    Dada uma conexão, o objeto fornecerá funcionalidades para executar comandos\
    SQL
    """

    @staticmethod
    def executarComando(
        conexao: ConexaoPostgresAdapter,
        sql: str,
        parametros,
        bulk: bool = False,
        manterTransacao=False,
        template: str = None,
    ) -> None:
        """
        Executa uma instrução sql sem retorno

        Note:
            Se não for passada uma conexão, será obtida a primeira disponível\
        no Pool.

        :param conexao: Objeto do tipo ConexaoPadrao que será a conexão \
        utilizado para interagir com o banco de dados
        :param sql: Texto do Comando SQL a ser executado. Caso haja \
        parâmetros, os mesmos devem ser passados no argumento parametros
        :param parametros: Quando (Bulk = False) > Dicionário contendo os \
        parâmetros a serem aplicados no comando sql, no formato <Nome, Valor> \
        Quando (Bulk = True) > lista de listas no formato \
        Registros[Campos[],Campos[],...,Campos[]]
        :param bulk: Informa se a lista de parametros contém 1 (False) ou \
            varios registros (True)
        :param manterTransacao: Indica se há controle transacional ou se a \
        transação é implícita
        :param template: Utilizado para a realização de BulkInsert, deve conter \
        o formato de substituição dos campos no SQL
        """
        if bulk:
            conexao.executarBulk(sql, parametros, manterTransacao, template)
        else:
            conexao.executarComando(sql, parametros, manterTransacao)

    @staticmethod
    def executarConsulta(
        conexao: ConexaoPostgresAdapter,
        sql: str,
        parametros: dict,
        classeRetorno,
        manterTransacao=False,
    ) -> List[object]:
        """
        Executa uma instrução sql retornando uma lista de DTO

        Note:
            Se não for passada uma conexão, será obtida a primeira disponível no\
        Pool.

        :param conexao: Objeto do tipo ConexaoPadrao que será a conexão \
        utilizado para interagir com o banco de dados
        :param sql: Texto do Comando SQL a ser executado. Caso haja \
        parâmetros, os mesmos devem ser passados no argumento parametros
        :param parametros: Dicionário contendo os parãmetros a serem aplicados\
        no comando sql, no formato <Nome, Valor>
        :param classeRetorno: Classe dos objetos Dto que serão retornados na lista
        manterTransacao:
        :param manterTransacao: Indica se há controle transacional ou se a \
        transação é implícita
        :return: Lista de Objetos populados
        """
        listaDeRegistros = conexao.executarConsulta(sql, parametros, manterTransacao)
        if classeRetorno is not None:
            return UtilidadesBanco.obterObjetosPreenchidos(
                listaDeRegistros, classeRetorno
            )
        else:
            return listaDeRegistros

    @staticmethod
    def obterObjetosPreenchidos(registros: List[dict], classeRetorno) -> List[object]:
        """
        Preenche uma lista de objetos a partir de um retorno de uma query

        :param registros: Lista de dict com os dados retornados pela consulta
        :param classeRetorno: Classe dos objetos Dto que serão retornados na lista
        :return: objetos preenchidos
        """
        return [
            utilidades.preencher_objeto(registro, classeRetorno)
            for registro in registros
        ]
