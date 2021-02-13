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

