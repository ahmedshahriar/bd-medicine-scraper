from django.contrib import admin

# Register your models here.
from crawler.models import Medicine, Generic


class MedicineAdmin(admin.ModelAdmin):
    list_display = ('brand_id', 'brand_name', 'dosage_form', 'generic_id')
    list_filter = ('generic_id', 'created', 'dosage_form')
    search_fields = ('brand_name', 'dosage_form')
    prepopulated_fields = {'slug': ('brand_name',)}
    # raw_id_fields = ('generic',)
    date_hierarchy = 'created'
    ordering = ('created',)


class GenericAdmin(admin.ModelAdmin):
    list_display = ('generic_id', 'generic_name', 'monograph_link', 'desc_counter')
    list_filter = ('created', 'desc_counter')
    search_fields = ('generic_name', )
    prepopulated_fields = {'slug': ('generic_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)


admin.site.register(Generic, GenericAdmin)

admin.site.register(Medicine, MedicineAdmin)
