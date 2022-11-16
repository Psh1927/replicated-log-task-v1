import requests

print(requests.post('http://127.0.0.1:8080', json='test_1').ok)
print(requests.post('http://127.0.0.1:8080', json='test_2').ok)
#requests.post('http://127.0.0.1:8081', data='test_2')
