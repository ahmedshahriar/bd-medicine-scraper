from django.db import models

# Create your models here.
from django.db.models.functions import Length


class Medicine(models.Model):
    brand_id = models.IntegerField(blank=False, null=False, unique=True)
    brand_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    dosage_form = models.CharField(max_length=255)
    generic_id = models.IntegerField()
    strength = models.CharField(max_length=255)
    manufacturer_id = models.IntegerField()
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


class Generic(models.Model):
    generic_id = models.IntegerField(blank=False, null=False, unique=True)
    generic_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    monograph_link = models.TextField(null=True, blank=True)

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
    desc_counter = models.IntegerField(default=0)

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
                          self.precautions_description,self.pregnancy_and_lactation_description,
                          self.pediatric_usage_description,self.overdose_effects_description,
                          self.duration_of_treatment_description,self.reconstitution_description,
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
