from django.contrib import admin

# Register your models here.
# Register your models here.
from crawler.models import Medicine


class MedicineAdmin(admin.ModelAdmin):
    list_display = ('brand_id', 'brand_name', 'dosage_form', 'generic_id')


admin.site.register(Medicine, MedicineAdmin)
