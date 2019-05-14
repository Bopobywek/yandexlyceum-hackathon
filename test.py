import requests

# print(requests.post(url='http://127.0.0.1:8080/api/auth', params={'login': '123', 'password': '123'}).json())
# print(requests.post(url='http://127.0.0.1:8080/api/auth', params={'login': '123', 'password': '123'}).status_code)
#
#
# print(requests.post(url='http://127.0.0.1:8080/api/auth', params={'login': '1234', 'password': '12341234'}).status_code)
# print(requests.post(url='http://127.0.0.1:8080/api/auth', params={'login': '1234', 'password': '12341234'}).json())

#
# print(requests.post(url='http://127.0.0.1:8080/api/auth', params={'login': '1234', 'password': '1234123s4'}).status_code)
# print(requests.post(url='http://127.0.0.1:8080/api/auth', params={'login': '1234', 'password': '12341s234'}).json())
#
#
# print(requests.post(url='http://127.0.0.1:8080/api/auth', params={'password': '123'}).json())
# print(requests.post(url='http://127.0.0.1:8080/api/auth', params={'password': '123'}).status_co

# print(requests.get(url='http://127.0.0.1:8080/api/task', params={'token':
#     requests.post(url='http://127.0.0.1:8080/api/auth',
#                   params={'login': '1234',
#                           'password': '12341234'}).json().get(
#         'token')}).json())

# print(requests.get(url='http://127.0.0.1:8080/api/task/23213123123321312', params={'token': '123'}).json())
#
# print(requests.get(url='http://127.0.0.1:8080/api/task/23123231', params={}).json())
#
# print('----------------------------------------------')

# print(requests.post(url='http://127.0.0.1:8080/api/task',
#                     params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
#                                                    params={'login': '1234',
#                                                            'password': '12341234'}).json().get('token'),
#                             'title': '332', 'content': '668',
#                             'deadline': 'Два дня',
#                             'priority': 'Второстепенный'}).json())


# print(requests.post(url='http://127.0.0.1:8080/api/task', params={'token': '123'}).json())
#
# print(requests.post(url='http://127.0.0.1:8080/api/task', params={}).json())
print('GET TEST')
print(requests.get(url='http://127.0.0.1:8080/api/task/1',
                   params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
                                                  params={'login': '1234',
                                                          'password': '12341234'}).json().get('token')}).json())

print(requests.get(url='http://127.0.0.1:8080/api/task/2',
                   params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
                                                  params={'login': '1234',
                                                          'password': '12341234'}).json().get('token')}).json())

print(requests.get(url='http://127.0.0.1:8080/api/task/3',
                   params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
                                                  params={'login': '1234',
                                                          'password': '12341234'}).json().get('token')}).json())

print(requests.get(url='http://127.0.0.1:8080/api/task/1',
                   params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
                                                  params={'login': '1234'}).json().get('token')}).json())
print(requests.get(url='http://127.0.0.1:8080/api/task/1',
                   params={}).json())
print('DELETE TEST')
print(requests.delete(url='http://127.0.0.1:8080/api/task/1',
                      params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
                                                     params={'login': '1234',
                                                             'password': '12341234'}).json().get('token')}).json())

print(requests.delete(url='http://127.0.0.1:8080/api/task/2',
                      params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
                                                     params={'login': '1234',
                                                             'password': '12341234'}).json().get('token')}).json())

print(requests.delete(url='http://127.0.0.1:8080/api/task/3',
                      params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
                                                     params={'login': '1234',
                                                             'password': '12341234'}).json().get('token')}).json())

print(requests.delete(url='http://127.0.0.1:8080/api/task/1',
                      params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
                                                     params={'login': '1234'}).json().get('token')}).json())
print(requests.delete(url='http://127.0.0.1:8080/api/task/1',
                      params={}).json())

print('PUT TEST')
print(requests.put(url='http://127.0.0.1:8080/api/task/4',
                    params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
                                                   params={'login': '1234',
                                                           'password': '12341234'}).json().get('token'),
                            'title': 'dsasad', 'content': '66dasdsa8',
                            'deadline': 'Три дня',
                            'priority': 'Второстепенный'}).json())
print(requests.put(url='http://127.0.0.1:8080/api/task/432213213213',
                    params={'token': requests.post(url='http://127.0.0.1:8080/api/auth',
                                                   params={'login': '1234',
                                                           'password': '12341234'}).json().get('token'),
                            'title': 'dsasad', 'content': '66dasdsa8',
                            'deadline': 'Три дня',
                            'priority': 'Второстепенный'}).json())
