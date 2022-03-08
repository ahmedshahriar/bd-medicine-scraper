# bd-medicine-scraper
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) ![Django CI](https://github.com/ahmedshahriar/bd-medicine-scraper/actions/workflows/django-ci.yml/badge.svg) [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/ahmedshahriarsakib/bangladesh-medicine-analytics) [![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://github.dev/ahmedshahriar/bd-medicine-scraper)

## Overview
Welcome to the bd-medicine-scraper repository!

In this project, I scraped Medicine data (from [medex.com.bd](https://medex.com.bd)) using **scrapy** and integrated it with **Django REST Framework**. The data is stored in a **PostgreSQL** database. I designed the scraper in a way to keep the relations between models.

I also customized the django admin panels, added additional features such as - 
- auto complete lookup relational fields
- custom filtering (alphabetical, model property)
- bulk actions (export to csv)

I customized the scrapy command to run scrapy spiders from django command line. (ex- `python manage.py spider_name`)\
Integrated custom django command to export models to csv. (ex- `python manage.py export_model_name export_data_path`)\
I also added proxy configuration to scrapy.



## Run   

Create a python virtual environment and run these commands from root directory-
```
pip insrall -r requirements.txt
```

This will run the django app-
```
python manage.py runserver
```

NB: Migrate before running the app
```
python manage.py makemigrations && python manage.py migrate
```

To run all spiders-

```
python run_crawler.py
```

To run a specific spider-
```
python manage.py <spider_name>
```
ex - `python manage.py med`


## Data Analytics

### Dataset
The scraped dataset is available in kaggle - 
- [Assorted Medicine Dataset of Bangladesh](https://www.kaggle.com/ahmedshahriarsakib/assorted-medicine-dataset-of-bangladesh)

The dataset has 6 CSV files -
Here is a list of the CSV files  with their featured columns:

1. medicine.csv (21k+ entries)
   - brand name
   - medicine type (allopathic or herbal)
   - generic
   - strength
   - manufacturer
   - package container (unit price and pack info)
   - Package Size (unit price)
2. manufacturer.csv (245 entries)
   - name
3. indication.csv (2043 entries)
   - name
4. generic.csv (1809 entries)
   - name
   - monographic link (PDF URL)
   - drug class
   - indication
   - generic details such as "Indication description", "Pharmacology description", "Dosage & Administration description" etc.
5. drug class.csv (452 entries)
   - name
6. dosage form.csv (123 entries)
   - name

### Analytics
[Bangladesh Medicine Analytics - Notebook on Kaggle](https://www.kaggle.com/ahmedshahriarsakib/bangladesh-medicine-analytics)

## Tests
Workflow script - [django-ci.yml](https://github.com/ahmedshahriar/bd-medicine-scraper/blob/dev/.github/workflows/django-ci.yml)

Run the tests using:\
`coverage run --omit='*/venv/*' manage.py test`
or
`python manage.py test`

Check the coverage\
`coverage html`

## Built With

```
Django==3.2.12
djangorestframework==3.12.2
django-admin-autocomplete-filter==0.7.1
django-filter==21.1
coverage==6.2
Scrapy==2.4.1
scrapy-djangoitem==1.1.1
psycopg2==2.9.3
```



## Preview

![django_admin_generics](https://user-images.githubusercontent.com/40615350/157111319-f84830b8-f9e3-4a3f-9f72-b0afc586ccb9.png)

![django_admin_medicine](https://user-images.githubusercontent.com/40615350/157111248-31ca4ee0-97e1-412e-92b1-31a451bb846c.png)

![django_admin_dosage_form](https://user-images.githubusercontent.com/40615350/157111180-98bb2b6a-bb15-4159-ba4b-48f92dd97538.png)

![django_admin_manufacturer](https://user-images.githubusercontent.com/40615350/157111404-3e3ff9e3-f9f4-4bd6-b176-c08fa32ecee1.png)