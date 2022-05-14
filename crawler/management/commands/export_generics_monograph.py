import os
from pathlib import Path

import requests

from django.core.management.base import BaseCommand
from django.utils.autoreload import logger

from crawler.models import Generic, Medicine


class Command(BaseCommand):
    help = "Export Generic Monograph to PDFs. This command will download the drug monograph PDFs from the URLs listed " \
           "on generic data. "

    def handle(self, *args, **options):
        logger.info("Export Generic Monograph to PDFs")
        try:
            monograph_links = (
                Generic.objects.values_list("monograph_link", flat=True).exclude(monograph_link__isnull=True)
                    .exclude(monograph_link__exact=''))
            logger.info("Total monograph links: {}".format(len(monograph_links)))
            for monograph_link in monograph_links:
                if monograph_link:
                    logger.info(monograph_link)

                    # option 1: use wget with the link directly
                    # monograph_link = monograph_link.replace(" ", "%20")
                    # os.system("wget -O /tmp/generic_monograph.pdf " + monograph_link)
                    # os.system("pdfjam --outfile /tmp/generic_monograph.pdf /tmp/generic_monograph.pdf")
                    # os.system(
                    #     "mv /tmp/generic_monograph.pdf /tmp/generic_monograph_" + str(monograph_link).split("/")[-1])

                    # option 2: use requests with the link directly
                    response = requests.get(monograph_link)
                    dirname = 'monograph-data/'
                    os.makedirs(os.path.dirname(dirname), exist_ok=True)
                    with open(Path(dirname + str(monograph_link).split("/")[-1] + '.pdf'), 'wb') as f:
                        f.write(response.content)

        except Exception as ge:
            logger.warning(ge)
