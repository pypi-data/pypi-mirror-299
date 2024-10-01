from typing import List

from importador_docfis_lib.dao.cfop_dao import CfopDAO
from importador_docfis_lib.dao.cliente_dao import ClienteDAO
from importador_docfis_lib.dao.estabelecimento_dao import EstabelecimentoDAO
from importador_docfis_lib.dao.nfce_dao import NFCeDAO
from importador_docfis_lib.dao.operacao_cfop_slot_dao import OperacaoCfopSlotDAO
from importador_docfis_lib.dao.produto_dao import ProdutoDAO
from importador_docfis_lib.dao.unidade_dao import UnidadeDAO
from importador_docfis_lib.dto.cfop import CFOP
from importador_docfis_lib.dto.estabelecimento import Estabelecimento
from importador_docfis_lib.dto.unidade import Unidade
from importador_docfis_lib.enums.enum_tipo_documento import EnumTipoDocumento
from importador_docfis_lib.utils.conexao_postgres_adapter import ConexaoPostgresAdapter


class ControllerEstabelecimento:
    """
    Classe responsável por gerenciar as operações de Estabelecimentos
    """

    def __init__(self, conn) -> None:
        self.conexao = ConexaoPostgresAdapter(conn)

    def retornar_estabelecimentos(
        self,
        estabelecimentos: list[str] = None,
        tipo_documento: EnumTipoDocumento | str = None,
    ) -> List[Estabelecimento]:
        """
        Retorna todos os estabelecimentos parametrizados, sem clientes, produtos e clientes
        :return: Estabelecimentos
        :rtype: List[Estabelecimento]
        """
        estabelecimentos: List[Estabelecimento] = EstabelecimentoDAO(
            self.conexao
        ).retornar_estabelecimentos()
        cfops: List[CFOP] = CfopDAO(self.conexao).retornar_cfops()
        unidades: List[Unidade] = UnidadeDAO().retornar_unidades()

        for estabelecimento in estabelecimentos:
            estabelecimento.unidades = {
                unidade.identificador: unidade
                for unidade in unidades
                if (
                    (unidade.cadastro is None)
                    or (unidade.cadastro == estabelecimento.cadastro)
                )
            }

            estabelecimento.cfops = {cfop.identificador: cfop for cfop in cfops}

            estabelecimento.operacoes = OperacaoCfopSlotDAO(
                self.conexao
            ).retornar_operacoes_cfop_slots(estabelecimento)

            estabelecimento.clientes = {
                cliente.identificador: cliente
                for cliente in ClienteDAO(self.conexao).retornar_clientes(
                    estabelecimento
                )
            }

            estabelecimento.produtos = {
                produto.identificador: produto
                for produto in ProdutoDAO(self.conexao).retornar_produtos(
                    estabelecimento
                )
            }

            if (
                tipo_documento == EnumTipoDocumento.NFCE.value
                or tipo_documento == EnumTipoDocumento.NFCE
            ):
                estabelecimento.nfces = {
                    nfce.identificador: nfce
                    for nfce in NFCeDAO(self.conexao).retornar_nfces(estabelecimento)
                }
        return estabelecimentos

    def retornar_estabelecimento(
        self,
        estabelecimento: str,
        tipo_documento: EnumTipoDocumento | str = None,
    ) -> Estabelecimento:
        return self.retornar_estabelecimentos([estabelecimento], tipo_documento)[0]
