import csv
import datetime

from crawler.models import Medicine, Generic, DosageForm, DrugClass, Indication, Manufacturer
from django.core.management import BaseCommand
from django.utils.autoreload import logger


class Command(BaseCommand):  # see https://gist.github.com/2724472

    help = "Mapping the generics with medicines"

    def add_arguments(self, parser):
        parser.add_argument('model_name',
                            type=str,
                            help='model name for the csv export, e.g. medicine, generic, dosage_form, drug_class, '
                                 'indication, manufacturer')

        parser.add_argument('outfile',
                            nargs='?',
                            type=str,
                            help='Save path, like </path/to/outfile.csv> or "/data/medicine.csv"')

    def handle(self, *args, **options):
        model_name = options['model_name']
        export_file = f"{options['outfile']}.csv" if options['outfile'] else '{}.csv'.format(model_name)
        logger.info("Exporting... %s" % model_name)

        model_dict = {'medicine': Medicine, 'generic': Generic, 'dosage_form': DosageForm, 'drug_class': DrugClass,
                      'indication': Indication, 'manufacturer': Manufacturer}

        model_class = model_dict[model_name]

        with open('%s' % export_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            fields = [field for field in model_class._meta.get_fields() if not field.many_to_many \
                      and not field.one_to_many]

            # Write a first row with header information
            writer.writerow([field.verbose_name for field in fields])

            # Write data rows
            for obj in model_class.objects.all():
                data_row = []
                for field in fields:
                    value = getattr(obj, field.name)
                    if isinstance(value, datetime.datetime):
                        value = value.strftime('%d/%m/%Y')
                    data_row.append(value)
                writer.writerow(data_row)
            logger.info(f.name, "exported")
