import string

from django.contrib import admin

# Register your models here.
from crawler.models import Medicine, Generic, Manufacturer, DosageForm


# https://gist.github.com/ahmedshahriar/4240f0451261c4bb8364dd5341c7cf59
# https://books.agiliq.com/projects/django-admin-cookbook/en/latest/filtering_calculated_fields.html

class AlphabetFilter(admin.SimpleListFilter):
    title = 'Name Alphabetically'
    parameter_name = 'alphabet'

    def lookups(self, request, model_admin):
        abc = list(string.ascii_lowercase)
        return ((c.upper(), c.upper()) for c in abc)

    def queryset(self, request, queryset):
        if self.value() and isinstance(queryset.model, Medicine):
            return queryset.filter(brand_name__startswith=self.value())
        if self.value() and isinstance(queryset.model, Generic):
            return queryset.filter(generic_name__startswith=self.value())
        if self.value() and isinstance(queryset.model, Manufacturer):
            return queryset.filter(manufacturer_name__startswith=self.value())


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('brand_id', 'brand_name', 'dosage_form', 'generic_id', 'get_med_type')
    list_filter = ('generic_id', 'dosage_form', AlphabetFilter, 'type', 'created')
    search_fields = ('brand_name', 'dosage_form')
    prepopulated_fields = {'slug': ('brand_name',)}
    # raw_id_fields = ('generic',)
    date_hierarchy = 'created'
    ordering = ('created',)

    def get_med_type(self, obj):
        if obj.type == 0:
            return 'Allopathic'
        else:
            return 'Herbal'

    get_med_type.short_description = 'Medicine Type'


@admin.register(Generic)
class GenericAdmin(admin.ModelAdmin):
    list_display = ('generic_id', 'generic_name', 'monograph_link', 'descriptions_count')
    list_filter = ('created', 'descriptions_count')
    search_fields = ('generic_name',)
    prepopulated_fields = {'slug': ('generic_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('manufacturer_id', 'manufacturer_name', 'generics_count', 'brand_names_count')
    list_filter = ('created', AlphabetFilter,)
    search_fields = ('manufacturer_name',)
    prepopulated_fields = {'slug': ('manufacturer_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)


@admin.register(DosageForm)
class DosageFormAdmin(admin.ModelAdmin):
    list_display = ('dosage_form_id', 'dosage_form_name', 'brand_names_count')
    list_filter = ('created', AlphabetFilter,)
    search_fields = ('dosage_form_name',)
    prepopulated_fields = {'slug': ('dosage_form_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)
