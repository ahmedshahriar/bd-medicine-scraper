from django.core.management.base import BaseCommand

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from medexbot.spiders.indication_spider import IndicationSpider


class Command(BaseCommand):
    help = "Release the Indication"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(IndicationSpider)
        process.start()
