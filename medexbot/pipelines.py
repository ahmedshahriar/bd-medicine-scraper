# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful links
# https://stackoverflow.com/questions/32743469/scrapy-python-multiple-item-classes-in-one-pipeline
#

# useful for handling different item types with a single interface
import logging

from crawler.models import Medicine, Generic, Manufacturer, DosageForm, Indication, DrugClass
from medexbot.items import MedItem, GenericItem, ManufacturerItem, DosageFormItem, IndicationItem, DrugClassItem


class MedexbotPipeline:
    def process_item(self, item, spider):
        logging.info("MedexbotPipeline: Processing item")
        if isinstance(item, MedItem):
            return self.handle_meds(item, spider)
        if isinstance(item, GenericItem):
            return self.handle_generic(item, spider)
        if isinstance(item, ManufacturerItem):
            return self.handle_manufacturer(item, spider)
        if isinstance(item, DosageFormItem):
            return self.handle_dosage_form(item, spider)
        if isinstance(item, IndicationItem):
            return self.handle_indication(item, spider)
        # if isinstance(item, DrugClassItem):
        #     return self.handle_drug_class(item, spider)

    def handle_meds(self, item, spider):
        try:
            medicine = Medicine.objects.get(brand_id=item["brand_id"])
            logging.info("Medicine already exists")
            return item
        except Medicine.DoesNotExist:
            pass
        item.save()
        return item

    def handle_generic(self, item, spider):
        try:
            generic = Generic.objects.get(generic_id=item["generic_id"])
            logging.info("generic already exists")
            return item
        except Generic.DoesNotExist:
            pass
        item.save()
        return item

    def handle_manufacturer(self, item, spider):
        try:
            manufacturer = Manufacturer.objects.get(manufacturer_id=item["manufacturer_id"])
            logging.info("generic already exists")
            return item
        except Manufacturer.DoesNotExist:
            pass
        item.save()
        return item

    def handle_dosage_form(self, item, spider):
        try:
            dosage_form = DosageForm.objects.get(dosage_form_id=item["dosage_form_id"])
            logging.info("dosage form already exists")
            return item
        except DosageForm.DoesNotExist:
            pass
        item.save()
        return item

    def handle_indication(self, item, spider):
        try:
            indication = Indication.objects.get(indication_id=item["indication_id"])
            logging.info("indication already exists")
            return item
        except Indication.DoesNotExist:
            pass
        item.save()
        return item

    # def handle_drug_class(self, item, spider):
    #     try:
    #         drug_class = DrugClass.objects.get(drug_class_id=item["drug_class_id"])
    #         logging.info("Drug Class already exists")
    #         return item
    #     except DrugClass.DoesNotExist:
    #         pass
    #     item.save()
    #     return item
