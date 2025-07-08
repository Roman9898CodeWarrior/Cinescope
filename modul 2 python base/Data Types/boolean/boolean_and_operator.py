'''
a = [1, 2, 3]
b = [4, 5, 6]
c = a + b
assert len(c) == len(a) + len(b)


numbers = [10, 20, 40, 50]
numbers.insert(2, 30)
numbers.clear()
print(numbers)

list = [
    [1, 2, 3],
    ["a", "b", "c"]
]
list.append([True, False])
assert list[1][1] == 'b'
last_item = list[0].pop()
assert last_item == 3
print(list)
'''

'''
tuple_1 = ("apple", "banana", "cherry", "apple")
first_apple_index = tuple_1.index('apple')
print(first_apple_index)
print(tuple_1.count('apple'))
a, b, *rest = tuple_1
tuple_2 = tuple(rest)
print(tuple_2)
assert len(tuple_2) == 2, 'Длинна второго кортежа не равна 2'
'''

'''
password = ''
while password != '12345':
    password = input('Введите пароль: ')

print("Доступ разрешён")
'''

'''
countdown = 10
while countdown > 0:
    if countdown % 2 != 0:
        print('Обратный отсчет нечетных чисел:', countdown)

    countdown -= 1

print('Обратный отсчет завершен.')
'''


'''
some_list = [10, 0, 5, "abc", 2]

for el in some_list:
    try:
        print(100 / el)
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль невозможно.")
    except TypeError:
        print(f"Ошибка: Неверный тип данных: {el}")
'''
'''
def calculate_delivery_cost(weight, distance, fragile=False):
    if fragile == True:
        price_of_delevery = 10 * weight + 5 * distance / 100 * 150
        return price_of_delevery if price_of_delevery > 200 else 200
    else:
        price_of_delevery = 10 * weight + 5 * distance
        return price_of_delevery if price_of_delevery > 200 else 200
'''
'''
def analyze_numbers(numbers):
    numbers_data = {}

    if len(numbers) == 0:
        numbers_data['average'] = None
        numbers_data['min'] = None
        numbers_data['max'] = None
        numbers_data['even_count'] = None
        return numbers_data

    even_count = 0

    for number in numbers:
        if number % 2 == 0:
            even_count += 1


    numbers_data['average'] = sum(numbers) / len(numbers)
    numbers_data['min'] = min(numbers)
    numbers_data['max'] = max(numbers)
    numbers_data['even_count'] = even_count

    return numbers_data


print(analyze_numbers([1, 2, 3, 4, 5]))
'''
'''
def filter_list(data, threshold):
    new_list = []

    for num in data:
        if num >= threshold:
            new_list.append(num)

    return new_list

data = [1, 5, 10, 2, 8, 12]
threshold = 7

print(filter_list(data, threshold))
'''
'''
def outer_function(m):
    def inner_function():
        print(f'Внутренняя {m}')

    return inner_function()

outer_function('vavavwsfagafawg')
'''

'''
def safe_divide(a, b):
    try:
        res = a / b
    except ZeroDivisionError:
        print("Ошибка: деление на ноль!")
    except Exception as e:
        print("Произошла ошибка:", e)
    else:
        return res

print(safe_divide(5, 0))
'''

'''
def read_file_content(file_path):
    try:
        if len(file_path) == 0:
            print('Путь к файлу не указан.')
            return None
        file = open(file_path, "r")
        content = file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла '{file_path}': {e}")
        return None
    else:
        print(f"Содержимое файла '{file_path}':\n{content}")
        return content


read_file_content('')
'''

