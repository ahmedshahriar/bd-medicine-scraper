import re

import scrapy


class IndicationSpider(scrapy.Spider):
    name = "indication"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/indications?page=1']

    def parse(self, response):
        for indication_info in response.css('div.data-row'):
            indication_link = indication_info.css('div.data-row-top a ::attr(href)').get()
            indication_id = re.findall("indications/(\S*)/", indication_link)[0]

            indication_name = indication_info.css('div.data-row-top a ::text').get()
            stat = indication_info.css('div.col-xs-12 ::text').extract()[-1].strip()


        pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
        yield from response.follow_all(pagination_links, self.parse)
