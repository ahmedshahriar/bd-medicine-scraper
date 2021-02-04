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
        # generic_details['indications'] = response.css('div#indications h4 ::text').get().strip()
        generic_details['indication_description'] = response.xpath(
            '//div[@id="indications"]/following-sibling::node()[2]').get().strip()

        # ###Therapeutic Class
        # therapeutic_class = extract_with_css('div#drug_classes h4 ::text')
        generic_details['therapeutic_class_description'] = response.xpath(
            '//div[@id="drug_classes"]/following-sibling::node()[2]').get()

        # ###Pharmacology
        # pharmacology = extract_with_css('div#mode_of_action h4 ::text')
        generic_details['pharmacology_description'] = response.xpath(
            '//div[@id="mode_of_action"]/following-sibling::node()[2]').get()

        item = GenericItem()
        for k, v in generic_details.items():
            item[k] = v
        yield item
