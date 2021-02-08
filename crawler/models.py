from django.db import models


# Create your models here.
class Medicine(models.Model):
    brand_id = models.IntegerField(max_length=20, blank=False, null=False, unique=True)
    brand_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    dosage_form = models.CharField(max_length=255)
    generic_id = models.IntegerField(max_length=20)
    strength = models.CharField(max_length=255)
    manufacturer_id = models.IntegerField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('brand_name',)

    def __str__(self):
        return self.brand_name


class Generic(models.Model):
    generic_id = models.IntegerField(max_length=20, blank=False, null=False, unique=True)
    generic_name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    monograph_link = models.TextField()
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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('generic_name',)

    def __str__(self):
        return self.generic_name
