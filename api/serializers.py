from crawler.models import Medicine, Generic, Manufacturer
from rest_framework import serializers


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'brand_name', 'slug', 'type', 'dosage_form', 'strength', 'manufacturer_id']


class GenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generic
        fields = ['id', 'generic_name', 'slug', 'monograph_link', 'indication_description', 'therapeutic_class_description', 'descriptions_count']