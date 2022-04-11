from django.test import TestCase
from crawler.models import Medicine, Generic, Manufacturer, DrugClass, Indication, DosageForm


# Tests for the Medicine model
class MedicineTestCase(TestCase):
    def setUp(self):
        # Create a Dosage Form object
        DosageForm.objects.create(dosage_form_name='Test Dosage Form',
                                  slug='test-dosage-form',
                                  brand_names_count=10,
                                  created='2020-01-01',
                                  updated='2020-01-01'
                                  )
        # Create a Drug Class object
        DrugClass.objects.create(drug_class_name='Test Drug Class',
                                 slug='test-drug-class',
                                 generics_count=10,
                                 created='2020-01-01',
                                 updated='2020-01-01'
                                 )
        # Create an Indication object
        Indication.objects.create(indication_name='Test Indication',
                                  slug='test-indication',
                                  generics_count=10,
                                  created='2020-01-01',
                                  updated='2020-01-01'
                                  )

        # Create a Generic object
        Generic.objects.create(generic_name='Test Generic',
                               slug='test-generic-slug',
                               monograph_link='https://www.google.com',
                               drug_class=DrugClass.objects.get(drug_class_name='Test Drug Class'),
                               indication=Indication.objects.get(indication_name='Test Indication'),
                               indication_description='Test Indication Description',
                               therapeutic_class_description='Test Therapeutic Class Description',
                               pharmacology_description='Test Pharmacological Description',
                               dosage_description='Test Dosage Description',
                               administration_description='Test Administration Description',
                               interaction_description='Test Interaction Description',
                               contraindications_description='Test Contraindications Description',
                               side_effects_description='Test Side Effects Description',
                               pregnancy_and_lactation_description='Test Pregnancy and Lactation Description',
                               precautions_description='Test Precautions Description',
                               pediatric_usage_description='Test Pediatric Usage Description',
                               overdose_effects_description='Test Overdose Effects Description',
                               duration_of_treatment_description='Test Duration of Treatment Description',
                               reconstitution_description='Test Reconstitution Description',
                               storage_conditions_description='Test Storage Conditions Description',
                               descriptions_count=1,
                               created='2019-01-01',
                               updated='2019-01-01'
                               )
        # Create a Manufacturer object
        Manufacturer.objects.create(manufacturer_name='Test Manufacturer',
                                    slug='test-manufacturer',
                                    generics_count=10,
                                    brand_names_count=10,
                                    created='2019-01-01',
                                    updated='2019-01-01'
                                    )
        # Create a medicine object
        Medicine.objects.create(brand_name='Test Medicine',
                                type='Allopathic',
                                slug='test-medicine',
                                dosage_form='Test Dosage Form',
                                generic=Generic.objects.get(generic_name='Test Generic'),
                                strength='Test Strength',
                                manufacturer=Manufacturer.objects.get(manufacturer_name='Test Manufacturer'),
                                package_container='Test Package Container',
                                pack_size_info='Test Package Size',
                                created='2019-01-01',
                                updated='2019-01-01'
                                )

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

    def test_generic_content(self):
        generic = Generic.objects.get(generic_name='Test Generic')
        self.assertEqual(generic.generic_name, 'Test Generic')
        self.assertEqual(str(generic), 'Test Generic')
