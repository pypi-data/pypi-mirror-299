import uuid
from typing import List

from importador_docfis_lib.dto.estabelecimento import Estabelecimento
from importador_docfis_lib.dto.produto import Produto
from importador_docfis_lib.utils.conexao_postgres_adapter import ConexaoPostgresAdapter
from importador_docfis_lib.utils.utilidades_banco import UtilidadesBanco


class ProdutoDAO:
    def __init__(self, conexao: ConexaoPostgresAdapter):
        """
        Construtor do DAO de produtos
        """
        self.__conexao = conexao

    def retornar_produtos(self, estabelecimento=None) -> List[Produto]:
        """
        Lista todos os produtos
        """
        return UtilidadesBanco.executarConsulta(
            self.__conexao, self.obterSQLConsulta(estabelecimento), [], Produto
        )

    @staticmethod
    def obterSQLConsulta(estabelecimento: Estabelecimento = None) -> str:
        """
        Retorna o comando SQL para consulta de Produtos
        :return: SQL para consulta de Produtos
        """
        if estabelecimento is None:
            return "select  	it.id\
                            ,	it.item\
                            ,	it.grupoinventario\
                            ,	it.especificacao\
                            ,	es.estabelecimento\
                    from	estoque.itens it\
                    join	ns.conjuntosprodutos cp\
                        on it.id = cp.registro\
                    join	ns.estabelecimentosconjuntos ec\
                        on cp.conjunto = ec.conjunto\
                    join	ns.estabelecimentos es \
                        on      ec.estabelecimento = es.estabelecimento"
        else:
            return (
                "select  	it.id\
                            ,	it.item\
                            ,	it.especificacao\
                            ,	it.grupoinventario\
                            ,	es.estabelecimento\
                    from	estoque.itens it\
                    join	ns.conjuntosprodutos cp\
                        on it.id = cp.registro\
                    join	ns.estabelecimentosconjuntos ec\
                        on cp.conjunto = ec.conjunto\
                    join	ns.estabelecimentos es \
                        on      ec.estabelecimento = es.estabelecimento \
                            and es.estabelecimento = '"
                + str(estabelecimento.id)
                + "'"
            )

    @staticmethod
    def obterSQLInsertItem() -> str:
        """
        Retorna o comando SQL para insert na tabela estoque.itens
        :return: SQL para insert na tabela estoque.itens
        """
        return "insert into estoque.itens (id, item, id_grupo, reduzido, \
                unidade, especificacao, precocusto, precomediocusto, \
                precovenda, cst_icms_a, cst_icms_b, icms, decimaisinventario,\
                tipi, codigobarra, grupoinventario, tipoipi, ii, \
                tipomedicamento, tipocalctrib, unidadetrib, cest, produto) values %s"

    @staticmethod
    def obterListaValoresItem(produto: Produto) -> List:
        """
        retorna uma lista com os valores dos campos do objeto produto
        Note: A ordem dos campo é a seguinte: id, item, id_grupo, reduzido, \
            unidade, especificacao, precocusto, precomediocusto, precovenda, \
            cst_icms_a, cst_icms_b, icms, decimaisinventario, tipi, codigobarra, \
            grupoinventario, tipoipi, ii, tipomedicamento, tipocalctrib, \
            unidadetrib, cest, produto
        :param produto: Produto a ter os valores retornados
        :return: Lista com os valores na ordem correta para execução do Insert
        """
        valores = list()
        valores.append(str(produto.id))  # id
        valores.append(produto.item)  # item
        valores.append(None)  # id_grupo
        valores.append(produto.item[:14])  # reduzido
        valores.append(
            str(produto.dados.id_unidade)
            if produto.dados.id_unidade is not None
            else None
        )  # unidade
        valores.append(produto.especificacao)  # especificacao
        valores.append(0)  # precocusto
        valores.append(0)  # precomediocusto
        valores.append(produto.dados.vUnCom)  # precovenda
        valores.append(produto.dados.icms.orig)  # cst_icms_a
        valores.append(produto.dados.icms.CST)  # cst_icms_b
        valores.append(produto.dados.icms.aliquotaICMSTotal)  # icms
        valores.append(2)  # decimaisinventario
        valores.append(produto.dados.NCM)  # tipi
        valores.append(produto.dados.cEAN)  # codigobarra
        valores.append(0)  # grupoinventario
        valores.append(0)  # tipoipi
        valores.append(0)  # ii
        valores.append(0)  # tipomedicamento
        valores.append(int(produto.dados.pis.CST))  # tipocalctrib
        valores.append(
            str(produto.dados.id_unidade_trib)
            if produto.dados.id_unidade_trib is not None
            else None
        )  # unidadetrib
        valores.append(produto.dados.CEST)  # cest
        valores.append(str(produto.id_produto))  # produto
        return valores

    @staticmethod
    def obterSQLInsertProduto() -> str:
        """
        Retorna o comando SQL para inserir na tabela de estoque.produtos
        :return: SQL para insert na tabela de estoque.produtos
        """
        return "insert into estoque.produtos(produto, codigo, especificacao,\
                TipoProduto, Bloqueado, OrigemMercadoria, codigodebarras, \
                tipodemedicamento, TIPI, unidadedemedida, cest) values %s"

    @staticmethod
    def obterListaValoresProduto(produto: Produto) -> List:
        """
        retorna uma lista com os valores dos campos do objeto produto
        Note: A ordem dos campo é a seguinte: produto, codigo, especificacao, \
            TipoProduto, Bloqueado, OrigemMercadoria, codigodebarras, \
            tipodemedicamento, TIPI, unidadedemedida
        :param produto: Produto a ter os valores retornados
        :return: Lista com os valores na ordem correta para execução do Insert
        """
        if produto.id_produto is None:
            produto.id_produto = uuid.uuid4()

        valores = list()
        valores.append(str(produto.id_produto))  # produto
        valores.append(produto.item)  # codigo
        valores.append(produto.especificacao)  # especificacao
        valores.append(0)  # TipoProduto
        valores.append(False)  # Bloqueado
        valores.append(produto.dados.icms.orig)  # OrigemMercadoria
        valores.append(produto.dados.cEAN)  # codigodebarras
        valores.append(0)  # tipodemedicamento
        valores.append(produto.dados.NCM)  # TIPI
        valores.append(
            str(produto.dados.id_unidade)
            if produto.dados.id_unidade is not None
            else None
        )  # unidadedemedida
        valores.append(produto.dados.CEST)  # cest
        return valores

    @staticmethod
    def obterSQLInsertConjuntos() -> str:
        """
        Retorna o comando SQL para insert na tabela ns.conjuntosprodutos
        :return: SQL para insert na tabela ns.conjuntosprodutos
        """
        return "insert into ns.conjuntosprodutos \
                (conjuntoproduto, registro, conjunto) \
                values %s"

    @staticmethod
    def obterListaValoresConjunto(produto: Produto) -> List:
        """
        retorna uma lista com os valores dos campos do objeto produto
        Note: A ordem dos campo é a seguinte: id, id_item, conjunto

        :param produto:  Produto a ter os valores retornados
        :return: Lista com os valores na ordem correta para execução do Insert
        """
        valores = list()
        valores.append(str(uuid.uuid4()))
        valores.append(str(produto.id))
        valores.append(str(produto.conjunto))
        return valores

    def gravarProdutos(self, produtos: List[Produto]) -> None:
        """
        Grava os itens no banco de dados, incluindo estoque.itens, \
        estoque.produtos e ns.conjuntosprodutos

        :param produtos: List[Produto] - Lista dos produtos que devem\
         ser criados
        """
        parametros = [
            ProdutoDAO.obterListaValoresProduto(produto)
            for produto in produtos
            if not produto.somenteConjunto
        ]
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao,
                ProdutoDAO.obterSQLInsertProduto(),
                parametros,
                True,
                True,
            )

        parametros = [
            ProdutoDAO.obterListaValoresItem(produto)
            for produto in produtos
            if not produto.somenteConjunto
        ]
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao, ProdutoDAO.obterSQLInsertItem(), parametros, True, True
            )

        parametros = [
            ProdutoDAO.obterListaValoresConjunto(produto) for produto in produtos
        ]
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao,
                ProdutoDAO.obterSQLInsertConjuntos(),
                parametros,
                True,
                True,
            )

        parametros = [
            ProdutoDAO.obterListaValoresConjuntoProdutos(produto)
            for produto in produtos
        ]
        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao,
                ProdutoDAO.obterSQLInsertConjuntos(),
                parametros,
                True,
                True,
            )

    def obterListaValoresConjuntoProdutos(produto: Produto) -> List:
        """
        retorna uma lista com os valores dos campos do objeto produto
        Note: A ordem dos campo � a seguinte: id, id_produto, conjunto

        :param produto:  Produto a ter os valores retornados
        :return: Lista com os valores na ordem correta para execu��o do Insert
        """
        valores = list()
        valores.append(str(uuid.uuid4()))
        valores.append(str(produto.id_produto))
        valores.append(str(produto.conjunto))
        return valores
