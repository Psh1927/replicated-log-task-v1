import requests

print("Get list from Master\n", requests.get('http://127.0.0.1:8080').text)
print("Get list from Secondary-1:\n", requests.get('http://127.0.0.1:8081').text)
print("Get list from Secondary-2:\n", requests.get('http://127.0.0.1:8082').text)
print("Send test_1: ", requests.post('http://127.0.0.1:8080', data='test_1').ok)
print("Send test_2: ", requests.post('http://127.0.0.1:8080', data='test_2').ok)
print("Send test_3: ", requests.post('http://127.0.0.1:8080', data='test_3').ok)
print("Get list from Master\n", requests.get('http://127.0.0.1:8080').text)
print("Get list from Secondary-1:\n", requests.get('http://127.0.0.1:8081').text)
print("Get list from Secondary-2:\n", requests.get('http://127.0.0.1:8082').text)
print("Send test_4: ", requests.post('http://127.0.0.1:8080', data='test_4').ok)
print("Send test_5: ", requests.post('http://127.0.0.1:8080', data='test_5').ok)
print("Send test_6: ", requests.post('http://127.0.0.1:8080', data='test_6').ok)
print("Send test_7: ", requests.post('http://127.0.0.1:8080', data='test_7').ok)
print("Get list from Master:\n", requests.get('http://127.0.0.1:8080').text)
print("Get list from Secondary-1:\n", requests.get('http://127.0.0.1:8081').text)
print("Get list from Secondary-2:\n", requests.get('http://127.0.0.1:8082').text)


