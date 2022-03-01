import logging
import re

import scrapy
from django.db import IntegrityError
from django.utils.text import slugify

from crawler.models import Generic, Manufacturer
from medexbot.items import MedItem


class MedSpider(scrapy.Spider):
    name = "med"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/brands?page=1', 'https://medex.com.bd/brands?herbal=1&page=1']

    def clean_text(self, raw_html):
        """
        :param raw_html: this will take raw html code
        :return: text without html tags
        """
        cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        return re.sub(cleaner, '', raw_html)

    def parse(self, response):
        for med_info in response.css('a.hoverable-block'):
            # med_page_links = med_info.css('a.hoverable-block ::attr("href") ')
            med_page_links = ['https://medex.com.bd/brands/7701/3rd-cef-100mg',
                              'https://medex.com.bd/brands/9538/3-f-500mg']
            # https://medex.com.bd/brands/7701/3rd-cef-100mg
            # https://medex.com.bd/brands/9538/3-f-500mg
            yield from response.follow_all(med_page_links, self.parse_med)

            # pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
            # yield from response.follow_all(pagination_links, self.parse)

    def parse_med(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        item = MedItem()
        item['brand_id'] = re.findall("brands/(\S*)/", response.url)[0]
        item['brand_name'] = response.css('h1.page-heading-1-l span ::text').getall()[0].strip()
        item['type'] = 'herbal' if response.css(
            'h1.page-heading-1-l img ::attr(alt)').get().strip() == 'Herbal' else 'allopathic'
        item['dosage_form'] = extract_with_css('small.h1-subtitle ::text')
        # generic_name = extract_with_css('div[title="Generic Name"] a ::text')
        item['strength'] = extract_with_css('div[title="Strength"] ::text')

        # generic extraction

        generic_link = extract_with_css('div[title="Generic Name"] a ::attr(href)')
        generic_id = re.findall("generics/(\S*)/", generic_link)[0]
        try:
            item['generic'] = Generic.objects.get(generic_id=generic_id)
        except Generic.DoesNotExist as ge:
            logging.info(ge)
            item['generic'] = None
        except IntegrityError as ie:
            logging.info(ie)
            item['generic'] = None

        # manufacturer extraction

        manufacturer_link = extract_with_css('div[title ="Manufactured by"] a ::attr(href)')
        manufacturer_id = re.findall(r"companies/(\d+)/", manufacturer_link)[0]
        try:
            item['manufacturer'] = Manufacturer.objects.get(manufacturer_id=manufacturer_id)
        except Manufacturer.DoesNotExist as me:
            logging.info(me)
            item['manufacturer'] = None
        except IntegrityError as ie:
            logging.info(ie)
            item['manufacturer'] = None
        # med_details['package_container'] = [self.clean_text(spec_value).strip() for spec_value in response.css(
        # 'div.package-container').getall()]

        # todo : debug package container
        # https://medex.com.bd/brands/7701/3rd-cef-100mg
        # https://medex.com.bd/brands/9538/3-f-500mg
        # check all the dosage forms and add exceptions https://medex.com.bd/dosage-forms

        # todo : debug veterenary
        # https://medex.com.bd/brands/31317/a-mectin-vet-10mg

        # item['package_container'] = ' '.join(extract_with_css('div.package-container ::text').split())
        # item['pack_size_info'] = ' '.join(extract_with_css('span.pack-size-info ::text').split())

        # todo : remove overlapping pack size info
        package_container = ','.join([re.sub(r'\s+', ' ', i).strip() for i in response.css('div.package-container ::text').getall()])
        pack_size_info = ','.join([re.sub(r'\s+', ' ', i).strip() for i in response.css('span.pack-size-info ::text').getall() if i.strip() is not ''])

        item['package_container'] = package_container
        item['pack_size_info'] = pack_size_info

        item['slug'] = slugify(item['brand_name'] + item['dosage_form'] + item['strength'],
                               allow_unicode=True)

        yield item
