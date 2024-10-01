import uuid
from typing import List

from importador_docfis_lib.dto_handler.pagamento import Pagamento
from importador_docfis_lib.utils import utilidades


class PagamentoDAO:
    
    @staticmethod
    def obterSQLInsertFormaDePagamento() -> str:
        """ Retorna o comando SQL para insert na tabela ns.df_formapagamentos """
        return """ WITH valor(id, id_docfis, tipopag, valorpag, cnpjcredoracartao, bandeira, ordem, valortroco, ind_pag, lastupdate, tenant) AS (VALUES %s)
                    INSERT INTO ns.df_formapagamentos(id, id_docfis, tipopag, valorpag, cnpjcredoracartao, bandeira, ordem, valortroco, ind_pag, lastupdate, tenant)
                    SELECT pag.id::uuid, pag.id_docfis::uuid, pag.tipopag::smallint, pag.valorpag::numeric, 
                    pag.cnpjcredoracartao, pag.bandeira::smallint, pag.ordem::bigint, pag.valortroco::numeric, pag.ind_pag::smallint, pag.lastupdate::timestamp without time zone, 
                    pag.tenant::bigint
                    FROM valor pag
                    WHERE EXISTS(SELECT 1 FROM ns.df_docfis doc WHERE pag.id_docfis::uuid = doc.id) """


    @staticmethod
    def obterListaValoresPagamento(pagamento: Pagamento, id_nfe: uuid.UUID, ordem: int) -> List:
        valores = list()
        valores.append(str(uuid.uuid4())) # id uuid NOT NULL DEFAULT uuid_generate_v4(),
        valores.append(str(id_nfe)) # id_docfis uuid,
        valores.append(pagamento.tPag) # tipopag smallint,
        valores.append(pagamento.vPag) # valorpag numeric(20,2),
        valores.append(None) # cnpjcredoracartao character varying(14),
        valores.append(None) # bandeira smallint,
        valores.append(ordem) # ordem bigint,
        valores.append(0) # valortroco numeric(15,2),
        valores.append(pagamento.indPag) # ind_pag smallint
        valores.append(utilidades.now_brazil()) # lastupdate timestamp without time zone DEFAULT now(),
        valores.append(0) # tenant bigint,
        return valores

    # @staticmethod
    # def obterListaValoresPagamentoSAT(pagamento: PagamentoSAT, id_nfe: uuid.UUID, ordem: int) -> List:
    #     valores = list()
    #     valores.append(str(uuid.uuid4())) # id uuid NOT NULL DEFAULT uuid_generate_v4(),
    #     valores.append(str(id_nfe)) # id_docfis uuid,
    #     valores.append(pagamento.cMP) # tipopag smallint,
    #     valores.append(pagamento.vMP) # valorpag numeric(20,2),
    #     valores.append(None) # cnpjcredoracartao character varying(14),
    #     valores.append(None) # bandeira smallint,
    #     valores.append(ordem) # ordem bigint,
    #     valores.append(0) # valortroco numeric(15,2),
    #     valores.append(pagamento.indMP) # ind_pag smallint
    #     valores.append(utilidades.now_brazil()) # lastupdate timestamp without time zone DEFAULT now(),
    #     valores.append(0) # tenant bigint,
    #     return valores


    @staticmethod
    def obterSQLInsertTroco() -> str:
        """ Retorna o comando SQL para insert na tabela \
        ns.df_formapagamentos_troco """
        return PagamentoDAO.obterSQLInsertFormaDePagamento()
    

    @staticmethod
    def obterListaValoresTroco(id_nfe: uuid.UUID, valorTroco: float):
        valores = list()
        valores.append(str(uuid.uuid4())) # id uuid NOT NULL DEFAULT uuid_generate_v4(),
        valores.append(str(id_nfe)) # id_docfis uuid,
        valores.append(100) # tipopag smallint,
        valores.append(valorTroco * -1) # valorpag numeric(20,2),
        valores.append(None) # cnpjcredoracartao character varying(14),
        valores.append(None) # bandeira smallint,
        valores.append(1000) # ordem bigint,
        valores.append(valorTroco) # valortroco numeric(15,2),
        valores.append(100) # ind_pag smallint
        valores.append(utilidades.now_brazil()) # lastupdate timestamp without time zone DEFAULT now(),
        valores.append(0) # tenant bigint,
        return valores