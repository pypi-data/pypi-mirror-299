from typing import List

import psycopg2
import psycopg2.extensions
import psycopg2.extras


class ConexaoPostgresAdapter:
    """
    Classe responsável por encapsular as operações com banco de dados Postgres.
    É uma extensão da classe ConexaoPadrao.
    """

    def __init__(self, conexao):
        self.__conexao = conexao
        self.__cursor = conexao.cursor()
        self.__ocupada = False
        self.__alocada = False

    @property
    def conexao(self):
        """
        Conexão ao Banco de Dados Postgres
        """
        return self.__conexao

    @property
    def cursor(self):
        """
        Cursor conectado ao Banco de Dados Postgres
        """
        return self.__cursor

    def executarComando(
        self, sql: str, parametros: dict, manterTransacao=False
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
            self.__ocupada = True
            self.cursor.execute(sql, parametros)
            if not manterTransacao:
                self.__conexao.commit()
        finally:
            self.__ocupada = False

    def executarBulk(
        self, sql: str, parametros: list, manterTransacao=False, template: str = None
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
            template:   Utilizado para a realização de BulkInsert, deve conter \
        o formato de substituição dos campos no SQL
        """
        self.__ocupada = True
        try:
            psycopg2.extras.execute_values(
                self.cursor, sql, parametros, template, 10000
            )
            if not manterTransacao:
                self.__conexao.commit()
        except:
            if not manterTransacao:
                self.__conexao.rollback()
            raise
        finally:
            self.__ocupada = False

    def executarConsulta(
        self, sql: str, parametros: dict, manterTransacao=False
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
        self.__ocupada = True
        try:
            self.cursor.execute(sql, parametros)
            resultado = self.cursor.fetchall()
            retorno = [
                {
                    campo.name: registro[self.cursor.description.index(campo)]
                    for campo in self.cursor.description
                }
                for registro in resultado
            ]
            if not manterTransacao:
                self.__conexao.commit()
        except:
            if not manterTransacao:
                self.__conexao.rollback()
            raise
        finally:
            self.__ocupada = False
        return retorno

    def disponivel(self) -> bool:
        """
        Retorna True quando a conexão está disponível para uso
        :return: Disponível? Sim ou Não
        """
        return not (self.__ocupada or self.__alocada)

    def fechar(self) -> None:
        """
        Fecha a conexão ao banco de dados
        """
        try:
            self.cursor.close()
        except Exception:
            pass  # abafar exceção
        try:
            self.conexao.close()
        except Exception:
            pass  # abafar exceção

    def start_transaction(self) -> None:
        """
        Inicia uma transação
        """
        self.commit()

    def commit(self) -> None:
        """
        Confirma uma transação
        """
        self.conexao.commit()

    def rollback(self) -> None:
        """
        Cancela uma transação
        """
        self.conexao.rollback()

    def obterExclusividade(self) -> None:
        """
        Marca a conexão como "ocupada" por um objeto
        """
        self.__alocada = True

    def liberarExclusividade(self) -> None:
        """
        Desmarca a conexão como "ocupada" por um objeto
        """
        self.__alocada = False
        self.__ocupada = False

    def forcarLiberacao(self) -> None:
        """
        Retira a exclusividade da conexao, quando possível
        """
        if self.conexao.status != psycopg2.extensions.STATUS_IN_TRANSACTION:
            self.liberarExclusividade()
