from typing import List
import uuid

from nasajon.dto.cliente import Cliente
from nasajon.dto.estabelecimento import Estabelecimento
from nasajon.dto_handler.participante import Participante
from nasajon.utils import utilidades
from nasajon.utils.conexao_postgres_adapter import ConexaoPostgresAdapter
from nasajon.utils.utilidades_banco import UtilidadesBanco


class ClienteDAO:
    """
    Classe responsável pelas operações de CRUD de clientes junto ao Banco de Dados
    """

    def __init__(self, conexao: ConexaoPostgresAdapter):
        """
        Construtor do DAO de clientes
        """
        self.__conexao = conexao

    def retornar_clientes(self, estabelecimento: Estabelecimento) -> List[Cliente]:
        """
        Lista todos os clientes
        """
        return UtilidadesBanco.executarConsulta(
            self.__conexao, self.obterSQLConsulta(estabelecimento), [], Cliente
        )

    def gravarClientes(self, clientes: List[Participante]):
        """
        Grava os Clientes no banco de dados, incluindo ns.pessoas e ns.conjuntosclientes

        Args:
            clientes:   List[Participante] - Lista dos clientes que devem ser criados
            assincrono: Determina se o comando deve esperar o retorno (False) ou rodar em processo separado (True)
        """
        parametros = [self.obterListaValoresPessoa(cliente) for cliente in clientes]
        UtilidadesBanco.executarComando(
            self.__conexao, self.obterSQLInsertPessoa(), parametros, True, True
        )

        parametros = [
            self.obterListaValoresEndereco(cliente)
            for cliente in clientes
            if cliente.xLgr != ""
        ]

        if len(parametros) > 0:
            UtilidadesBanco.executarComando(
                self.__conexao, self.obterSQLInsertEndereco(), parametros, True, True
            )

        parametros = [self.obterListaValoresConjunto(cliente) for cliente in clientes]
        UtilidadesBanco.executarComando(
            self.__conexao, self.obterSQLInsertConjuntos(), parametros, True, True
        )

    @staticmethod
    def obterSQLConsulta(estabelecimento: Estabelecimento = None) -> str:
        """Retorna o comando SQL para carregar os clientes do banco de dados"""
        if estabelecimento is None:
            return "select  	ps.id\
                            ,	desformata_documento(ps.cnpj) as cnpj\
                            ,	ps.nome\
                            ,	es.estabelecimento\
                    from	ns.pessoas ps\
                    join	ns.conjuntosclientes cc on ps.id = cc.registro\
                    join	ns.estabelecimentosconjuntos ec \
                        on cc.conjunto = ec.conjunto\
                    join	ns.estabelecimentos es \
                        on  ec.estabelecimento = es.estabelecimento"
        else:
            return (
                "select  	ps.id\
                            ,	desformata_documento(ps.cnpj) as cnpj\
                            ,	ps.nome\
                            ,	es.estabelecimento\
                    from	ns.pessoas ps\
                    join	ns.conjuntosclientes cc on ps.id = cc.registro\
                    join	ns.estabelecimentosconjuntos ec \
                        on cc.conjunto = ec.conjunto\
                    join	ns.estabelecimentos es \
                        on  ec.estabelecimento = es.estabelecimento \
                             and es.estabelecimento = '"
                + str(estabelecimento.id)
                + "'"
            )

    @staticmethod
    def obterSQLInsertPessoa() -> str:
        """Retorna o comando SQL para insert na tabela ns.pessoas"""
        return """insert into ns.pessoas (id, pessoa, tp_identificacao, nome, nomefantasia, 
                inscricaoestadual, cnpj, chavecnpj, datacadastro, inscricaomunicipal, tiposimples, 
                proximocontato, inscestsubstituto, icmssimp, produtorrural, substitutomunicipal, bloqueado, clienteativado, 
                fornecedorativado, contribuinteipi, email, regimereceita, transportadoraativado, contribuinteicms, retemiss, qualificacao, 
                suframa, fichaativado, tributoativado, tomadorfolhaativado, formatributacaofunrural) values %s"""

    @staticmethod
    def obterListaValoresPessoa(pessoa: Participante) -> List:
        """
        retorna uma lista com os valores dos campos do objeto pessoa
        Note: A ordem dos campo é a seguinte \
        (id, pessoa, tp_identificacao, nome, nomefantasia, 
        inscricaoestadual, cnpj, chavecnpj, datacadastro, inscricaomunicipal, tiposimples, 
        proximocontato, inscestsubstituto, icmssimp, produtorrural, substitutomunicipal, bloqueado, clienteativado, 
        fornecedorativado, contribuinteipi, email, regimereceita, transportadoraativado, contribuinteicms, retemiss, qualificacao, 
        suframa, fichaativado, tributoativado, tomadorfolhaativado, formatributacaofunrural)
        """
        valores = list()
        valores.append(str(pessoa.id))  # id
        valores.append(
            pessoa.identificador + (("_" + pessoa.UF) if pessoa.CPF else "")
        )  # pessoa
        valores.append(0)  # tp_identificacao
        valores.append(pessoa.xNome)  # nome
        valores.append(pessoa.xNome)  # nomefantasia
        valores.append(pessoa.IE)  # inscricaoestadual
        if len(pessoa.CPF) == 11:
            valores.append("{}{}{}.{}{}{}.{}{}{}-{}{}".format(*pessoa.CPF))  # cnpj
        elif len(pessoa.CNPJ) == 14:
            valores.append(
                "{}{}.{}{}{}.{}{}{}/{}{}{}{}-{}{}".format(*pessoa.CNPJ)
            )  # cnpj
        else:
            valores.append(pessoa.CPF if pessoa.CPF else pessoa.CNPJ)  # cnpj
        valores.append(pessoa.identificador)  # chavecnpj
        valores.append(utilidades.now_brazil())  # datacadastro
        valores.append(pessoa.IM)  # inscricaomunicipal
        valores.append(0)  # tiposimples
        valores.append(utilidades.now_brazil())  # proximocontato
        valores.append("")  # inscestsubstituto
        valores.append(0)  # icmssimp
        valores.append(False)  # produtorrural
        valores.append(False)  # substitutomunicipal
        valores.append(False)  # bloqueado
        valores.append(1)  # clienteativado
        valores.append(1)  # fornecedorativado
        valores.append(False)  # contribuinteipi
        valores.append(pessoa.email)  # email
        valores.append(0)  # regimereceita
        valores.append(0)  # transportadoraativado
        valores.append(False)  # contribuinteicms
        valores.append(0)  # retemiss
        valores.append(0)  # qualificacao
        valores.append("ISENTO")  # suframa
        valores.append(1)  # fichaativado
        valores.append(0)  # tributoativado
        valores.append(0)  # tomadorfolhaativado
        valores.append(0)  # formatributacaofunrural
        return valores

    @staticmethod
    def obterSQLInsertConjuntos() -> str:
        """Retorna o comando SQL para insert na tabela ns.conjuntosclientes"""
        return "insert into ns.conjuntosclientes \
                (conjuntocliente, registro, conjunto) values %s"

    @staticmethod
    def obterListaValoresConjunto(pessoa: Participante) -> List:
        """
        retorna uma lista com os valores dos campos do objeto conjuntoPessoas
        Note: A ordem dos campo é a seguinte (conjuntocliente,id_cliente, \
        conjunto)
        """
        valores = list()
        valores.append(str(uuid.uuid4()))
        valores.append(str(pessoa.id))
        valores.append(str(pessoa.conjunto))
        return valores

    @staticmethod
    def obterSQLInsertEndereco() -> str:
        """Retorna o comando SQL para insert na tabela ns.pessoas"""
        return """insert into ns.enderecos (tipologradouro, logradouro, numero, complemento, cep, bairro, tipoendereco, uf, ibge, cidade, endereco, id_pessoa) values %s"""

    @staticmethod
    def obterListaValoresEndereco(pessoa: Participante) -> List:
        """
        retorna uma lista com os valores dos campos do objeto endereco
        Note: A ordem dos campo é a seguinte \
        (tipologradouro, logradouro, numero, complemento, cep, bairro, tipoendereco, uf, ibge, cidade, endereco, id_pessoa)
        """
        valores = list()

        valores.append(pessoa.tipo_logradouro)  # tipologradouro
        valores.append(pessoa.xLgr)  # logradouro
        valores.append(pessoa.nro[0:10])  # numero
        valores.append(pessoa.xCpl)  # complemento
        valores.append(pessoa.CEP)  # cep
        valores.append(pessoa.xBairro)  # bairro
        valores.append(0)  # tipoendereco
        valores.append(pessoa.UF)  # uf
        valores.append(
            pessoa.cMun if pessoa.cMun is not None and pessoa.cMun != "" else None
        )  # ibge
        valores.append(pessoa.xMun)  # cidade
        valores.append(str(pessoa.id_endereco))  # endereco
        valores.append(str(pessoa.id))  # id_pessoa
        return valores
