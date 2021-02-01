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