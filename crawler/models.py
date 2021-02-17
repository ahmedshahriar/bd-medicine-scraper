from django.db import models


# Create your models here.

class DrugClass(models.Model):
    drug_class_id = models.IntegerField(blank=False, null=True, unique=True)
    drug_class_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    generics_count = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('drug_class_name',)
        verbose_name = "drug class"
        verbose_name_plural = 'drug classes'

    def __str__(self):
        return self.drug_class_name


class DosageForm(models.Model):
    dosage_form_id = models.IntegerField(blank=False, null=True, unique=True)
    dosage_form_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    brand_names_count = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('dosage_form_name',)
        verbose_name = "dosage form"
        verbose_name_plural = 'dosage forms'

    def __str__(self):
        return self.dosage_form_name


class Indication(models.Model):
    indication_id = models.IntegerField(blank=False, null=True, unique=True)
    indication_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    generics_count = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('indication_name',)
        verbose_name = "indication"
        verbose_name_plural = 'indications'

    def __str__(self):
        return self.indication_name


class Generic(models.Model):
    generic_id = models.IntegerField(blank=False, null=True, unique=True)
    generic_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    monograph_link = models.TextField(null=True, blank=True)

    drug_class = models.ForeignKey(DrugClass, on_delete=models.CASCADE, related_name='drug_classes', null=True)

    indication = models.ForeignKey(Indication, on_delete=models.CASCADE, related_name='indications', null=True)

    indication_description = models.TextField(null=True, blank=True)
    therapeutic_class_description = models.TextField(null=True, blank=True)
    pharmacology_description = models.TextField(null=True, blank=True)
    dosage_description = models.TextField(null=True, blank=True)
    administration_description = models.TextField(null=True, blank=True)
    interaction_description = models.TextField(null=True, blank=True)
    contraindications_description = models.TextField(null=True, blank=True)
    side_effects_description = models.TextField(null=True, blank=True)
    pregnancy_and_lactation_description = models.TextField(null=True, blank=True)
    precautions_description = models.TextField(null=True, blank=True)
    pediatric_usage_description = models.TextField(null=True, blank=True)
    overdose_effects_description = models.TextField(null=True, blank=True)
    duration_of_treatment_description = models.TextField(null=True, blank=True)
    reconstitution_description = models.TextField(null=True, blank=True)
    storage_conditions_description = models.TextField(null=True, blank=True)

    # counter for sum of all description
    descriptions_count = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('generic_name',)
        verbose_name = "generic"
        verbose_name_plural = 'generics'
        indexes = [
            models.Index(fields=['generic_name'], name='%(app_label)s_%(class)s_name_index'),
        ]

    def save(self, *args, **kwargs):
        try:
            class_attr = (self.indication_description, self.therapeutic_class_description,
                          self.pharmacology_description, self.dosage_description,
                          self.administration_description, self.interaction_description,
                          self.contraindications_description, self.side_effects_description,
                          self.precautions_description, self.pregnancy_and_lactation_description,
                          self.pediatric_usage_description, self.overdose_effects_description,
                          self.duration_of_treatment_description, self.reconstitution_description,
                          self.storage_conditions_description)
            self.desc_counter = sum([1 if len(str(x)) > 4 else 0 for x in class_attr])
            super(Generic, self).save(*args, **kwargs)
        except Exception as e:
            pass

    # todo best approach to save and store counter value
    # @property
    # def desc_count(self):
    #     class_attr = (self.indication_description, self.therapeutic_class_description, self.pharmacology_description,
    #                   self.dosage_description, self.administration_description, self.interaction_description,
    #                   self.contraindications_description, self.side_effects_description, self.precautions_description,
    #                   self.pregnancy_and_lactation_description, self.pediatric_usage_description,
    #                   self.overdose_effects_description, self.duration_of_treatment_description,
    #                   self.reconstitution_description, self.storage_conditions_description)
    #     desc = sum([1 if len(str(x)) > 4 else 0 for x in class_attr])
    #     # desc = 1 if len(str(self.administration_description).strip()) >= 1 else 0
    #     # desc = 1 if len(str(self.administration_description).strip()) > 4 else 0
    #     return desc
    # # rename property : https://stackoverflow.com/questions/7241000/django-short-description-for-property
    # desc_count.fget.short_description = 'Descriptions Count'

    def __str__(self):
        return self.generic_name


class Manufacturer(models.Model):
    manufacturer_id = models.IntegerField(blank=False, null=True, unique=True)
    manufacturer_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    generics_count = models.IntegerField()
    brand_names_count = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('manufacturer_name',)
        verbose_name = "manufacturer"
        verbose_name_plural = 'manufacturers'
        indexes = [
            models.Index(fields=['manufacturer_name'], name='%(app_label)s_MANF_name_index'),
        ]

    def __str__(self):
        return self.manufacturer_name





class Medicine(models.Model):
    brand_id = models.IntegerField(blank=False, null=True, unique=True)
    brand_name = models.CharField(max_length=255, blank=False, null=False)
    type = models.IntegerField(blank=False, null=False, default=0)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    # dosage_form = models.ForeignKey(DosageForm, on_delete=models.CASCADE, related_name='dosage_forms', null=True)
    dosage_form = models.CharField(max_length=255)
    generic = models.ForeignKey(Generic, on_delete=models.CASCADE, related_name='medicines', null=True)
    # generic_id = models.IntegerField()
    strength = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='medicines', null=True)
    # manufacturer_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('brand_name',)
        verbose_name = "medicine"
        verbose_name_plural = 'medicines'
        indexes = [
            models.Index(fields=['brand_name'], name='%(app_label)s_%(class)s_name_index'),
        ]

    def __str__(self):
        return self.brand_name
