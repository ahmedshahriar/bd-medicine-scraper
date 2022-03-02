from django.test import TestCase
from crawler.models import Medicine, Generic, Manufacturer, DrugClass, Indication, DosageForm


# Tests for the Medicine model
class MedicineTestCase(TestCase):
    def setUp(self):
        Medicine.objects.create(brand_name='Test Medicine',
                                generic=Generic.objects.create(generic_name='Test Generic'),
                                manufacturer=Manufacturer.objects.create(manufacturer_name='Test Manufacturer',
                                                                         generics_count=1,
                                                                         brand_names_count=1),
                                dosage_form='Test Dosage Form')

    def test_medicine_content(self):
        medicine = Medicine.objects.get(brand_name='Test Medicine')
        generic = Generic.objects.get(generic_name='Test Generic')
        manufacturer = Manufacturer.objects.get(manufacturer_name='Test Manufacturer')
        dosage_form = f'{medicine.dosage_form}'
        self.assertEqual(medicine.brand_name, 'Test Medicine')
        self.assertEqual(medicine.generic, generic)
        self.assertEqual(medicine.manufacturer, manufacturer)
        self.assertEqual(medicine.dosage_form, dosage_form)
        self.assertEqual(str(medicine), 'Test Medicine')  # or self.assertEqual(medicine.__str__(), 'Test Medicine')
        self.assertEqual(str(generic), 'Test Generic')
        self.assertEqual(str(manufacturer), 'Test Manufacturer')
