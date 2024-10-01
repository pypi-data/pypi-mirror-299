from typing import List

from importador_docfis_lib.dto.cfop import CFOP
from importador_docfis_lib.utils.conexao_postgres_adapter import ConexaoPostgresAdapter
from importador_docfis_lib.utils.utilidades_banco import UtilidadesBanco

class CfopDAO:

    def __init__(self, conexao: ConexaoPostgresAdapter):
        """
        Construtor do DAO de CFOP
        """
        self.__conexao = conexao
    

    def retornar_cfops(self) -> List[CFOP]:
        """
        Lista todos os clientes
        """
        return UtilidadesBanco.executarConsulta(
                self.__conexao,
                CfopDAO.obterSQLConsulta(),
                [],
                CFOP
            )

    def gravarCFOP(self, cfops: List[CFOP]):
        """
        Grava os CFOP no banco de dados
        """
        parametros = [
            self.obterListaValoresCFOP(cfop) 
            for cfop in cfops
        ]
        UtilidadesBanco.executarComando(
                self.__conexao, 
                self.obterSQLInsertCFOP(), 
                parametros, 
                True, 
                True)

    @staticmethod
    def obterSQLConsulta() -> str:
        
        sql =  "SELECT c.tipo, c.cfop, grupo, c.descricao, c.retorno, c.statusicms, c.statusipi, \
                    c.rapis, c.remas, c.tipomov, c.soposse, c.transporte, c.cnae, c.codserv, c.cpsrb, \
                    c.observacao, c.discriminacaorps, c.retempis, c.retemcofins, c.retemcsll, \
                    c.retemirrf, c.ibptaxa, c.id, c.aliquotaiss, c.cfopservico, c.reducaobase, \
                    c.ibptaxamunicipal, c.ibptaxafederal, c.incluirdeducoes, c.afeta_customedio, \
                    c.custo_nota_origem, c.id_cfop_lcp_116_2003, c.tipotributacaoservico, \
                    c.codigobeneficiofiscal, c.sugerirtipotributacaoservico, c.lastupdate, \
                    c.tenant \
                FROM ns.cfop c"

        return sql
                

                        
    @staticmethod
    def obterSQLInsertCFOP() -> str:
        """ Retorna o comando SQL para insert na tabela ns.cfop """
        return """insert into ns.cfop (id, cfop, tipo, grupo, descricao) values %s"""

    @staticmethod
    def obterListaValoresCFOP(cfop: CFOP) -> List:
        """
        retorna uma lista com os valores para o insert no cfop
        """
        valores = list()
        valores.append(str(cfop.id)) # id
        valores.append(cfop.cfop) # cfop
        valores.append(cfop.tipo) # tipo
        valores.append(4) # grupo
        valores.append("CFOP INCLUIDO NA IMPORTACAO") # descricao
        
        return valores