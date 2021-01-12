import re

import scrapy


class MedSpider(scrapy.Spider):
    name = "med"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/brands?page=1']

    def parse(self, response):
        for med_info in response.css('a.hoverable-block'):
            med_page_links = med_info.css('a.hoverable-block ::attr("href") ')
            yield from response.follow_all(med_page_links, self.parse_med)

            pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
            yield from response.follow_all(pagination_links, self.parse)

    def parse_med(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        med_details = dict()
        med_details['brand_name'] = response.xpath(
            '/html/body/main/section/div[2]/div/div[1]/div/div[1]/h1/span[2]/text() ').get()
        med_details['dosage_form'] = extract_with_css('small.h1-subtitle ::text')
        # generic_name = extract_with_css('div[title="Generic Name"] a ::text')
        generic_link = extract_with_css('div[title="Generic Name"] a ::attr(href)')
        med_details['generic_id'] = re.findall("generics/(\S*)/", generic_link)[0]
        med_details['strength'] = extract_with_css('div[title="Strength"] ::text')
        manufacturer_link = extract_with_css('div[title ="Manufactured by"] a ::attr(href)')
        med_details['manufacturer_id'] = re.findall("companies/(\S*)/", manufacturer_link)[0]

        yield med_details
