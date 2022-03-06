import logging
import subprocess


def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    logging.info(proc_stdout)


subprocess_cmd('python manage.py manufacturer_crawl --logfile manufacturer_crawl.txt')
subprocess_cmd('python manage.py generic_crawl --logfile generic_crawl.txt')
subprocess_cmd('python manage.py med_crawl --logfile med_crawl.txt')
subprocess_cmd('python manage.py med_generic_mapper')
subprocess_cmd('python manage.py drug_class_crawl --logfile drug_class_crawl.txt')
subprocess_cmd('python manage.py dosage_form_crawl --logfile dosage_form_crawl.txt')
subprocess_cmd('python manage.py indication_crawl --logfile indication_crawl.txt')
