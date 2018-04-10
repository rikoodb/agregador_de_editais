# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from edital.edital import insere_no_db_edital
from edital.edital import procura_edital_db
import settings


def first(sel, xpath):
    # xpath eh um seletor html
    # extract_first extrai apenas o primeiro elemento
    return sel.xpath(xpath).extract_first()


class Finep_govSpider(scrapy.Spider):
    name = "finep_gov"
    start_urls = ['http://finep.gov.br/chamadas-publicas?situacao=aberta']

    def parse(self, response):
        # pega a data atual

        hoje = datetime.now()

        # extrai os dados necessarios do site
        for sel in response.css('div.item'):

            dat_publicacao = sel.css('div.data_pub span::text').extract_first()
            dat_prazo_envio = sel.css('div.prazo span::text').extract_first()
            titulo = sel.css('a::text').extract_first()

            # converte de y-n-d para d/m/y
            convert_dat_prazo_envio = datetime.strptime(dat_prazo_envio,
                                                        '%d/%m/%Y')

            # Se a data do edital for maior que a data de hoje
            if hoje <= convert_dat_prazo_envio:

                # extrai o link com essa data

                link = response.urljoin(first(sel, './/h3/a/@href'))

                # armazena tudo em um dicionario

                informacoes = {
                    'link': link,
                    'data_publicacao': dat_publicacao,
                    'data_prazo_envio': dat_prazo_envio,
                    'titulo': titulo
                }
                edital = procura_edital_db(settings.conn, settings.cursor, informacoes['link'])

                if not edital:

                    insere_no_db_edital(settings.conn, settings.cursor, informacoes['link'],
                                        informacoes['data_publicacao'],
                                        informacoes['data_prazo_envio'],
                                        informacoes['titulo'])

                    yield informacoes
