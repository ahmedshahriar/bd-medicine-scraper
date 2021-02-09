from django.contrib import admin

# Register your models here.
from crawler.models import Medicine, Generic


class MedicineAdmin(admin.ModelAdmin):
    list_display = ('brand_id', 'brand_name', 'dosage_form', 'generic_id')


class GenericAdmin(admin.ModelAdmin):
    list_display = ('generic_id', 'generic_name', 'monograph_link', 'indication_description')


admin.site.register(Generic, GenericAdmin)

admin.site.register(Medicine, MedicineAdmin)
