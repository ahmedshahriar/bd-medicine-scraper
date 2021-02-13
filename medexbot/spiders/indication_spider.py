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

            brand_names_counter = indication_info.css('div.col-xs-12 ::text').re(r"(\d+)")
            generics_count = 0 if len(brand_names_counter) == 0 else brand_names_counter[0]

            yield from response.follow_all(indication_info.css('div.data-row-top a ::attr(href)'),
                                           self.parse_indication,
                                           meta={"indication_id": indication_id, "indication_name": indication_name,
                                                 "generics_count": generics_count})

        pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_indication(self, response):
        indication_id = response.request.meta['indication_id']
        indication_name = response.request.meta['indication_name']
        generics_count = response.request.meta['generics_count']

        generic_links = response.css('div.data-row-top a ::attr(href)').extract()
        generic_ids = [re.findall("generics/(\S*)/", generic_link)[0] for generic_link in generic_links]

        yield {
            "indication_id": indication_id,
            "indication_name": indication_name,
            "generics_count": generics_count,
            "generic_ids": generic_ids
        }
