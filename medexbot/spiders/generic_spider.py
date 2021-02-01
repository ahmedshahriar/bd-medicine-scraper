import re

import scrapy

from medexbot.items import GenericItem


class GenericSpider(scrapy.Spider):
    name = "generic"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/generics?page=1']

    def parse(self, response):
        generic_page_links = response.css('a.hoverable-block ::attr("href") ')
        yield from response.follow_all(generic_page_links, self.parse_generic)

        pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
        # response.css('span[property="city"]::text').extract_first()
        yield from response.follow_all(pagination_links, self.parse)

    def parse_generic(self, response):
        generic_details = dict()

        generic_details['generic_id'] = re.findall("generics/(\S*)/", response.url)[0]
        generic_details['generic_name'] = response.css('h1.page-heading-1-l ::text').get().strip()
        generic_details['monograph_link'] = response.css('span.hidden-sm a ::attr(href)').get()
        """ medicine description """
        # indications
        generic_details['indications'] = response.css('div#indications h4 ::text').get().strip()
        generic_details['indication_description'] = response.xpath(
            '//div[@id="indications"]/following-sibling::node()[2]').get().strip()

        item = GenericItem()
        item['generic_id'] = generic_details['generic_id']
        item['generic_name'] = generic_details['generic_name']
        item['monograph_link'] = generic_details['monograph_link']
        item['indication_description'] = generic_details['indication_description']
        yield item
