from crawler.models import Medicine
from rest_framework import serializers


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'brand_name', 'slug', 'type', 'dosage_form', 'strength', 'manufacturer_id']