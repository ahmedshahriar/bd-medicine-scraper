from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from medexbot.spiders.drug_class_spider import DrugClassSpider


class Command(BaseCommand):
    help = "Release the drug class"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(DrugClassSpider)
        process.start()
