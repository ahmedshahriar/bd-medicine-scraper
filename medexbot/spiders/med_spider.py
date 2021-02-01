import re

import scrapy

from medexbot.items import MedItem


class MedSpider(scrapy.Spider):
    name = "med"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/brands?page=1']

    def clean_text(self, raw_html):
        """
        :param raw_html: this will take raw html code
        :return: text without html tags
        """
        cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        return re.sub(cleaner, '', raw_html)

    def parse(self, response):
        for med_info in response.css('a.hoverable-block'):
            med_page_links = med_info.css('a.hoverable-block ::attr("href") ')
            yield from response.follow_all(med_page_links, self.parse_med)

            # pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
            # yield from response.follow_all(pagination_links, self.parse)

    def parse_med(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        med_details = dict()
        med_details['brand_id'] = re.findall("brands/(\S*)/", response.url)[0]
        med_details['brand_name'] = response.css('h1.page-heading-1-l span ::text').getall()[0].strip()
        med_details['dosage_form'] = extract_with_css('small.h1-subtitle ::text')
        # generic_name = extract_with_css('div[title="Generic Name"] a ::text')
        generic_link = extract_with_css('div[title="Generic Name"] a ::attr(href)')
        med_details['generic_id'] = re.findall("generics/(\S*)/", generic_link)[0]
        # med_details['strength'] = extract_with_css('div[title="Strength"] ::text')
        # manufacturer_link = extract_with_css('div[title ="Manufactured by"] a ::attr(href)')
        # med_details['manufacturer_id'] = re.findall("companies/(\S*)/", manufacturer_link)[0]
        # med_details['package_container'] = [self.clean_text(spec_value).strip() for spec_value in response.css(
        # 'div.package-container').getall()]


        # todo : debug package container
        # https://medex.com.bd/brands/7701/3rd-cef-100mg
        # https://medex.com.bd/brands/9538/3-f-500mg

        # med_details['package_container'] = extract_with_css('div.package-container ::text ')
        # med_details['pack_size_info'] = extract_with_css('span.pack-size-info ::text')

        # yield med_details
        item = MedItem()
        item['brand_id'] = med_details['brand_id']
        item['brand_name'] = med_details['brand_name']
        item['dosage_form'] = med_details['dosage_form']
        item['generic_id'] = med_details['generic_id']
        yield item
