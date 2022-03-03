import logging
import re
import time

import scrapy
from django.db import IntegrityError
from django.utils.text import slugify

from crawler.models import Generic, Manufacturer
from medexbot.items import MedItem, GenericItem


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

    def parse(self, response, **kwargs):
        # for med_info in response.css('a.hoverable-block'):
        #     med_page_links = med_info.css('a.hoverable-block ::attr("href") ')
        med_page_links = ['https://medex.com.bd/brands/31677/cefa-1-vet-75gm']
        yield from response.follow_all(med_page_links, self.parse_med)

        # pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
        # yield from response.follow_all(pagination_links, self.parse)

    def parse_generic(self, response):
        item = GenericItem()
        item['generic_id'] = re.findall("generics/(\S*)/", response.url)[0]
        item['generic_name']= response.css('h1.page-heading-1-l ::text').get().strip()
        item['monograph_link'] = response.css('span.hidden-sm a ::attr(href)').get()
        """ medicine description """
        # indications
        # generic_details['indications'] = response.css('div#indications h4 ::text').get().strip()
        item['indication_description'] = response.xpath(
            '//div[@id="indications"]/following-sibling::node()[2]').get().strip()

        # ###Therapeutic Class
        # therapeutic_class = extract_with_css('div#drug_classes h4 ::text')
        item['therapeutic_class_description'] = response.xpath(
            '//div[@id="drug_classes"]/following-sibling::node()[2]').get()

        # ###Pharmacology
        # pharmacology = extract_with_css('div#mode_of_action h4 ::text')
        item['pharmacology_description'] = response.xpath(
            '//div[@id="mode_of_action"]/following-sibling::node()[2]').get()

        # ##Dosage
        # dosage = extract_with_css('div#dosage h4 ::text')
        item['dosage_description'] = response.xpath('//div[@id="dosage"]/following-sibling::node()[2]').get()

        # ##Administration
        # administration = extract_with_css('div#administration h4 ::text')
        item['administration_description'] = response.xpath(
            '//div[@id="administration"]/following-sibling::node()[2]').get()

        # ##Interaction
        # interaction = extract_with_css('div#interaction h4 ::text')
        item['interaction_description'] = response.xpath(
            '//div[@id="interaction"]/following-sibling::node()[2]').get()

        # ##Contraindications
        # contraindications = extract_with_css('div#contraindications h4 ::text')
        item['contraindications_description'] = response.xpath(
            '//div[@id="contraindications"]/following-sibling::node()[2]').get()

        # ##Side Effects
        # side_effects = extract_with_css('div#side_effects h4 ::text')
        item['side_effects_description'] = response.xpath(
            '//div[@id="side_effects"]/following-sibling::node()[2]').get()

        # ##Pregnancy & Lactation
        # pregnancy_and_lactation = extract_with_css('div#pregnancy_cat h4 ::text')
        item['pregnancy_and_lactation_description'] = response.xpath(
            '//div[@id="pregnancy_cat"]/following-sibling::node()[2]').get()

        # ## Precautions
        # precautions = extract_with_css('div#precautions h4 ::text')
        item['precautions_description'] = response.xpath(
            '//div[@id="precautions"]/following-sibling::node()[2]').get()

        # ## Use in Special Populations
        # pediatric_usage = extract_with_css('div#pediatric_uses h4 ::text')
        item['pediatric_usage_description'] = response.xpath(
            '//div[@id="pediatric_uses"]/following-sibling::node()[2]').get()

        # ##Overdose Effects
        # overdose_effects = extract_with_css('div#overdose_effects h4 ::text')
        item['overdose_effects_description'] = response.xpath(
            '//div[@id="overdose_effects"]/following-sibling::node()[2]').get()

        # ##Duration of treatment
        # duration_of_treatment = extract_with_css('div#duration_of_treatment h4 ::text')
        item['duration_of_treatment_description'] = response.xpath(
            '//div[@id="duration_of_treatment"]/following-sibling::node()[2]').get()

        # ##Reconstitution
        # reconstitution = extract_with_css('div#reconstitution h4 ::text')
        item['reconstitution_description'] = response.xpath(
            '//div[@id="reconstitution"]/following-sibling::node()[2]').get()

        # ##Storage Conditions
        # storage_conditions = extract_with_css('div#storage_conditions h4 ::text')
        item['storage_conditions_description'] = response.xpath(
            '//div[@id="storage_conditions"]/following-sibling::node()[2]').get()

        item['slug'] = slugify(item['generic_name'] + '-' + item['generic_id'],
                               allow_unicode=True)
        yield item

    def parse_med(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        item = MedItem()
        item['brand_id'] = re.findall(r"brands/(\S*)/", response.url)[0]
        item['brand_name'] = response.css('h1.page-heading-1-l span ::text').getall()[0].strip()
        item['type'] = 'herbal' if response.css(
            'h1.page-heading-1-l img ::attr(alt)').get().strip() == 'Herbal' else 'allopathic'
        item['dosage_form'] = extract_with_css('small.h1-subtitle ::text')
        # generic_name = extract_with_css('div[title="Generic Name"] a ::text')
        item['strength'] = extract_with_css('div[title="Strength"] ::text')

        # manufacturer extraction

        manufacturer_link = extract_with_css('div[title ="Manufactured by"] a ::attr(href)')
        manufacturer_id = re.findall(r"companies/(\d+)/", manufacturer_link)[0]
        manufacturer_name = extract_with_css('div[title ="Manufactured by"] a ::text')
        try:
            item['manufacturer'] = Manufacturer.objects.get(manufacturer_id=manufacturer_id)
        except Manufacturer.DoesNotExist as me:
            logging.info(me)
            item['manufacturer'] = Manufacturer.objects.create(manufacturer_id=manufacturer_id,
                                                               manufacturer_name=manufacturer_name,
                                                               slug=slugify(manufacturer_name + '-' +
                                                                            manufacturer_id,
                                                                            allow_unicode=True))
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
        package_container = ','.join(
            [re.sub(r'\s+', ' ', i).strip() for i in response.css('div.package-container ::text').getall()])
        pack_size_info = ','.join(
            [re.sub(r'\s+', ' ', i).strip() for i in response.css('span.pack-size-info ::text').getall() if
             i.strip() is not ''])

        item['package_container'] = package_container
        item['pack_size_info'] = pack_size_info

        item['slug'] = slugify(item['brand_name'] + item['dosage_form'] + item['strength'],
                               allow_unicode=True)
        # generic extraction

        generic_link = extract_with_css('div[title="Generic Name"] a ::attr(href)')
        generic_id = re.findall(r"generics/(\S*)/", generic_link)[0]

        try:
            item['generic'] = Generic.objects.get(generic_id=generic_id)
        except Generic.DoesNotExist as ge:
            logging.info(ge)
            with open('generic_id.txt', 'a') as f:
                f.write(item['brand_id']+','+generic_id + '\n')

            yield response.follow(generic_link, self.parse_generic)
            item['generic'] = None
        except IntegrityError as ie:
            logging.info(ie)
            item['generic'] = None

        yield item
