# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from crawler.models import Medicine


class MedexbotPipeline:
    def process_item(self, item, spider):
        # try:
        #     question = Medicine.objects.get(identifier=item["identifier"])
        #     print("Question already exist")
        #     return item
        # except Medicine.DoesNotExist:
        #     pass
        #
        # medicine = Medicine()
        # medicine.identifier = item["identifier"]
        # medicine.title = item["title"]
        # medicine.url = item["url"]
        # medicine.save()
        return item
