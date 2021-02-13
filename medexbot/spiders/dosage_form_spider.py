import re

import scrapy


class DosageFormSpider(scrapy.Spider):
    name = "dosage"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/dosage-forms']


    def parse(self, response):
        for dosage_form_info in response.css('a.hoverable-block')[:30]:
            dosage_form_link = dosage_form_info.css('a.hoverable-block ::attr("href") ').get()
            dosage_form_id = re.findall("dosage-forms/(\S*)/", dosage_form_link)[0]

            dosage_form_name = dosage_form_info.css('div.data-row-top img ::attr("title") ').get()
            brand_names_counter = dosage_form_info.css('div.data-row-company ::text').re(r"(\d+)")
            brand_names_count = 0 if len(brand_names_counter) == 0 else brand_names_counter

            yield from response.follow_all(dosage_form_info.css('a.hoverable-block ::attr("href") '),
                                           self.parse_dosage_form,
                                           meta={"dosage_form_id": dosage_form_id, "dosage_form_name": dosage_form_name,
                                                 "brand_names_count": brand_names_count})

    def parse_dosage_form(self, response):
        dosage_form_id = response.request.meta['dosage_form_id']
        dosage_form_name = response.request.meta['dosage_form_name']
        brand_names_count = response.request.meta['brand_names_count']

        brand_name_links = response.css('a.hoverable-block  ::attr(href)').extract()
        brand_name_ids = [re.findall("brands/(\S*)/", brand_name_link)[0] for brand_name_link in brand_name_links]


        print( {
            "dosage_form_id": dosage_form_id,
            "dosage_form_name": dosage_form_name,
            "brand_names_count": brand_names_count,
            "brand_name_ids": brand_name_ids
        })