import logging
import os

from django.core.management.base import BaseCommand
from crawler.models import Generic, Medicine


class Command(BaseCommand):
    help = "Mapping the generics with medicines"

    def handle(self, *args, **options):
        print("Mapping the generics with medicines")
        with open("generic_id.txt", "r") as f:
            print("Reading the file")
            for line in f:
                brand_id, generic_id = line.split(",")
                try:
                    generic = Generic.objects.get(generic_id=generic_id)
                    medicine = Medicine.objects.get(brand_id=brand_id)
                    medicine.generic = generic
                    medicine.save()
                except Exception as ge:
                    logging.info(ge)
