# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from crawler.models import Medicine
from medexbot.items import MedItem


class MedexbotPipeline:
    def process_item(self, item, spider):
        if isinstance(item, MedItem):
            return self.handleMeds(item, spider)
        logging.info("MedexbotPipeline: Processing item")


    def handleMeds(self, item, spider):
        try:
            medicine = Medicine.objects.get(brand_id=item["brand_id"])
            print("Medicine already exists")
            return item
        except Medicine.DoesNotExist:
            pass
        item.save()
        return item
