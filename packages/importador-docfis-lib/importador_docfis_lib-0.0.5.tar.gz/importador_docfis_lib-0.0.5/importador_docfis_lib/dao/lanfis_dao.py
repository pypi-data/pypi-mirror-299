from typing import List
from uuid import UUID

from importador_docfis_lib.dto_handler.nfce import NFCE
from importador_docfis_lib.utils import utilidades
from importador_docfis_lib.utils.lanfis import Lanfis


class LanfisDAO:
    """ Classe de Domínio para Lançamento Fiscal """

    @staticmethod
    def obterSQLInsertLanFis() -> str:
        """ Retorna o comando SQL para Insert na tabela scritta.lf_lanfis """
        return """ WITH valor(id_ano, tipo, datalanc, modelo, serie, subserie, numero, aliquota, origem, cfop, emissao, atenumero, 
                    tppessoa, cancelado, orgaopublico, retemiss, retemir, reteminss, ipipresumido, dataretiss, datadeclaracao, 
                    situacaosped, versao, crt, tipoicms, tipoipi, tipoiss, observacao, obsestoque, codmunic, declaracaoimportacao, 
                    codigodip, codigoirrf, codigopis, codigocsll, codigocofins, valorcontabil, baseicms, valoricms, isentasicms, 
                    outrasicms, baseicmsdif, icmsnaocred, reducaobaseicms, diferencialicms, antecipacaoicms, valoradic, 
                    basest, valorstprop, valorstterc, valorstnaoret, valorstpis, valorstcofins, baseipi, valoripi, isentasipi, 
                    outrasipi, ipinaocred, baseiss, valoriss, isentasiss, outrasiss, issoutromunic, materiais, subempreitada, 
                    outrasdeducoes, valorcide, valordescontos, descnaotrib, frete, seguro, outrasdespesas, baseinss, baseir, 
                    basecsll, basepis, basecofins, inssretido, irretido, csllretido, pisretido, cofinsretido, 
                    deducaoir, deducaocsll, deducaopis, deducaocofins, id_docfis, id_estabelecimento, id_pessoa, id_ecf, 
                    id_redz, id, id_obra, id_grupodiferenciado, id_scp, vinculoreceita, vicmsufdest, vicmsufremet, 
                    vfcpufdest, chavegold_docfis, outras_retencoes, obs_outras_retencoes, valorcontabilpis, valorcontabilcofins, 
                    data_cancelamento, vfcp, vbcfcp, vbcfcpst, vfcpst, vfcpstret, vbcfcpufdest, vbcfcpstret, lastupdate, tenant)
                    AS (VALUES %s)
                    INSERT INTO scritta.lf_lanfis(id_ano, tipo, datalanc, modelo, serie, subserie, numero, aliquota, origem, cfop, emissao, atenumero, 
                    tppessoa, cancelado, orgaopublico, retemiss, retemir, reteminss, ipipresumido, dataretiss, datadeclaracao, 
                    situacaosped, versao, crt, tipoicms, tipoipi, tipoiss, observacao, obsestoque, codmunic, declaracaoimportacao, 
                    codigodip, codigoirrf, codigopis, codigocsll, codigocofins, valorcontabil, baseicms, valoricms, isentasicms, 
                    outrasicms, baseicmsdif, icmsnaocred, reducaobaseicms, diferencialicms, antecipacaoicms, valoradic, 
                    basest, valorstprop, valorstterc, valorstnaoret, valorstpis, valorstcofins, baseipi, valoripi, isentasipi, 
                    outrasipi, ipinaocred, baseiss, valoriss, isentasiss, outrasiss, issoutromunic, materiais, subempreitada, 
                    outrasdeducoes, valorcide, valordescontos, descnaotrib, frete, seguro, outrasdespesas, baseinss, baseir, 
                    basecsll, basepis, basecofins, inssretido, irretido, csllretido, pisretido, cofinsretido, 
                    deducaoir, deducaocsll, deducaopis, deducaocofins, id_docfis, id_estabelecimento, id_pessoa, id_ecf, 
                    id_redz, id, id_obra, id_grupodiferenciado, id_scp, vinculoreceita, vicmsufdest, vicmsufremet, 
                    vfcpufdest, chavegold_docfis, outras_retencoes, obs_outras_retencoes, valorcontabilpis, valorcontabilcofins, 
                    data_cancelamento, vfcp, vbcfcp, vbcfcpst, vfcpst, vfcpstret, vbcfcpufdest, vbcfcpstret, lastupdate, tenant)
                    SELECT lan.id_ano::integer, lan.tipo::integer, lan.datalanc::date, lan.modelo, lan.serie, lan.subserie, lan.numero, lan.aliquota::numeric, 
                    lan.origem::integer, lan.cfop, lan.emissao::date, lan.atenumero, lan.tppessoa::integer, lan.cancelado::boolean, lan.orgaopublico::boolean, 
                    lan.retemiss::boolean, lan.retemir::boolean, lan.reteminss::boolean, lan.ipipresumido::boolean, lan.dataretiss::date, lan.datadeclaracao::date, 
                    lan.situacaosped::integer, lan.versao::integer, lan.crt::integer, lan.tipoicms::integer, lan.tipoipi::integer, lan.tipoiss::integer, 
                    lan.observacao, lan.obsestoque, lan.codmunic, lan.declaracaoimportacao, lan.codigodip, lan.codigoirrf, lan.codigopis, lan.codigocsll, 
                    lan.codigocofins, lan.valorcontabil::numeric, lan.baseicms::numeric, lan.valoricms::numeric, lan.isentasicms::numeric, lan.outrasicms::numeric, 
                    lan.baseicmsdif::numeric, lan.icmsnaocred::numeric, lan.reducaobaseicms::numeric, lan.diferencialicms::numeric, lan.antecipacaoicms::numeric, 
                    lan.valoradic::numeric, lan.basest::numeric, lan.valorstprop::numeric, lan.valorstterc::numeric, lan.valorstnaoret::numeric, lan.valorstpis::numeric, 
                    lan.valorstcofins::numeric, lan.baseipi::numeric, lan.valoripi::numeric, lan.isentasipi::numeric, lan.outrasipi::numeric, lan.ipinaocred::numeric, 
                    lan.baseiss::numeric, lan.valoriss::numeric, lan.isentasiss::numeric, lan.outrasiss::numeric, lan.issoutromunic::numeric, lan.materiais::numeric, 
                    lan.subempreitada::numeric, lan.outrasdeducoes::numeric, lan.valorcide::numeric, lan.valordescontos::numeric, lan.descnaotrib::numeric, 
                    lan.frete::numeric, lan.seguro::numeric, lan.outrasdespesas::numeric, lan.baseinss::numeric, lan.baseir::numeric, lan.basecsll::numeric, 
                    lan.basepis::numeric, lan.basecofins::numeric, lan.inssretido::numeric, lan.irretido::numeric, lan.csllretido::numeric, lan.pisretido::numeric, 
                    lan.cofinsretido::numeric, lan.deducaoir::numeric, lan.deducaocsll::numeric, lan.deducaopis::numeric, lan.deducaocofins::numeric, lan.id_docfis::uuid, 
                    lan.id_estabelecimento::uuid, lan.id_pessoa::uuid, lan.id_ecf::uuid, lan.id_redz::uuid, lan.id::uuid, lan.id_obra::uuid, 
                    lan.id_grupodiferenciado::uuid, lan.id_scp::uuid, lan.vinculoreceita::integer, lan.vicmsufdest::numeric, lan.vicmsufremet::numeric, 
                    lan.vfcpufdest::numeric, lan.chavegold_docfis, lan.outras_retencoes::numeric, lan.obs_outras_retencoes, 
                    lan.valorcontabilpis::numeric, lan.valorcontabilcofins::numeric, lan.data_cancelamento::date, lan.vfcp::numeric, 
                    lan.vbcfcp::numeric, lan.vbcfcpst::numeric, lan.vfcpst::numeric, lan.vfcpstret::numeric, lan.vbcfcpufdest::numeric, lan.vbcfcpstret::numeric, 
                    lan.lastupdate::timestamp without time zone, lan.tenant::bigint
                    FROM valor lan
                    WHERE EXISTS(SELECT 1 FROM ns.df_docfis doc WHERE lan.id_docfis::uuid = doc.id) """
                    
    # @staticmethod
    # def obterSQLInsertLanFisCTE() -> str:
    #     """ Retorna o comando SQL para Insert na tabela scritta.lf_lanfis """
        
    #     parametros = """id_estabelecimento, id_ano, tipo, modelo, datalanc, numero, aliquota, origem, id_docfis, emissao, 
    #     serie, subserie, cfop, cancelado, id_pessoa, situacaosped, tipoicms, atenumero, observacao, crt, codigodip, frete, seguro, outrasdespesas, 
    #     valordescontos, descnaotrib, basepis, basecofins, basecsll, baseir, valorcontabil, baseicms, valoricms, isentasicms, outrasicms, baseicmsdif, 
    #     reducaobaseicms, diferencialicms, antecipacaoicms, valoradic, basest, valorstprop, valorstterc, valorstnaoret, tipoipi, baseipi, valoripi, isentasipi, 
    #     outrasipi, ipinaocred, ipipresumido, tipoiss, codmunic, baseiss, valoriss, isentasiss, outrasiss, issoutromunic, materiais, subempreitada, outrasdeducoes, 
    #     reteminss, irretido, baseinss, inssretido, pisretido, cofinsretido, csllretido, orgaopublico, retemiss, dataretiss, datadeclaracao, vicmsufdest, vicmsufremet,
    #     vfcpufdest, vinculoreceita, valorcontabilpis, valorcontabilcofins, data_cancelamento, vbcfcp, vfcp, vbcfcpufdest, vbcfcpst, vfcpst, vbcfcpstret, vfcpstret, tppessoa"""
        
    #     return f""" INSERT INTO scritta.lf_lanfis({parametros})
    #                 VALUES %s """

    @staticmethod
    def obterListaValoresLanFisNFCe(nfe: NFCE, chaveLancamento: str, id: UUID) -> List:
        """
        Retorna os valores dos campos para insert na tabela scritta.lf_lanfis
        Args:
            nfe: Nota Fiscal
            chaveLancamento: Chave do Lancamento (concatenar CFOP + '|' + Alíquota ICMS + '|' + CST)
            id: Identificador do lançamento no Banco de Dados
        """
        valores = list()
        itens = Lanfis.filtrarItensDaNotaPorChaveDoLancamentoFiscal(nfe, chaveLancamento)
        valores.append(nfe.dhEmi.year)  # id_ano integer NOT NULL,
        valores.append(0)  # tipo integer NOT NULL,
        valores.append(nfe.dhEmi)  # datalanc date NOT NULL,
        valores.append("NCE")  # modelo character varying(3) NOT NULL,
        valores.append(nfe.serie)  # serie character varying(3) NOT NULL,
        valores.append("-")  # subserie character varying(2) NOT NULL,
        valores.append(nfe.nNF)  # numero character varying(15) NOT NULL,
        valores.append(itens[0].icms.aliquotaICMSTotal)  # aliquota numeric(20,2),
        valores.append(0)  # origem integer,
        valores.append(itens[0].CFOP)  # cfop character varying(9),
        valores.append(nfe.dhEmi)  # emissao date NOT NULL,
        valores.append(nfe.nNF)  # atenumero character varying(9),
        valores.append(None)  # tppessoa integer,
        valores.append(False)  # cancelado boolean,
        valores.append(False)  # orgaopublico boolean,
        valores.append(False)  # retemiss boolean,
        valores.append(False)  # retemir boolean,
        valores.append(False)  # reteminss boolean,
        valores.append(False)  # ipipresumido boolean,
        valores.append(None)  # dataretiss date,
        valores.append(None)  # datadeclaracao date,
        valores.append(0)  # situacaosped integer,
        valores.append(4)  # versao integer,
        valores.append(3)  # crt integer,
        valores.append('1' + str(itens[0].icms.orig) + str(itens[0].icms.CST))  # tipoicms integer
        valores.append(0)  # tipoipi integer,
        valores.append(2)  # tipoiss integer,
        valores.append(None)  # observacao character varying(255),
        valores.append(None)  # obsestoque character varying(255),
        valores.append(None)  # codmunic character varying(8),
        valores.append(None)  # declaracaoimportacao character varying(12),
        valores.append(None)  # codigodip character varying(3),
        valores.append(None)  # codigoirrf character varying(6),
        valores.append(None)  # codigopis character varying(6),
        valores.append(None)  # codigocsll character varying(6),
        valores.append(None)  # codigocofins character varying(6),
        valores.append(sum([item.valorContabil for item in itens]))  # valorcontabil numeric(20,2),
        valores.append(sum([item.icms.vBC for item in itens]))  # baseicms numeric(20,2),
        valores.append(sum([item.icms.vICMS + item.icms.vFCP for item in itens]))  # valoricms numeric(20,2),
        valores.append(
            sum([item.icms.retornarIsentasICMS(item.valorContabil) for item in itens]))  # isentasicms numeric(20,2),
        valores.append(
            sum([item.icms.retornar_outras_icms(item.valorContabil) for item in itens]))  # outrasicms numeric(20,2),
        valores.append(0)  # baseicmsdif numeric(20,2),
        valores.append(0)  # icmsnaocred numeric(20,2),
        valores.append(0)  # reducaobaseicms numeric(20,2),
        valores.append(0)  # diferencialicms numeric(20,2),
        valores.append(0)  # antecipacaoicms numeric(20,2),
        valores.append(0)  # valoradic numeric(20,2),
        valores.append(0)  # basest numeric(20,2),
        valores.append(0)  # valorstprop numeric(20,2),
        valores.append(0)  # valorstterc numeric(20,2),
        valores.append(0)  # valorstnaoret numeric(20,2),
        valores.append(0)  # valorstpis numeric(20,2),
        valores.append(0)  # valorstcofins numeric(20,2),
        valores.append(0)  # baseipi numeric(20,2),
        valores.append(0)  # valoripi numeric(20,2),
        valores.append(0)  # isentasipi numeric(20,2),
        valores.append(0)  # outrasipi numeric(20,2),
        valores.append(0)  # ipinaocred numeric(20,2),
        valores.append(0)  # baseiss numeric(20,2),
        valores.append(0)  # valoriss numeric(20,2),
        valores.append(0)  # isentasiss numeric(20,2),
        valores.append(0)  # outrasiss numeric(20,2),
        valores.append(0)  # issoutromunic numeric(20,2),
        valores.append(0)  # materiais numeric(20,2),
        valores.append(0)  # subempreitada numeric(20,2),
        valores.append(0)  # outrasdeducoes numeric(20,2),
        valores.append(0)  # valorcide numeric(20,2),
        valores.append(0)  # valordescontos numeric(20,2),
        valores.append(sum(item.icms.vICMSDeson for item in itens))  # descnaotrib numeric(20,2),
        valores.append(0)  # frete numeric(20,2),
        valores.append(0)  # seguro numeric(20,2),
        valores.append(sum([item.vOutro for item in itens]))  # outrasdespesas numeric(20,2),
        valores.append(None)  # baseinss numeric(20,2),
        valores.append(None)  # baseir numeric(20,2),
        valores.append(None)  # basecsll numeric(20,2),
        valores.append(None)  # basepis numeric(20,2),
        valores.append(None)  # basecofins numeric(20,2),
        valores.append(0)  # inssretido numeric(20,2),
        valores.append(0)  # irretido numeric(20,2),
        valores.append(0)  # csllretido numeric(20,2),
        valores.append(0)  # pisretido numeric(20,2),
        valores.append(0)  # cofinsretido numeric(20,2),
        valores.append(0)  # deducaoir numeric(20,2),
        valores.append(0)  # deducaocsll numeric(20,2),
        valores.append(0)  # deducaopis numeric(20,2),
        valores.append(0)  # deducaocofins numeric(20,2),
        valores.append(str(nfe.id))  # id_docfis uuid,
        valores.append(str(nfe.id_emitente))  # id_estabelecimento uuid,
        if nfe.destinatario.id is not None:
            valores.append(str(nfe.destinatario.id))  # id_pessoa uuid,
        else:
            valores.append(None)
        valores.append(None)  # id_ecf uuid,
        valores.append(None)  # id_redz uuid,
        valores.append(str(id))  # id uuid NOT NULL DEFAULT uuid_generate_v4(),
        valores.append(None)  # id_obra uuid,
        valores.append(None)  # id_grupodiferenciado uuid,
        valores.append(None)  # id_scp uuid,
        valores.append(None)  # vinculoreceita integer,
        valores.append(None)  # vicmsufdest numeric(20,2),
        valores.append(None)  # vicmsufremet numeric(20,2),
        valores.append(0)  # vfcpufdest numeric(20,2),
        valores.append(None)  # chavegold_docfis text,
        valores.append(None)  # outras_retencoes numeric(20,2) DEFAULT 0,
        valores.append(None)  # obs_outras_retencoes character varying(200) DEFAULT NULL::character varying,
        valores.append(
            nfe.pis.vPIS
            if nfe.pis.vPIS > 0
            else sum([item.pis.vPIS for item in nfe.lista_itens])
        )  # valorcontabilpis numeric(20,2) NOT NULL DEFAULT 0.00,
        valores.append(
            nfe.cofins.vCOFINS
            if nfe.cofins.vCOFINS > 0
            else sum([item.cofins.vCOFINS for item in nfe.lista_itens])
        )  # valorcontabilcofins numeric(20,2) NOT NULL DEFAULT 0.00,
        valores.append(None)  # data_cancelamento date,
        valores.append(sum([item.icms.vFCP for item in itens]))  # vfcp numeric(15,2),
        valores.append(sum([item.icms.vBC for item in itens]))  # vbcfcp numeric(15,2),
        valores.append(None)  # vbcfcpst numeric(15,2),
        valores.append(None)  # vfcpst numeric(15,2),
        valores.append(None)  # vfcpstret numeric(15,2),
        valores.append(None)  # vbcfcpufdest numeric(15,2),
        valores.append(None)  # vbcfcpstret numeric(15,2),
        valores.append(utilidades.now_brazil())  # lastupdate timestamp without time zone,
        valores.append(None)  # tenant bigint,
        return valores

    # @staticmethod
    # def obterListaValoresLanFisNFeEntrada(nfe: NFCE, chaveLancamento: str, id: UUID) -> List:
    #     """
    #     Retorna os valores dos campos para insert na tabela scritta.lf_lanfis
    #     Args:
    #         nfe: Nota Fiscal
    #         chaveLancamento: Chave do Lancamento (concatenar CFOP + '|' + Alíquota ICMS + '|' + CST)
    #         id: Identificador do lançamento no Banco de Dados
    #     """
    #     valores = list()
    #     itens = Lanfis.filtrarItensDaNotaPorChaveDoLancamentoFiscal(nfe, chaveLancamento)
    #     valores.append(nfe.dhEmi.year)  # id_ano integer NOT NULL,
    #     valores.append(0)  # tipo integer NOT NULL,
    #     valores.append(nfe.dhEmi)  # datalanc date NOT NULL,
    #     valores.append("NCE")  # modelo character varying(3) NOT NULL,
    #     valores.append(nfe.serie)  # serie character varying(3) NOT NULL,
    #     valores.append("-")  # subserie character varying(2) NOT NULL,
    #     valores.append(nfe.nNF)  # numero character varying(15) NOT NULL,
    #     valores.append(itens[0].icms.aliquotaICMSTotal)  # aliquota numeric(20,2),
    #     valores.append(0)  # origem integer,
    #     valores.append(itens[0].CFOP)  # cfop character varying(9),
    #     valores.append(nfe.dhEmi)  # emissao date NOT NULL,
    #     valores.append(nfe.nNF)  # atenumero character varying(9),
    #     valores.append(None)  # tppessoa integer,
    #     valores.append(False)  # cancelado boolean,
    #     valores.append(False)  # orgaopublico boolean,
    #     valores.append(False)  # retemiss boolean,
    #     valores.append(False)  # retemir boolean,
    #     valores.append(False)  # reteminss boolean,
    #     valores.append(False)  # ipipresumido boolean,
    #     valores.append(None)  # dataretiss date,
    #     valores.append(None)  # datadeclaracao date,
    #     valores.append(0)  # situacaosped integer,
    #     valores.append(4)  # versao integer,
    #     valores.append(3)  # crt integer,
    #     valores.append('1' + str(itens[0].icms.orig) + str(itens[0].icms.CST))  # tipoicms integer
    #     valores.append(0)  # tipoipi integer,
    #     valores.append(2)  # tipoiss integer,
    #     valores.append(None)  # observacao character varying(255),
    #     valores.append(None)  # obsestoque character varying(255),
    #     valores.append(None)  # codmunic character varying(8),
    #     valores.append(None)  # declaracaoimportacao character varying(12),
    #     valores.append(None)  # codigodip character varying(3),
    #     valores.append(None)  # codigoirrf character varying(6),
    #     valores.append(None)  # codigopis character varying(6),
    #     valores.append(None)  # codigocsll character varying(6),
    #     valores.append(None)  # codigocofins character varying(6),
    #     valores.append(sum([item.valorContabil for item in itens]))  # valorcontabil numeric(20,2),
    #     valores.append(sum([item.icms.vBC for item in itens]))  # baseicms numeric(20,2),
    #     valores.append(sum([item.icms.vICMS + item.icms.vFCP for item in itens]))  # valoricms numeric(20,2),
    #     valores.append(
    #         sum([item.icms.retornarIsentasICMS(item.valorContabil) for item in itens]))  # isentasicms numeric(20,2),
    #     valores.append(
    #         sum([item.icms.retornarOutrasICMS(item.valorContabil) for item in itens]))  # outrasicms numeric(20,2),
    #     valores.append(0)  # baseicmsdif numeric(20,2),
    #     valores.append(0)  # icmsnaocred numeric(20,2),
    #     valores.append(0)  # reducaobaseicms numeric(20,2),
    #     valores.append(0)  # diferencialicms numeric(20,2),
    #     valores.append(0)  # antecipacaoicms numeric(20,2),
    #     valores.append(0)  # valoradic numeric(20,2),
    #     valores.append(0)  # basest numeric(20,2),
    #     valores.append(0)  # valorstprop numeric(20,2),
    #     valores.append(0)  # valorstterc numeric(20,2),
    #     valores.append(0)  # valorstnaoret numeric(20,2),
    #     valores.append(0)  # valorstpis numeric(20,2),
    #     valores.append(0)  # valorstcofins numeric(20,2),
    #     valores.append(0)  # baseipi numeric(20,2),
    #     valores.append(0)  # valoripi numeric(20,2),
    #     valores.append(0)  # isentasipi numeric(20,2),
    #     valores.append(0)  # outrasipi numeric(20,2),
    #     valores.append(0)  # ipinaocred numeric(20,2),
    #     valores.append(0)  # baseiss numeric(20,2),
    #     valores.append(0)  # valoriss numeric(20,2),
    #     valores.append(0)  # isentasiss numeric(20,2),
    #     valores.append(0)  # outrasiss numeric(20,2),
    #     valores.append(0)  # issoutromunic numeric(20,2),
    #     valores.append(0)  # materiais numeric(20,2),
    #     valores.append(0)  # subempreitada numeric(20,2),
    #     valores.append(0)  # outrasdeducoes numeric(20,2),
    #     valores.append(0)  # valorcide numeric(20,2),
    #     valores.append(0)  # valordescontos numeric(20,2),
    #     valores.append(sum(item.icms.vICMSDeson for item in itens))  # descnaotrib numeric(20,2),
    #     valores.append(0)  # frete numeric(20,2),
    #     valores.append(0)  # seguro numeric(20,2),
    #     valores.append(sum([item.vOutro for item in itens]))  # outrasdespesas numeric(20,2),
    #     valores.append(None)  # baseinss numeric(20,2),
    #     valores.append(None)  # baseir numeric(20,2),
    #     valores.append(None)  # basecsll numeric(20,2),
    #     valores.append(None)  # basepis numeric(20,2),
    #     valores.append(None)  # basecofins numeric(20,2),
    #     valores.append(0)  # inssretido numeric(20,2),
    #     valores.append(0)  # irretido numeric(20,2),
    #     valores.append(0)  # csllretido numeric(20,2),
    #     valores.append(0)  # pisretido numeric(20,2),
    #     valores.append(0)  # cofinsretido numeric(20,2),
    #     valores.append(0)  # deducaoir numeric(20,2),
    #     valores.append(0)  # deducaocsll numeric(20,2),
    #     valores.append(0)  # deducaopis numeric(20,2),
    #     valores.append(0)  # deducaocofins numeric(20,2),
    #     valores.append(str(nfe.id))  # id_docfis uuid,
    #     valores.append(str(nfe.destinatario.id_estabelecimento))  # id_estabelecimento uuid,
    #     if nfe.emitente is not None:
    #         valores.append(str(nfe.emitente.id))  # id_pessoa uuid,
    #     else:
    #         valores.append(None)
    #     valores.append(None)  # id_ecf uuid,
    #     valores.append(None)  # id_redz uuid,
    #     valores.append(str(id))  # id uuid NOT NULL DEFAULT uuid_generate_v4(),
    #     valores.append(None)  # id_obra uuid,
    #     valores.append(None)  # id_grupodiferenciado uuid,
    #     valores.append(None)  # id_scp uuid,
    #     valores.append(None)  # vinculoreceita integer,
    #     valores.append(None)  # vicmsufdest numeric(20,2),
    #     valores.append(None)  # vicmsufremet numeric(20,2),
    #     valores.append(0)  # vfcpufdest numeric(20,2),
    #     valores.append(None)  # chavegold_docfis text,
    #     valores.append(None)  # outras_retencoes numeric(20,2) DEFAULT 0,
    #     valores.append(None)  # obs_outras_retencoes character varying(200) DEFAULT NULL::character varying,
    #     valores.append(
    #         nfe.pis.vPIS
    #         if nfe.pis.vPIS > 0
    #         else sum([item.pis.vPIS for item in nfe.listaItens])
    #     )  # valorcontabilpis numeric(20,2) NOT NULL DEFAULT 0.00,
    #     valores.append(
    #         nfe.cofins.vCOFINS
    #         if nfe.cofins.vCOFINS > 0
    #         else sum([item.cofins.vCOFINS for item in nfe.listaItens])
    #     )  # valorcontabilcofins numeric(20,2) NOT NULL DEFAULT 0.00,
    #     valores.append(None)  # data_cancelamento date,
    #     valores.append(sum([item.icms.vFCP for item in itens]))  # vfcp numeric(15,2),
    #     valores.append(sum([item.icms.vBC for item in itens]))  # vbcfcp numeric(15,2),
    #     valores.append(None)  # vbcfcpst numeric(15,2),
    #     valores.append(None)  # vfcpst numeric(15,2),
    #     valores.append(None)  # vfcpstret numeric(15,2),
    #     valores.append(None)  # vbcfcpufdest numeric(15,2),
    #     valores.append(None)  # vbcfcpstret numeric(15,2),
    #     valores.append(utilidades.now_brazil())  # lastupdate timestamp without time zone,
    #     valores.append(None)  # tenant bigint,
    #     return valores
    
    # @staticmethod
    # def obterListaValoresLanFisSAT(sat: SAT, chaveLancamento: str, id: UUID) -> List:
    #     """
    #     Retorna os valores dos campos para insert na tabela scritta.lf_lanfis
    #     Args:
    #         sat: Nota Fiscal
    #         chaveLancamento: Chave do Lancamento (concatenar CFOP + '|' + Alíquota ICMS + '|' + CST)
    #         id: Identificador do lançamento no Banco de Dados
    #     """
    #     valores = list()
    #     itens = Lanfis.filtrarItensDaNotaPorChaveDoLancamentoFiscal(sat, chaveLancamento)
    #     valores.append(sat.dEmi.year)  # id_ano integer NOT NULL,
    #     valores.append(0)  # tipo integer NOT NULL,
    #     valores.append(sat.dEmi)  # datalanc date NOT NULL,
    #     valores.append("SAT")  # modelo character varying(3) NOT NULL,
    #     valores.append(sat.numeroCaixa)  # serie character varying(3) NOT NULL,
    #     valores.append("-")  # subserie character varying(2) NOT NULL,
    #     valores.append(sat.nCFe)  # numero character varying(15) NOT NULL,
    #     valores.append(itens[0].icms.aliquotaICMSTotal)  # aliquota numeric(20,2),
    #     valores.append(0)  # origem integer,
    #     valores.append(itens[0].CFOP)  # cfop character varying(9),
    #     valores.append(sat.dEmi)  # emissao date NOT NULL,
    #     valores.append(sat.nCFe)  # atenumero character varying(9),
    #     valores.append(None)  # tppessoa integer,
    #     valores.append(False)  # cancelado boolean,
    #     valores.append(False)  # orgaopublico boolean,
    #     valores.append(False)  # retemiss boolean,
    #     valores.append(False)  # retemir boolean,
    #     valores.append(False)  # reteminss boolean,
    #     valores.append(False)  # ipipresumido boolean,
    #     valores.append(None)  # dataretiss date,
    #     valores.append(None)  # datadeclaracao date,
    #     valores.append(0)  # situacaosped integer,
    #     valores.append(4)  # versao integer,
    #     valores.append(3)  # crt integer,
    #     valores.append('1' + str(itens[0].icms.orig) + str(itens[0].icms.CST))  # tipoicms integer
    #     valores.append(0)  # tipoipi integer,
    #     valores.append(2)  # tipoiss integer,
    #     valores.append(None)  # observacao character varying(255),
    #     valores.append(None)  # obsestoque character varying(255),
    #     valores.append(None)  # codmunic character varying(8),
    #     valores.append(None)  # declaracaoimportacao character varying(12),
    #     valores.append(None)  # codigodip character varying(3),
    #     valores.append(None)  # codigoirrf character varying(6),
    #     valores.append(None)  # codigopis character varying(6),
    #     valores.append(None)  # codigocsll character varying(6),
    #     valores.append(None)  # codigocofins character varying(6),
    #     valores.append(sum([item.valorContabil for item in itens]))  # valorcontabil numeric(20,2),
    #     if ((itens[0].icms.aliquotaICMSTotal is not None) and (itens[0].icms.aliquotaICMSTotal > 0)):
    #         valores.append(sum([item.vProd for item in itens]))  # baseicms numeric(20,2),
    #     else:
    #         valores.append(0)  # baseicms numeric(20,2),
    #     valores.append(sum([item.icms.vICMS + item.icms.vFCP for item in itens]))  # valoricms numeric(20,2),
    #     valores.append(
    #         sum([item.icms.retornarIsentasICMS(item.valorContabil) for item in itens]))  # isentasicms numeric(20,2),
    #     valores.append(
    #         sum([item.icms.retornarOutrasICMS(item.valorContabil) for item in itens]))  # outrasicms numeric(20,2),
    #     valores.append(0)  # baseicmsdif numeric(20,2),
    #     valores.append(0)  # icmsnaocred numeric(20,2),
    #     valores.append(0)  # reducaobaseicms numeric(20,2),
    #     valores.append(0)  # diferencialicms numeric(20,2),
    #     valores.append(0)  # antecipacaoicms numeric(20,2),
    #     valores.append(0)  # valoradic numeric(20,2),
    #     valores.append(0)  # basest numeric(20,2),
    #     valores.append(0)  # valorstprop numeric(20,2),
    #     valores.append(0)  # valorstterc numeric(20,2),
    #     valores.append(0)  # valorstnaoret numeric(20,2),
    #     valores.append(0)  # valorstpis numeric(20,2),
    #     valores.append(0)  # valorstcofins numeric(20,2),
    #     valores.append(0)  # baseipi numeric(20,2),
    #     valores.append(0)  # valoripi numeric(20,2),
    #     valores.append(0)  # isentasipi numeric(20,2),
    #     valores.append(0)  # outrasipi numeric(20,2),
    #     valores.append(0)  # ipinaocred numeric(20,2),
    #     valores.append(0)  # baseiss numeric(20,2),
    #     valores.append(0)  # valoriss numeric(20,2),
    #     valores.append(0)  # isentasiss numeric(20,2),
    #     valores.append(0)  # outrasiss numeric(20,2),
    #     valores.append(0)  # issoutromunic numeric(20,2),
    #     valores.append(0)  # materiais numeric(20,2),
    #     valores.append(0)  # subempreitada numeric(20,2),
    #     valores.append(0)  # outrasdeducoes numeric(20,2),
    #     valores.append(0)  # valorcide numeric(20,2),
    #     valores.append(0)  # valordescontos numeric(20,2),
    #     valores.append(sum(item.icms.vICMSDeson for item in itens))  # descnaotrib numeric(20,2),
    #     valores.append(0)  # frete numeric(20,2),
    #     valores.append(0)  # seguro numeric(20,2),
    #     valores.append(sum([item.vOutro for item in itens]))  # outrasdespesas numeric(20,2),
    #     valores.append(None)  # baseinss numeric(20,2),
    #     valores.append(None)  # baseir numeric(20,2),
    #     valores.append(None)  # basecsll numeric(20,2),
    #     valores.append(None)  # basepis numeric(20,2),
    #     valores.append(None)  # basecofins numeric(20,2),
    #     valores.append(0)  # inssretido numeric(20,2),
    #     valores.append(0)  # irretido numeric(20,2),
    #     valores.append(0)  # csllretido numeric(20,2),
    #     valores.append(0)  # pisretido numeric(20,2),
    #     valores.append(0)  # cofinsretido numeric(20,2),
    #     valores.append(0)  # deducaoir numeric(20,2),
    #     valores.append(0)  # deducaocsll numeric(20,2),
    #     valores.append(0)  # deducaopis numeric(20,2),
    #     valores.append(0)  # deducaocofins numeric(20,2),
    #     valores.append(str(sat.id))  # id_docfis uuid,
    #     valores.append(str(sat.id_emitente))  # id_estabelecimento uuid,
    #     if sat.destinatario.id is not None:
    #         valores.append(str(sat.destinatario.id))  # id_pessoa uuid,
    #     else:
    #         valores.append(None)
    #     valores.append(None)  # id_ecf uuid,
    #     valores.append(None)  # id_redz uuid,
    #     valores.append(str(id))  # id uuid NOT NULL DEFAULT uuid_generate_v4(),
    #     valores.append(None)  # id_obra uuid,
    #     valores.append(None)  # id_grupodiferenciado uuid,
    #     valores.append(None)  # id_scp uuid,
    #     valores.append(None)  # vinculoreceita integer,
    #     valores.append(None)  # vicmsufdest numeric(20,2),
    #     valores.append(None)  # vicmsufremet numeric(20,2),
    #     valores.append(0)  # vfcpufdest numeric(20,2),
    #     valores.append(None)  # chavegold_docfis text,
    #     valores.append(None)  # outras_retencoes numeric(20,2) DEFAULT 0,
    #     valores.append(None)  # obs_outras_retencoes character varying(200) DEFAULT NULL::character varying,
    #     valores.append(
    #         sat.pis.vPIS
    #         if sat.pis.vPIS > 0
    #         else sum([item.pis.vPIS for item in sat.listaItens])
    #     )  # valorcontabilpis numeric(20,2) NOT NULL DEFAULT 0.00,
    #     valores.append(
    #         sat.cofins.vCOFINS
    #         if sat.cofins.vCOFINS > 0
    #         else sum([item.cofins.vCOFINS for item in sat.listaItens])
    #     )  # valorcontabilcofins numeric(20,2) NOT NULL DEFAULT 0.00,
    #     valores.append(None)  # data_cancelamento date,
    #     valores.append(sum([item.icms.vFCP for item in itens]))  # vfcp numeric(15,2),
    #     valores.append(sum([item.icms.vBC for item in itens]))  # vbcfcp numeric(15,2),
    #     valores.append(None)  # vbcfcpst numeric(15,2),
    #     valores.append(None)  # vfcpst numeric(15,2),
    #     valores.append(None)  # vfcpstret numeric(15,2),
    #     valores.append(None)  # vbcfcpufdest numeric(15,2),
    #     valores.append(None)  # vbcfcpstret numeric(15,2),
    #     valores.append(utilidades.now_brazil())  # lastupdate timestamp without time zone,
    #     valores.append(None)  # tenant bigint,
    #     return valores

    # @staticmethod
    # def obterListaValoresLanFisCTE(cte: CTE) -> List:
    #     """
    #     Retorna os valores dos campos para insert na tabela scritta.lf_lanfis
    #     Args:
    #         cte: CTE
    #         id: Identificador do lançamento no Banco de Dados
    #     """
    #     valores = list()
    #     valores.append(str(cte.estabelecimento.id))  # id_estabelecimento uuid,
    #     valores.append(cte.dhEmi.year)  # id_ano integer NOT NULL,
    #     valores.append(0)  # tipo integer NOT NULL,
    #     valores.append("CTE")  # modelo character varying(3) NOT NULL,
    #     valores.append(cte.dhEmi)  # datalanc date NOT NULL,
    #     valores.append(cte.nCT)  # numero character varying(15) NOT NULL,
    #     valores.append(cte.icms.pICMSOutraUF if cte.icms.pICMS == 0 and cte.icms.vBCOutraUF > 0 else cte.icms.pICMS)  # aliquota numeric(20,2),
    #     valores.append(3)  # origem integer,
    #     valores.append(str(cte.id))  # id_docfis uuid,
    #     valores.append(cte.dhEmi)  # emissao date NOT NULL,
    #     valores.append(cte.serie)  # serie character varying(3) NOT NULL,
    #     valores.append("-")  # subserie character varying(2) NOT NULL,
    #     valores.append(cte.CFOP)  # cfop character varying(9),
    #     valores.append(cte.cStat == '101')  # cancelado boolean,
    #     valores.append(str(cte.retornarIdPessoa()) if cte.retornarIdPessoa() is not None else None )  # id_pessoa uuid,
    #     valores.append(0)  # situacaosped integer,
    #     valores.append(1000 + int(cte.icms.CST))  # tipoicms integer
    #     valores.append(cte.nCT)  # atenumero character varying(9),
    #     valores.append('')  # observacao character varying(255),
    #     valores.append(0)  # crt integer,
    #     valores.append('2.3')  # codigodip character varying(3),
    #     valores.append(0)  # frete numeric(20,2),
    #     valores.append(0)  # seguro numeric(20,2),
    #     valores.append(0)  # outrasdespesas numeric(20,2),
    #     valores.append(0)  # valordescontos numeric(20,2),
    #     valores.append(0)  # descnaotrib numeric(20,2),
    #     valores.append(0)  # basepis numeric(20,2),
    #     valores.append(0)  # basecofins numeric(20,2),
    #     valores.append(0)  # basecsll numeric(20,2),
    #     valores.append(0)  # baseir numeric(20,2),
    #     valores.append(cte.vTPrest)  # valorcontabil numeric(20,2),
    #     valores.append(cte.icms.vBC)  # baseicms numeric(20,2),
    #     valores.append(cte.icms.vICMS)  # valoricms numeric(20,2),
    #     valores.append(cte.calcularIsentasICMS())  # isentasicms numeric(20,2),
    #     valores.append(cte.calcularOutrasICMS())  # outrasicms numeric(20,2),
    #     valores.append(0)  # baseicmsdif numeric(20,2),
    #     valores.append(cte.calcularIsentasICMS() if cte.icms.pRedBC > 0 else 0)  # reducaobaseicms numeric(20,2),
    #     valores.append(0)  # diferencialicms numeric(20,2),
    #     valores.append(0)  # antecipacaoicms numeric(20,2),
    #     valores.append(0)  # valoradic numeric(20,2),
    #     valores.append(0)  # basest numeric(20,2),
    #     valores.append(0)  # valorstprop numeric(20,2),
    #     valores.append(0)  # valorstterc numeric(20,2),
    #     valores.append(0)  # valorstnaoret numeric(20,2),
    #     valores.append(0)  # tipoipi integer,
    #     valores.append(0)  # baseipi numeric(20,2),
    #     valores.append(0)  # valoripi numeric(20,2),
    #     valores.append(cte.vTPrest if cte.estabelecimento.lanc_ipi == 0 else 0)  # isentasipi ajeitar numeric(20,2),
    #     valores.append(cte.vTPrest if cte.estabelecimento.lanc_ipi == 1 else 0)  # outrasipi numeric(20,2),
    #     valores.append(0)  # ipinaocred numeric(20,2),
    #     valores.append(False)  # ipipresumido boolean,
    #     valores.append(0)  # tipoiss integer,
    #     valores.append(cte.cMunIni)  # codmunic character varying(8),
    #     valores.append(0)  # baseiss numeric(20,2),
    #     valores.append(0)  # valoriss numeric(20,2),
    #     valores.append(0)  # isentasiss numeric(20,2),
    #     valores.append(0)  # outrasiss numeric(20,2),
    #     valores.append(0)  # issoutromunic numeric(20,2),
    #     valores.append(0)  # materiais numeric(20,2),
    #     valores.append(0)  # subempreitada numeric(20,2),
    #     valores.append(cte.pedagio)  # outrasdeducoes numeric(20,2),
    #     valores.append(False)  # reteminss boolean,
    #     valores.append(cte.vIR)  # irretido numeric(20,2),
    #     valores.append(0)  # baseinss numeric(20,2),
    #     valores.append(cte.vINSS)  # inssretido numeric(20,2),
    #     valores.append(cte.vPIS)  # pisretido numeric(20,2),
    #     valores.append(cte.vCOFINS)  # cofinsretido numeric(20,2),
    #     valores.append(cte.vCSLL)  # csllretido numeric(20,2),        
    #     valores.append(False)  # orgaopublico boolean,
    #     valores.append(False)  # retemiss boolean,
    #     valores.append(datetime.today())  # dataretiss date,
    #     valores.append(datetime.today())  # datadeclaracao date,
    #     valores.append(0)  # vicmsufdest numeric(20,2),
    #     valores.append(0)  # vicmsufremet numeric(20,2),
    #     valores.append(0)  # vfcpufdest numeric(20,2),
    #     valores.append(0)  # vinculoreceita integer,
    #     valores.append(cte.calcularPIS())  # valorcontabilpis numeric(20,2) NOT NULL DEFAULT 0.00,
    #     valores.append(cte.calcularCOFINS())  # valorcontabilcofins numeric(20,2) NOT NULL DEFAULT 0.00,
    #     valores.append(datetime.today())  # data_cancelamento date,
    #     valores.append(0)  # vbcfcp numeric(15,2),
    #     valores.append(0)  # vfcp numeric(15,2),
    #     valores.append(0)  # vbcfcpufdest numeric(15,2),
    #     valores.append(0)  # vbcfcpst numeric(15,2),
    #     valores.append(0)  # vfcpst numeric(15,2),
    #     valores.append(0)  # vbcfcpstret numeric(15,2),
    #     valores.append(0)  # vfcpstret numeric(15,2),
    #     valores.append(0)  # tppessoa integer,
    #     return valores

    # @staticmethod
    # def obterSQLInsertLanFisNFSE() -> str:
    #     """ Retorna o comando SQL para Insert na tabela scritta.lf_lanfis """
        
    #     parametros = """id, id_estabelecimento, id_ano, tipo, modelo, datalanc, numero, serie, subserie, aliquota, origem, id_docfis, emissao, 
    #     cfop, cancelado, id_pessoa, situacaosped, valorcontabil, codmunic, baseiss, valoriss, outrasiss, issoutromunic, isentasiss, outrasdeducoes, 
    #     outrasdespesas, reteminss, irretido, inssretido, pisretido, cofinsretido, csllretido, valorcontabilpis, valorcontabilcofins, retemiss, data_cancelamento,observacao """
        
    #     return f""" INSERT INTO scritta.lf_lanfis({parametros})
    #                 VALUES %s """
                    
    # @staticmethod
    # def obterSQLCancelarLanFisNFSE() -> str:
    #     """ Retorna o comando SQL para cancelar na tabela scritta.lf_lanfis """

    #     return """UPDATE scritta.lf_lanfis as lf SET cancelado = True, situacaosped = 4, data_cancelamento = data.data_cancelamento
    #                FROM (VALUES %s) AS data (id, data_cancelamento) WHERE lf.id = data.id::uuid"""
                    
    # @staticmethod
    # def obterListaValoresLanFisNFSE(nfse: NFSE) -> List:
    #     """
    #     Retorna os valores dos campos para insert na tabela scritta.lf_lanfis
    #     Args:
    #         cte: CTE
    #         id: Identificador do lançamento no Banco de Dados
    #     """
    #     valores = list()
    #     valores.append(str(nfse.id_lanfis))  # id uuid,
    #     valores.append(str(nfse.estabelecimento.id))  # id_estabelecimento uuid,
    #     valores.append(nfse.emissao.year)  # id_ano integer NOT NULL,
    #     valores.append(4 if nfse.entrada else 3)  # tipo integer NOT NULL,
    #     valores.append("NES")  # modelo character varying(3) NOT NULL,
    #     valores.append(nfse.emissao_rps if nfse.emissao_rps is not None and nfse.saida else nfse.emissao)  # datalanc date NOT NULL,
    #     valores.append(nfse.numero)  # numero character varying(15) NOT NULL,
    #     valores.append("")  # serie character varying(3) NOT NULL,
    #     valores.append("")  # subserie character varying(2) NOT NULL,
    #     valores.append(nfse.aliquota)  # aliquota numeric(20,2),
    #     valores.append(5)  # origem integer,
    #     valores.append(str(nfse.id))  # id_docfis uuid,
    #     valores.append(nfse.emissao)  # emissao date NOT NULL,
    #     valores.append(nfse.cfop_servico)  # cfop character varying(9),
    #     valores.append(nfse.cancelado)  # cancelado boolean,
    #     valores.append(str(nfse.prestador.id) if nfse.entrada else (str(nfse.tomador.id) if nfse.tomador is not None else None) )  # id_pessoa uuid,
    #     valores.append(0 if nfse.retornarSituacaoDocfis() == 2 else 4)  # situacaosped integer,
    #     valores.append(nfse.servicos)  # valorcontabil numeric(20,2),
    #     valores.append(nfse.municipio_prestacao if nfse.municipio_prestacao != "" and nfse.municipio_prestacao != "3550308" else None)  # codmunic character varying(8),
    #     if nfse.situacao == 'F':
    #         valores.append(0)  # baseiss numeric(20,2),
    #         valores.append(0)  # valoriss numeric(20,2),
    #         valores.append(nfse.servicos - nfse.deducoes)  # outrasiss numeric(20,2),
    #         valores.append(nfse.ISS)  # issoutromunic numeric(20,2),
    #     else:
    #         valores.append(0 if nfse.isento else (nfse.servicos - nfse.deducoes))  # baseiss numeric(20,2),
    #         valores.append(nfse.ISS)  # valoriss numeric(20,2),
    #         valores.append(0)  # outrasiss numeric(20,2),
    #         valores.append(0)  # issoutromunic numeric(20,2),
    #     valores.append((nfse.servicos - nfse.deducoes) if nfse.isento else 0)  # isentasiss numeric(20,2),
    #     valores.append(nfse.deducoes)  # outrasdeducoes numeric(20,2),
    #     valores.append(nfse.recebido - nfse.servicos)  # outrasdespesas numeric(20,2),
    #     valores.append(nfse.INSS > 0)  # reteminss boolean,
    #     valores.append(nfse.IR)  # irretido numeric(20,2),
    #     valores.append(nfse.INSS)  # inssretido numeric(20,2),
    #     valores.append(nfse.PIS)  # pisretido numeric(20,2),
    #     valores.append(nfse.COFINS)  # cofinsretido numeric(20,2),
    #     valores.append(nfse.CSLL)  # csllretido numeric(20,2),  
    #     valores.append(nfse.calcularPIS())  # valorcontabilpis numeric(20,2),
    #     valores.append(nfse.calcularCOFINS())  # valorcontabilcofins numeric(20,2),
    #     valores.append(nfse.retemISS)  # retemiss boolean,
    #     valores.append(nfse.data_cancelamento)  # data_cancelamento date,
    #     valores.append(nfse.observacao)  # observacao date,
    #     return valores
    
    # @staticmethod
    # def obterListaValoresCancelamentoLanFisNFSE(nfse: NFSE) -> List:
    #     """
    #     Retorna os valores dos campos para insert na tabela scritta.lf_lanfis
    #     Args:
    #         cte: CTE
    #         id: Identificador do lançamento no Banco de Dados
    #     """
    #     valores = list()
    #     valores.append(str(nfse.id_lanfis))  # id uuid,
    #     valores.append(nfse.data_cancelamento)  # data_cancelamento date,
        
    #     return valores
    
    # @staticmethod
    # def obterSQLInsertLanServicosNFSE() -> str:
    #     """ Retorna o comando SQL para Insert na tabela scritta.lf_servicos """
        
    #     parametros = """id_ano, id_lanfis, ordem, descricao, id_servico, tipo, quantidade, valor, baseiss, unidade"""
        
    #     return f""" INSERT INTO scritta.lf_servicos({parametros})
    #                 VALUES %s """
                    
    # @staticmethod
    # def obterListaValoresLanServicosNFSE(tipo, valor, nfse: NFSE) -> List:
    #     """
    #     Retorna os valores dos campos para insert na tabela scritta.lf_servicos
    #     """
    #     valores = list()
    #     valores.append(nfse.emissao.year)  # id_ano integer,
    #     valores.append(str(nfse.id_lanfis))  # id_lanfis uuid,
    #     valores.append(nfse.ordem) # ordem
    #     valores.append(nfse.descricao) # descricao
    #     valores.append(str(nfse.servicos_ids[tipo])) # id_servico
    #     valores.append(tipo) # tipo
    #     valores.append(1) # quantidade
    #     valores.append(valor) # valor
    #     valores.append(0 if nfse.isento else valor) # baseiss
    #     valores.append("UND") # unidade
        
    #     return valores