'''
def devide_list_of_numbers(list_of_numbers):
    res = []
    for num in list_of_numbers:
        try:
            res.append(100 / num)
        except ZeroDivisionError:
            print("Ошибка: деление на ноль!")
        except TypeError:
            print("Ошибка: некорректный тип данных в списке! В списке должны быть только целые числа или числа с дробной частью.")

    print(res)
    return res


devide_list_of_numbers([1, 0, 'fafawf', 23, 100])
'''
'''
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages



instance_of_book = Book('harry potter', 'Joan Rouling', 12000)

print(instance_of_book.title)
print(instance_of_book.author)
print(instance_of_book.pages)

instance_of_book.title = 'Lord of the rings'
print(instance_of_book.title)

instance_of_book.rating = 4.6
print(instance_of_book.rating)
'''
'''
class NumbersComparisonClass:
    def __init__(self, first_num, second_num):
        self.first_num = first_num
        self.second_num = second_num

    def define_bigger_num(self):
        bigger_num = 0

        if self.first_num > self.second_num:
            bigger_num = self.first_num
        elif self.second_num > self.first_num:
            bigger_num = self.second_num
        else:
            print('Both numbers are equals.')
            return None

        even_of_not = 'even' if bigger_num % 2 == 0 else 'not even'

        if bigger_num > 0:
            positive_or_negative = 'positive'
        elif bigger_num < 0:
            positive_or_negative = 'negative'
        else:
            positive_or_negative = 'neutral'

        print(f'Bigger number is {bigger_num}. That number is {even_of_not} and {positive_or_negative}.')


some_numbers_comparison = NumbersComparisonClass(0, 0)

some_numbers_comparison.define_bigger_num()
'''
'''
def __init__(self, name, balance):
    try:
        balance_is_positive = balance >= 0
        balance_is_positive == True
    except ValueError:
        print('Начальный баланс не может быть отрицательным.')
    else:
        self.name = name
        self.balance = balance
        
        
def withdraw(self, amount):
    try:
        self.balance -= amount >= 100
    except ValueError:
        print('На балансе должен остаться минимальный остаток в 100.')
    else:
        self.balance -= amount
'''
'''
class Account:
    def __init__(self, name, balance):
      if balance < 0:
          raise ValueError('Начальный баланс не может быть отрицательным.')

      self.name = name
      self.balance = balance


    def deposit(self, amount):
        self.balance += amount


    def withdraw(self, amount):
        if self.balance - amount < 0:
            raise ValueError('Баланс не может быть отрицательным.')

        self.balance -= amount

class SavingsAccount(Account):
    def __init__(self, name, balance, interest_rate):
        super().__init__(name, balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        if self.balance - amount < 100:
            raise ValueError('На балансе должен быть минимальный остаток в 100.')

        self.balance -= amount


first_account = Account('first', -3)

savings_account = SavingsAccount('second', 500, 15)
print(savings_account.name)
print(savings_account.balance)

savings_account.withdraw(401)
print(savings_account.balance)
'''
'''
class Animal:
    species = set()

    def __init__(self, name, species):
        self.name = name
        Animal.add_species(species)

    @classmethod
    def add_species(cls, species):
        Animal.species.add(species)

    @classmethod
    def show_species(cls):
        print(Animal.species)

horse = Animal('Tom', 'horse')
dog = Animal('Max', 'dog')
dog_1 = Animal('Rex', 'dog')

Animal.show_species()
'''
'''
class CurrencyConverter:

    @staticmethod
    def usd_to_eur(amount):
        return amount * 0.85

    @staticmethod
    def eur_to_usd(amount):
        return amount * 1.18

print(CurrencyConverter.eur_to_usd(100))
'''
'''
class Book:
    def __init__(self, title, author, pages):
        self._title = title
        self._author = author
        self._pages = pages

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def pages(self):
        return self._pages

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @author.setter
    def author(self, new_author):
        self._author = new_author

    @pages.setter
    def pages(self, new_pages_number):
        if new_pages_number >= 0:
            self._pages = new_pages_number
        else:
            print('Количество страниц в книге не может быть меньше 0')

book = Book("Мастер и Маргарита", "Михаил Булгаков", 384)
print(book.title)  # Вывод: Мастер и Маргарита
book.pages = -10  # Вывод: Количество страниц не может быть отрицательным.
print(book.pages) #вывод 384
book.pages = 400
print(book.pages) #вывод 400
'''

class BankAccount:
    def __init__(self, account_number, balance):
        self._account_number = account_number
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, sum):
        if sum > 0:
            self._balance += sum
        else:
            print('Операция снятия средств не поддерживается. Используйте метод withdraw().')

    def withdraw(self, sum):
        if 0 < sum <= self._balance:
            self._balance -= sum
        else:
            print('Сумма снятия д.б. больше 0, но не должна превышать остаток на счету.')

some_account = BankAccount('1234568', 1000)

print(some_account.balance)
some_account.withdraw(1001)
print(some_account.balance)

'''
class Safe:
    def __init__(self, code, balance):
        self.__code = code  # Приватный код
        self.__balance = balance  # Приватный баланс

    def check_balance(self, code):
        if code == self.__code:
            return f"Баланс в сейфе: {self.__balance} золотых"
        else:
            return "Неверный код. Доступ запрещён."

# Создаём сейф
safe = Safe("1234", 1000)

# Попробуем проверить баланс
print(safe.check_balance("1234"))  # Баланс в сейфе: 1000 золотых
print(safe.check_balance("0000"))  # Неверный код. Доступ запрещён.
'''
'''
global_variable = 20

def modify_global():
    return  global_variable + 5

print(modify_global())  # Вывод: 30
'''


