from typing import List

from nasajon.dto.unidade import Unidade
from nasajon.utils.conexao_postgres_adapter import ConexaoPostgresAdapter
from nasajon.utils.utilidades_banco import UtilidadesBanco


class UnidadeDAO:
    def __init__(self, conexao: ConexaoPostgresAdapter):
        """
        Construtor do DAO de unidades
        """
        self.__conexao = conexao

    @staticmethod
    def obterSQLConsulta() -> str:
        """
        Retorna a instrução SQL para carregar os dados do banco de dados
        :return: SQL para carregar os dados do banco de dados
        """
        return "select unidade as id, codigo, id_grupo as cadastro \
                from estoque.unidades"

    def retornar_unidades(self) -> List[Unidade]:
        """
        Lista todas as unidades do banco de dados, por Grupo Empresarial
        :return: Lista das Unidades preenchidas
        """
        return UtilidadesBanco.executarConsulta(
            self.__conexao, UnidadeDAO.obterSQLConsulta(), [], Unidade
        )
