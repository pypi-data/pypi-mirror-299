from typing import List

from importador_docfis_lib.dto.estabelecimento import Estabelecimento
from importador_docfis_lib.dto.operacao_cfop_slot import OperacaoCfopSlot
from importador_docfis_lib.utils.conexao_postgres_adapter import ConexaoPostgresAdapter
from importador_docfis_lib.utils.utilidades_banco import UtilidadesBanco

class OperacaoCfopSlotDAO:

    def __init__(self, conexao: ConexaoPostgresAdapter):
        """
        Construtor do DAO de OperacaoCfopSlot
        """
        self.__conexao = conexao


    def retornar_operacoes_cfop_slots(self, estabelecimento: Estabelecimento) -> List[OperacaoCfopSlot]:
        """
        Lista todas os OperacõesCfopSlots 
        """
        return UtilidadesBanco.executarConsulta(
                self.__conexao,
                OperacaoCfopSlotDAO.obterSQLConsulta(estabelecimento),
                [],
                OperacaoCfopSlot
            )

    @staticmethod
    def obterSQLConsulta(estabelecimento: Estabelecimento) -> str:
        return "select 	opr.operacao, \
                        opr.codigo, \
                        opr.descricao, \
                        opr.sinal, \
                        opr.afetacustodosprodutos,\
                        cfp.cfop,\
                        string_agg(ocs.slot,',') as slots, \
                        est.estabelecimento as id_estabelecimento \
                from estoque.operacoes opr \
                join ns.estabelecimentos est 	on      (opr.id_empresa = est.empresa) \
                                                    or  (opr.id_empresa is null) \
                join estoque.operacoescfops ocf on opr.operacao = ocf.operacao \
                                                and ocf.ativo = True \
                join ns.cfop cfp on ocf.cfop = cfp.id \
                join estoque.operacoescfopsslots ocs 	on      opr.operacao = ocs.operacao \
                                                            and ocf.operacaocfop = ocs.operacaocfop \
                                                            and ocs.entrada = False \
                where       ((est.estabelecimento = '"+ str(estabelecimento.id) +"') or (opr.id_empresa is null)) \
                        and opr.sinal = 0 \
                group by 1, 2, 3, 4, 5, 6, 8"