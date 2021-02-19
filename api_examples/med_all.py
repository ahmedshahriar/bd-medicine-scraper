import requests

base_url = 'http://127.0.0.1:8000/api/'
# retrieve all medicines
r = requests.get(f'{base_url}medicines/')
courses = r.json()
available_medicines = ', '.join([medicine['brand_name'] for medicine in courses])
print(f'Available medicines : {available_medicines}')
