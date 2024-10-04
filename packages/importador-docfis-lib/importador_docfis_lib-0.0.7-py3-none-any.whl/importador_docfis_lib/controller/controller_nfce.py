import io
import xml
from importador_docfis_lib.dao.nfce_dao import NFCeDAO
from importador_docfis_lib.dto.estabelecimento import Estabelecimento
from importador_docfis_lib.dto_handler.nfce import NFCE
from importador_docfis_lib.handler.nfce_handler import NFCeHandler
from importador_docfis_lib.utils.conexao_postgres_adapter import ConexaoPostgresAdapter


class ControllerNFCE:
    def __init__(self, conn) -> None:
        self.conexao = ConexaoPostgresAdapter(conn)

    def parse_xml(
        self,
        xml_str: str,
        estabelecimentos: dict[str, Estabelecimento] = None,
        estabelecimento: Estabelecimento = None,
    ):
        parser = xml.sax.make_parser()
        handler = NFCeHandler(
            parser, estabelecimentos=estabelecimentos, estabelecimento=estabelecimento
        )
        parser.setContentHandler(handler)
        stream = io.StringIO(xml_str)
        parser.parse(stream)
        nfce = handler.nfce
        stream.close()
        nfce.xml = xml_str
        if not nfce.identificador:
            raise Exception('XML não contém parte do protNFe, então é possível que a nota não tenha sido emitida para garantir que a chave da nota é única')

        if estabelecimento is None:
            estabelecimento = estabelecimentos[nfce.identificadorEmitente]

        nfce.id_emitente = estabelecimento.id
        nfce.codigo_emitente = estabelecimento.codigo

        consulta_nfce = NFCeDAO(self.conexao).retornar_nfce_identificador(
            nfce.identificador, estabelecimento
        )
        if consulta_nfce:
            nfce.id = consulta_nfce[0].id

        nfce.operacaoCfopSlot = estabelecimento.retornar_operacao_cfop(
            nfce.calcular_cfop()
        )

        nfce.outras_icms = sum(
            item.icms.retornar_outras_icms(item.valorContabil)
            for item in nfce.lista_itens
        )

        return nfce

    def gravar_nota(
        self,
        nota: NFCE,
        estabelecimento: Estabelecimento,
        sobrescrever=False,
    ):
        try:
            self.conexao.comecar_transacao()
            dao = NFCeDAO(self.conexao)

            if sobrescrever and nota.id:
                dao.atualizar_nfce([nota], [estabelecimento])
            elif nota.id:
                raise Exception("Nota já existe no banco.")
            else:
                dao.incluir_nfce([nota], [estabelecimento])
            self.conexao.commit()
        except Exception as e:
            self.conexao.rollback()
            raise e
        
    def gravar_notas(
        self,
        notas: list[NFCE],
        estabelecimentos: list[Estabelecimento],
        sobrescrever=False,
    ):
        try:
            self.conexao.start_transaction()
            dao = NFCeDAO(self.conexao)
            notas_inserir = [nota for nota in notas if nota.id is None]
            notas_atualizar = [nota for nota in notas if nota.id is not None]

            if sobrescrever:
                dao.atualizar_nfce(notas_atualizar, estabelecimentos)

            dao.incluir_nfce(notas_inserir, estabelecimentos)
            self.conexao.commit()
        except Exception as e:
            self.conexao.rollback()
            raise e
