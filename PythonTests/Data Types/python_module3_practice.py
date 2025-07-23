'''
def restore_health(current_health, potion):
    restored_health = current_health + potion
    return restored_health if restored_health <= 100 else 100

print(restore_health(90, 15))  # Вывод: 100
print(restore_health(50, 30))  # Вывод: 80
'''
'''
class GoblinTrader:
    def __init__(self, gold):
        self._gold = gold

    def buy_item(self, item_name, item_price):
        if self._gold >= item_price:
            self._gold -= item_price
            print(f'Предмет "{item_name}" успешно приобретен.')
        else:
            print('Недостаточно золота!')

trader = GoblinTrader(200)
trader.buy_item("Свиток скорости", 150)  # Вывод: Куплен Свиток скорости
trader.buy_item("Книга заклинаний", 100)  # Вывод: Недостаточно золота!
'''
'''
class GoblinMerchant:
    def __init__(self, gold):
        self._gold = gold

    def tax_rate(self):
        return 0.1

    @classmethod
    def from_rich_merchant(cls):
        return cls(1000)

    def buy_item(self, item_name, item_price):
        price_with_tax_rate = item_price + item_price * self.tax_rate()
        if self._gold >= price_with_tax_rate:
            self._gold -= price_with_tax_rate
            print(f'Предмет "{item_name}" успешно приобретен.')
        else:
            print('Недостаточно золота!')

merchant = GoblinMerchant(200)
merchant.buy_item("Амулет удачи", 150)  # Ожидается успешная покупка или недостаток золота
rich_merchant = GoblinMerchant.from_rich_merchant()
rich_merchant.buy_item("Волшебный посох", 500)  # Ожидается успешная покупка
'''
'''
class GoblinBank:
    def __init__(self, initial_gold):
         if initial_gold >= 0:
             self.__gold = initial_gold
         else:
            raise ValueError('Начальное колличество золота не может быть отрицательным.')

    def get_gold(self):
        return self.__gold

    def deposit_gold(self, amount):
        self.__gold += amount if amount > 0 else print('Вносимый депозит должен быть больше 0.')

    def withdraw_gold(self, amount):
        self.__gold -= amount if self.__gold >= amount else print('На счете недостаточно средств.')

    
    def withdraw_gold(self, amount):
        if amount > self.__gold:
            print("Недостаточно золота!")
        elif amount > 0:
            self.__gold -= amount
            print(f"Снято {amount} золота. Текущий баланс: {self.__gold}")
        else:
            print("Сумма должна быть больше 0!")



bank = GoblinBank(100)

print(bank.get_gold())  # Вывод: 100
bank.deposit_gold(50)   # Вывод: Добавлено 50 золота. Текущий баланс: 150
print(bank.get_gold())
bank.withdraw_gold(30)  # Вывод: Снято 30 золота. Текущий баланс: 120
print(bank.get_gold())
bank.withdraw_gold(200) # Вывод: Недостаточно золота!
 '''

'''
class Hero:
    def __init__(self, name, health):
        self.__name = name
        self.__health = health

    def take_damage(self, damage):
        if damage > 0:
            self.__health -= damage
            print(f'Здоровью было нанесено {damage} урона. Теперь здоровье = {self.__health}')
        else:
            raise ValueError('Урон д.б. больше 0.')


class Warrior(Hero):
    def attack(self):
        print("Нанёс 20 урона мечом")


class Mage(Hero):
    def attack(self):
        print("Нанёс 15 урона заклинанием")

warrior = Warrior("Тралл", 120)
mage = Mage("Джайна", 80)



warrior.attack()  # Вывод: Нанёс 20 урона мечом
mage.attack()     # Вывод: Нанёс 15 урона заклинанием
 '''
'''
class Peon:
    def work(self):
        print('Собирает золото.')

class Knight:
    def work(self):
        print('Сражается.')

def daily_work(hero):
    hero.work()

peon = Peon()
knight = Knight()

daily_work(peon)   # Вывод: Собирает золото
daily_work(knight) # Вывод: Сражается с врагами
 '''
'''
from abc import ABC, abstractmethod

class Artifact(ABC):
    @abstractmethod
    def activate(self):
        pass

class HealingArtifact(Artifact):
    def act(self):
        return "Восстановлено 50 здоровья"

class DamageArtifact(Artifact):
    def activate(self):
        return "Нанесено 30 урона врагу"

# Пример использования
heal_artifact = HealingArtifact()
damage_artifact = DamageArtifact()

print(heal_artifact.activate())  # Вывод: Восстановлено 50 здоровья
print(damage_artifact.activate()) # Вывод: Нанесено 30 урона врагу
 '''

class Hero:
    def __init__(self, name: str, health: int, still_alive: bool=True):
        self.name = name
        self.health = health
        self.still_alive = still_alive

    @property
    def health(self):
        return self.health

    @health.setter
    def health(self, new_health: int):
        self.health = new_health
        if self.health <= 0:
            self.still_alive = False

    def take_damage(self, damage: int):
        if damage > 0:
            self.health -= damage
        else:
            raise ValueError('Урон д.б. больше 0.')

class Warrior(Hero):
    def __init__(self, name: str, health: int, stance: str, still_alive: bool=True):
        super.__init__(name, health, still_alive)
        if stance == 'Атакующая' or stance == 'Защитная':
            self.stance = stance
        else:
            raise ValueError('Такой стойки у воина не может быть.')

    def change_stance(self, new_stance: str):
        if new_stance == 'Атакующая' or new_stance == 'Защитная':
            self.stance = new_stance
        else:
            raise ValueError('Такой стойки у воина не может быть.')

    def take_damage(self, damage: int):
        if damage <= 0:
            raise ValueError('Урон д.б. больше 0.')
        elif self.stance == 'Защитная':
            self.health = self.health - damage * 0.8
        else:
            self.health = self.health - damage

    def attack(self, Hero):
        if self.stance =='Атакующая':
            Hero.take_damage(20 * 1.15)
        else:
            Hero.take_damage(20)

class Mage(Hero):
    def __init__(self, name, health, magic_shield: float, still_alive: bool=True):
        super.__init__(name, health, still_alive)
        if 0.00 <= magic_shield <= 1.00:
            self.magic_shield = magic_shield
        else:
            raise ValueError('Значение атрибута magic_shield д.б. от 0 до 1)')

    def attack(self, Hero):
        Hero.take_damage(15)

    def take_damage(self, damage: int):
        if damage > 0:
            self.health = self.health - (damage * 1 - self.magic_shield)
        else:
            raise ValueError('Урон д.б. больше 0.')



def_hero = Hero('Конон', 100)
print(def_hero.health)

