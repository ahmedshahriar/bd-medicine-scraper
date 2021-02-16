from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from medexbot.spiders.dosage_form_spider import DosageFormSpider


class Command(BaseCommand):
    help = "Release the Dosage Form spider"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(DosageFormSpider)
        process.start()
