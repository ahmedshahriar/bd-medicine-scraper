import logging
import re

import scrapy
from django.db import IntegrityError
from django.utils.text import slugify

from crawler.models import Generic, Indication
from medexbot.items import IndicationItem


class IndicationSpider(scrapy.Spider):
    name = "indication"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/indications?page=1']

    def parse(self, response, **kwargs):
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

    def generic_id_mapping(self, indication, generic_ids):
        # populating indication field in Generic Model
        for generic_id in generic_ids:
            try:
                generic = Generic.objects.get(generic_id=generic_id)
                logging.info("generic indication value inserting...")
                # https://docs.djangoproject.com/en/3.1/ref/models/instances/#specifying-which-fields-to-save
                generic.indication = indication
                generic.save(update_fields=['indication'])
            except Generic.DoesNotExist as ge:
                logging.info(ge)
            except IntegrityError as ie:
                logging.info(ie)

    def parse_indication(self, response):
        generic_ids = None

        item = IndicationItem()
        item['indication_id'] = response.request.meta['indication_id']
        item['indication_name'] = response.request.meta['indication_name']
        item['generics_count'] = response.request.meta['generics_count']
        item['slug'] = slugify(item['indication_name'] + '-' + item['indication_id'],
                               allow_unicode=True)

        try:
            generic_links = response.css('div.data-row-top a ::attr(href)').extract()
            generic_ids = [re.findall("generics/(\S*)/", generic_link)[0] for generic_link in generic_links]
        except IndexError as ie:
            logging.info(ie)

        try:
            indication = Indication.objects.get(indication_id=item["indication_id"])
            print("Indication instance already exists",str(indication.indication_name))
            self.generic_id_mapping(indication, generic_ids)
        except Indication.DoesNotExist:
            indication = item.save()
            print("Indication instance creating...", str(indication.indication_name))
            self.generic_id_mapping(indication, generic_ids)

        yield item
