from typing import List

from sqlalchemy.engine.base import Connection

class ConexaoPostgresAdapter:
    """
    Classe responsável por encapsular as operações com banco de dados Postgres.
    É uma extensão da classe ConexaoPadrao.
    """

    def __init__(self, conexao: Connection):
        self.__conexao = conexao
        self._transaction = None

    def comecar_transacao(self):
        if self._transaction is None:
            self._transaction = self.__conexao.begin()

    def fechar_transacao(self):
        if self._transaction is None:
            self._transaction = None

    def commit(self):
        if self._transaction is not None:
            self._transaction.commit()
            self._transaction = None

    def rollback(self):
        if self._transaction is not None:
            self._transaction.rollback()
            self._transaction = None

    @property
    def conexao(self):
        """
        Conexão ao Banco de Dados Postgres
        """
        return self.__conexao

    def executarComando(
        self, sql: str, parametros: dict, manter_transacao=False
    ) -> None:
        """
        Executa uma instrução sql sem retorno
        :param sql: Texto do Comando SQL a ser executado. Caso haja \
        parâmetros, os mesmos devem ser passados no argumento parametros
        :param parametros: Dicionário contendo os parâmetros a serem aplicados\
        no comando sql, no formato <Nome, Valor>
        :param manterTransacao: Parâmetro booleano para indicar se há um controle\
        externo de transação ou não.
        """
        try:
            self.comecar_transacao()
            if parametros:
                self.conexao.execute(sql, parametros)
            else:
                self.conexao.execute(sql)
            if not manter_transacao:
                self.commit()
        except:
            if not manter_transacao:
                self.rollback()
            raise

    def executarBulk(
        self, sql: str, parametros: list, manter_transacao=False
    ) -> None:
        """
        Executa uma instrução sql em lote, sem retorno

        Args:
            sql:        Texto do Comando SQL a ser executado. Caso haja \
        parâmetros, os mesmos devem ser passados no argumento parametros
            parametros: lista de listas no formato: \
        Registros[Campos[],Campos[],...,Campos[]]
            manterTransacao: Parâmetro booleano para indicar se há um controle\
        externo de transação ou não.
        """
        try:
            self.comecar_transacao()
            for parametro in parametros:
                self.conexao.execute(sql, parametro)
            if not manter_transacao:
                self.commit()
        except:
            if not manter_transacao:
                self.rollback()
            raise

    def executarConsulta(
        self, sql: str, parametros: dict
    ) -> List[dict]:
        """
       Executa uma instrução sql retornando uma lista de dicionário \
       (nome_campo:Valor)

       :param sql: Texto do Comando SQL a ser executado. Caso haja \
       parâmetros, os mesmos devem ser passados no argumento parametros
       :param parametros: Dicionário contendo os parâmetros a serem aplicados\
       no comando sql, no formato <Nome, Valor>
       :param manterTransacao: Parâmetro booleano para indicar se há um controle\
       externo de transação ou não.
       :return: List[dict]
       """
        try:
            new_transaction = self._transaction is None
            if not new_transaction:
                self.comecar_transacao()
            cursor = self.conexao.execute(sql, parametros)
            resultado = cursor.fetchall()
        finally:
            cursor.close()
            if not new_transaction:
                self.fechar_transacao()
        return [dict(res.items()) for res in resultado]
