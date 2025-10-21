import requests

url = 'https://httpbin.org/ip'
response = requests.get(url)
response.raise_for_status()
data = response.json()
print(f'Status code: {response.status_code}')
print(f'IP: {data.get('origin', '')}')
