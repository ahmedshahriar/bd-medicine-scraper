import re

import scrapy


class MedSpider(scrapy.Spider):
    name = "med"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/brands?page=1']

    def parse(self, response):

        for med_info in response.css('a.hoverable-block'):
            med_page_links = med_info.css('a.hoverable-block ::attr("href") ')
            print(med_page_links)
            pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
            # response.css('span[property="city"]::text').extract_first()
            yield from response.follow_all(pagination_links, self.parse)