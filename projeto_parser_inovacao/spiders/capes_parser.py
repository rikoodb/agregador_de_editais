import scrapy
from edital.edital import procura_edital_db
from edital.edital import insere_no_db_edital
import settings


def first(sel, xpath):
    return sel.xpath(xpath).extract_first()


class CAPES_govSpider(scrapy.Spider):
    name = "CAPES_gov"
    start_urls = ['http://capes.gov.br/editais-abertos']

    def parse(self, response):

        for sel in response.css('div.content-container'):

            link = response.urljoin(first(sel, './/h3/a/@href'))
            titulo = sel.css('a::text').extract_first()
            data_publicacao = None
            data_prazo_envio = None

            informacoes = {
                'link': link,
                'data_publicacao': data_publicacao,
                'data_prazo_envio': data_prazo_envio,
                'titulo': titulo
            }
            edital = procura_edital_db(settings.conn, settings.cursor, informacoes['link'])

            if not edital:
                insere_no_db_edital(settings.conn, settings.cursor, informacoes['link'],
                                    informacoes['data_publicacao'],
                                    informacoes['data_prazo_envio'],
                                    informacoes['titulo'])

                yield informacoes
