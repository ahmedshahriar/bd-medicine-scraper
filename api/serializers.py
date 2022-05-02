from rest_framework import serializers

from crawler.models import Medicine, Generic, DrugClass, DosageForm, Indication, Manufacturer


class MedicineSerializer(serializers.ModelSerializer):
    generic_name = serializers.ReadOnlyField(source='generic.generic_name', read_only=True)
    manufacturer_name = serializers.ReadOnlyField(source='manufacturer.manufacturer_name', read_only=True)

    class Meta:
        model = Medicine
        # read_only_fields = ('id', 'generic_name', 'manufacturer_name')
        # fields = ['id', 'brand_name', 'slug', 'type', 'dosage_form', 'generic_name', 'strength', 'manufacturer_name']
        exclude = ('created', 'updated', 'generic', 'manufacturer')


class GenericSerializer(serializers.ModelSerializer):
    medicines = MedicineSerializer(many=True, read_only=True)

    class Meta:
        model = Generic
        exclude = ('created', 'updated')


class DrugClassSerializer(serializers.ModelSerializer):
    # generics = GenericSerializer(many=True, read_only=True)

    class Meta:
        model = DrugClass
        fields = ['id', 'drug_class_id', 'slug', 'drug_class_name', 'generics_count',
                  # 'generics'
                  ]
        # exclude = ('created', 'updated') # medicines, generics


class IndicationSerializer(serializers.ModelSerializer):
    generics = GenericSerializer(many=True, read_only=True)

    class Meta:
        model = Indication
        # fields = ['id', 'indication_id', 'slug', 'indication_name', 'generics_count', 'generics']
        exclude = ('created', 'updated') # medicines


class DosageFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = DosageForm
        # fields = ['id', 'dosage_form_id', 'slug', 'dosage_form_name', 'brand_names_count']
        exclude = ('created', 'updated')


class ManufacturerSerializer(serializers.ModelSerializer):
    medicines = MedicineSerializer(many=True, read_only=True)

    class Meta:
        model = Manufacturer
        # fields = ['id', 'manufacturer_id', 'slug', 'manufacturer_name', 'generics_count', 'brand_names_count',
        #           'medicines']
        exclude = ('created', 'updated')  # medicines
