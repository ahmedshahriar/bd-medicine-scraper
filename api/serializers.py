from rest_framework import serializers

from crawler.models import Medicine, Generic, DrugClass, DosageForm, Indication, Manufacturer


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'brand_name', 'slug', 'type', 'dosage_form', 'strength', 'manufacturer_id']


class GenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generic
        fields = ['id', 'generic_name', 'slug', 'monograph_link', 'indication_description',
                  'therapeutic_class_description', 'descriptions_count']


class DrugClassSerializer(serializers.ModelSerializer):
    generics = GenericSerializer(many=True, read_only=True)

    class Meta:
        model = DrugClass
        fields = ['id', 'drug_class_id', 'slug', 'drug_class_name', 'generics_count', 'generics']


class IndicationSerializer(serializers.ModelSerializer):
    generics = GenericSerializer(many=True, read_only=True)

    class Meta:
        model = Indication
        fields = ['id', 'indication_id', 'slug', 'indication_name', 'generics_count', 'generics']


class DosageFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = DosageForm
        fields = ['id', 'dosage_form_id', 'slug', 'dosage_form_name', 'brand_names_count']


class ManufacturerSerializer(serializers.ModelSerializer):
    medicines = MedicineSerializer(many=True, read_only=True)

    class Meta:
        model = Manufacturer
        fields = ['id', 'manufacturer_id', 'slug', 'manufacturer_name', 'generics_count', 'brand_names_count', 'medicines']