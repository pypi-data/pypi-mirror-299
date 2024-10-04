from typing import List

from importador_docfis_lib.dto.estabelecimento import Estabelecimento
from importador_docfis_lib.utils.conexao_postgres_adapter import ConexaoPostgresAdapter
from importador_docfis_lib.utils.utilidades_banco import UtilidadesBanco

class EstabelecimentoDAO:
    """
    Classe responsável pelas operações de CRUD de Estabelecimentos junto ao Banco de Dados
    """
    def __init__(self, conexao: ConexaoPostgresAdapter):
        """
        Construtor do DAO de Estabelecimentos
        """
        self.__conexao = conexao


    def retornar_estabelecimentos(self, estabelecimentos: list[str] = None) -> List[Estabelecimento]:
        """
        Lista todos os estabelecimentos
        """
        return UtilidadesBanco.executarConsulta(
            self.__conexao,
            EstabelecimentoDAO.obterSQLConsulta(estabelecimentos),
            [],
            Estabelecimento)
        
    def retornarRegimePIS(self, id_empresa, ano):
        sql = "select regimepis from scritta.cfgempresa where id_empresa = %s and id_ano = %s"
        
        return UtilidadesBanco.executarConsulta(self.__conexao, sql, [id_empresa, ano], None)

    @staticmethod
    def obterSQLConsulta(estabelecimentos: list[str] = None) -> str:

        """ Retorna o comando SQL para carregar os estabelecimentos do banco """
        sql = "select "
        sql += "           e.estabelecimento as id, "
        sql += "           e.raizcnpj||e.ordemcnpj as cnpj, "
        sql += "           e.inscricaoestadual as inscricao_estadual, "
        sql += "           e.codigo, "
        sql += "           pce.id_figuratributaria, "
        sql += "           coalesce(       pce.id_localdeestoque "
        sql += "                    , (	select l.localdeestoque "
        sql += "	                    from estoque.locaisdeestoques l "
        sql += "		                    where l.codigo = scritta.obter_codigo_local_estoque_padrao(e.estabelecimento) "
        sql += "                           limit 1 "
        sql += "	                        ) "
        sql += "                   ) as id_localdeestoque, "
        sql += "           pce.id_operacao, "
        sql += "           i.UF as uf, "
        sql += "           i.ibge, "
        sql += "           conf.integer_ini as lanc_ipi, "
        sql += "           e.empresa as id_empresa, "
        sql += "           max(c.cadastro::TEXT) as cadastro, "
        sql += "           max(ec.conjunto::TEXT)::UUID as conjunto_produtos, "
        sql += "           max(cc.conjunto::TEXT)::UUID as conjunto_clientes, "
        sql += "           max(cs.conjunto::TEXT)::UUID as conjunto_servicos, "
        sql += "           e.estabelecimento_multinota, "
        sql += "           em.tenant_multinotas "
        sql += "       from "
        sql += "        ns.estabelecimentos e "
        sql += "       left join "
        sql += "           ns.estabelecimentosconjuntos ec "
        sql += "               on (e.estabelecimento = ec.estabelecimento "
        sql += "                   and ec.cadastro = 0) "
        sql += "       left join "
        sql += "           ns.estabelecimentosconjuntos cc "
        sql += "               on (e.estabelecimento = cc.estabelecimento "
        sql += "                   and cc.cadastro = 6) "
        sql += "       left join "
        sql += "           ns.estabelecimentosconjuntos cs "
        sql += "               on (e.estabelecimento = cs.estabelecimento "
        sql += "                   and cs.cadastro = 3) "
        sql += "      left join "
        sql += "           ns.empresas em "
        sql += "               on e.empresa = em.empresa "
        sql += "       left join "
        sql += "           ns.gruposempresariaiscadastros gc "
        sql += "               on gc.grupoempresarial = em.grupoempresarial "
        sql += "       left join "
        sql += "           ns.cadastros c "
        sql += "               on c.cadastro = gc.cadastro "
        sql += "       left join "
        sql += "           scritta.perfilimp_config_estoque pce "
        sql += "               on pce.id_estabelecimento = e.estabelecimento "
        sql += "       left join "
        sql += "           scritta.perfilimp pim on pce.id_perfil = pim.id "
        sql += "               and pim.nome = 'VAREJISTA' "
        sql += "       left join "
        sql += "           ns.configuracoes conf on nome_ini = 'CFGFISC' and campo_ini = 'LANCIPISERV' and chave_ini = e.estabelecimento"
        sql += "       join ns.municipios i on e.ibge = i.ibge "
        if estabelecimentos:
            sql += "    Where UPPER(e.codigo) in ('" + "','".join(estabelecimentos) + "') or concat(e.raizcnpj, e.ordemcnpj) in ('" + "','".join(estabelecimentos) + "') " 
        sql += "       group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17"
        return sql
    
    def recupera_caminho_instalacao(self):
        """"
            Recupera o caminho de instalacao do sistema
        """
        sql = "select valor from ns.configuracoes where aplicacao = 0 and campo = 2 limit 1"
        resultado = UtilidadesBanco.executarConsulta(self.__conexao, sql, None, None, False)
        
        if str(resultado) == '[]':
            return ''
        else:
            return resultado[0]['valor'] 
