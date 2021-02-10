import re

import scrapy


class ManufacturerSpider(scrapy.Spider):
    name = "manufacturer"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/companies?page=1']

    def parse(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        # manufacturer_name = response.css('div.data-row-top a ::text').extract()
        for company_info in response.css('div.data-row'):
            manufacturer_link = company_info.css('div.data-row-top a ::attr(href)').get()
            manufacturer_id = re.findall("companies/(\S*)/", manufacturer_link)[0]

            print( {
                "manufacturer_id": manufacturer_id,
                "manufacturer_name": company_info.css('div.data-row-top a ::text').get(),
                # "stat": company_info.xpath('//div[@class="data-row-top"]/following-sibling::node()[1]').get()
                "stat": company_info.css('div.col-xs-12 ::text').extract()[-1].strip()
            })

        # pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
        # yield from response.follow_all(pagination_links, self.parse)
