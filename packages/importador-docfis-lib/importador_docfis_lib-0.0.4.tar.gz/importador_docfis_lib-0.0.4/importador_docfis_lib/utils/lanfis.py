import uuid
from typing import List

from nasajon.dto_handler.item_nota import ItemNota
from nasajon.dto_handler.nfce import NFCE

class Lanfis:
    """ Classe de Domínio para Lançamento Fiscal """

    @staticmethod
    def decomporChaveLancamento(chave: str):
        """
        retorna os componentes da chave do lan�amento separados:
            CFOP;
            Aliquota ICMS
            Redução ICMS
            CST
        """
        return chave.split('|')[0], chave.split('|')[1], chave.split('|')[2]

    @staticmethod
    def comporChaveLancamento(cfop: str, aliquotaICMS: float, CST: int) -> str:
        """
        retorna os componentes da chave do lançamento concatenados:
            CFOP + '|' + Aliquota ICMS + '|' + Redução ICMS + CST
        """
        return cfop + '|' + str(aliquotaICMS) + '|' + str(CST)

    @staticmethod
    def obterChavesLancamentosNFCe(nfe: NFCE) -> set:
        """ Retorna as chaves de lançamento fiscal para a nota fornecida """
        return set(
            [
                (item.CFOP + "|" + str(item.icms.aliquotaICMSTotal) + "|" + '1' + str(item.icms.orig) + str(
                    item.icms.CST))
                for item in nfe.lista_itens
            ]
        )
      
    # @staticmethod
    # def obterChavesLancamentosSAT(sat: SAT) -> set:
    #     """ Retorna as chaves de lançamento fiscal para a nota fornecida """
    #     return set(
    #         [
    #             (item.CFOP + "|" + str(item.icms.aliquotaICMSTotal) + "|" + '1' + str(item.icms.orig) + str(
    #                 item.icms.CST))
    #             for item in sat.listaItens
    #         ]
    #     )   

    @staticmethod
    def obterLancamentosNFCe(nfe: NFCE) -> dict:
        """
        Retorna um dicionário (chave, id) para os lançamentos fiscais
        da nota fornecida
        """
        return {
            chave: uuid.uuid4()
            for chave in Lanfis.obterChavesLancamentosNFCe(nfe)
        }

    # def obterLancamentosSAT(sat: SAT) -> dict:
    #     """
    #     Retorna um dicionário (chave, id) para os lançamentos fiscais
    #     da nota fornecida
    #     """
    #     return {
    #         chave: uuid.uuid4()
    #         for chave in Lanfis.obterChavesLancamentosSAT(sat)
    #     }    

    @staticmethod
    def filtrarItensDaNotaPorChaveDoLancamentoFiscal(nfe: NFCE, chave: str) -> List[ItemNota]:
        """
        Retorna uma lista com os itens da nota que devem ser considerados \
        no lançamento fiscal que tem esta chave
        """
        cfop, aliquota, CST = Lanfis.decomporChaveLancamento(chave)
        return [
            item for item
            in nfe.lista_itens
            if ((item.CFOP == cfop) and (str(float(item.icms.aliquotaICMSTotal)) == str(aliquota)) and str(
                '1' + str(item.icms.orig) + str(item.icms.CST)) == str(CST))
        ]
