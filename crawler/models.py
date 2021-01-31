from django.db import models


# Create your models here.
class Medicine(models.Model):
    brand_id = models.IntegerField()
    brand_name = models.CharField(max_length=255)
    dosage_form = models.CharField(max_length=255)
    generic_id = models.IntegerField()

    def __str__(self):
        return self.brand_name


