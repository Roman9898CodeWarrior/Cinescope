import requests
'''
def test_api():
    response = requests.get('https://restful-booker.herokuapp.com/booking')

    # Смотрим, что нам пришло
    print(f"Статус ответа: {response.status_code}")
    print(f"Тело ответа: {response.text}")


def test_post_request():
    import requests

    # делаем словарь для отправки
    data = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-04",
            "checkout": "2025-01-15"
        },
        "additionalneeds": "Breakfast"
    }

    url = 'https://restful-booker.herokuapp.com/booking'

    # отправляем наш запрос
    response_on_post = requests.post(
        f'{url}', json=data)

    response_on_post.raise_for_status()

    booking_id = response_on_post.json()['id']

    response_on_get = requests.get(
        f'{url}', params=booking_id)

    response_on_post.raise_for_status()

    assert response_on_get.json()['firstname'] == 'Jim'


def test_post_practice():
    url = 'https://restful-booker.herokuapp.com/booking'
    payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-04",
            "checkout": "2025-01-15"
        },
        "additionalneeds": "Breakfast"
    }

    response = requests.post(f'{url}', json=payload)

    print(response.text)
    print(response.request.body)

'''
'''
def outer_function(a):
    b = inner_function(a + 1)
    c = b * 3
    return c

def inner_function(x):
    return x * 2

result = outer_function(5)
print(result)
'''


'''
def outer_function():
    c = 2 + 3
    return c

def inner_function(x):
    return x * 2

result = outer_function()
print(result)
inner_function(2)


def process_data(data):
    processed_data = transform_data(data)
    result = calculate_result(processed_data)
    return result

def transform_data(data):
    return [x * 2 for x in data]

def calculate_result(data):
    return sum(data)

data = [1, 2, 3]
final_result = process_data(data)
print(final_result)



def inner(a, b):
    c = a + b
    d = c * 2 # Поставьте тут точку останова
    return d

def outer(x):
    y = 10
    z = inner(x, y)
    return z

result = outer(5)
print(result)
'''

def a(x): print("a"); return x + 1
def b(x): print("b"); return x * 2
def c(x): print("c"); return x ** 2

result = a(b(c(2))) # Поставьте тут точку останова
print(result)


