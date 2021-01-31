# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from itemadapter import ItemAdapter

from crawler.models import Medicine


class MedexbotPipeline:
    def process_item(self, item, spider):
        logging.info("MedexbotPipeline: Processing item")
        try:
            medicine = Medicine.objects.get(brand_id=item["brand_id"])
            print("Medicine already exist")
            return item
        except Medicine.DoesNotExist:
            pass
        item.save()
        return item
