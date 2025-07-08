'''
number = -12721314324133423

if number % 2 == 0:
    print(f'{number} - четное число')
else:
    print(f'{number} - нечетное число')
'''
'''
quantity = 17
price = 800

if quantity * price > 10000:
    order_sum = int(quantity * price / 100 * 80)
    print(f'Сумма вашего заказа - {order_sum}$.')
elif quantity * price > 5000:
    order_sum = int(quantity * price / 100 * 90)
    print(f'Сумма вашего заказа - {order_sum}$.')
else:
    order_sum = int(quantity * price)
    print(f'Сумма вашего заказа - {order_sum}$.')
'''
'''
password = ''
while password != 'qwerty123':
    password = input('Введите пароль: ')
    if password == '':
        print('Необходимо ввести пароль.')
    else:
        print('Введен неверный пароль.')

print("Доступ разрешён")
'''
'''
numbers = [1, 2, 3, 4, 5]

sum = 0
for number in numbers:
    sum += number

print(f'Сумма чисел в массиве numbers равна - {sum}.')
'''
'''
nums = [3, 4, 11, 4, 4]
nums[2] = 100
print(nums)
'''
'''
empty_list = []

rng = range(1, 101, 3)
empty_list = list(rng)
print(empty_list)
'''
'''
menu = {"cheescake": 250, "rizotto": 320, "steak": 420}
menu['karpacho'] = '1500'
print(menu)
menu['karpacho'] = '1100'
print(menu)
'''
'''
products = {"яблоко": 100, "банан": 50, "апельсин": 70}
order = 'ябл'

if order in products:
    print(products[order])
else:
    print('У нас нет такого товара.')
'''
'''
r = range(1, 6)
for num in r:
    print(pow(num, 2))
'''
'''
n = 5
sum = 0
r = range(1, n + 1)

for num in r:
    sum += num

print(sum)
'''
'''
r = range(10, 0, -1)
for num in r:
    print(num)
'''
'''
fruits = ["яблоко", "банан", "груша"]
for fr in fruits:
    print(fr)
'''
'''
numbers = [3, 8, 1, 9, 4]
max = 0

for number in numbers:
    if number > max:
        max = number

print(max)
'''
'''
products = {"яблоко": 100, "банан": 50, "апельсин": 70}
sum = 0
for product, price in products.items():
   sum += price

print(sum)
'''
'''
countdown = 1
while countdown <= 10:
    print(countdown)
    countdown += 1
'''
'''
n = 5
sum = 0
while n > 0:
    sum += n
    n -= 1

print(sum)
'''
'''
nums = [2, 7, 4, 9, 6, 5]

el_index = 0
while el_index < len(nums):
    if nums[el_index] % 2 == 0:
        nums.pop(el_index)
    el_index += 1

print(nums)
'''
'''
a = [1, 2, 3]
b = list(a)
b[0] = 100
print(a)
print(b)
'''
'''
time = 10983
hours, minutes, seconds = time // 3600, (time % 3600) // 60, time % 60
print(f'Результат работы - {hours} час, {minutes} минута, {seconds} секунда.')
'''
'''
number = int(input('Введите число. '))
print(f'{number} входит в диапазон от 10 до 20' ) if 10 <= number <=20 else print(f'{number} не входит в диапазон от 10 до 20' )
'''
'''
first_num = int(input('Введите число. '))
second_num = int(input('Введите число. '))
operator = input('Введите знак. ')

if operator == '+':
    print(first_num + second_num)
elif operator == '-':
    print(first_num - second_num)
elif operator == '*':
    print(first_num * second_num)
elif operator == '**':
    print(first_num ** second_num)
elif operator == '/':
    try:
        print(first_num / second_num)
    except ZeroDivisionError:
        print('Ошибка - деление на 0 невозможно.')
elif operator == '//':
    try:
        print(first_num // second_num)
    except ZeroDivisionError:
        print('Ошибка - деление на 0 невозможно.')
elif operator == '%':
    try:
        print(first_num % second_num)
    except ZeroDivisionError:
        print('Ошибка - деление на 0 невозможно.')
        
 '''




'''
text = "Python is awesome!"
print(text.upper())
print(text.replace('awesome', 'amazing'))
 '''
'''
text = "Hello, Python!"
print(text[0:5])
print(text[::2])
 '''
'''
pi = 3.14159
print(round(pi, 2))
 '''
'''
quote = "Python is easy and powerful!"
print(quote.replace("easy", "fun").replace("powerful", "versatile"))
 '''
'''
name = "Alice"
age = 25
print(f'{name} is {age} years old.')
 '''
'''
data = "Price: 1234.5678 USD"
number_from_string = float(data[7:16])
rounded_number = round(number_from_string, 2)
print(f'Rounded price: {rounded_number} USD')
 '''
'''
fruits = ["apple", "banana", "cherry", "date"]
fruits.append('kiwi')
fruits.remove('banana')
print(fruits)
'''
'''
person = {"name": "Alice", "age": 25, "city": "New York"}
person['age'] = 26
person['profession'] = 'engineer'
print(person)
'''
'''
numbers = (10, 20, 30, 40, 50)
print(numbers[1])
'''
'''
colors = {"red", "blue", "green"}
colors.add('yellow')
colors.discard('blue')
print(colors)
'''
'''
r = range(1, 21)
l = list(r)
sum = 0
new_l = []

for num in l:
    sum += num
    if num % 3 == 0:
        new_l.append(num)

print(l)
print(new_l)
print(sum)
'''

'''
num = 10
while num > 0:
    print(num)
    num -= 1
print("Счёт завершён!")
'''

items_for_sale = {'Зелье лечения': 100, 'Зелье маны': 80, 'Свиток скорости': 150, 'Артефакт магии': 300}
quantity_of_items_for_sale = {'Зелье лечения': 17, 'Зелье маны': 8, 'Свиток скорости': 4, 'Артефакт магии': 3}

def count_order_sum(item, quantity):
    if items_for_sale[item] * quantity > 500:
       order_sum = int(items_for_sale[item] * quantity / 100 * 80)
       print(f'С вас {order_sum} золотых.')
    else:
        order_sum = int(items_for_sale[item] * quantity)
        print(f'С вас {order_sum} золотых.')

required_item = input('Что нужно? ')
if required_item in items_for_sale and quantity_of_items_for_sale[required_item] >= 1:
    required_item_count = int(input('и сколько нужно? '))
    if quantity_of_items_for_sale[required_item] >= required_item_count:
        count_order_sum(required_item, required_item_count)
    else:
        yes_or_not = input('У меня столько нет. Возьмешь сколько есть?')
        if yes_or_not == 'yes':
            count_order_sum(required_item, quantity_of_items_for_sale[required_item])
        else:
            print('В таком случае всего хорошего.')
else:
    print('У меня такого нет, попробуй в другом месте!')

