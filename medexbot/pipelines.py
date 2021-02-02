# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful links
# https://stackoverflow.com/questions/32743469/scrapy-python-multiple-item-classes-in-one-pipeline
#

# useful for handling different item types with a single interface
import logging

from crawler.models import Medicine, Generic
from medexbot.items import MedItem, GenericItem


class MedexbotPipeline:
    def process_item(self, item, spider):
        logging.info("MedexbotPipeline: Processing item")
        if isinstance(item, MedItem):
            return self.handle_meds(item, spider)
        if isinstance(item, GenericItem):
            return self.handle_generic(item, spider)

    def handle_meds(self, item, spider):
        try:
            medicine = Medicine.objects.get(brand_id=item["brand_id"])
            print("Medicine already exists")
            return item
        except Medicine.DoesNotExist:
            pass
        item.save()
        return item

    def handle_generic(self, item, spider):
        try:
            generic = Generic.objects.get(generic_id=item["generic_id"])
            print("generic already exists")
            return item
        except Generic.DoesNotExist:
            pass
        item.save()
        return item
