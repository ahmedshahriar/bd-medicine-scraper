import re

import scrapy
from django.utils.text import slugify

from medexbot.items import GenericItem


class GenericSpider(scrapy.Spider):
    name = "generic"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/generics?page=1', 'https://medex.com.bd/generics?herbal=1']

    def parse(self, response):
        generic_page_links = response.css('a.hoverable-block ::attr("href") ')
        yield from response.follow_all(generic_page_links, self.parse_generic)

        # pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
        # yield from response.follow_all(pagination_links, self.parse)

    def parse_generic(self, response):
        item = GenericItem()

        item['generic_id'] = re.findall("generics/(\S*)/", response.url)[0]
        item['generic_name'] = response.css('h1.page-heading-1-l ::text').get().strip()
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
