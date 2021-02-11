import string

from django.contrib import admin

# Register your models here.
from crawler.models import Medicine, Generic, Manufacturer


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
    list_display = ('brand_id', 'brand_name', 'dosage_form', 'generic_id')
    list_filter = ('generic_id', 'created', 'dosage_form', AlphabetFilter,)
    search_fields = ('brand_name', 'dosage_form')
    prepopulated_fields = {'slug': ('brand_name',)}
    # raw_id_fields = ('generic',)
    date_hierarchy = 'created'
    ordering = ('created',)


@admin.register(Generic)
class GenericAdmin(admin.ModelAdmin):
    list_display = ('generic_id', 'generic_name', 'monograph_link', 'desc_counter')
    list_filter = ('created', 'desc_counter')
    search_fields = ('generic_name',)
    prepopulated_fields = {'slug': ('generic_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('manufacturer_id', 'manufacturer_name', 'generics', 'brand_names')
    list_filter = ('created', AlphabetFilter,)
    search_fields = ('manufacturer_name',)
    prepopulated_fields = {'slug': ('manufacturer_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)
