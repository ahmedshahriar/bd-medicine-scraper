import re

import scrapy


class DosageFormSpider(scrapy.Spider):
    name = "dosage"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/dosage-forms']


    def parse(self, response):
        for dosage_form_info in response.css('a.hoverable-block'):
            dosage_form_link = dosage_form_info.css('a.hoverable-block ::attr("href") ').get()
            dosage_form_id = re.findall("dosage-forms/(\S*)/", dosage_form_link)[0]

            dosage_form_name = dosage_form_info.css('div.data-row-top img ::attr("title") ').get()
            stat = dosage_form_info.css('div.data-row-company ::text').extract()[-1].strip()

            yield from response.follow_all(dosage_form_info.css('a.hoverable-block ::attr("href") '),
                                           self.parse_dosage_form,
                                           meta={"dosage_form_id": dosage_form_id, "dosage_form_name": dosage_form_name,
                                                 "stat": stat})

    def parse_dosage_form(self, response):
        dosage_form_id = response.request.meta['dosage_form_id']
        dosage_form_name = response.request.meta['dosage_form_name']
        stat = response.request.meta['stat']

        brand_name_links = response.css('a.hoverable-block  ::attr(href)').extract()
        brand_name_ids = [re.findall("brands/(\S*)/", brand_name_link)[0] for brand_name_link in brand_name_links]

        yield {
            "dosage_form_id": dosage_form_id,
            "dosage_form_name": dosage_form_name,
            "stat": stat,
            "brand_name_ids": brand_name_ids
        }