import uuid
from typing import List
from uuid import UUID

from importador_docfis_lib.dto_handler.item_nota import ItemNota
from importador_docfis_lib.utils import utilidades


class ItemNotaDAO:
    """Classe de Domínio para Lançamento Fiscal"""

    @staticmethod
    def obterSQLInsertDf_Itens() -> str:
        """Retorna o comando SQL para insert na tabela ns.df_itens"""
        return """WITH valor(id_ano, especificacao, cfop, unidade, tiposoma, classe, tiporec, ignorasoma, vinculoreceita, semmov, 
                    unitario, quantidade, frete, seguro, despesas, desconto, descnaotrib, valor, lote, quantlote, fabricacao, validade, 
                    precomax, remas, tanque, bico, cide, basecide, valorcide, valoriof, pesoliq, pesobruto, capacidade, volumes, impexp, 
                    valorimpexp, acdraw, cst_icms, csosn, icmsorigem, icmsdestino, encargosicms, reducaoicms, baseicms, valoricms, diferencial, 
                    antecipacao, icmsdiferido, abatimentoicms, valorciap, mesesciap, tipoipi, tiposomaipi, ipi, reducaoipi, encargosipi, 
                    baseipi, valoripi, abatimentoipi, ipisemcred, seloipi, lacrepi, lucro, tipost, reducaost, basestfixa, basesubst, substtribprop, 
                    substtribterc, substnaoretida, substobs, tipo_pc, pisimp, cofinsimp, basepisimp, basecofinsimp, valorpisimp, valorcofinsimp, 
                    basestpis, basestcofins, valorstpis, valorstcofins, ordem, id_item, id_docfis, id, id_proprietario, id_receptor, id_obra, 
                    tipo_linha, id_linha, id_vendedor, ipienquadramentocodigo, ipienquadramentodescricao, cest, valorpercentualfcpicmsdestino, 
                    valoraliquotainternaicmsdestino, valorpercentualpartilhaicmsdestino, valorfcpicmsdestino, valoricmsdestino, valoricmsinterestadualorigem, 
                    valorpercentualicmsinter, valorcontabilpis, valorcontabilcofins, situacaogerencial, chavegold, valordebitopis, valordebitocofins, 
                    id_localestoque, linha_pendente, custototal, percentualfatorcomissao, percentualcomissao, pfcp, vfcp, vbcfcp, vbcfcpst, 
                    pfcpst, vfcpst, pfcpstret, vfcpstret, vbcfcpufdest, vbcfcpstret, pst, valorcustosextra, predbcefet, picmsefet, vbcefet, vicmsefet, 
                    lastupdate, tenant, motdesicms, tipi, origem, cbenef, nbenef)
                    AS (VALUES %s)
                    INSERT INTO ns.df_itens(id_ano, especificacao, cfop, unidade, tiposoma, classe, tiporec, ignorasoma, vinculoreceita, semmov, 
                    unitario, quantidade, frete, seguro, despesas, desconto, descnaotrib, valor, lote, quantlote, fabricacao, validade, 
                    precomax, remas, tanque, bico, cide, basecide, valorcide, valoriof, pesoliq, pesobruto, capacidade, volumes, impexp, 
                    valorimpexp, acdraw, cst_icms, csosn, icmsorigem, icmsdestino, encargosicms, reducaoicms, baseicms, valoricms, diferencial, 
                    antecipacao, icmsdiferido, abatimentoicms, valorciap, mesesciap, tipoipi, tiposomaipi, ipi, reducaoipi, encargosipi, 
                    baseipi, valoripi, abatimentoipi, ipisemcred, seloipi, lacrepi, lucro, tipost, reducaost, basestfixa, basesubst, substtribprop, 
                    substtribterc, substnaoretida, substobs, tipo_pc, pisimp, cofinsimp, basepisimp, basecofinsimp, valorpisimp, valorcofinsimp, 
                    basestpis, basestcofins, valorstpis, valorstcofins, ordem, id_item, id_docfis, id, id_proprietario, id_receptor, id_obra, 
                    tipo_linha, id_linha, id_vendedor, ipienquadramentocodigo, ipienquadramentodescricao, cest, valorpercentualfcpicmsdestino, 
                    valoraliquotainternaicmsdestino, valorpercentualpartilhaicmsdestino, valorfcpicmsdestino, valoricmsdestino, valoricmsinterestadualorigem, 
                    valorpercentualicmsinter, valorcontabilpis, valorcontabilcofins, situacaogerencial, chavegold, valordebitopis, valordebitocofins, 
                    id_localestoque, linha_pendente, custototal, percentualfatorcomissao, percentualcomissao, pfcp, vfcp, vbcfcp, vbcfcpst, 
                    pfcpst, vfcpst, pfcpstret, vfcpstret, vbcfcpufdest, vbcfcpstret, pst, valorcustosextra, predbcefet, picmsefet, vbcefet, vicmsefet, 
                    lastupdate, tenant, motdesicms, tipi, origem, cbenef, nbenef)
                    SELECT it.id_ano::integer, it.especificacao, it.cfop, it.unidade, it.tiposoma::integer, it.classe::integer, it.tiporec::integer, it.ignorasoma::boolean, 
                    it.vinculoreceita::integer, it.semmov::boolean, it.unitario::numeric, it.quantidade::numeric, it.frete::numeric, it.seguro::numeric, it.despesas::numeric, 
                    it.desconto::numeric, it.descnaotrib::numeric, it.valor::numeric, it.lote, it.quantlote::numeric, it.fabricacao::date, it.validade::date, it.precomax::numeric, 
                    it.remas::integer, it.tanque::integer, it.bico::integer, it.cide::numeric, it.basecide::numeric, it.valorcide::numeric, it.valoriof::numeric, it.pesoliq::numeric, 
                    it.pesobruto::numeric, it.capacidade::numeric, it.volumes::integer, it.impexp::numeric, it.valorimpexp::numeric, it.acdraw, it.cst_icms, it.csosn, 
                    it.icmsorigem::numeric, it.icmsdestino::numeric, it.encargosicms::numeric, it.reducaoicms::numeric, it.baseicms::numeric, it.valoricms::numeric, 
                    it.diferencial::numeric, it.antecipacao::numeric, it.icmsdiferido::numeric, it.abatimentoicms::numeric, it.valorciap::numeric, it.mesesciap::integer, 
                    it.tipoipi::integer, it.tiposomaipi::integer, it.ipi::numeric, it.reducaoipi::numeric, it.encargosipi::numeric, it.baseipi::numeric, it.valoripi::numeric, 
                    it.abatimentoipi::numeric, it.ipisemcred::numeric, it.seloipi, it.lacrepi, it.lucro::numeric, it.tipost::integer, it.reducaost::numeric, it.basestfixa::numeric, 
                    it.basesubst::numeric, it.substtribprop::numeric, it.substtribterc::numeric, it.substnaoretida::numeric, it.substobs::numeric, it.tipo_pc::integer, 
                    it.pisimp::numeric, it.cofinsimp::numeric, it.basepisimp::numeric, it.basecofinsimp::numeric, it.valorpisimp::numeric, it.valorcofinsimp::numeric, 
                    it.basestpis::numeric, it.basestcofins::numeric, it.valorstpis::numeric, it.valorstcofins::numeric, it.ordem::bigint, it.id_item::uuid, it.id_docfis::uuid, 
                    it.id::uuid, it.id_proprietario::uuid, it.id_receptor::uuid, it.id_obra::uuid, it.tipo_linha::smallint, it.id_linha::uuid, it.id_vendedor::uuid, 
                    it.ipienquadramentocodigo, it.ipienquadramentodescricao, it.cest, it.valorpercentualfcpicmsdestino::numeric, it.valoraliquotainternaicmsdestino::numeric, 
                    it.valorpercentualpartilhaicmsdestino::numeric, it.valorfcpicmsdestino::numeric, it.valoricmsdestino::numeric, it.valoricmsinterestadualorigem::numeric, 
                    it.valorpercentualicmsinter::numeric, it.valorcontabilpis::numeric, it.valorcontabilcofins::numeric, it.situacaogerencial::integer, it.chavegold, 
                    it.valordebitopis::numeric, it.valordebitocofins::numeric, it.id_localestoque::uuid, it.linha_pendente::boolean, it.custototal::numeric, 
                    it.percentualfatorcomissao::numeric, it.percentualcomissao::numeric, it.pfcp::numeric, it.vfcp::numeric, it.vbcfcp::numeric, it.vbcfcpst::numeric, 
                    it.pfcpst::numeric, it.vfcpst::numeric, it.pfcpstret::numeric, it.vfcpstret::numeric, it.vbcfcpufdest::numeric, it.vbcfcpstret::numeric, it.pst::numeric, 
                    it.valorcustosextra::numeric, it.predbcefet::numeric, it.picmsefet::numeric, it.vbcefet::numeric, it.vicmsefet::numeric, it.lastupdate::timestamp without time zone, 
                    it.tenant::bigint, it.motdesicms::integer, it.tipi, it.origem::integer, it.cbenef, it.nbenef
                    FROM valor it
                    WHERE EXISTS(SELECT 1 FROM ns.df_docfis doc WHERE it.id_docfis::uuid = doc.id)"""

    @staticmethod
    def obterListaValoresItensNFCe(
        itemNota: ItemNota, id_nfe: UUID, ano: int, ordem: int, CfopNFe: str
    ) -> List:
        """
        retorna uma lista com os valores dos campos do objeto ItemNota
        Note: os nomes dos campos estão nos comentários
        """
        valores = list()
        if itemNota.id is None:
            itemNota.id = uuid.uuid4()
        if itemNota.ordem == 0:
            itemNota.ordem = ordem
        valores.append(ano)  #  id_ano integer,
        valores.append(itemNota.xProd)  #  especificacao character varying(120),
        valores.append(
            itemNota.CFOP if itemNota.CFOP != CfopNFe else None
        )  #  cfop character varying(8),
        valores.append(itemNota.uCom)  #  unidade character varying(6),
        valores.append(None)  #  tiposoma integer,
        valores.append(None)  #  classe integer,
        valores.append(None)  #  tiporec integer,
        valores.append(None)  #  ignorasoma boolean,
        valores.append(None)  #  vinculoreceita integer,
        valores.append(None)  #  semmov boolean,
        valores.append(itemNota.vUnCom)  #  unitario numeric(20,6),
        valores.append(itemNota.qCom)  #  quantidade numeric(20,4),
        valores.append(0)  #  frete numeric(20,2),
        valores.append(0)  #  seguro numeric(20,2),
        valores.append(itemNota.vOutro)  #  despesas numeric(20,2),
        valores.append(itemNota.vDesc)  #  desconto numeric(20,2),
        valores.append(
            itemNota.icms.retornarValorDesoneracao()
        )  #  descnaotrib numeric(20,2),
        valores.append(itemNota.vProd)  #  valor numeric(20,2),
        valores.append(None)  #  lote character varying(20),
        valores.append(None)  #  quantlote numeric(20,2),
        valores.append(None)  #  fabricacao date,
        valores.append(None)  #  validade date,
        valores.append(None)  #  precomax numeric(20,2),
        valores.append(None)  #  remas integer,
        valores.append(None)  #  tanque integer,
        valores.append(None)  #  bico integer,
        valores.append(None)  #  cide numeric(20,2),
        valores.append(None)  #  basecide numeric(20,2),
        valores.append(None)  #  valorcide numeric(20,2),
        valores.append(None)  #  valoriof numeric(20,2),
        valores.append(None)  #  pesoliq numeric(20,2),
        valores.append(None)  #  pesobruto numeric(20,2),
        valores.append(None)  #  capacidade numeric(20,2),
        valores.append(None)  #  volumes integer,
        valores.append(0)  #  impexp numeric(20,2),
        valores.append(0)  #  valorimpexp numeric(20,2),
        valores.append(None)  #  acdraw character varying(20),
        valores.append(itemNota.icms.CST)  #  cst_icms character varying(2),
        valores.append(None)  #  csosn character varying(3),
        valores.append(itemNota.icms.aliquotaICMSTotal)  #  icmsorigem numeric(20,2),
        valores.append(itemNota.icms.aliquotaICMSTotal)  #  icmsdestino numeric(20,2),
        valores.append(0)  #  encargosicms numeric(20,2),
        valores.append(itemNota.icms.pRedBC)  #  reducaoicms numeric(20,4),
        valores.append(itemNota.icms.vBC)  #  baseicms numeric(20,2),
        valores.append(itemNota.icms.valorICMSTotal)  #  valoricms numeric(20,2),
        valores.append(0)  #  diferencial numeric(20,2),
        valores.append(0)  #  antecipacao numeric(20,2),
        valores.append(0)  #  icmsdiferido numeric(20,2),
        valores.append(itemNota.icms.vICMSDeson)  #  abatimentoicms numeric(20,2),
        valores.append(None)  #  valorciap numeric(20,2),
        valores.append(None)  #  mesesciap integer,
        valores.append(2)  #  tipoipi integer,
        valores.append(None)  #  tiposomaipi integer,
        valores.append(0)  #  ipi numeric(20,2),
        valores.append(0)  #  reducaoipi numeric(20,4),
        valores.append(0)  #  encargosipi numeric(20,2),
        valores.append(0)  #  baseipi numeric(20,2),
        valores.append(0)  #  valoripi numeric(20,2),
        valores.append(0)  #  abatimentoipi numeric(20,2),
        valores.append(0)  #  ipisemcred numeric(20,2),
        valores.append(None)  #  seloipi character varying(20),
        valores.append(None)  #  lacrepi character varying(20),
        valores.append(None)  #  lucro numeric(20,2),
        valores.append(0)  #  tipost integer,
        valores.append(0)  #  reducaost numeric(20,4),
        valores.append(0)  #  basestfixa numeric(20,2),
        valores.append(0)  #  basesubst numeric(20,2),
        valores.append(0)  #  substtribprop numeric(20,2),
        valores.append(0)  #  substtribterc numeric(20,2),
        valores.append(0)  #  substnaoretida numeric(20,2),
        valores.append(0)  #  substobs numeric(20,2),
        valores.append(None)  #  tipo_pc integer,
        valores.append(0)  #  pisimp numeric(20,4),
        valores.append(0)  #  cofinsimp numeric(20,4),
        valores.append(0)  #  basepisimp numeric(20,2),
        valores.append(0)  #  basecofinsimp numeric(20,2),
        valores.append(0)  #  valorpisimp numeric(20,2),
        valores.append(0)  #  valorcofinsimp numeric(20,2),
        valores.append(0)  #  basestpis numeric(20,2),
        valores.append(0)  #  basestcofins numeric(20,2),
        valores.append(0)  #  valorstpis numeric(20,2),
        valores.append(0)  #  valorstcofins numeric(20,2),
        valores.append(itemNota.ordem)  #  ordem bigint NOT NULL,
        if itemNota.id_produto is None:
            raise Exception("Item sem produto!")
        valores.append(str(itemNota.id_produto))  #  id_item uuid,
        valores.append(str(id_nfe))  #  id_docfis uuid,
        valores.append(
            str(itemNota.id)
        )  #  id uuid NOT NULL DEFAULT uuid_generate_v4(),
        valores.append(None)  #  id_proprietario uuid,
        valores.append(None)  #  id_receptor uuid,
        valores.append(None)  #  id_obra uuid,
        valores.append(None)  #  tipo_linha smallint,
        valores.append(str(itemNota.df_linha))  #  id_linha uuid,
        valores.append(None)  #  id_vendedor uuid,
        valores.append(None)  #  ipienquadramentocodigo character varying(10),
        valores.append(None)  #  ipienquadramentodescricao text,
        valores.append(str(itemNota.CEST))  #  cest character varying(7),
        valores.append(
            itemNota.icms.pFCP
        )  #  valorpercentualfcpicmsdestino numeric(20,2),
        valores.append(None)  #  valoraliquotainternaicmsdestino numeric(20,2),
        valores.append(None)  #  valorpercentualpartilhaicmsdestino numeric(20,2),
        valores.append(itemNota.icms.vFCP)  #  valorfcpicmsdestino numeric(20,2),
        valores.append(None)  #  valoricmsdestino numeric(20,2),
        valores.append(None)  #  valoricmsinterestadualorigem numeric(20,2),
        valores.append(None)  #  valorpercentualicmsinter numeric(20,2),
        valores.append(itemNota.pis.vPIS)  #  valorcontabilpis numeric(20,2),
        valores.append(itemNota.cofins.vCOFINS)  #  valorcontabilcofins numeric(20,2),
        valores.append(None)  #  situacaogerencial integer,
        valores.append(None)  #  chavegold text,
        valores.append(0)  #  valordebitopis numeric(20,2) NOT NULL DEFAULT 0.00,
        valores.append(0)  #  valordebitocofins numeric(20,2) NOT NULL DEFAULT 0.00,
        valores.append(None)  #  id_localestoque uuid,
        valores.append(None)  #  linha_pendente boolean,
        valores.append(None)  #  custototal numeric(20,6),
        valores.append(None)  #  percentualfatorcomissao numeric(20,6),
        valores.append(None)  #  percentualcomissao numeric(20,6),
        valores.append(itemNota.icms.pFCP)  #  pfcp numeric(15,2),
        valores.append(itemNota.icms.vFCP)  #  vfcp numeric(15,2),
        valores.append(itemNota.icms.vBCFCP)  #  vbcfcp numeric(15,2),
        valores.append(None)  #  vbcfcpst numeric(15,2),
        valores.append(None)  #  pfcpst numeric(15,2),
        valores.append(None)  #  vfcpst numeric(15,2),
        valores.append(None)  #  pfcpstret numeric(15,2),
        valores.append(None)  #  vfcpstret numeric(15,2),
        valores.append(None)  #  vbcfcpufdest numeric(15,2),
        valores.append(None)  #  vbcfcpstret numeric(15,2),
        valores.append(None)  #  pst numeric(15,2),
        valores.append(None)  #  valorcustosextra numeric(15,6),
        valores.append(None)  #  predbcefet numeric(20,2),
        valores.append(None)  #  picmsefet numeric(20,4),
        valores.append(None)  #  vbcefet numeric(20,2),
        valores.append(None)  #  vicmsefet numeric(20,2),
        valores.append(
            utilidades.now_brazil()
        )  #  lastupdate timestamp without time zone DEFAULT now(),
        valores.append(None)  #  tenant bigint,
        valores.append(itemNota.icms.motDesICMS)  #  motdesicms
        valores.append(itemNota.NCM)  # tipi
        valores.append(itemNota.icms.orig)  # origem
        valores.append(itemNota.cBenef)  # cbenef character varying(10)
        valores.append(itemNota.nBenef)  # nbenef character varying(6)
        return valores

    @staticmethod
    def obterSQLInsertDf_Linhas() -> str:
        """Retorna o comando SQL para insert na tabela ns.df_linhas"""
        return """ WITH valor(df_linha, id_item, id_cfop, id_docfis, tipolinha, quantidadecomercial, valorunitariocomercial, 
                        valortotal, valordesconto, quantidadetributavel, valorunitariotributacao, valorfrete, valorseguro, 
                        valoroutrasdespesas, extipi, razaoconversao, alteratotalnfe, ordem, id_localdeestoque, 
                        codigoitemfornecedor, id_unidade_comercial, unidade_comercial, id_unidade_tributada, unidade_tributada, 
                        tipo_documento_origem, codigoitemdocfis, descricaoitemdocfis, aprovado, indicador_escala_relevante, volume_razao)
                    AS (VALUES %s)
                    INSERT INTO ns.df_linhas(df_linha, id_item, id_cfop, id_docfis, tipolinha, quantidadecomercial, valorunitariocomercial, 
                        valortotal, valordesconto, quantidadetributavel, valorunitariotributacao, valorfrete, valorseguro,
                        valoroutrasdespesas, extipi, razaoconversao, alteratotalnfe, ordem, id_localdeestoque, codigoitemfornecedor, 
                        id_unidade_comercial, unidade_comercial, id_unidade_tributada, unidade_tributada, tipo_documento_origem,
                        codigoitemdocfis, descricaoitemdocfis, aprovado, indicador_escala_relevante, volume_razao)	
                    SELECT it.df_linha::uuid, it.id_item::uuid, it.id_cfop::uuid, it.id_docfis::uuid, it.tipolinha::smallint, it.quantidadecomercial::numeric, 
                        it.valorunitariocomercial::numeric, it.valortotal::numeric, it.valordesconto::numeric, it.quantidadetributavel::numeric, 
                        it.valorunitariotributacao::numeric, it.valorfrete::numeric, it.valorseguro::numeric, it.valoroutrasdespesas::numeric, 
                        it.extipi::numeric, it.razaoconversao::numeric, it.alteratotalnfe::boolean, it.ordem::integer, it.id_localdeestoque::uuid, 
                        it.codigoitemfornecedor::varchar, it.id_unidade_comercial::uuid, it.unidade_comercial::varchar, it.id_unidade_comercial::uuid, it.unidade_tributada::varchar, 
                        it.tipo_documento_origem::integer, it.codigoitemdocfis::varchar, it.descricaoitemdocfis::varchar, it.aprovado::boolean, 
                        it.indicador_escala_relevante::integer, it.volume_razao::double precision
                    FROM valor it
                    LEFT JOIN ns.df_docfis doc ON it.id_docfis::uuid = doc.id
                    WHERE doc.id is not Null """

    @staticmethod
    def obterListaValoresDf_Linhas(
        itemNota: ItemNota, id_nfe: UUID, ordem: int
    ) -> List:
        """
        retorna uma lista com os valores dos campos para df_linhas
        Note: os nomes dos campos estão nos comentários
        """
        valores = list()
        if itemNota.ordem == 0:
            itemNota.ordem = ordem
        if itemNota.id_produto is None:
            raise Exception("Item sem produto!")
        if itemNota.df_linha is None:
            itemNota.df_linha = uuid.uuid4()
        valores.append(str(itemNota.df_linha))  # df_linha uuid
        valores.append(str(itemNota.id_produto))  # id_item uuid
        valores.append(itemNota.id_cfop)  # id_cfop character varying(8),
        valores.append(str(id_nfe))  # id_docfis uuid
        valores.append(1)  # tipo_linha smallint
        valores.append(itemNota.qCom)  # quantidadecomercial numeric(20,4)
        valores.append(itemNota.vUnCom)  # valorunitariocomercial numeric(20,2)
        valores.append(itemNota.vProd)  # valortotal numeric(20,2)
        valores.append(itemNota.vDesc)  # desconto numeric(20,2)
        valores.append(itemNota.qCom)  # quantidadetributavel numeric(20,4)
        valores.append(itemNota.vUnCom)  # valorunitariotributacao numeric(20,2)
        valores.append(0)  # valorfrete numeric(20,2)
        valores.append(0)  # valorseguro numeric(20,2)
        valores.append(itemNota.vOutro)  # valoroutrasdespesas numeric(20,2)
        valores.append(0)  # extipi
        valores.append(0)  # razaoconversao
        valores.append(False)  # alteratotalnfe boolean
        valores.append(itemNota.ordem)  # ordem bigint NOT NULL,
        valores.append(itemNota.idLocalDeEstoque)  # id_localdeestoque UUID
        valores.append(itemNota.cProd)  # codigoitemfornecedor character varying(60)
        valores.append(itemNota.id_unidade)  # id_unidade_comercial UUID
        valores.append(itemNota.uCom)  # unidade_comercial character varying(6)
        valores.append(itemNota.id_unidade_trib)  # id_unidade_tributada UUID
        valores.append(itemNota.uCom)  # unidade_tributada character varying(6)
        valores.append(0)  # tipo_documento_origem integer
        valores.append(itemNota.cProd)  # codigoitemfornecedor character varying(60)
        valores.append(itemNota.xProd)  # descricaoitemdocfis character varying(120)
        valores.append(False)  # aprovado boolean
        valores.append(0)  # indicador_escala_relevante integer
        valores.append(0)  # volume_razao character doubleprecision
        return valores
