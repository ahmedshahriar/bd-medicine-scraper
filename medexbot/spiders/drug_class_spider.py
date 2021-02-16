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
        for drug_class in response.css('li.sc-2-list-item'):
            drug_class_link = drug_class.css('a ::attr("href") ').get()
            drug_class_id = re.findall("drug-classes/(\S*)/", drug_class_link)[0]
            drug_class_name = drug_class.css('a ::text').get()

            yield from response.follow_all(drug_class.css('a ::attr("href") '), self.parse_drug_generic,
                                           meta={"drug_class_id": drug_class_id, "drug_class_name": drug_class_name})
    # todo debug this drug class
    # https://medex.com.bd/drug-classes/618/other-antibiotic

    def parse_drug_generic(self, response):
        item = DrugClassItem()
        item['drug_class_id'] = response.request.meta['drug_class_id']
        item['drug_class_name'] = response.request.meta['drug_class_name']
        item['generics_count'] = len(response.css('a.hoverable-block'))
        item.save()

        drug_class = None
        try:
            drug_class = DrugClass.objects.get(drug_class_id=item["drug_class_id"])
            logging.info("Drug Class already exists")
        except DrugClass.DoesNotExist:
            pass

        # drug_class = item.save()
        # print(drug_class)
        # todo generic ids mapping
        generic_links = response.css('a.hoverable-block  ::attr(href)').extract()
        generic_ids = [re.findall("generics/(\S*)/", generic_link)[0] for generic_link in generic_links]

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

        # yield item
