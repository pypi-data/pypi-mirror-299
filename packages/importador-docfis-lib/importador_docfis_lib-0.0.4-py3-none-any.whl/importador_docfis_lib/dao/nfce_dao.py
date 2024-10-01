import uuid
from datetime import datetime
from nasajon.dao.pagamento_dao import PagamentoDAO
from nasajon.dto_handler.item_nota import ItemNota
from nasajon.utils import utilidades
from nasajon.utils.conexao_postgres_adapter import ConexaoPostgresAdapter
from nasajon.dao.item_nota_dao import ItemNotaDAO
from nasajon.dao.lanfis_dao import LanfisDAO
from nasajon.dao.lf_itens_dao import Lf_ItensDAO
from nasajon.dto.estabelecimento import Estabelecimento
from nasajon.dto_handler.nfce import NFCE
from nasajon.utils.lanfis import Lanfis
from nasajon.utils.utilidades_banco import UtilidadesBanco


class NFCeDAO:
    """
    Classe responsável pelas operações de CRUD de NFCe junto ao Banco de Dados
    """

    def __init__(self, conexao: ConexaoPostgresAdapter):
        """
        Construtor do DAO de NFCe
        """
        self.__conexao = conexao

    @staticmethod
    def obterListaCamposDelete(nfce: NFCE) -> list:
        """
        retorna uma lista com os valores dos campos do objeto nfce
        Note: A ordem dos campo é a seguinte (id)
        """
        campos = list()
        campos.append(str(nfce.id))
        return campos

    def atualizar_nfce(
        self, notas: list[NFCE], listaEstabelecimentos: list[Estabelecimento]
    ):
        """
        Grava as notas no banco de dados, incluindo ns.df_docfis, ns.df_itens, \
        scritta.lanfis e scritta.lf_itens, ns.df_pagamentos e fila de \
        contabilização
        
        Args:
            notas:   list[NFCE] - Lista das notas que devem ser persistidas
        """
        if len(notas) == 0:
            return
        try:
            self.diferirConstraints()
            self.desativarRastro()
            self.desativarContabilizacao()
            self.gravarDocfisUpdate(notas)
            self.gravarDfLinhas(notas)
            self.gravarDfItens(notas)
            self.gravarLanfis(notas)
            self.gravarLfItens(notas)
            self.gravarPagamentos(notas)
            self.gravarTroco(notas)
            self.gravarMovimentoDeEstoque(notas)
            self.gravarAjustes(notas, listaEstabelecimentos)
            self.gravarEnfileiramento(notas)
            self.ativarRastro()
            self.ativarContabilizacao()
        except Exception as e:
            raise e

    def incluir_nfce(
        self,
        notas: list[NFCE],
        listaEstabelecimentos: list[Estabelecimento],
        atualizar_produtos: bool = False,
    ):
        """
        Grava as notas no banco de dados, incluindo ns.df_docfis, ns.df_itens, \
        scritta.lanfis e scritta.lf_itens, ns.df_pagamentos e fila de \
        contabilização

        Args:
            notas:   list[NFCE] - Lista das notas que devem ser persistidas
        """
        if len(notas) == 0:
            return
        try:
            self.diferirConstraints()
            self.desativarRastro()
            self.desativarContabilizacao()
            self.gravarDocfisInsert(notas)
            self.gravarDfLinhas(notas)
            self.gravarDfItens(notas)
            self.gravarLanfis(notas)
            self.gravarLfItens(notas)
            self.gravarPagamentos(notas)
            self.gravarTroco(notas)
            self.gravarMovimentoDeEstoque(notas)
            self.gravarAjustes(notas, listaEstabelecimentos)
            self.gravarEnfileiramento(notas)

            if atualizar_produtos:
                self.atualizarProdutosItens(notas)

            self.ativarRastro()
            self.ativarContabilizacao()
        except Exception as e:
            raise e

    def retornar_nfces(
        self, estabelecimento: Estabelecimento = None, anos: list[str] = None
    ) -> list[NFCE]:
        """
        Lista todos os produtos
        """

        sql = " select distinct d.id, d.chavene as identificador, "
        sql += "       d.id_estabelecimento as id_emitente, "
        sql += "       (t.id is null) and (c.contabilizacao is null) as pode_excluir "
        sql += " from ns.df_docfis d "
        sql += " inner join ns.estabelecimentos e "
        sql += "       on     d.id_estabelecimento = e.estabelecimento "
        sql += " left join contabilizacao.contabilizacoes c on c.docfis=d.id and c.processado "
        sql += " left join financas.titulos t"
        sql += "     join financas.baixas b on b.id_titulo=t.id"
        sql += "                              on t.id_docfis=d.id"
        sql += " where     d.modelo = 'NCE' "
        sql += "      and d.chavene > ' ' "
        if estabelecimento is not None:
            sql += "          and e.estabelecimento = '" + str(estabelecimento.id) + "'"
        sql += "      and d.id_estabelecimento is not null "
        if anos:
            sql += "      and d.id_ano in (" + ",".join(anos) + ") "

        return UtilidadesBanco.executarConsulta(self.__conexao, sql, [], NFCE)

    def retornar_nfce_identificador(
        self,
        identificador,
        estabelecimento: Estabelecimento = None,
        anos: list[str] = None,
    ) -> list[NFCE]:
        """
        Lista todos os produtos
        """

        sql = " select distinct d.id, d.chavene as identificador, "
        sql += "       d.id_estabelecimento as id_emitente, "
        sql += "       (t.id is null) and (c.contabilizacao is null) as pode_excluir "
        sql += " from ns.df_docfis d "
        sql += " inner join ns.estabelecimentos e "
        sql += "       on     d.id_estabelecimento = e.estabelecimento "
        sql += " left join contabilizacao.contabilizacoes c on c.docfis=d.id and c.processado "
        sql += " left join financas.titulos t"
        sql += "     join financas.baixas b on b.id_titulo=t.id"
        sql += "                              on t.id_docfis=d.id"
        sql += " where     d.modelo = 'NCE' "
        sql += "      and d.chavene > ' ' "
        if estabelecimento is not None:
            sql += "          and e.estabelecimento = '" + str(estabelecimento.id) + "'"
        sql += "      and d.id_estabelecimento is not null "
        sql += f"     and d.chavene = '{identificador}'"
        if anos:
            sql += "      and d.id_ano in (" + ",".join(anos) + ") LIMIT 1"

        return UtilidadesBanco.executarConsulta(self.__conexao, sql, [], NFCE)

    def retornarNFCeCancelamento(self, listaChavesNFCe):
        """
        Lista NFCes para cancelamento
        """

        lista = "', '".join([nfce.chNFe for nfce in listaChavesNFCe])

        sql = "SELECT D.CHAVENE, EST.CODIGO AS CODIGO_ESTABELECIMENTO "
        sql += "FROM NS.DF_DOCFIS D "
        sql += "INNER JOIN NS.ESTABELECIMENTOS EST ON D.ID_ESTABELECIMENTO = EST.ESTABELECIMENTO "
        sql += "WHERE MODELO = 'NCE' "
        sql += f"AND CHAVENE IN ('{lista}');"

        return UtilidadesBanco.executarConsulta(
            self.__conexao,
            sql,
            True,
            None,
        )

    def retornarNFCeInutilizacao(self, listaChavesNFCe):
        """
        Lista NFCes para inutilização
        """

        estabelecimentos = "', '".join([nfce.CNPJ for nfce in listaChavesNFCe])
        numeros = "', '".join([nfce.nNFIni for nfce in listaChavesNFCe])
        atenumeros = "', '".join([nfce.nNFFin for nfce in listaChavesNFCe])

        sql = "SELECT D.NUMERO, D.ATENUMERO, EST.ESTABELECIMENTO "
        sql += "FROM NS.DF_DOCFIS D "
        sql += "INNER JOIN NS.ESTABELECIMENTOS EST ON D.ID_ESTABELECIMENTO = EST.ESTABELECIMENTO "
        sql += "WHERE D.MODELO = 'NCE' "
        sql += f"AND CONCAT(EST.RAIZCNPJ, EST.ORDEMCNPJ) IN ('{estabelecimentos}') "
        sql += f"AND (D.NUMERO IN ('{numeros}') AND D.ATENUMERO IN ('{atenumeros}'));"

        return UtilidadesBanco.executarConsulta(
            self.__conexao,
            sql,
            True,
            None,
        )

    def excluirDependenciasNFCe(self, listaNFCe: list[NFCE]):
        """
        Exclui as NFCe listadas utilizando a API de exclusão em lote do Scritta
        """
        nomeTabela = "tb_tmp_delete_docfis_" + str(uuid.uuid4()).replace("-", "")
        try:
            horario_atual = datetime.now()
            print(horario_atual.__str__() + " >>> Iniciou exclusão")
            self.diferirConstraints()
            self.desativarRastro()
            self.desativarContabilizacao()

            sql = "drop table if exists " + nomeTabela
            UtilidadesBanco.executarComando(self.__conexao, sql, None, False, True)

            sql = (
                "create temporary table "
                + nomeTabela
                + "(id uuid not null primary key)"
            )
            UtilidadesBanco.executarComando(self.__conexao, sql, None, False, True)

            sql = "insert into " + nomeTabela + " (id) values %s"
            parametros = [self.obterListaCamposDelete(nfce) for nfce in listaNFCe]
            UtilidadesBanco.executarComando(self.__conexao, sql, parametros, True, True)

            sql = (
                "select * from scritta.api_docfis_deletar_dependencias('"
                + nomeTabela
                + "', False)"
            )
            UtilidadesBanco.executarComando(self.__conexao, sql, None, False, False)

            sql = f"delete from ns.df_docfis df where df.id in (select id from {nomeTabela})"
            UtilidadesBanco.executarComando(self.__conexao, sql, None, False, False)

            print(
                datetime.now().__str__()
                + " >>> Terminou exclusão "
                + str((datetime.now() - horario_atual).total_seconds())
                + " segundos"
            )
        except:
            raise
        finally:
            sql = "drop table if exists " + nomeTabela
            UtilidadesBanco.executarComando(self.__conexao, sql, None, False, True)

            self.ativarRastro()
            self.ativarContabilizacao()

    def primeiraExecucao(self) -> bool:
        """
        Indica se é a primeira vez que o importador é executado nessa base de dados
        :return: True se for a primeira execução, False se não for
        """
        sql = "Select valor from ns.configuracoes where sessao=0 and valor='novo importador executado'"
        ja_existe = (
            len(
                UtilidadesBanco.executarConsulta(self.__conexao, sql, None, None, False)
            )
            > 0
        )
        if not ja_existe:
            sql = "insert into ns.configuracoes (sessao, valor) values (0,'novo importador executado')"
        UtilidadesBanco.executarComando(self.__conexao, sql, None, False, False)
        return not ja_existe

    def diferirConstraints(self):
        """Altera as constraints para validação tardia"""
        sql = "set constraints all deferred"
        UtilidadesBanco.executarComando(self.__conexao, sql, None, False, True)

    def desativarRastro(self):
        """Desativa os triggers do Rastro"""
        sql = 'SET SESSION "sistema.ativa_rastro"' + " = 'FALSE'"
        UtilidadesBanco.executarComando(self.__conexao, sql, None, False, True)

    def ativarRastro(self):
        """Ativa os triggers do Rastro"""
        sql = 'SET SESSION "sistema.ativa_rastro"' + " = 'TRUE'"
        UtilidadesBanco.executarComando(self.__conexao, sql, None, False, True)

    def desativarContabilizacao(self):
        """Desativa o trigger da contabilização na ns.df_docfis"""
        sql = "SELECT contabilizacao.desativar_trigger_docfis()"
        UtilidadesBanco.executarComando(self.__conexao, sql, None, False, True)

    def ativarContabilizacao(self):
        """Ativa o trigger da contabilização na ns.df_docfis"""
        sql = "SELECT contabilizacao.ativar_trigger_docfis()"
        UtilidadesBanco.executarComando(self.__conexao, sql, None, False, True)

    def gravarDocfisInsert(self, notas: list[NFCE]):
        """Grava na tabela ns.df_docfis"""

        try:
            parametros = [NFCeDAO.obterListaValoresNFCe(nfe) for nfe in notas]
            if len(parametros) > 0:
                UtilidadesBanco.executarComando(
                    self.__conexao,
                    NFCeDAO.obterSQLInsertDocFis(),
                    parametros,
                    bulk=True,
                    manterTransacao=True,
                )
        except Exception as e:
            raise e

    def gravarDocfisUpdate(
        self, notas: list[NFCE], icms_desonerado_desconto: bool = False
    ):
        """Grava na tabela ns.df_docfis"""
        icms_deson = "null"
        if not icms_desonerado_desconto:
            icms_deson = "true"
        for nfce in notas:
            sql = (
                "UPDATE ns.df_docfis SET \
                  baseicms = "
                + str(nfce.retornarBaseICMS())
                + ", valoricms = "
                + str(nfce.retornarValorICMS())
                + ", valordestacado = "
                + str(nfce.vNF)
                + ", valor = "
                + str(
                    float(nfce.vNF)
                    - float(
                        sum(
                            item.icms.retornarValorDesoneracao()
                            for item in nfce.lista_itens
                        )
                    )
                )
                + ", outras = "
                + str(nfce.retornarValorMercadorias() - nfce.retornarBaseICMS())
                + ", isentasicms = "
                + str((float(nfce.vNF) - float(nfce.retornarBaseICMS() + nfce.vOutro)))
                + ", outrosvalores = "
                + str(nfce.vOutro)
                + ", datacriacao  = now()"
                + ", horacriacao = now()"
                + ", lastupdate = now()"
                + "', cfop = '"
                + str(nfce.calcular_cfop())
                + "', cfopdif = "
                + str(nfce.existeCFOPDiferente())
                + ",  mercadorias = "
                + str(nfce.retornarValorMercadorias())
                + ", cancelado = false "
                + ", situacao = 2 "
                + ", icmsdesonsemdesc = "
                + str(icms_deson)
                + ", versao = 4 "
                + " WHERE id = '"
                + str(nfce.id)
                + "'"
            )
            UtilidadesBanco.executarComando(self.__conexao, sql, [], False, True)

    def gravarDfItens(self, notas: list[NFCE]):
        """Grava na tabela ns.df_itens"""
        parametros = [
            ItemNotaDAO.obterListaValoresItensNFCe(
                item,
                nfe.id,
                nfe.dhEmi.year,
                nfe.lista_itens.index(item) + 1,
                nfe.calcular_cfop(),
            )
            for nfe in notas
            for item in nfe.lista_itens
        ]
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao,
                ItemNotaDAO.obterSQLInsertDf_Itens(),
                parametros,
                True,
                True,
            )

    def gravarDfLinhas(self, notas: list[NFCE]):
        """Grava na tabela ns.df_linhas"""
        parametros = [
            ItemNotaDAO.obterListaValoresDf_Linhas(
                item, nfe.id, nfe.lista_itens.index(item) + 1
            )
            for nfe in notas
            for item in nfe.lista_itens
        ]
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao,
                ItemNotaDAO.obterSQLInsertDf_Linhas(),
                parametros,
                True,
                True,
            )

    def gravarLanfis(self, notas: list[NFCE]):
        """Grava na tabela scritta.lf_lanfis"""
        parametros = [
            LanfisDAO.obterListaValoresLanFisNFCe(nfe, chave, id)
            for nfe in notas
            for chave, id in nfe.obterLancamentosFiscais()
        ]
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao, LanfisDAO.obterSQLInsertLanFis(), parametros, True, True
            )

    def gravarLfItens(self, notas: list[NFCE]):
        """Grava na tabela scritta.lf_itens"""
        parametros = [
            Lf_ItensDAO.obterListaValoresLfItensNFCe(nfe, item, idLanfis)
            for nfe in notas
            for chave, idLanfis in nfe.obterLancamentosFiscais()
            for item in Lanfis.filtrarItensDaNotaPorChaveDoLancamentoFiscal(nfe, chave)
        ]
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao,
                Lf_ItensDAO.obterSQLInsertLfItens(),
                parametros,
                True,
                True,
            )

    def gravarEnfileiramento(self, notas: list[NFCE]):
        """Insere as notas na fila de contabilização"""
        comandos = ""
        for nfe in notas:
            sql = self.obterSQLInsertContabilizacao()
            parametros = NFCeDAO.obterListaValoresContabilizacao(nfe)
            comandos += sql.format(*parametros) + " \r\n"
        if len(comandos) > 0:
            UtilidadesBanco.executarComando(self.__conexao, comandos, None, False, True)

    def cancelarNFCe(self, notas: list[str]):
        UtilidadesBanco.executarComando(
            self.__conexao, NFCeDAO.obterSQLCancelamentoNotas(notas), [], False, False
        )
        UtilidadesBanco.executarComando(
            self.__conexao,
            NFCeDAO.obterSQLCancelamentoLancamentos(notas),
            [],
            False,
            False,
        )

    def inutilizarNFCe(self, notas: list[NFCE]):
        try:
            parametros_doc = [
                NFCeDAO.obterListaValoresNFCeInutilizacao(nfe) for nfe in notas
            ]
            if len(parametros_doc) > 0:
                UtilidadesBanco.executarComando(
                    self.__conexao,
                    NFCeDAO.obterSQLInutilizacaoNotas(),
                    parametros_doc,
                    True,
                    False,
                )
        except Exception as e:
            raise e

        try:
            parametros_lanfis = [
                NFCeDAO.obterListaValoresNFCeInutilizacaoLanfis(nfe) for nfe in notas
            ]
            if len(parametros_lanfis) > 0:
                UtilidadesBanco.executarComando(
                    self.__conexao,
                    NFCeDAO.obterSQLInutilizacaoLancamentos(),
                    parametros_lanfis,
                    True,
                    False,
                )
        except Exception as e:
            raise e

    @staticmethod
    def obterSQLCancelamentoNotas(notas: list[NFCE]) -> str:
        vetor = "{"
        vetor = vetor + ",".join([nota.identificador for nota in notas])
        vetor = vetor + "}"

        return (
            "update ns.df_docfis set cancelado = True, situacao = 15 where chavene = any('"
            + vetor
            + "'::varchar(50)[])"
        )

    @staticmethod
    def obterSQLCancelamentoLancamentos(notas: list[NFCE]) -> str:
        vetor = "{"
        vetor = vetor + ",".join([nota.identificador for nota in notas])
        vetor = vetor + "}"

        return (
            "update scritta.lf_lanfis set cancelado = True \
                where id_docfis = any (\
                    (select array_agg(id) from ns.df_docfis \
                    where chavene = any('"
            + vetor
            + "'::varchar(50)[]))::UUID[]\
                )"
        )

    @staticmethod
    def obterSQLInutilizacaoNotas() -> str:
        SQL = """ INSERT INTO NS.DF_DOCFIS(id, id_ano, sinal, tipo, modelo, serie, subserie, numero, periodo, lancamento, 
                                           emissao, cfop, atenumero, situacao, situacaosped, observacao, 
                                           percbaseinss, percbaseir, id_estabelecimento, id_emitente, origem, 
                                           data_cancelamento, gerafinanceiro, id_conjunto_anexo, status, lastupdate)
                  VALUES %s """

        return SQL

    @staticmethod
    def obterSQLInutilizacaoLancamentos() -> str:
        SQL = """ WITH nsdoc(id_ano, tipo, datalanc, modelo, serie, subserie, numero, cfop, emissao, atenumero, 
                              cancelado, orgaopublico,retemiss, ipipresumido, dataretiss, datadeclaracao, situacaosped,
                              tipoiss, observacao, id_docfis, id_estabelecimento, data_cancelamento, lastupdate) 
                   AS (VALUES %s)
                   INSERT INTO SCRITTA.LF_LANFIS (id_ano, tipo, datalanc, modelo, serie, subserie, numero, cfop, emissao, 
                              atenumero, cancelado, orgaopublico,retemiss, ipipresumido, dataretiss, datadeclaracao, 
                              situacaosped, tipoiss, observacao, id_docfis, id_estabelecimento, data_cancelamento, lastupdate)
                   SELECT docimp.id_ano::integer, docimp.tipo::integer, docimp.datalanc::date, docimp.modelo::varchar, 
                          docimp.serie::varchar, docimp.subserie::varchar, docimp.numero::varchar, docimp.cfop::varchar, 
                          docimp.emissao::date, docimp.atenumero::varchar, docimp.cancelado::boolean, docimp.orgaopublico::boolean, 
                          docimp.retemiss::boolean, docimp.ipipresumido::boolean, docimp.dataretiss::date, docimp.datadeclaracao::date, 
                          docimp.situacaosped::integer, docimp.tipoiss::integer, docimp.observacao::varchar, docimp.id_docfis::uuid, 
                          docimp.id_estabelecimento::uuid, docimp.data_cancelamento::date, docimp.lastupdate::timestamp without time zone  
                   FROM nsdoc docimp
                   WHERE EXISTS(SELECT 1 
                                FROM NS.DF_DOCFIS doc 
                                WHERE doc.modelo = 'NCE'
                                AND doc.numero = docimp.numero::varchar
                                AND doc.atenumero = docimp.atenumero::varchar
                                AND doc.id_estabelecimento = docimp.id_estabelecimento::uuid  
                                LIMIT 1000) """

        return SQL

    def gravarMovimentoDeEstoque(self, notas: list[NFCE]):
        """Grava na tabela ns.df_docfis"""
        parametros = list()
        for nfce in notas:
            ordem = 0
            for item in nfce.lista_itens:
                ordem += ordem
                if (nfce.operacaoCfopSlot is not None) and (
                    nfce.operacaoCfopSlot.slots
                ):
                    for slot in nfce.operacaoCfopSlot.slots:
                        parametros.append(
                            NFCeDAO.obterListaValoresMovimentoEstoque(
                                nfce, item, slot, ordem
                            )
                        )
                else:
                    parametros.append(
                        NFCeDAO.obterListaValoresMovimentoEstoque(
                            nfce, item, "FISCAL", ordem
                        )
                    )
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao,
                NFCeDAO.obterSQLMovimentoEstoque(),
                parametros,
                True,
                True,
            )

    def gravarPagamentos(self, notas: list[NFCE]):
        """Grava na tabela ns.df_formaspagamentos"""
        parametros = [
            PagamentoDAO.obterListaValoresPagamento(
                pagamento, nfe.id, nfe.listaPagamentos.index(pagamento)
            )
            for nfe in notas
            for pagamento in nfe.listaPagamentos
        ]
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao,
                PagamentoDAO.obterSQLInsertFormaDePagamento(),
                parametros,
                True,
                True,
            )

    def gravarTroco(self, notas: list[NFCE]):
        """Grava na tabela ns.df_formaspagamento_troco"""
        parametros = [
            PagamentoDAO.obterListaValoresTroco(nfe.id, nfe.vTroco) for nfe in notas
        ]
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao,
                PagamentoDAO.obterSQLInsertTroco(),
                parametros,
                True,
                True,
            )

    def gravarAjustes(
        self, notas: list[NFCE], listaEstabelecimentos: list[Estabelecimento]
    ):
        parametros = [
            NFCeDAO.obterListaValoresAjuste(nfe, item, listaEstabelecimentos)
            for nfe in notas
            for item in nfe.lista_itens
            if item.icms.vICMSDeson > 0
            and item.nBenef is not None
            and str(item.nBenef) != ""
            and self.NotaExistente(nfe)
        ]

        if parametros:
            UtilidadesBanco.executarComando(
                self.__conexao, NFCeDAO.obterSQLInsertAjuste(), parametros, True, True
            )

        parametrosC197 = [
            NFCeDAO.obterListaValoresAjusteC197(nfe, item, listaEstabelecimentos)
            for nfe in notas
            for item in nfe.lista_itens
            if item.icms.vICMSDeson > 0
            and item.nBenef is not None
            and str(item.nBenef) != ""
            and item.icms.motDesICMS is not None
            and str(item.icms.motDesICMS) != ""
            and listaEstabelecimentos[nfe.identificadorEmitente].uf.upper() == "RJ"
            and item.icms.CST in ("20", "30", "40", "51", "70")
            and self.NotaExistente(nfe)
        ]

        if parametrosC197:
            UtilidadesBanco.executarComando(
                self.__conexao,
                NFCeDAO.obterSQLInsertAjuste(),
                parametrosC197,
                True,
                True,
            )

    def obterSQLAtualizacaoItem(self, notas: list[NFCE]) -> str:
        chave = "('"
        chave = chave + "','".join([nota.identificador for nota in notas])
        chave = chave + "')"

        sql = " UPDATE ESTOQUE.ITENS ITEM"
        sql += " SET"
        sql += " TIPI = COALESCE( NULLIF( FOO.TIPI, '' ), ITEM.TIPI ),"
        sql += " CST_ICMS_B = COALESCE( NULLIF( FOO.CST_ICMS, '' ), ITEM.CST_ICMS_B ),"
        sql += " ESPECIFICACAO = COALESCE( NULLIF( FOO.ESPECIFICACAO, '') , ITEM.ESPECIFICACAO ),"
        sql += " CEST = COALESCE( NULLIF( FOO.CEST, ''),  ITEM.CEST ),"
        sql += (
            " CST_ICMS_A = COALESCE( NULLIF(FOO.ORIGEM ::varchar, ''), ITEM.CST_ICMS_A)"
        )
        sql += " FROM (SELECT DISTINCT DF_ITEM.TIPI, DF_ITEM.CEST, DF_ITEM.CST_ICMS, DF_ITEM.ESPECIFICACAO, DF_ITEM.ID_ITEM, DF_ITEM.ORIGEM"
        sql += "  FROM NS.DF_ITENS DF_ITEM"
        sql += " INNER JOIN NS.DF_DOCFIS DOC"
        sql += " ON DF_ITEM.ID_DOCFIS = DOC.ID AND"
        sql += " DOC.SINAL = 0 AND TIPO =0"
        sql += " AND DOC.CHAVENE IN " + chave + " ) FOO"
        sql += " WHERE FOO.ID_ITEM = ITEM.ID"

        return sql

    def obterSQLAtualizacaoProduto(self, notas: list[NFCE]) -> str:
        chave = "('"
        chave = chave + "','".join([nota.identificador for nota in notas])
        chave = chave + "')"

        sql = " UPDATE ESTOQUE.PRODUTOS PRODUTO"
        sql += " SET"
        sql += " TIPI = COALESCE( NULLIF( FOO.TIPI, '' ), PRODUTO.TIPI ),"
        sql += " ORIGEMMERCADORIA = COALESCE(FOO.ORIGEM, PRODUTO.ORIGEMMERCADORIA),"
        sql += " ESPECIFICACAO = COALESCE( NULLIF( FOO.ESPECIFICACAO, '') , PRODUTO.ESPECIFICACAO ),"
        sql += " CEST = COALESCE( NULLIF( FOO.CEST, ''),  PRODUTO.CEST )"
        sql += " FROM (SELECT DISTINCT DF_ITEM.TIPI, DF_ITEM.CEST, DF_ITEM.CST_ICMS, DF_ITEM.ESPECIFICACAO, DF_ITEM.ID_ITEM, DF_ITEM.ORIGEM, ITENS.PRODUTO"
        sql += " FROM NS.DF_ITENS DF_ITEM"
        sql += " INNER JOIN NS.DF_DOCFIS DOC"
        sql += " ON DF_ITEM.ID_DOCFIS = DOC.ID AND"
        sql += " DOC.SINAL = 0 AND TIPO =0"
        sql += " AND DOC.CHAVENE IN " + chave
        sql += " INNER JOIN ESTOQUE.ITENS ITENS ON DF_ITEM.ID_ITEM = ITENS.ID ) FOO"
        sql += " WHERE FOO.PRODUTO = PRODUTO.PRODUTO"

        return sql

    def atualizarProdutosItens(self, notas: list[NFCE]):
        """Executa o SQL para atualização de produtos e itens diretamente no banco de dados"""

        UtilidadesBanco.executarComando(
            self.__conexao, self.obterSQLAtualizacaoItem(notas), None, False, True
        )

        UtilidadesBanco.executarComando(
            self.__conexao, self.obterSQLAtualizacaoProduto(notas), None, False, True
        )

    @staticmethod
    def obterSQLInsertAjuste() -> str:
        """Retorna o comando SQL para insert na tabela ns.df_docfis"""
        return "INSERT INTO scritta.lanaju( \
                id_ano, imposto, data, tipo, origem, tiposped, atividade, natureza, \
                tipocalcpc, origempc, tppessoa, modelodoc, tipodoc, seriedoc, \
                numerodoc, documentacao, complemento, codigogia, codigodarf, \
                sped, sped_pc, sped_out, sped_detalhe, utilizacao, uf, descricao, \
                debito, credito, debito2, credito2, cotepe, anexo, base, icms, \
                valor, outros, pis, cofins, evento, id_item, id_docfis, id_estabelecimento, \
                id_pessoa, id_cancelamento, id_grec, id, id_obra, id_scp, id_lanfis, \
                lastupdate, tenant, tipo_ecf, tipo_ecf_pcr, tipo_ecf_din, ecf_pcr, \
                ecf_din) \
                VALUES %s"

    @staticmethod
    def obterListaValoresAjuste(
        nfe: NFCE, item: ItemNota, listaEstabelecimentos: list[Estabelecimento]
    ) -> list:
        valores = list()
        id = uuid.uuid4()
        valores.append(nfe.dhEmi.year)  # id_ano integer NOT NULL,
        valores.append(8)  # imposto integer NOT NULL,
        valores.append(nfe.dhEmi)  # data date NOT NULL,
        valores.append(13)  # tipo integer NOT NULL DEFAULT 0,
        valores.append(8)  # origem integer,
        valores.append(0)  # tiposped integer,
        valores.append(None)  # atividade integer,
        valores.append(20)  # natureza integer,
        valores.append(None)  # tipocalcpc integer,
        valores.append(None)  # origempc integer,
        valores.append(None)  # tppessoa integer,
        valores.append(nfe.mod)  # modelodoc character varying(3),
        valores.append(None)  # tipodoc character varying(3),
        valores.append(nfe.serie)  # seriedoc character varying(3),
        valores.append(nfe.nNF)  # numerodoc character varying(15),
        valores.append(None)  # documentacao character varying(150),
        valores.append(None)  # complemento character varying(150),
        valores.append(None)  # codigogia character varying(20),
        valores.append(None)  # codigodarf character varying(6),
        valores.append(item.nBenef)  # sped character varying(12),
        valores.append(None)  # sped_pc character varying(12),
        valores.append(None)  # sped_out character varying(12),
        valores.append(None)  # sped_detalhe character varying(12),
        valores.append(None)  # utilizacao character varying(12),
        valores.append(
            listaEstabelecimentos[nfe.identificadorEmitente].uf
        )  # uf character varying(2),
        valores.append("NFCe nº " + nfe.nNF)  # descricao character varying(150),
        valores.append(None)  # debito character varying(16),
        valores.append(None)  # credito character varying(16),
        valores.append(None)  # debito2 character varying(16),
        valores.append(None)  # credito2 character varying(16),
        valores.append(item.CFOP)  # cotepe character varying(20),
        valores.append(None)  # anexo character varying(14),
        valores.append(item.icms.vBC)  # base numeric(20,2),
        valores.append(item.icms.aliquotaICMSTotal)  # icms numeric(20,2),
        valores.append(item.icms.vICMSDeson)  # valor numeric(20,2),
        valores.append(None)  # outros numeric(20,2),
        valores.append(None)  # pis numeric(20,2),
        valores.append(None)  # cofins numeric(20,2),
        valores.append(None)  # evento bigint,
        valores.append(str(item.id_produto))  # id_item uuid,
        valores.append(str(nfe.id))  # id_docfis uuid,
        valores.append(str(nfe.id_emitente))  # id_estabelecimento uuid,
        if nfe.destinatario is not None and nfe.destinatario.id is not None:
            valores.append(str(nfe.destinatario.id))  # id_pessoa uuid,
        else:
            valores.append(None)
        valores.append(None)  # id_cancelamento uuid,
        valores.append(None)  # id_grec uuid,
        valores.append(str(id))  # id uuid NOT NULL DEFAULT uuid_generate_v4(),
        valores.append(None)  # id_obra uuid,
        valores.append(None)  # id_scp uuid,
        valores.append(None)  # id_lanfis uuid,
        valores.append(
            utilidades.now_brazil()
        )  # lastupdate timestamp without time zone DEFAULT now(),
        valores.append(None)  # tenant bigint,
        valores.append(None)  # tipo_ecf integer,
        valores.append(None)  # tipo_ecf_pcr integer,
        valores.append(None)  # tipo_ecf_din integer,
        valores.append(None)  # ecf_pcr character varying(60),
        valores.append(None)  # ecf_din character varying(60)
        return valores

    @staticmethod
    def obterSQLInsertDocFis() -> str:
        """Retorna o comando SQL para insert na tabela ns.df_docfis"""

        parametros_docfis = """id_ano, sinal, tipo, modelo, serie, subserie, numero, periodo, 
                    lancamento, emissao, cfop, cfopservico, tppessoa, atenumero, 
                    datainiserv, datafimserv, datasaida, datadeclaracao, datanotaconhec, 
                    horasaida, porcaixa, petroleo, notafatura, cfopdif, cfopserdif, 
                    cancelado, orgaopublico, somaiss, issoutromunic, retautomatica, 
                    retemiss, retemir, reteminss, retemcofins, retemcsll, retempis, 
                    retorno, porcontigencia, versao, situacao, situacaosped, tipocalctrib, 
                    tpligacao, grupotensao, crt, messerv, anoserv, tiponfe, tpoperador, 
                    tpconsignatario, consumidor, tiporedespacho, remas, rapis, tipofrete, 
                    tiporecolhimento, tipotransporte, volumes, tipodocexterior, parcelas, 
                    tipocontab, mesescredicms, anoaidf, anopexpam, tipoimp, classe, 
                    tiporeceita, tipoconsumo, tiponavegacao, tipoveiculo, naturezafrete, 
                    tipotarifaar, chavene, chaveneini, chavene01, chavene02, chavene03, 
                    chavene04, chavenefim, codigoirrf, codigopis, codigocsll, codigocofins, 
                    numacdraw, campoligacao, terminal, codarea, rntrc, serierps, 
                    rps, cnae, codmunic, codserv, municdest, codif, numerofrete, 
                    marca, tipovolume, placa, placa02, placa03, ufplaca, ufplaca02, 
                    ufplaca03, doccomexterior, parcelamento, renavam, codigodip, 
                    observacao, obsestoque, selofiscal, aidf, numeropexpam, lacre, 
                    unidadecarga, frota, veiculo, viagem, otm, frete, seguro, basetransp, 
                    iss, deducaoiss, inss, ir, valoriss, baseiss, baseinss, valorinss, 
                    valorinssadicional, valorinssnaoretido, valorinsssubempreitada, 
                    baseir, valorir, basecofins, valorcofins, basecsll, valorcsll, 
                    basepis, valorpis, deducaobaseir, valordeducaoir, desconto, mercadorias, 
                    servicos, valor, diferenca, valordestacado, baseicms, icms, valoricms, 
                    icmsnaocred, isentasicms, outrasicms, reducaoicms, reducaoipi, 
                    baseipi, valoripi, ipi, isentasipi, outras, basesubst, substprop, 
                    substterc, substnaoret, icmsretido, pisimp, cofinsimp, basepisimp, 
                    basecofinsimp, valorpisimp, valorcofinsimp, consumo, kwh, fretemm, 
                    pesotx, freteliquido, valorsec_cat, despacho, pedagio, despportuarias, 
                    cargadescarga, taxaterrestre, advalorem, valorgris, outrosvalores, 
                    pesobruto, pesoliquido, cubagem, anotacoes, percbaseinss, percbaseir, 
                    id_itemntr, id, id_conhectransp, id_estabelecimento, id_orgao, 
                    id_operador, id_redespachador, id_emitente, id_pessoa, id_consignatario, 
                    id_coleta, id_entrega, id_remetente, id_destinatario, id_transportadora, 
                    id_motorista, id_obra, id_grupodiferenciado, id_scp, tipodocumento, 
                    xml_docengine, xml_transmitido, tipopedido, formapagamento, autorizacaocartao, 
                    documentocartao, dataautorizacaocartao, valoravista, vezescartao, 
                    anotacao, id_proposta, id_grupoempresarial, id_promocao, id_posicaoworkflow, 
                    id_midiaorigem, id_conta, id_layoutbancario, id_informacaocartao, 
                    datanegocio, aprovadopor, datahoraaprovacao, acrescimofinanceiro, 
                    origem, id_objetoservico, id_docfis, id_cfop, discriminacaoservicos, 
                    statusrps, tiporps, tipotributacaoservicorps, regimeespecialtributacao, 
                    incentivocultural, ufprestacaoservico, cidadeprestacaoservico, 
                    id_estabelecimentocontraparte, descricaopagamento, datavalidade, 
                    contato, informacoespedido, id_oportunidade, id_parcelamento, 
                    id_docproposta, xml_cancelamento, motivo_cancelamento, data_cancelamento, 
                    datacriacao, horacriacao, referenciaexterna, tipoordemservico, 
                    origemordemservico, contrato, processamentocontrato, id_pedido, 
                    documento_operacao, documento_operacao_codigo, xml_titulos, 
                    ordemservico_id, valorliquido, caixa, pontodevenda, id_serie, 
                    dataentradasaida, tipoemitente, tiporeceptor, formadepagamento, 
                    tipooperacao, uffatogerador, modocompra, tipodeemissao, chave, 
                    observacao_movimentacao, tabeladepreco, id_localdeestoqueorigem, 
                    id_localdeestoquedestino, df_endereco_retirada, df_endereco_entrega, 
                    municipiofatogerador, xml_contingencia, datacontingencia, justificativacontingencia, 
                    debitoautomatico, contigencia_justificativa, contigencia_imprimiu, 
                    contigencia_datahora, numeroprotocolo, tipoambiente, lotecobrancaordemservico_id, 
                    documentorateado, requisicaoalmoxarifado_id, gerafinanceiro, 
                    id_conjunto_anexo, descricaoservicos, rps_original, tipo_retencao_iss, 
                    xml_rps, anotacoes_sistema, anotacoes_manuais, uf_embarque, local_embarque, 
                    local_despacho, origemdocumento, link_nfse, id_documento_vinculado, 
                    pessoamunicipio, id_usuario_cadastro, prazoentrega, notaimportacao, 
                    chavegold, wkf_data, wkf_estado, usuario_solicitacao_id, usuario_solicitacao_data, 
                    emailenviado, id_instancia, situacaogerencial, totalvalorfaturar, 
                    finalidadeemissao, id_operacao_nfs, analistacompra, infopiscompra, 
                    infocofinscompra, infoicmscompra, infoicmsstcompra, infoipicompra, 
                    status, vendedor, categoriadeproduto, uf_habilitacao, tipo_assinante, 
                    autenticacao_lote_digital, outras_retencoes, numero_titulo, vbcufdest, 
                    pfcpufdest, picmsufdest, picmsinter, picmsinterpart, vfcpufdest, 
                    vicmsufdest, vicmsufremet, dataprevisao_entradasaida, template_discriminacaorps, 
                    indiedest, sistema, tipo_insercao, indfinal, iddest, indpres, 
                    reconstruirxml, id_pedidoservico, iddestinoremessa, lotedigital, 
                    pretituloverificado, possuiadiantamento, tabeladefrete, observacao_dadosgerais, 
                    nota_antecipada, rascunho, recalcularimpostos, volumemanual, 
                    status_conferencia, id_rateiopadrao, outrosacrescimos, titulo_observacao, 
                    projeto_padrao_id, numeroexterno, naturezaoperacao, total_desconto, 
                    id_docfis_contrato, reinf_maodeobra, id_transacaofinanceira, 
                    id_contratofinanceiro, versao_dfe, troco, tipointegracao_pagamento, 
                    tenant, codigo_verificacao, rota, rota_liberado, id_opeinterna, 
                    id_moeda, id_cotacao, xmlexplodido, romaneio_doc_atendido, icmsdesonsemdesc,  lastupdate"""

        return f"""WITH nsdoc({parametros_docfis}) AS (VALUES %s)
                    INSERT INTO NS.DF_DOCFIS ({parametros_docfis})
                    SELECT docimp.id_ano, docimp.sinal, docimp.tipo, docimp.modelo, docimp.serie, docimp.subserie, docimp.numero, docimp.periodo::integer, 
                    docimp.lancamento, docimp.emissao, docimp.cfop, docimp.cfopservico, docimp.tppessoa::integer, docimp.atenumero, docimp.datainiserv::date, 
                    docimp.datafimserv::date, docimp.datasaida::date, docimp.datadeclaracao::date, docimp.datanotaconhec::date, docimp.horasaida::time without time zone, 
                    docimp.porcaixa::boolean, docimp.petroleo::boolean, docimp.notafatura::boolean, docimp.cfopdif, docimp.cfopserdif, docimp.cancelado, docimp.orgaopublico, 
                    docimp.somaiss, docimp.issoutromunic, docimp.retautomatica, docimp.retemiss, docimp.retemir, docimp.reteminss, docimp.retemcofins, 
                    docimp.retemcsll, docimp.retempis, docimp.retorno, docimp.porcontigencia, docimp.versao, docimp.situacao, docimp.situacaosped, 
                    docimp.tipocalctrib, docimp.tpligacao::integer, docimp.grupotensao::integer, docimp.crt, docimp.messerv::integer, docimp.anoserv::integer, docimp.tiponfe, 
                    docimp.tpoperador::integer, docimp.tpconsignatario::integer, docimp.consumidor, docimp.tiporedespacho, docimp.remas, docimp.rapis, docimp.tipofrete, 
                    docimp.tiporecolhimento, docimp.tipotransporte::integer, docimp.volumes, docimp.tipodocexterior::integer, docimp.parcelas, docimp.tipocontab::integer, 
                    docimp.mesescredicms::integer, docimp.anoaidf::integer, docimp.anopexpam::integer, docimp.tipoimp::integer, docimp.classe::integer, docimp.tiporeceita::integer, 
                    docimp.tipoconsumo::integer, docimp.tiponavegacao::integer, docimp.tipoveiculo::integer, docimp.naturezafrete::integer, docimp.tipotarifaar::integer, docimp.chavene, 
                    docimp.chaveneini, docimp.chavene01, docimp.chavene02, docimp.chavene03, docimp.chavene04, docimp.chavenefim, docimp.codigoirrf, docimp.codigopis, 
                    docimp.codigocsll, docimp.codigocofins, docimp.numacdraw, docimp.campoligacao, docimp.terminal, docimp.codarea, docimp.rntrc, 
                    docimp.serierps, docimp.rps, docimp.cnae, docimp.codmunic, docimp.codserv, docimp.municdest, docimp.codif, docimp.numerofrete, 
                    docimp.marca, docimp.tipovolume, docimp.placa, docimp.placa02, docimp.placa03, docimp.ufplaca, docimp.ufplaca02, docimp.ufplaca03, 
                    docimp.doccomexterior, docimp.parcelamento, docimp.renavam, docimp.codigodip, docimp.observacao, docimp.obsestoque, docimp.selofiscal, 
                    docimp.aidf, docimp.numeropexpam, docimp.lacre, docimp.unidadecarga, docimp.frota, docimp.veiculo, docimp.viagem, docimp.otm, 
                    docimp.frete, docimp.seguro, docimp.basetransp, docimp.iss, docimp.deducaoiss, docimp.inss, docimp.ir, docimp.valoriss, docimp.baseiss, 
                    docimp.baseinss, docimp.valorinss, docimp.valorinssadicional, docimp.valorinssnaoretido, docimp.valorinsssubempreitada, docimp.baseir, 
                    docimp.valorir, docimp.basecofins, docimp.valorcofins, docimp.basecsll, docimp.valorcsll, docimp.basepis, docimp.valorpis, 
                    docimp.deducaobaseir, docimp.valordeducaoir, docimp.desconto, docimp.mercadorias, docimp.servicos, docimp.valor, docimp.diferenca, 
                    docimp.valordestacado::numeric, docimp.baseicms, docimp.icms::numeric, docimp.valoricms, docimp.icmsnaocred, docimp.isentasicms, docimp.outrasicms, 
                    docimp.reducaoicms, docimp.reducaoipi, docimp.baseipi, docimp.valoripi, docimp.ipi, docimp.isentasipi, docimp.outras, docimp.basesubst, 
                    docimp.substprop, docimp.substterc, docimp.substnaoret, docimp.icmsretido, docimp.pisimp, docimp.cofinsimp, docimp.basepisimp, 
                    docimp.basecofinsimp, docimp.valorpisimp, docimp.valorcofinsimp, docimp.consumo, docimp.kwh, docimp.fretemm, docimp.pesotx, 
                    docimp.freteliquido, docimp.valorsec_cat, docimp.despacho, docimp.pedagio, docimp.despportuarias, docimp.cargadescarga, 
                    docimp.taxaterrestre, docimp.advalorem, docimp.valorgris, docimp.outrosvalores, docimp.pesobruto, docimp.pesoliquido, docimp.cubagem, 
                    docimp.anotacoes, docimp.percbaseinss, docimp.percbaseir, docimp.id_itemntr::uuid, docimp.id::uuid, docimp.id_conhectransp::uuid, docimp.id_estabelecimento::uuid, 
                    docimp.id_orgao::uuid, docimp.id_operador::uuid, docimp.id_redespachador::uuid, docimp.id_emitente::uuid, docimp.id_pessoa::uuid, docimp.id_consignatario::uuid, 
                    docimp.id_coleta::uuid, docimp.id_entrega::uuid, docimp.id_remetente::uuid, docimp.id_destinatario::uuid, docimp.id_transportadora::uuid, docimp.id_motorista::uuid, 
                    docimp.id_obra::uuid, docimp.id_grupodiferenciado::uuid, docimp.id_scp::uuid, docimp.tipodocumento::integer, docimp.xml_docengine, docimp.xml_transmitido, 
                    docimp.tipopedido::smallint, docimp.formapagamento::smallint, docimp.autorizacaocartao, docimp.documentocartao, docimp.dataautorizacaocartao::date, docimp.valoravista::numeric, 
                    docimp.vezescartao::smallint, docimp.anotacao, docimp.id_proposta::uuid, docimp.id_grupoempresarial::uuid, docimp.id_promocao::uuid, docimp.id_posicaoworkflow::uuid, 
                    docimp.id_midiaorigem::uuid, docimp.id_conta::uuid, docimp.id_layoutbancario::uuid, docimp.id_informacaocartao::uuid, docimp.datanegocio::date, docimp.aprovadopor::uuid, 
                    docimp.datahoraaprovacao::timestamp without time zone, docimp.acrescimofinanceiro::numeric, docimp.origem, docimp.id_objetoservico::uuid, docimp.id_docfis::uuid, docimp.id_cfop::uuid, 
                    docimp.discriminacaoservicos, docimp.statusrps::smallint, docimp.tiporps::smallint, docimp.tipotributacaoservicorps::smallint, docimp.regimeespecialtributacao::smallint, 
                    docimp.incentivocultural::smallint, docimp.ufprestacaoservico, docimp.cidadeprestacaoservico, docimp.id_estabelecimentocontraparte::uuid, 
                    docimp.descricaopagamento, docimp.datavalidade::date, docimp.contato, docimp.informacoespedido, docimp.id_oportunidade::uuid, 
                    docimp.id_parcelamento::uuid, docimp.id_docproposta::uuid, docimp.xml_cancelamento, docimp.motivo_cancelamento, docimp.data_cancelamento::timestamp without time zone, 
                    docimp.datacriacao::date, docimp.horacriacao::time(0) without time zone, docimp.referenciaexterna, docimp.tipoordemservico, docimp.origemordemservico::integer, docimp.contrato::uuid, 
                    docimp.processamentocontrato::uuid, docimp.id_pedido::uuid, docimp.documento_operacao::uuid, docimp.documento_operacao_codigo, docimp.xml_titulos, 
                    docimp.ordemservico_id::uuid, docimp.valorliquido::numeric, docimp.caixa::numeric, docimp.pontodevenda::uuid, docimp.id_serie::uuid, docimp.dataentradasaida::timestamp without time zone, 
                    docimp.tipoemitente::integer, docimp.tiporeceptor::integer, docimp.formadepagamento::smallint, docimp.tipooperacao::integer, docimp.uffatogerador, docimp.modocompra::smallint, 
                    docimp.tipodeemissao::integer, docimp.chave, docimp.observacao_movimentacao, docimp.tabeladepreco::uuid, docimp.id_localdeestoqueorigem::uuid, 
                    docimp.id_localdeestoquedestino::uuid, docimp.df_endereco_retirada::uuid, docimp.df_endereco_entrega::uuid, docimp.municipiofatogerador, 
                    docimp.xml_contingencia, docimp.datacontingencia::date, docimp.justificativacontingencia, docimp.debitoautomatico::boolean, docimp.contigencia_justificativa, 
                    docimp.contigencia_imprimiu::boolean, docimp.contigencia_datahora::timestamp without time zone, docimp.numeroprotocolo, docimp.tipoambiente::integer, docimp.lotecobrancaordemservico_id::uuid, 
                    docimp.documentorateado::uuid, docimp.requisicaoalmoxarifado_id::uuid, docimp.gerafinanceiro::boolean, docimp.id_conjunto_anexo::uuid, docimp.descricaoservicos, 
                    docimp.rps_original::uuid, docimp.tipo_retencao_iss::integer, docimp.xml_rps, docimp.anotacoes_sistema, docimp.anotacoes_manuais, docimp.uf_embarque, 
                    docimp.local_embarque, docimp.local_despacho, docimp.origemdocumento::smallint, docimp.link_nfse, docimp.id_documento_vinculado::uuid, docimp.pessoamunicipio::uuid, 
                    docimp.id_usuario_cadastro::uuid, docimp.prazoentrega::integer, docimp.notaimportacao::integer, docimp.chavegold, docimp.wkf_data::timestamp without time zone, docimp.wkf_estado, 
                    docimp.usuario_solicitacao_id::uuid, docimp.usuario_solicitacao_data::timestamp without time zone, docimp.emailenviado::boolean, docimp.id_instancia::uuid, docimp.situacaogerencial::integer, 
                    docimp.totalvalorfaturar::numeric, docimp.finalidadeemissao::smallint, docimp.id_operacao_nfs::uuid, docimp.analistacompra::uuid, docimp.infopiscompra::numeric, docimp.infocofinscompra::numeric, 
                    docimp.infoicmscompra::numeric, docimp.infoicmsstcompra::numeric, docimp.infoipicompra::numeric, docimp.status::smallint, docimp.vendedor::uuid, docimp.categoriadeproduto::uuid, 
                    docimp.uf_habilitacao, docimp.tipo_assinante::smallint, docimp.autenticacao_lote_digital, docimp.outras_retencoes::numeric, docimp.numero_titulo, 
                    docimp.vbcufdest::numeric, docimp.pfcpufdest::numeric, docimp.picmsufdest::numeric, docimp.picmsinter::numeric, docimp.picmsinterpart::numeric, docimp.vfcpufdest::numeric, docimp.vicmsufdest::numeric, 
                    docimp.vicmsufremet::numeric, docimp.dataprevisao_entradasaida::date, docimp.template_discriminacaorps::uuid, docimp.indiedest::smallint, docimp.sistema::smallint, 
                    docimp.tipo_insercao::smallint, docimp.indfinal::smallint, docimp.iddest::smallint, docimp.indpres::smallint, docimp.reconstruirxml::boolean, docimp.id_pedidoservico::uuid, docimp.iddestinoremessa::uuid, 
                    docimp.lotedigital::uuid, docimp.pretituloverificado::boolean, docimp.possuiadiantamento::boolean, docimp.tabeladefrete::uuid, docimp.observacao_dadosgerais, 
                    docimp.nota_antecipada::boolean, docimp.rascunho::boolean, docimp.recalcularimpostos::boolean, docimp.volumemanual::boolean, docimp.status_conferencia::smallint, docimp.id_rateiopadrao::uuid, 
                    docimp.outrosacrescimos::numeric, docimp.titulo_observacao, docimp.projeto_padrao_id::uuid, docimp.numeroexterno, docimp.naturezaoperacao, docimp.total_desconto::numeric, 
                    docimp.id_docfis_contrato::uuid, docimp.reinf_maodeobra, docimp.id_transacaofinanceira::uuid, docimp.id_contratofinanceiro::uuid, docimp.versao_dfe, docimp.troco::numeric, 
                    docimp.tipointegracao_pagamento::integer, docimp.tenant::bigint, docimp.codigo_verificacao, docimp.rota::uuid, docimp.rota_liberado::boolean, docimp.id_opeinterna::uuid, 
                    docimp.id_moeda::uuid, docimp.id_cotacao::uuid, docimp.xmlexplodido::boolean, docimp.romaneio_doc_atendido::boolean, docimp.icmsdesonsemdesc::boolean, docimp.lastupdate::timestamp without time zone
                    FROM nsdoc docimp
                    WHERE NOT EXISTS(SELECT 1
                         FROM ns.df_docfis doc
                         WHERE (docimp.id_estabelecimento::uuid = doc.id_estabelecimento::uuid
                         AND docimp.id_ano::integer = doc.id_ano
                         AND docimp.chavene = doc.chavene
                         AND docimp.serie = doc.serie
                         AND docimp.numero = doc.numero
                         AND docimp.periodo::integer = doc.periodo
                         AND docimp.id_emitente = doc.id_emitente::text
                         AND doc.modelo = 'NCE'
                         AND doc.tipo = 0
                         AND doc.sinal = 0)
                         LIMIT 1000) """

    @staticmethod
    def obterListaValoresNFCe(
        nfce: NFCE, icms_desonerado_desconto: bool = False
    ) -> list:
        """
        retorna uma lista com os valores dos campos do objeto nfe
        Note: os nomes dos campos estão nos comentários
        """
        if nfce.id is None:
            nfce.id = uuid.uuid4()
        valores = list()
        valores.append(nfce.dhEmi.year)  # id_ano integer NOT NULL,
        valores.append(0)  # sinal integer NOT NULL,
        valores.append(0)  # tipo integer NOT NULL,
        valores.append("NCE")  # modelo character varying(3) NOT NULL,
        valores.append(nfce.serie)  # serie character varying(3),
        valores.append("-")  # subserie character varying(2),
        valores.append(nfce.nNF)  # numero character varying(15),
        valores.append(nfce.dhEmi.strftime("%Y") + "00")  # periodo integer NOT NULL,
        valores.append(nfce.dhEmi)  # lancamento date,
        valores.append(nfce.dhEmi)  # emissao date,
        valores.append(nfce.calcular_cfop())  # cfop character varying(9),
        valores.append(None)  # cfopservico character varying(9),
        valores.append(None)  # tppessoa integer,
        valores.append(nfce.nNF)  # atenumero character varying(15),
        valores.append(None)  # datainiserv date,
        valores.append(None)  # datafimserv date,
        valores.append(nfce.dhEmi)  # datasaida date,
        valores.append(None)  # datadeclaracao date,
        valores.append(None)  # datanotaconhec date,
        valores.append(None)  # horasaida time without time zone,
        valores.append(None)  # porcaixa boolean,
        valores.append(None)  # petroleo boolean,
        valores.append(None)  # notafatura boolean,
        valores.append(nfce.existeCFOPDiferente())  # cfopdif boolean,
        valores.append(False)  # cfopserdif boolean,
        valores.append(False)  # cancelado boolean,
        valores.append(False)  # orgaopublico boolean,
        valores.append(False)  # somaiss boolean,
        valores.append(False)  # issoutromunic boolean,
        valores.append(False)  # retautomatica boolean,
        valores.append(False)  # retemiss boolean,
        valores.append(False)  # retemir boolean,
        valores.append(False)  # reteminss boolean,
        valores.append(False)  # retemcofins boolean,
        valores.append(False)  # retemcsll boolean,
        valores.append(False)  # retempis boolean,
        valores.append(False)  # retorno boolean,
        valores.append(False)  # porcontigencia boolean,
        valores.append(4)  # versao integer,
        valores.append(2)  # situacao integer,
        valores.append(0)  # situacaosped integer,
        valores.append(1)  # tipocalctrib integer,
        valores.append(None)  # tpligacao integer,
        valores.append(None)  # grupotensao integer,
        valores.append(3)  # crt integer,
        valores.append(None)  # messerv integer,
        valores.append(None)  # anoserv integer,
        valores.append(0)  # tiponfe integer,
        valores.append(None)  # tpoperador integer,
        valores.append(0)  # tpconsignatario integer,
        valores.append(10)  # consumidor integer, valor para nota importada
        valores.append(0)  # tiporedespacho integer,
        valores.append(0)  # remas integer,
        valores.append(0)  # rapis integer,
        valores.append(1)  # tipofrete integer,
        valores.append(0)  # tiporecolhimento integer,
        valores.append(None)  # tipotransporte integer,
        valores.append(1)  # volumes integer,
        valores.append(None)  # tipodocexterior integer,
        valores.append(1)  # parcelas integer DEFAULT 0,
        valores.append(None)  # tipocontab integer,
        valores.append(None)  # mesescredicms integer,
        valores.append(None)  # anoaidf integer,
        valores.append(None)  # anopexpam integer,
        valores.append(0)  # tipoimp integer,
        valores.append(None)  # classe integer,
        valores.append(None)  # tiporeceita integer,
        valores.append(None)  # tipoconsumo integer,
        valores.append(None)  # tiponavegacao integer,
        valores.append(None)  # tipoveiculo integer,
        valores.append(None)  # naturezafrete integer,
        valores.append(None)  # tipotarifaar integer,
        valores.append(nfce.chNFe)  # chavene character varying(44),
        valores.append(nfce.chNFe[0:34])  # chaveneini character varying(34),
        valores.append(nfce.chNFe[0:6])  # chavene01 character varying(6),
        valores.append(nfce.chNFe[6:20])  # chavene02 character varying(14),
        valores.append(nfce.chNFe[20:25])  # chavene03 character varying(5),
        valores.append(nfce.chNFe[25:34])  # chavene04 character varying(9),
        valores.append(nfce.chNFe[34:44])  # chavenefim character varying(10),
        valores.append(None)  # codigoirrf character varying(6),
        valores.append(None)  # codigopis character varying(6),
        valores.append(None)  # codigocsll character varying(6),
        valores.append(None)  # codigocofins character varying(6),
        valores.append(None)  # numacdraw character varying(20),
        valores.append(None)  # campoligacao character varying(20),
        valores.append(None)  # terminal character varying(15),
        valores.append(None)  # codarea character varying(5),
        valores.append(None)  # rntrc character varying(14),
        valores.append(None)  # serierps character varying(5),
        valores.append(None)  # rps character varying(15),
        valores.append(None)  # cnae character varying(9),
        valores.append(nfce.cMunFG)  # codmunic character varying(8),
        valores.append(None)  # codserv character varying(8),
        valores.append(nfce.cMunFG)  # municdest character varying(8),
        valores.append(None)  # codif character varying(21),
        valores.append(None)  # numerofrete character varying(22),
        valores.append(None)  # marca character varying(12),
        valores.append(None)  # tipovolume character varying(10),
        valores.append(None)  # placa character varying(7),
        valores.append(None)  # placa02 character varying(7),
        valores.append(None)  # placa03 character varying(7),
        valores.append(None)  # ufplaca character varying(2),
        valores.append(None)  # ufplaca02 character varying(2),
        valores.append(None)  # ufplaca03 character varying(2),
        valores.append(None)  # doccomexterior character varying(12),
        valores.append(None)  # parcelamento character varying(6),
        valores.append(None)  # renavam character varying(9),
        valores.append(None)  # codigodip character varying(3),
        valores.append(nfce.infCpl)  # observacao character varying(5000),
        valores.append(None)  # obsestoque character varying(150),
        valores.append(None)  # selofiscal character varying(12),
        valores.append(None)  # aidf character varying(11),
        valores.append(None)  # numeropexpam character varying(8),
        valores.append(None)  # lacre character varying(15),
        valores.append(None)  # unidadecarga character varying(20),
        valores.append(None)  # frota character varying(20),
        valores.append(None)  # veiculo character varying(30),
        valores.append(None)  # viagem character varying(9),
        valores.append(None)  # otm character varying(8),
        valores.append(nfce.vFrete)  # frete numeric(20,2),
        valores.append(nfce.vSeg)  # seguro numeric(20,2),
        valores.append(0)  # basetransp numeric(20,2),
        valores.append(0)  # iss numeric(20,2),
        valores.append(0)  # deducaoiss numeric(20,2),
        valores.append(0)  # inss numeric(20,2),
        valores.append(0)  # ir numeric(20,2),
        valores.append(0)  # valoriss numeric(20,2),
        valores.append(0)  # baseiss numeric(20,2),
        valores.append(0)  # baseinss numeric(20,2),
        valores.append(0)  # valorinss numeric(20,2),
        valores.append(0)  # valorinssadicional numeric(20,2),
        valores.append(0)  # valorinssnaoretido numeric(20,2),
        valores.append(0)  # valorinsssubempreitada numeric(20,2),
        valores.append(0)  # baseir numeric(20,2),
        valores.append(0)  # valorir numeric(20,2),
        valores.append(0)  # basecofins numeric(20,2),
        valores.append(0)  # valorcofins numeric(20,2),
        valores.append(0)  # basecsll numeric(20,2),
        valores.append(0)  # valorcsll numeric(20,2),
        valores.append(0)  # basepis numeric(20,2),
        valores.append(0)  # valorpis numeric(20,2),
        valores.append(0)  # deducaobaseir numeric(20,2),
        valores.append(0)  # valordeducaoir numeric(20,2),
        valores.append(0)  # desconto numeric(20,2),
        valores.append(nfce.retornarValorMercadorias())  # mercadorias numeric(20,2),
        valores.append(0)  # servicos numeric(20,2),
        valores.append(
            float(nfce.vNF)
            - sum(item.icms.retornarValorDesoneracao() for item in nfce.lista_itens)
        )  # valor numeric(20,2),
        valores.append(0)  # diferenca numeric(20,2),
        valores.append(nfce.vNF)  # valordestacado numeric(20,2),
        valores.append(nfce.retornarBaseICMS())  # baseicms numeric(20,2),
        valores.append(None)  # icms numeric(20,2),
        valores.append(nfce.retornarValorICMS())  # valoricms numeric(20,2),
        valores.append(0)  # icmsnaocred numeric(20,2),
        valores.append(nfce.retornarIsentasICMS())  # isentasicms numeric(20,2),
        valores.append(nfce.outras_icms)  # outrasicms numeric(20,2),
        valores.append(0)  # reducaoicms numeric(20,4),
        valores.append(0)  # reducaoipi numeric(20,4),
        valores.append(0)  # baseipi numeric(20,2),
        valores.append(0)  # valoripi numeric(20,2),
        valores.append(0)  # ipi numeric(20,2),
        valores.append(0)  # isentasipi numeric(20,2),
        valores.append(0)  # outras numeric(20,2),
        valores.append(0)  # basesubst numeric(20,2),
        valores.append(0)  # substprop numeric(20,2),
        valores.append(0)  # substterc numeric(20,2),
        valores.append(0)  # substnaoret numeric(20,2),
        valores.append(0)  # icmsretido numeric(20,2),
        valores.append(0)  # pisimp numeric(20,4),
        valores.append(0)  # cofinsimp numeric(20,4),
        valores.append(0)  # basepisimp numeric(20,2),
        valores.append(0)  # basecofinsimp numeric(20,2),
        valores.append(0)  # valorpisimp numeric(20,2),
        valores.append(0)  # valorcofinsimp numeric(20,2),
        valores.append(0)  # consumo numeric(20,2),
        valores.append(0)  # kwh numeric(20,2),
        valores.append(0)  # fretemm numeric(20,2),
        valores.append(0)  # pesotx numeric(20,2),
        valores.append(0)  # freteliquido numeric(20,2),
        valores.append(0)  # valorsec_cat numeric(20,2),
        valores.append(0)  # despacho numeric(20,2),
        valores.append(0)  # pedagio numeric(20,2),
        valores.append(0)  # despportuarias numeric(20,2),
        valores.append(0)  # cargadescarga numeric(20,2),
        valores.append(0)  # taxaterrestre numeric(20,2),
        valores.append(0)  # advalorem numeric(20,2),
        valores.append(0)  # valorgris numeric(20,2),
        valores.append(nfce.vOutro)  # outrosvalores numeric(20,2),
        valores.append(0)  # pesobruto double precision,
        valores.append(0)  # pesoliquido double precision,
        valores.append(0)  # cubagem double precision,
        valores.append(None)  # anotacoes text,
        valores.append(0)  # percbaseinss double precision DEFAULT 100,
        valores.append(0)  # percbaseir double precision DEFAULT 100,
        valores.append(None)  # id_itemntr uuid,
        valores.append(str(nfce.id))  # id uuid NOT NULL DEFAULT uuid_generate_v4(),
        valores.append(None)  # id_conhectransp uuid,
        valores.append(str(nfce.id_emitente))  # id_estabelecimento uuid,
        valores.append(None)  # id_orgao uuid,
        valores.append(None)  # id_operador uuid,
        valores.append(None)  # id_redespachador uuid,
        valores.append(str("00000000-0000-0000-0000-000000000000"))  # id_emitente uuid,
        if nfce.destinatario.id is not None:
            valores.append(str(nfce.destinatario.id))  # id_pessoa uuid,
        else:
            valores.append(None)
        valores.append(None)  # id_consignatario uuid,
        valores.append(None)  # id_coleta uuid,
        valores.append(None)  # id_entrega uuid,
        valores.append(None)  # id_remetente uuid,
        if nfce.destinatario.id is not None:
            valores.append(str(nfce.destinatario.id))  # id_destinatario uuid,
        else:
            valores.append(None)
        valores.append(None)  # id_transportadora uuid,
        valores.append(None)  # id_motorista uuid,
        valores.append(None)  # id_obra uuid,
        valores.append(None)  # id_grupodiferenciado uuid,
        valores.append(None)  # id_scp uuid,
        valores.append(None)  # tipodocumento integer,
        valores.append(None)  # xml_docengine text,
        valores.append(nfce.xml.replace("\ufeff", ""))  # xml_transmitido text,
        valores.append(None)  # tipopedido smallint,
        valores.append(None)  # formapagamento smallint,
        valores.append(None)  # autorizacaocartao character varying(30),
        valores.append(None)  # documentocartao character varying(30),
        valores.append(None)  # dataautorizacaocartao date,
        valores.append(None)  # valoravista numeric(20,2),
        valores.append(None)  # vezescartao smallint,
        valores.append(None)  # anotacao text,
        valores.append(None)  # id_proposta uuid,
        valores.append(None)  # id_grupoempresarial uuid,
        valores.append(None)  # id_promocao uuid,
        valores.append(None)  # id_posicaoworkflow uuid,
        valores.append(None)  # id_midiaorigem uuid,
        valores.append(None)  # id_conta uuid,
        valores.append(None)  # id_layoutbancario uuid,
        valores.append(None)  # id_informacaocartao uuid,
        valores.append(None)  # datanegocio date,
        valores.append(None)  # aprovadopor uuid,
        valores.append(None)  # datahoraaprovacao timestamp without time zone,
        valores.append(None)  # acrescimofinanceiro numeric(20,2),
        valores.append(0)  # origem integer NOT NULL DEFAULT 0,
        valores.append(None)  # id_objetoservico uuid,
        valores.append(None)  # id_docfis uuid,
        valores.append(nfce.retornarIdCFOP())  # id_cfop uuid,
        valores.append(None)  # discriminacaoservicos text,
        valores.append(None)  # statusrps smallint,
        valores.append(None)  # tiporps smallint,
        valores.append(None)  # tipotributacaoservicorps smallint,
        valores.append(None)  # regimeespecialtributacao smallint,
        valores.append(None)  # incentivocultural smallint,
        valores.append(None)  # ufprestacaoservico character varying(2),
        valores.append(None)  # cidadeprestacaoservico character varying(50),
        valores.append(None)  # id_estabelecimentocontraparte uuid,
        valores.append(None)  # descricaopagamento text,
        valores.append(None)  # datavalidade date,
        valores.append(None)  # contato character varying(150),
        valores.append(None)  # informacoespedido text,
        valores.append(None)  # id_oportunidade uuid,
        valores.append(None)  # id_parcelamento uuid,
        valores.append(None)  # id_docproposta uuid,
        valores.append(None)  # xml_cancelamento text,
        valores.append(None)  # motivo_cancelamento character varying(150),
        valores.append(None)  # data_cancelamento timestamp without time zone,
        valores.append(utilidades.now_brazil())  # datacriacao date,
        valores.append(utilidades.now_brazil())  # horacriacao time(0) without time zone,
        valores.append(None)  # referenciaexterna character varying(60),
        valores.append(None)  # tipoordemservico character varying(30),
        valores.append(None)  # origemordemservico integer,
        valores.append(None)  # contrato uuid,
        valores.append(None)  # processamentocontrato uuid,
        valores.append(None)  # id_pedido uuid,
        valores.append(
            (
                nfce.operacaoCfopSlot.operacao
                if (
                    (nfce.operacaoCfopSlot is not None)
                    and (nfce.operacaoCfopSlot.operacao is not None)
                )
                else None
            )
        )  # documento_operacao uuid,
        valores.append(
            (
                nfce.operacaoCfopSlot.codigo
                if (
                    (nfce.operacaoCfopSlot is not None)
                    and (nfce.operacaoCfopSlot.codigo is not None)
                )
                else None
            )
        )  # documento_operacao_codigo
        valores.append(None)  # xml_titulos text,
        valores.append(None)  # ordemservico_id uuid,
        valores.append(None)  # valorliquido numeric(20,2),
        valores.append(None)  # caixa integer,
        valores.append(None)  # pontodevenda uuid,
        valores.append(None)  # id_serie uuid,
        valores.append(nfce.dhEmi)  # dataentradasaida timestamp without time zone,
        valores.append(0)  # tipoemitente smallint,
        valores.append(1)  # tiporeceptor smallint,
        valores.append(None)  # formadepagamento smallint,
        valores.append(None)  # tipooperacao smallint
        valores.append(None)  # uffatogerador character varying(2),
        valores.append(None)  # modocompra smallint,
        valores.append(None)  # tipodeemissao smallint,
        valores.append(nfce.chNFe)  # chave character varying(44),
        valores.append(None)  # observacao_movimentacao character varying,
        valores.append(None)  # tabeladepreco uuid,
        valores.append(None)  # id_localdeestoqueorigem uuid,
        valores.append(None)  # id_localdeestoquedestino uuid,
        valores.append(None)  # df_endereco_retirada uuid,
        valores.append(None)  # df_endereco_entrega uuid,
        valores.append(nfce.cMunFG)  # municipiofatogerador character varying(8),
        valores.append(None)  # xml_contingencia text,
        valores.append(None)  # datacontingencia date,
        valores.append(None)  # justificativacontingencia text,
        valores.append(False)  # debitoautomatico boolean NOT NULL DEFAULT false,
        valores.append(None)  # contigencia_justificativa text,
        valores.append(None)  # contigencia_imprimiu boolean,
        valores.append(None)  # contigencia_datahora timestamp without time zone,
        valores.append(None)  # numeroprotocolo character varying(30),
        valores.append(None)  # tipoambiente smallint,
        valores.append(None)  # lotecobrancaordemservico_id uuid,
        valores.append(None)  # documentorateado uuid,
        valores.append(None)  # requisicaoalmoxarifado_id uuid,
        valores.append(False)  # gerafinanceiro boolean NOT NULL DEFAULT true,
        valores.append(None)  # id_conjunto_anexo uuid DEFAULT uuid_generate_v4(),
        valores.append(None)  # descricaoservicos text,
        valores.append(None)  # rps_original uuid,
        valores.append(None)  # tipo_retencao_iss integer DEFAULT 0,
        valores.append(None)  # xml_rps text,
        valores.append(None)  # anotacoes_sistema text,
        valores.append(None)  # anotacoes_manuais text,
        valores.append(None)  # uf_embarque character varying(2),
        valores.append(None)  # local_embarque character varying(60),
        valores.append(None)  # local_despacho character varying(60),
        valores.append(3)  # origemdocumento smallint,
        valores.append(None)  # link_nfse character varying(500),
        valores.append(None)  # id_documento_vinculado uuid,
        valores.append(None)  # pessoamunicipio uuid,
        valores.append(None)  # id_usuario_cadastro uuid,
        valores.append(None)  # prazoentrega integer,
        valores.append(None)  # notaimportacao integer,
        valores.append(None)  # chavegold text,
        valores.append(None)  # wkf_data timestamp without time zone,
        valores.append(None)  # wkf_estado character varying(60),
        valores.append(None)  # usuario_solicitacao_id uuid,
        valores.append(None)  # usuario_solicitacao_data timestamp without time zone,
        valores.append(False)  # emailenviado boolean,
        valores.append(None)  # id_instancia uuid,
        valores.append(None)  # situacaogerencial integer,
        valores.append(None)  # totalvalorfaturar numeric(20,2),
        valores.append(None)  # finalidadeemissao smallint,
        valores.append(None)  # id_operacao_nfs uuid,
        valores.append(None)  # analistacompra uuid,
        valores.append(None)  # infopiscompra numeric(20,2),
        valores.append(None)  # infocofinscompra numeric(20,2),
        valores.append(None)  # infoicmscompra numeric(20,2),
        valores.append(None)  # infoicmsstcompra numeric(20,2),
        valores.append(None)  # infoipicompra numeric(20,2),
        valores.append(None)  # status smallint DEFAULT 0,
        valores.append(None)  # vendedor uuid,
        valores.append(None)  # categoriadeproduto uuid,
        valores.append(None)  # uf_habilitacao character varying(2),
        valores.append(None)  # tipo_assinante smallint,
        valores.append(None)  # autenticacao_lote_digital character varying(32),
        valores.append(0)  # outras_retencoes numeric(20,2) DEFAULT 0,
        valores.append(None)  # numero_titulo character varying(30),
        valores.append(None)  # vbcufdest numeric(20,2),
        valores.append(None)  # pfcpufdest numeric(20,2),
        valores.append(None)  # picmsufdest numeric(20,2),
        valores.append(None)  # picmsinter numeric(20,2),
        valores.append(None)  # picmsinterpart numeric(20,2),
        valores.append(None)  # vfcpufdest numeric(20,2),
        valores.append(None)  # vicmsufdest numeric(20,2),
        valores.append(None)  # vicmsufremet numeric(20,2),
        valores.append(None)  # dataprevisao_entradasaida date,
        valores.append(None)  # template_discriminacaorps uuid,
        valores.append(None)  # indiedest smallint,
        valores.append(3)  # sistema smallint,
        valores.append(None)  # tipo_insercao smallint,
        valores.append(None)  # indfinal smallint,
        valores.append(None)  # iddest smallint,
        valores.append(None)  # indpres smallint,
        valores.append(True)  # reconstruirxml boolean DEFAULT false,
        valores.append(None)  # id_pedidoservico uuid,
        valores.append(None)  # iddestinoremessa uuid,
        valores.append(None)  # lotedigital uuid,
        valores.append(None)  # pretituloverificado boolean DEFAULT false,
        valores.append(None)  # possuiadiantamento boolean,
        valores.append(None)  # tabeladefrete uuid,
        valores.append(None)  # observacao_dadosgerais character varying(1000),
        valores.append(None)  # nota_antecipada boolean,
        valores.append(False)  # rascunho boolean NOT NULL DEFAULT false,
        valores.append(False)  # recalcularimpostos boolean NOT NULL DEFAULT false,
        valores.append(None)  # volumemanual boolean DEFAULT false,
        valores.append(None)  # status_conferencia smallint,
        valores.append(None)  # id_rateiopadrao uuid,
        valores.append(None)  # outrosacrescimos numeric(20,2),
        valores.append(None)  # titulo_observacao character varying(1000),
        valores.append(None)  # projeto_padrao_id uuid,
        valores.append(None)  # numeroexterno character varying(255),
        valores.append(None)  # naturezaoperacao character varying(60),
        valores.append(nfce.retornarDescontoTotal())  # total_desconto numeric(20,6),
        valores.append(None)  # id_docfis_contrato uuid,
        valores.append(None)  # reinf_maodeobra character varying(12),
        valores.append(None)  # id_transacaofinanceira character varying(50),
        valores.append(None)  # id_contratofinanceiro character varying(50),
        valores.append(None)  # versao_dfe character varying(10),
        valores.append(nfce.vTroco)  # troco numeric(20,2),
        valores.append(None)  # tipointegracao_pagamento integer,
        valores.append(None)  # tenant bigint,
        valores.append(None)  # codigo_verificacao character varying(100),
        valores.append(None)  # rota uuid,
        valores.append(None)  # rota_liberado boolean,
        valores.append(None)  # id_opeinterna uuid,
        valores.append(None)  # id_moeda uuid,
        valores.append(None)  # id_cotacao uuid,
        valores.append(
            False
        )  # xmlexplodido boolean NOT NULL DEFAULT false, -- Indica que a última alteração no registro foi feita pela função explodexml, e que o xml e os dados no registro estão alinhados
        valores.append(None)  # romaneio_doc_atendido boolean DEFAULT false,
        if icms_desonerado_desconto:
            valores.append(None)
        else:
            valores.append(True)
        valores.append(
            utilidades.now_brazil()
        )  # lastupdate timestamp without time zone DEFAULT now(),
        return valores

    @staticmethod
    def obterSQLInsertContabilizacao() -> str:
        return "select contabilizacao.fn_avaliar_docfis(\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {},\
                    {});"

    @staticmethod
    def obterListaValoresContabilizacao(nfce: NFCE) -> list:
        """
        retorna uma lista com os valores dos campos do objeto nfe para contabilizacao
        """
        valores = list()
        valores.append(0)  # p_tipo = <Docfis>.tipo,
        valores.append("'NCE'")  # p_modelo = <Docfis>.modelo,
        valores.append(
            "'" + nfce.calcular_cfop() + "'"
        )  # p_cfop = <Docfis>.cfop, se não estiver preenchido, usar o CFOP de qualquer item da nota,
        valores.append(0)  # p_sinal = <Docfis>.sinal,
        valores.append("'" + str(nfce.id) + "'")  # p_id = <Docfis>.id,
        valores.append(
            "'" + str(nfce.id_emitente) + "'"
        )  # p_id_estabelecimento = <Docfis>.id_estabelecimento,
        valores.append(
            "'00000000-0000-0000-0000-000000000000'"
        )  # p_documento_operacao = <Docfis>.documento_operacao,
        valores.append(False)  # p_cancelado = <Docfis>.cancelado,
        valores.append("Null")  # p_data_cancelamento = <Docfis>.Data_cancelamento,
        valores.append(
            "'" + nfce.dhEmi.isoformat() + "'"
        )  # p_data_lancamento = <Docfis>.Data_Lancamento,
        valores.append(
            True
        )  # p_insert = True se for uma inserção, False se for um Update,
        valores.append(
            "Null"
        )  # p_nota = to_json(<Docfis>). Obs: Json da Docfis. Hoje só é realmente necessário se for uma nota que tenha algum serviço,
        valores.append(
            False
        )  # p_requisicao = (select requisicao from estoque.operacoes where operacao = <Docfis>.documento_operacao),
        valores.append(
            True
        )  # p_enfileirar_cancelamento = (contabilizacao.get_configuracoes_gerais((select empresa from ns.estabelecimentos where estabelecimento = p_id_estabelecimento),'enfileirar_cancelamento_somente_apos_apuracao')).enfileirar_cancelamento_somente_apos_apuracao,
        valores.append(
            0
        )  # p_tipo_cfop = (select tipo from ns.cfop where cfop = p_cfop and (tipo = 1 or tipo = 0)),
        valores.append(
            True
        )  # p_cfop_merc = exists(select 1 from contabilizacao.objetoscfops oc where oc.cfop = substr(replace(p_cfop,'.',''),1,4))
        return valores

    @staticmethod
    def obterListaCamposDocFis() -> list:
        """
        retorna uma lista com os campos do objeto nfe
        """
        valores = list()
        valores.append("id_ano")
        valores.append("sinal")
        valores.append("tipo")
        valores.append("modelo")
        valores.append("serie")
        valores.append("subserie")
        valores.append("numero")
        valores.append("periodo")
        valores.append("lancamento")
        valores.append("emissao")
        valores.append("cfop")
        valores.append("cfopservico")
        valores.append("tppessoa")
        valores.append("atenumero")
        valores.append("datainiserv")
        valores.append("datafimserv")
        valores.append("datasaida")
        valores.append("datadeclaracao")
        valores.append("datanotaconhec")
        valores.append("horasaida")
        valores.append("porcaixa")
        valores.append("petroleo")
        valores.append("notafatura")
        valores.append("cfopdif")
        valores.append("cfopserdif")
        valores.append("cancelado")
        valores.append("orgaopublico")
        valores.append("somaiss")
        valores.append("issoutromunic")
        valores.append("retautomatica")
        valores.append("retemiss")
        valores.append("retemir")
        valores.append("reteminss")
        valores.append("retemcofins")
        valores.append("retemcsll")
        valores.append("retempis")
        valores.append("retorno")
        valores.append("porcontigencia")
        valores.append("versao")
        valores.append("situacao")
        valores.append("situacaosped")
        valores.append("tipocalctrib")
        valores.append("tpligacao")
        valores.append("grupotensao")
        valores.append("crt")
        valores.append("messerv")
        valores.append("anoserv")
        valores.append("tiponfe")
        valores.append("tpoperador")
        valores.append("tpconsignatario")
        valores.append("consumidor")
        valores.append("tiporedespacho")
        valores.append("remas")
        valores.append("rapis")
        valores.append("tipofrete")
        valores.append("tiporecolhimento")
        valores.append("tipotransporte")
        valores.append("volumes")
        valores.append("tipodocexterior")
        valores.append("parcelas")
        valores.append("tipocontab")
        valores.append("mesescredicms")
        valores.append("anoaidf")
        valores.append("anopexpam")
        valores.append("tipoimp")
        valores.append("classe")
        valores.append("tiporeceita")
        valores.append("tipoconsumo")
        valores.append("tiponavegacao")
        valores.append("tipoveiculo")
        valores.append("naturezafrete")
        valores.append("tipotarifaar")
        valores.append("chavene")
        valores.append("chaveneini")
        valores.append("chavene01")
        valores.append("chavene02")
        valores.append("chavene03")
        valores.append("chavene04")
        valores.append("chavenefim")
        valores.append("codigoirrf")
        valores.append("codigopis")
        valores.append("codigocsll")
        valores.append("codigocofins")
        valores.append("numacdraw")
        valores.append("campoligacao")
        valores.append("terminal")
        valores.append("codarea")
        valores.append("rntrc")
        valores.append("serierps")
        valores.append("rps")
        valores.append("cnae")
        valores.append("codmunic")
        valores.append("codserv")
        valores.append("municdest")
        valores.append("codif")
        valores.append("numerofrete")
        valores.append("marca")
        valores.append("tipovolume")
        valores.append("placa")
        valores.append("placa02")
        valores.append("placa03")
        valores.append("ufplaca")
        valores.append("ufplaca02")
        valores.append("ufplaca03")
        valores.append("doccomexterior")
        valores.append("parcelamento")
        valores.append("renavam")
        valores.append("codigodip")
        valores.append("observacao")
        valores.append("obsestoque")
        valores.append("selofiscal")
        valores.append("aidf")
        valores.append("numeropexpam")
        valores.append("lacre")
        valores.append("unidadecarga")
        valores.append("frota")
        valores.append("veiculo")
        valores.append("viagem")
        valores.append("otm")
        valores.append("frete")
        valores.append("seguro")
        valores.append("basetransp")
        valores.append("iss")
        valores.append("deducaoiss")
        valores.append("inss")
        valores.append("ir")
        valores.append("valoriss")
        valores.append("baseiss")
        valores.append("baseinss")
        valores.append("valorinss")
        valores.append("valorinssadicional")
        valores.append("valorinssnaoretido")
        valores.append("valorinsssubempreitada")
        valores.append("baseir")
        valores.append("valorir")
        valores.append("basecofins")
        valores.append("valorcofins")
        valores.append("basecsll")
        valores.append("valorcsll")
        valores.append("basepis")
        valores.append("valorpis")
        valores.append("deducaobaseir")
        valores.append("valordeducaoir")
        valores.append("desconto")
        valores.append("mercadorias")
        valores.append("servicos")
        valores.append("valor")
        valores.append("diferenca")
        valores.append("valordestacado")
        valores.append("baseicms")
        valores.append("icms")
        valores.append("valoricms")
        valores.append("icmsnaocred")
        valores.append("isentasicms")
        valores.append("outrasicms")
        valores.append("reducaoicms")
        valores.append("reducaoipi")
        valores.append("baseipi")
        valores.append("valoripi")
        valores.append("ipi")
        valores.append("isentasipi")
        valores.append("outras")
        valores.append("basesubst")
        valores.append("substprop")
        valores.append("substterc")
        valores.append("substnaoret")
        valores.append("icmsretido")
        valores.append("pisimp")
        valores.append("cofinsimp")
        valores.append("basepisimp")
        valores.append("basecofinsimp")
        valores.append("valorpisimp")
        valores.append("valorcofinsimp")
        valores.append("consumo")
        valores.append("kwh")
        valores.append("fretemm")
        valores.append("pesotx")
        valores.append("freteliquido")
        valores.append("valorsec_cat")
        valores.append("despacho")
        valores.append("pedagio")
        valores.append("despportuarias")
        valores.append("cargadescarga")
        valores.append("taxaterrestre")
        valores.append("advalorem")
        valores.append("valorgris")
        valores.append("outrosvalores")
        valores.append("pesobruto")
        valores.append("pesoliquido")
        valores.append("cubagem")
        valores.append("anotacoes")
        valores.append("percbaseinss")
        valores.append("percbaseir")
        valores.append("id_itemntr")
        valores.append("id")
        valores.append("id_conhectransp")
        valores.append("id_estabelecimento")
        valores.append("id_orgao")
        valores.append("id_operador")
        valores.append("id_redespachador")
        valores.append("id_emitente")
        valores.append("id_pessoa")
        valores.append("id_consignatario")
        valores.append("id_coleta")
        valores.append("id_entrega")
        valores.append("id_remetente")
        valores.append("id_destinatario")
        valores.append("id_transportadora")
        valores.append("id_motorista")
        valores.append("id_obra")
        valores.append("id_grupodiferenciado")
        valores.append("id_scp")
        valores.append("tipodocumento")
        valores.append("xml_docengine")
        valores.append("xml_transmitido")
        valores.append("tipopedido")
        valores.append("formapagamento")
        valores.append("autorizacaocartao")
        valores.append("documentocartao")
        valores.append("dataautorizacaocartao")
        valores.append("valoravista")
        valores.append("vezescartao")
        valores.append("anotacao")
        valores.append("id_proposta")
        valores.append("id_grupoempresarial")
        valores.append("id_promocao")
        valores.append("id_posicaoworkflow")
        valores.append("id_midiaorigem")
        valores.append("id_conta")
        valores.append("id_layoutbancario")
        valores.append("id_informacaocartao")
        valores.append("datanegocio")
        valores.append("aprovadopor")
        valores.append("datahoraaprovacao")
        valores.append("acrescimofinanceiro")
        valores.append("origem")
        valores.append("id_objetoservico")
        valores.append("id_docfis")
        valores.append("id_cfop")
        valores.append("discriminacaoservicos")
        valores.append("statusrps")
        valores.append("tiporps")
        valores.append("tipotributacaoservicorps")
        valores.append("regimeespecialtributacao")
        valores.append("incentivocultural")
        valores.append("ufprestacaoservico")
        valores.append("cidadeprestacaoservico")
        valores.append("id_estabelecimentocontraparte")
        valores.append("descricaopagamento")
        valores.append("datavalidade")
        valores.append("contato")
        valores.append("informacoespedido")
        valores.append("id_oportunidade")
        valores.append("id_parcelamento")
        valores.append("id_docproposta")
        valores.append("xml_cancelamento")
        valores.append("motivo_cancelamento")
        valores.append("data_cancelamento")
        valores.append("datacriacao")
        valores.append("horacriacao")
        valores.append("referenciaexterna")
        valores.append("tipoordemservico")
        valores.append("origemordemservico")
        valores.append("contrato")
        valores.append("processamentocontrato")
        valores.append("id_pedido")
        valores.append("documento_operacao")
        valores.append("documento_operacao_codigo")
        valores.append("xml_titulos")
        valores.append("ordemservico_id")
        valores.append("valorliquido")
        valores.append("caixa")
        valores.append("pontodevenda")
        valores.append("id_serie")
        valores.append("dataentradasaida")
        valores.append("tipoemitente")
        valores.append("tiporeceptor")
        valores.append("formadepagamento")
        valores.append("tipooperacao")
        valores.append("uffatogerador")
        valores.append("modocompra")
        valores.append("tipodeemissao")
        valores.append("chave")
        valores.append("observacao_movimentacao")
        valores.append("tabeladepreco")
        valores.append("id_localdeestoqueorigem")
        valores.append("id_localdeestoquedestino")
        valores.append("df_endereco_retirada")
        valores.append("df_endereco_entrega")
        valores.append("municipiofatogerador")
        valores.append("xml_contingencia")
        valores.append("datacontingencia")
        valores.append("justificativacontingencia")
        valores.append("debitoautomatico")
        valores.append("contigencia_justificativa")
        valores.append("contigencia_imprimiu")
        valores.append("contigencia_datahora")
        valores.append("numeroprotocolo")
        valores.append("tipoambiente")
        valores.append("lotecobrancaordemservico_id")
        valores.append("documentorateado")
        valores.append("requisicaoalmoxarifado_id")
        valores.append("gerafinanceiro")
        valores.append("id_conjunto_anexo")
        valores.append("descricaoservicos")
        valores.append("rps_original")
        valores.append("tipo_retencao_iss")
        valores.append("xml_rps")
        valores.append("anotacoes_sistema")
        valores.append("anotacoes_manuais")
        valores.append("uf_embarque")
        valores.append("local_embarque")
        valores.append("local_despacho")
        valores.append("origemdocumento")
        valores.append("link_nfse")
        valores.append("id_documento_vinculado")
        valores.append("pessoamunicipio")
        valores.append("id_usuario_cadastro")
        valores.append("prazoentrega")
        valores.append("notaimportacao")
        valores.append("chavegold")
        valores.append("wkf_data")
        valores.append("wkf_estado")
        valores.append("usuario_solicitacao_id")
        valores.append("usuario_solicitacao_data")
        valores.append("emailenviado")
        valores.append("id_instancia")
        valores.append("situacaogerencial")
        valores.append("totalvalorfaturar")
        valores.append("finalidadeemissao")
        valores.append("id_operacao_nfs")
        valores.append("analistacompra")
        valores.append("infopiscompra")
        valores.append("infocofinscompra")
        valores.append("infoicmscompra")
        valores.append("infoicmsstcompra")
        valores.append("infoipicompra")
        valores.append("status")
        valores.append("vendedor")
        valores.append("categoriadeproduto")
        valores.append("uf_habilitacao")
        valores.append("tipo_assinante")
        valores.append("autenticacao_lote_digital")
        valores.append("outras_retencoes")
        valores.append("numero_titulo")
        valores.append("vbcufdest")
        valores.append("pfcpufdest")
        valores.append("picmsufdest")
        valores.append("picmsinter")
        valores.append("picmsinterpart")
        valores.append("vfcpufdest")
        valores.append("vicmsufdest")
        valores.append("vicmsufremet")
        valores.append("dataprevisao_entradasaida")
        valores.append("template_discriminacaorps")
        valores.append("indiedest")
        valores.append("sistema")
        valores.append("tipo_insercao")
        valores.append("indfinal")
        valores.append("iddest")
        valores.append("indpres")
        valores.append("reconstruirxml")
        valores.append("id_pedidoservico")
        valores.append("iddestinoremessa")
        valores.append("lotedigital")
        valores.append("pretituloverificado")
        valores.append("possuiadiantamento")
        valores.append("tabeladefrete")
        valores.append("observacao_dadosgerais")
        valores.append("nota_antecipada")
        valores.append("rascunho")
        valores.append("recalcularimpostos")
        valores.append("volumemanual")
        valores.append("status_conferencia")
        valores.append("id_rateiopadrao")
        valores.append("outrosacrescimos")
        valores.append("titulo_observacao")
        valores.append("projeto_padrao_id")
        valores.append("numeroexterno")
        valores.append("naturezaoperacao")
        valores.append("total_desconto")
        valores.append("id_docfis_contrato")
        valores.append("reinf_maodeobra")
        valores.append("id_transacaofinanceira")
        valores.append("id_contratofinanceiro")
        valores.append("versao_dfe")
        valores.append("troco")
        valores.append("tipointegracao_pagamento")
        valores.append("tenant")
        valores.append("codigo_verificacao")
        valores.append("rota")
        valores.append("rota_liberado")
        valores.append("id_opeinterna")
        valores.append("id_moeda")
        valores.append("id_cotacao")
        valores.append("xmlexplodido")
        valores.append("romaneio_doc_atendido")
        valores.append("lastupdate")
        return valores

    @staticmethod
    def obterListaValoresMovimentoEstoque(
        nfce: NFCE, item: ItemNota, slot: str, ordem: int
    ):
        valores = list()
        valores.append(nfce.dhEmi)  # data date NOT NULL,
        valores.append(7)  # origem integer,
        valores.append(0)  # sinal integer,
        valores.append(nfce.nNF)  # numero character varying(20),
        valores.append(
            "Referente a NFCe nº {}".format(nfce.nNF)
        )  # historico character varying(255),
        valores.append(item.qCom)  # quantidade numeric(23,7),
        valores.append(item.vUnCom)  # valor numeric(20,6),
        valores.append(item.vProd + item.vOutro)  # valorqtd numeric(20,6),
        valores.append(None)  # precomedio numeric(20,6),
        valores.append(3)  # tipomovimento integer,
        valores.append(None)  # tipooperacao integer,
        valores.append(0)  # tipoestoque integer,
        valores.append(item.icms.vICMS)  # icms numeric(20,2),
        valores.append(ordem)  # ordem bigint,
        valores.append(None)  # codigomovimento integer,
        valores.append(
            str(item.idLocalDeEstoque) if item.idLocalDeEstoque is not None else None
        )  # localdeestoque uuid,
        valores.append(str(item.id_produto))  # id_item uuid,
        valores.append(
            str(uuid.uuid4())
        )  # id uuid NOT NULL DEFAULT uuid_generate_v4(),
        valores.append(None)  # devolucaode uuid,
        valores.append(None)  # id_itemordpro uuid,
        valores.append(None)  # id_ordpro uuid,
        valores.append(str(nfce.id))  # id_docfis uuid,
        valores.append(None)  # id_documento uuid,
        valores.append(str(item.id))  # id_itemdocfis uuid,
        valores.append(None)  # id_item_doc uuid,
        valores.append(str(nfce.id_emitente))  # id_estabelecimento uuid,
        valores.append(None)  # id_proprietario uuid,
        valores.append(
            str(nfce.destinatario.id)
            if ((nfce.destinatario is not None) and (nfce.destinatario.id is not None))
            else None
        )  # id_pessoa uuid,
        valores.append(None)  # id_rzcp uuid,
        valores.append(None)  # id_itemrzcf uuid,
        valores.append(None)  # id_itemlanfis uuid,
        valores.append(None)  # id_lanfis uuid,
        valores.append(slot)  # slot character varying(30),
        valores.append(None)  # tipodocumento smallint,
        valores.append(None)  # xml_docengine text,
        valores.append(
            str(nfce.operacaoCfopSlot.operacao)
            if (
                (nfce.operacaoCfopSlot is not None)
                and (nfce.operacaoCfopSlot.operacao is not None)
            )
            else None
        )  # operacao_id uuid,
        valores.append(item.CFOP)  # cfop character varying(30),
        valores.append(
            nfce.operacaoCfopSlot.codigo
            if (
                (nfce.operacaoCfopSlot is not None)
                and (nfce.operacaoCfopSlot.codigo is not None)
            )
            else None
        )  # operacao_codigo character varying(30),
        valores.append(
            nfce.operacaoCfopSlot.descricao
            if (
                (nfce.operacaoCfopSlot is not None)
                and (nfce.operacaoCfopSlot.descricao is not None)
            )
            else None
        )  # operacao_descricao character varying(150),
        valores.append(None)  # usuariocriacao character(50),
        valores.append(utilidades.now_brazil())  # datacriacao date,
        valores.append(None)  # id_transformacaoordemdeproducao uuid,
        valores.append(item.vProd + item.vOutro)  # valorqtdcusto numeric(20,2),
        valores.append(None)  # id_ra uuid,
        valores.append(None)  # id_producao_ordemdeproducao uuid,
        valores.append(None)  # id_transferencia uuid,
        valores.append(None)  # id_inventario uuid,
        valores.append(True)  # atualiza_saldoestoque boolean,
        valores.append(
            utilidades.now_brazil()
        )  # lastupdate timestamp without time zone DEFAULT now(),
        valores.append(None)  # id_itemdocfis_origem uuid,
        valores.append(None)  # saldo_pendente boolean,
        valores.append(False)  # afeta_customedio_ajuste boolean,
        valores.append(None)  # devolucaoalmoxarifado uuid,
        valores.append(False)  # afetacusto boolean DEFAULT false,
        valores.append(None)  # id_rcpe_direto uuid,
        valores.append(None)  # id_rcpe_ordem uuid,
        valores.append(None)  # id_rcpe_outros uuid,
        valores.append(None)  # id_rcpe_produto uuid,
        valores.append(False)  # perda_ganho boolean DEFAULT false,
        valores.append(
            utilidades.now_brazil()
        )  # data_criacao timestamp without time zone DEFAULT clock_timestamp(),
        valores.append(None)  # acertosaldoitem uuid,
        valores.append(False)  # zerar_saldo boolean DEFAULT false,
        valores.append(None)  # id_associacao uuid,
        valores.append(0)  # tenant bigint,
        return valores

    @staticmethod
    def obterListaValoresNFCeInutilizacao(nfce: NFCE) -> list:
        """
        retorna uma lista com os valores dos campos do objeto nfe
        Note: os nomes dos campos estão nos comentários
        """
        if nfce.id is None:
            nfce.id = uuid.uuid4()
        valores = list()
        valores.append(str(nfce.id))  # id
        valores.append(nfce.dhEmi.year)  # id_ano integer NOT NULL
        valores.append(0)  # sinal integer NOT NULL
        valores.append(0)  # tipo integer NOT NULL
        valores.append("NCE")  # modelo character varying(3) NOT NULL
        valores.append(nfce.serie)  # serie character varying(3)
        valores.append("-")  # subserie character varying(2)
        valores.append(nfce.nNFIni)  # numero character varying(15)
        valores.append(nfce.dhEmi.strftime("%Y") + "00")  # periodo integer NOT NULL
        valores.append(str(nfce.dhEmi))  # lancamento date
        valores.append(str(nfce.dhEmi))  # emissao date
        valores.append("5949")  # cfop character varying(9)
        valores.append(nfce.nNFFin)  # atenumero
        valores.append(25)  # situacao
        valores.append(5)  # situacaosped
        valores.append("Inutilizacao de numero homologado")  # observacao
        valores.append(100)  # percbaseinss
        valores.append(100)  # percbaseir
        valores.append(str(nfce.id_emitente))  # id_estabelecimento
        valores.append("00000000-0000-0000-0000-000000000000")  # id_emitente
        valores.append(0)  # origem
        valores.append(str(nfce.dhEmi))  # data_cancelamento
        valores.append(True)  # gera_financeiro
        valores.append(None)  # id_conjunto_anexo
        valores.append(1)  # status
        valores.append(
            utilidades.now_brazil()
        )  # lastupdate timestamp without time zone DEFAULT now()

        return valores

    @staticmethod
    def obterListaValoresNFCeInutilizacaoLanfis(nfce: NFCE) -> list:
        """
        retorna uma lista com os valores dos campos do objeto nfe
        Note: os nomes dos campos estão nos comentários
        """
        valores = list()
        valores.append(nfce.dhEmi.year)  # id_ano integer NOT NULL
        valores.append(0)  # tipo integer NOT NULL
        valores.append(str(nfce.dhEmi))  # lancamento date
        valores.append("NCE")  # modelo character varying(3) NOT NULL
        valores.append(nfce.serie)  # serie character varying(3)
        valores.append("-")  # subserie character varying(2)
        valores.append(nfce.nNFIni)  # numero character varying(15)
        valores.append("5949")  # cfop character varying(9)
        valores.append(str(nfce.dhEmi))  # emissao date
        valores.append(nfce.nNFFin)  # atenumero
        valores.append(True)  # cancelado
        valores.append(False)  # orgaopublico
        valores.append(False)  # retemiss
        valores.append(False)  # ipipresumido
        valores.append(utilidades.now_brazil())  # dataretiss data atual
        valores.append(str(nfce.dhEmi))  # datadedeclaracao
        valores.append(5)  # situacaosped
        valores.append(25)  # tipoiss
        valores.append("Inutilizacao de numero homologado")  # observacao
        valores.append(str(nfce.id))  # id_docfis
        valores.append(str(nfce.id_emitente))  # id_estabelecimento
        valores.append(str(nfce.dhEmi))  # data_cancelamento
        valores.append(
            utilidades.now_brazil()
        )  # lastupdate timestamp without time zone DEFAULT now()

        return valores

    @staticmethod
    def obterSQLMovimentoEstoque():
        return """ WITH valor(data, origem, sinal, numero, historico, quantidade, valor, valorqtd, precomedio, tipomovimento, 
            tipooperacao, tipoestoque, icms, ordem, codigomovimento, localdeestoque, id_item, id, devolucaode, id_itemordpro, 
            id_ordpro, id_docfis, id_documento, id_itemdocfis, id_item_doc, id_estabelecimento, id_proprietario, id_pessoa, 
            id_rzcp, id_itemrzcf, id_itemlanfis, id_lanfis, slot, tipodocumento, xml_docengine, operacao_id, cfop, 
            operacao_codigo, operacao_descricao, usuariocriacao, datacriacao, id_transformacaoordemdeproducao, valorqtdcusto, 
            id_ra, id_producao_ordemdeproducao, id_transferencia, id_inventario, atualiza_saldoestoque, lastupdate, 
            id_itemdocfis_origem, saldo_pendente, afeta_customedio_ajuste, devolucaoalmoxarifado, afetacusto, id_rcpe_direto, 
            id_rcpe_ordem, id_rcpe_outros, id_rcpe_produto, perda_ganho, data_criacao, acertosaldoitem, zerar_saldo, id_associacao, tenant) 
            AS (VALUES %s)
            INSERT INTO estoque.itens_mov(data, origem, sinal, numero, historico, quantidade, valor, valorqtd, precomedio, tipomovimento, 
            tipooperacao, tipoestoque, icms, ordem, codigomovimento, localdeestoque, id_item, id, devolucaode, id_itemordpro, 
            id_ordpro, id_docfis, id_documento, id_itemdocfis, id_item_doc, id_estabelecimento, id_proprietario, id_pessoa, id_rzcp, 
            id_itemrzcf, id_itemlanfis, id_lanfis, slot, tipodocumento, xml_docengine, operacao_id, cfop, operacao_codigo, operacao_descricao, 
            usuariocriacao, datacriacao, id_transformacaoordemdeproducao, valorqtdcusto, id_ra, id_producao_ordemdeproducao, id_transferencia, 
            id_inventario, atualiza_saldoestoque, lastupdate, id_itemdocfis_origem, saldo_pendente, afeta_customedio_ajuste, devolucaoalmoxarifado, 
            afetacusto, id_rcpe_direto, id_rcpe_ordem, id_rcpe_outros, id_rcpe_produto, perda_ganho, data_criacao, acertosaldoitem, zerar_saldo, 
            id_associacao, tenant)
            SELECT mov.data::date, mov.origem::integer, mov.sinal::integer, mov.numero, mov.historico, mov.quantidade::numeric, mov.valor::numeric, mov.valorqtd::numeric, 
            mov.precomedio::numeric, mov.tipomovimento::integer, mov.tipooperacao::integer, mov.tipoestoque::integer, mov.icms::numeric, mov.ordem::bigint, 
            mov.codigomovimento::integer, mov.localdeestoque::uuid, mov.id_item::uuid, mov.id::uuid, mov.devolucaode::uuid, mov.id_itemordpro::uuid, 
            mov.id_ordpro::uuid, mov.id_docfis::uuid, mov.id_documento::uuid, mov.id_itemdocfis::uuid, mov.id_item_doc::uuid, mov.id_estabelecimento::uuid, 
            mov.id_proprietario::uuid, mov.id_pessoa::uuid, mov.id_rzcp::uuid, mov.id_itemrzcf::uuid, mov.id_itemlanfis::uuid, mov.id_lanfis::uuid, mov.slot, 
            mov.tipodocumento::smallint, mov.xml_docengine, mov.operacao_id::uuid, mov.cfop, mov.operacao_codigo, mov.operacao_descricao, mov.usuariocriacao, 
            mov.datacriacao::date, mov.id_transformacaoordemdeproducao::uuid, mov.valorqtdcusto::numeric, mov.id_ra::uuid, mov.id_producao_ordemdeproducao::uuid, 
            mov.id_transferencia::uuid, mov.id_inventario::uuid, mov.atualiza_saldoestoque::boolean, mov.lastupdate::timestamp without time zone, mov.id_itemdocfis_origem::uuid, 
            mov.saldo_pendente::boolean, mov.afeta_customedio_ajuste::boolean, mov.devolucaoalmoxarifado::uuid, mov.afetacusto::boolean, mov.id_rcpe_direto::uuid, 
            mov.id_rcpe_ordem::uuid, mov.id_rcpe_outros::uuid, mov.id_rcpe_produto::uuid, mov.perda_ganho::boolean, mov.data_criacao::timestamp without time zone, 
            mov.acertosaldoitem::uuid, mov.zerar_saldo::boolean, mov.id_associacao::uuid, mov.tenant::bigint
            FROM valor mov
            WHERE EXISTS(SELECT 1 FROM ns.df_docfis doc WHERE mov.id_docfis::uuid = doc.id) """

    @staticmethod
    def obterListaValoresAjusteC197(
        nfe: NFCE, item: ItemNota, listaEstabelecimentos: list[Estabelecimento]
    ) -> list:
        valores = list()
        id = uuid.uuid4()
        valores.append(nfe.dhEmi.year)  # id_ano integer NOT NULL,
        valores.append(9)  # imposto integer NOT NULL,
        valores.append(nfe.dhEmi)  # data date NOT NULL,
        valores.append(13)  # tipo integer NOT NULL DEFAULT 0,
        valores.append(8)  # origem integer,
        valores.append(0)  # tiposped integer,
        valores.append(None)  # atividade integer,
        valores.append(20)  # natureza integer,
        valores.append(None)  # tipocalcpc integer,
        valores.append(None)  # origempc integer,
        valores.append(None)  # tppessoa integer,
        if nfe.mod == "65":
            valores.append("NCE")  # modelodoc character varying(3),
        else:
            valores.append(nfe.mod)  # modelodoc character varying(3),
        valores.append(None)  # tipodoc character varying(3),
        valores.append(nfe.serie)  # seriedoc character varying(3),
        valores.append(nfe.nNF)  # numerodoc character varying(15),
        valores.append(nfe.nNF)  # documentacao character varying(150),
        valores.append(None)  # complemento character varying(150),
        valores.append(None)  # codigogia character varying(20),
        valores.append(None)  # codigodarf character varying(6),
        if item.icms.CST == "51":
            valores.append("90980001")  # sped character varying(12),
        else:
            valores.append("90980000")  # sped character varying(12),
        valores.append(None)  # sped_pc character varying(12),
        valores.append(None)  # sped_out character varying(12),
        valores.append(item.nBenef)  # sped_detalhe character varying(12),
        valores.append(None)  # utilizacao character varying(12),
        valores.append(
            listaEstabelecimentos[nfe.identificadorEmitente].uf
        )  # uf character varying(2),
        valores.append(item.cBenef)  # descricao character varying(150),
        valores.append(None)  # debito character varying(16),
        valores.append(None)  # credito character varying(16),
        valores.append(None)  # debito2 character varying(16),
        valores.append(None)  # credito2 character varying(16),
        valores.append(item.CFOP)  # cotepe character varying(20),
        valores.append(None)  # anexo character varying(14),
        valores.append(item.vProd)  # base numeric(20,2),
        valores.append(item.icms.aliquotaICMSTotal)  # icms numeric(20,2),
        valores.append(None)  # valor numeric(20,2),
        valores.append(item.icms.vICMSDeson)  # outros numeric(20,2),
        valores.append(None)  # pis numeric(20,2),
        valores.append(None)  # cofins numeric(20,2),
        valores.append(None)  # evento bigint,
        valores.append(str(item.id_produto))  # id_item uuid,
        valores.append(str(nfe.id))  # id_docfis uuid,
        valores.append(str(nfe.id_emitente))  # id_estabelecimento uuid,
        if nfe.destinatario is not None and nfe.destinatario.id is not None:
            valores.append(str(nfe.destinatario.id))  # id_pessoa uuid,
        else:
            valores.append(None)
        valores.append(None)  # id_cancelamento uuid,
        valores.append(None)  # id_grec uuid,
        valores.append(str(id))  # id uuid NOT NULL DEFAULT uuid_generate_v4(),
        valores.append(None)  # id_obra uuid,
        valores.append(None)  # id_scp uuid,
        valores.append(None)  # id_lanfis uuid,
        valores.append(
            utilidades.now_brazil()
        )  # lastupdate timestamp without time zone DEFAULT now(),
        valores.append(None)  # tenant bigint,
        valores.append(None)  # tipo_ecf integer,
        valores.append(None)  # tipo_ecf_pcr integer,
        valores.append(None)  # tipo_ecf_din integer,
        valores.append(None)  # ecf_pcr character varying(60),
        valores.append(None)  # ecf_din character varying(60)
        return valores

    def AtualizaChaveRetornaId(self, nfce: NFCE):
        sql = " SELECT distinct id "
        sql += " FROM ns.df_docfis "
        sql += " WHERE id_estabelecimento = '" + str(nfce.id_emitente) + "'"
        sql += " AND id_ano = '" + str(nfce.dhEmi.year) + "'"
        sql += " AND sinal = 0 "
        sql += " AND tipo = 0 "
        sql += " AND modelo = 'NCE' "
        sql += " AND serie = '" + str(nfce.serie) + "'"
        sql += " AND subserie = '-' "
        sql += " AND numero = '" + str(nfce.nNF) + "'"
        sql += " AND periodo = " + nfce.dhEmi.strftime("%Y") + "00"
        sql += " AND COALESCE(chavene, '') = '' "
        sql += " LIMIT 1 "

        ids_Notas = UtilidadesBanco.executarConsulta(self.__conexao, sql, True, None)

        if ids_Notas != []:
            for id_nota in ids_Notas:
                self.AtualizaChave(id_nota, nfce)
                return id_nota["id"]
        else:
            return None

    def AtualizaChave(self, nota_id, nota: NFCE):
        sql = "UPDATE ns.df_docfis "
        sql += " Set chavene = '" + str(nota.chNFe) + "'"
        sql += ", chaveneini = '" + str(nota.chNFe[0:34]) + "'"
        sql += ", chavene01 = '" + str(nota.chNFe[0:6]) + "'"
        sql += ", chavene02 = '" + str(nota.chNFe[6:20]) + "'"
        sql += ", chavene03 = '" + str(nota.chNFe[20:25]) + "'"
        sql += ", chavene04 = '" + str(nota.chNFe[25:34]) + "'"
        sql += ", chavenefim = '" + str(nota.chNFe[34:44]) + "'"
        sql += " WHERE id = '" + str(nota_id["id"]) + "'"

        UtilidadesBanco.executarComando(self.__conexao, sql, None, False, True)

    def NotaExistente(self, nfce: NFCE):
        sql = " SELECT id "
        sql += " FROM ns.df_docfis "
        sql += " WHERE id = '" + str(nfce.id) + "'"

        ids_Notas = UtilidadesBanco.executarConsulta(self.__conexao, sql, True, None)

        if ids_Notas != []:
            return True
        else:
            return False

    def AjustaChave(self, nfce: NFCE):
        nfce.id = self.AtualizaChaveRetornaId(self, nfce)
