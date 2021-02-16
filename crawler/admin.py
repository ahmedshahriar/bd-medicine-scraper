import string

from django.contrib import admin
# Register your models here.
from crawler.models import Medicine, Generic, Manufacturer, DosageForm, Indication, DrugClass


# change selection list count
# https://stackoverflow.com/questions/36474515/how-to-get-filtered-queryset-in-django-admin/36476084#36476084

# filtering
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
    list_display = ('brand_id', 'brand_name', 'dosage_form', 'generic', 'manufacturer', 'get_med_type')
    list_filter = ('generic_id', 'dosage_form', AlphabetFilter, 'type', 'created')
    search_fields = ('brand_name', 'dosage_form')
    prepopulated_fields = {'slug': ('brand_name',)}
    raw_id_fields = ('generic', 'manufacturer')
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


@admin.register(Indication)
class IndicationAdmin(admin.ModelAdmin):
    list_display = ('indication_id', 'indication_name', 'generics_count')
    list_filter = ('created', AlphabetFilter,)
    search_fields = ('indication_name',)
    prepopulated_fields = {'slug': ('indication_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)


@admin.register(DrugClass)
class DrugClassAdmin(admin.ModelAdmin):
    list_display = ('drug_class_id', 'drug_class_name', 'generics_count')
    list_filter = ('created', AlphabetFilter,)
    search_fields = ('drug_class_name',)
    prepopulated_fields = {'slug': ('drug_class_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)
