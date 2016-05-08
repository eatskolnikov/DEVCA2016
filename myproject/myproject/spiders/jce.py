# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

from myproject.items import MyprojectItem

class JceSpider(scrapy.Spider):
    name = "jce"
    allowed_domains = ["jce.gob.do"]
    start_urls = (
        'http://jce.gob.do/computoelectoral/Candidaturas',
    )

    def parse(self, response):
        province_block_headers = response.css("#LiveAccordionWrapper1053 h3 a.LA-ui-accordion-header").extract()
        for province_block_header in province_block_headers:
            province_block_headers_selector = Selector(text=province_block_header)
            province_block_id = str.join('', province_block_headers_selector.css("::attr('href')").extract())
            province_name = str.join('', province_block_headers_selector.css("::text").extract())
            province_block = response.css(province_block_id)
            rows = province_block.css('table.tg tr')
            for row in rows:
                row_text = str.join('', row.css('::text').extract())

                if 'provincia' in row_text.lower():
                    province_name = row_text.lower().replace('provincia :', '')
                    continue

                if 'circ' in row_text.lower():
                    province_name = row_text.lower().replace('provincia :', '')
                    continue

                if 'senador' in row_text.lower():
                    position = "senador"
                    continue

                if 'diputado' in row_text.lower():
                    position = "diputado"
                    continue

                if row.css('.tg-5mgg'):
                    party_header = row.css('.tg-5mgg')
                    party_header_colspan = str.join('', party_header.css("::attr('colspan')").extract())
                    print party_header_colspan
                    if (party_header_colspan == '4'):
                        party = str.join('', party_header.css('td.tg-5mgg::text').extract())
                    else:
                        party = str.join('', party_header.css('::text').extract())
                    continue



                candidate_name = row_text
                print province_name
                print party
                print position
                print candidate_name
                yield self.create_item(province_name, party, position, candidate_name)

    def create_item(self, province_name, party, position, candidate_name):

        item = MyprojectItem()
        item['province'] = province_name
        item['party'] = party
        item['position'] = position
        item['candidate'] = candidate_name
        return item