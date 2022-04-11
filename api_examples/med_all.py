import requests
import pprint

base_url = 'http://127.0.0.1:8000/api/'

try:
    # retrieve all medicines
    r = requests.get(f'{base_url}medicines/', headers={'Authorization': 'Token 28dd424d1d421342d23b6ecbee3beddacb6b6238'}) # replace with your token
    print(r.status_code)
    courses = r.json()
    print(pprint.pprint(courses))
    available_medicines = ', '.join([medicine['brand_name'] for medicine in courses['results']])
    print(f'Available medicines : {available_medicines}')
except Exception as e:
    print(f'Error: {e}')
