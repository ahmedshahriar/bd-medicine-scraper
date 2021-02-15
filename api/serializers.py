from crawler.models import Medicine
from rest_framework import serializers


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'title', 'slug', 'brand_name', 'type', 'dosage_form', 'strength', '' ]