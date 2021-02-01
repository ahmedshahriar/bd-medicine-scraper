import scrapy


class GenericsSpider(scrapy.Spider):
    name = "generics"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/generics?page=1']

    def parse(self, response):
        generic_page_links = response.css('a.hoverable-block ::attr("href") ')
        yield from response.follow_all(generic_page_links, self.parse_generic)

        pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
        # response.css('span[property="city"]::text').extract_first()
        yield from response.follow_all(pagination_links, self.parse)

    def parse_generic(self, response):

        generics_details = dict()

        generics_details['monograph_link'] = response.css('span.hidden-sm a ::attr(href)').get()
        """ medicine description """
        # ###indications
        generics_details['indications'] = response.css('div#indications h4 ::text').get().strip()
        generics_details['indication_description'] = response.xpath('//div[@id="indications"]/following-sibling::node()[2]').get().strip()

        yield generics_details