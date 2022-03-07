# bd-medicine-scraper
Welcome to the bd-medicine-scraper repository!

In this repository, I scraped Medicine data ([medex.com.bd](https://medex.com.bd)) using **scrapy** and integrated it with **Django REST Framework**. The data is stored in a **PostgreSQL** database. I designed the scraper in a way to keep the relations between models.
I also customized the django admin panels, added additional features such as - 
- auto complete lookup relational fields
- custom filtering (alphabetical, model property)
- bulk actions (export to csv)

## Tests
Run the tests using:\
`coverage run --omit='*/venv/*' manage.py test`
or
`python manage.py test`

Check the coverage\
`coverage html`

Built With
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