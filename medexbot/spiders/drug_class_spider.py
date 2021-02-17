import logging
import re

import scrapy
from django.db import IntegrityError

from crawler.models import Generic, DrugClass
from medexbot.items import DrugClassItem


class DrugClassSpider(scrapy.Spider):
    name = "drug_class"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/drug-classes']

    def parse(self, response):
        # todo fetch all drug classes' links
        # print(response.css('a[target="_blank"] ::attr("href")').getall())
        # print(response.css('li.sc-2-list-item').getall())
        for drug_class in response.css('a[target="_blank"]'):
            drug_class_link = drug_class.css('a ::attr("href") ').get()
            drug_class_id = re.findall("drug-classes/(\S*)/", drug_class_link)[0]
            drug_class_name = drug_class.css('a ::text').get()
            # print(drug_class_id, drug_class_name,drug_class_link)
            yield from response.follow_all(drug_class.css('a ::attr("href") '), self.parse_drug_generic,
                                           meta={"drug_class_id": drug_class_id, "drug_class_name": drug_class_name})

    # todo debug this drug class
    # https://medex.com.bd/drug-classes/618/other-antibiotic

    def generic_id_mapping(self, drug_class, generic_ids):
        for generic_id in generic_ids:
            try:
                generic = Generic.objects.get(generic_id=generic_id)
                logging.info("generic drug class value inserting")
                # https://docs.djangoproject.com/en/3.1/ref/models/instances/#specifying-which-fields-to-save
                generic.drug_class = drug_class
                generic.save(update_fields=['drug_class'])
            except Generic.DoesNotExist as ge:
                logging.info(ge)
            except IntegrityError as ie:
                logging.info(ie)

    def parse_drug_generic(self, response):
        generic_ids = None
        item = DrugClassItem()
        item['drug_class_id'] = response.request.meta['drug_class_id']
        item['drug_class_name'] = response.request.meta['drug_class_name']
        item['generics_count'] = len(response.css('a.hoverable-block'))

        try:
            generic_links = response.css('a.hoverable-block  ::attr(href)').extract()
            generic_ids = [re.findall("generics/(\S*)/", generic_link)[0] for generic_link in generic_links]
        except IndexError as ie:
            logging.info(ie)

        try:
            drug_class = DrugClass.objects.get(drug_class_id=item["drug_class_id"])
            # print("Drug Class already exists",str(drug_class.drug_class_name))
            self.generic_id_mapping(drug_class, generic_ids)
        except DrugClass.DoesNotExist:
            drug_class = item.save()
            # print("Drug Class creating...", str(drug_class.drug_class_name))
            self.generic_id_mapping(drug_class, generic_ids)

        # yield item
