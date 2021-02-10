import re

import scrapy


class ManufacturerSpider(scrapy.Spider):
    name = "manufacturer"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/companies?page=1']

    def parse(self, response):

        # manufacturer_name = response.css('div.data-row-top a ::text').extract()
        # "stat": company_info.xpath('//div[@class="data-row-top"]/following-sibling::node()[1]').get()
        # "stat": [int(s) for s in (company_info.css('div.col-xs-12 ::text').extract()[-1].strip()).split()
        # if s.isdigit()]
        for company_info in response.css('div.data-row'):
            manufacturer_details = dict()
            manufacturer_link = company_info.css('div.data-row-top a ::attr(href)').get()
            generic_counter, brand_name_counter = (int(s) for s in (
                company_info.css('div.col-xs-12 ::text').extract()[-1].strip()).split() if s.isdigit())

            manufacturer_details["manufacturer_id"] = re.findall("companies/(\S*)/", manufacturer_link)[0]
            manufacturer_details["manufacturer_name"] = company_info.css('div.data-row-top a ::text').get()
            manufacturer_details["generics"] = generic_counter
            manufacturer_details["brand_names"] = brand_name_counter
            print(manufacturer_details)

        pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
        yield from response.follow_all(pagination_links, self.parse)
