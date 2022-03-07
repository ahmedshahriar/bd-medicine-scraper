import csv
import datetime
import string

from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter

from django.http import HttpResponse

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
        if self.value() and (queryset.model is Medicine):
            return queryset.filter(brand_name__startswith=self.value())
        if self.value() and (queryset.model is Generic):
            return queryset.filter(generic_name__startswith=self.value())
        if self.value() and (queryset.model is Manufacturer):
            return queryset.filter(manufacturer_name__startswith=self.value())


class MedicineItemInline(admin.StackedInline):
    model = Medicine


class GenericItemInline(admin.TabularInline):
    model = Generic


def export_to_csv(model_admin, request, queryset):
    opts = model_admin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many \
              and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


class GenericFilter(AutocompleteFilter):
    title = 'Generic'  # display title
    field_name = 'generic'  # name of the foreign key field


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('brand_id', 'brand_name', 'dosage_form', 'generic', 'manufacturer', 'type')
    list_filter = (GenericFilter, AlphabetFilter, 'type', 'created', 'dosage_form', )
    search_fields = ('brand_name', 'dosage_form')
    prepopulated_fields = {'slug': ('brand_name',)}
    raw_id_fields = ('generic', 'manufacturer')
    date_hierarchy = 'created'
    ordering = ('created',)
    actions = [export_to_csv]


@admin.register(Generic)
class GenericAdmin(admin.ModelAdmin):
    list_display = ('generic_id', 'generic_name', 'monograph_link', 'drug_class', 'indication', 'descriptions_count')
    list_filter = ('created', 'descriptions_count', AlphabetFilter)
    search_fields = ('generic_name',)
    prepopulated_fields = {'slug': ('generic_name',)}
    raw_id_fields = ('drug_class', 'indication')
    date_hierarchy = 'created'
    ordering = ('created',)
    actions = [export_to_csv]
    # readonly_fields = ('desc_count',) # add `desc_count` to list_display to display the number of descriptions
    # https://books.agiliq.com/projects/django-admin-cookbook/en/latest/filtering_calculated_fields.html


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('manufacturer_id', 'manufacturer_name', 'generics_count', 'brand_names_count')
    list_filter = ('created', AlphabetFilter,)
    search_fields = ('manufacturer_name',)
    prepopulated_fields = {'slug': ('manufacturer_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)
    actions = [export_to_csv]
    inlines = [MedicineItemInline]


@admin.register(DosageForm)
class DosageFormAdmin(admin.ModelAdmin):
    list_display = ('dosage_form_id', 'dosage_form_name', 'brand_names_count')
    list_filter = ('created', AlphabetFilter,)
    search_fields = ('dosage_form_name',)
    prepopulated_fields = {'slug': ('dosage_form_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)
    actions = [export_to_csv]


@admin.register(Indication)
class IndicationAdmin(admin.ModelAdmin):
    list_display = ('indication_id', 'indication_name', 'generics_count')
    list_filter = ('created', AlphabetFilter,)
    search_fields = ('indication_name',)
    prepopulated_fields = {'slug': ('indication_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)
    actions = [export_to_csv]
    inlines = [GenericItemInline]


@admin.register(DrugClass)
class DrugClassAdmin(admin.ModelAdmin):
    list_display = ('drug_class_id', 'drug_class_name', 'generics_count')
    list_filter = ('created', AlphabetFilter,)
    search_fields = ('drug_class_name',)
    prepopulated_fields = {'slug': ('drug_class_name',)}
    date_hierarchy = 'created'
    ordering = ('created',)
    actions = [export_to_csv]
