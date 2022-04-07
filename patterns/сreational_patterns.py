from abc import ABC, abstractmethod
from copy import deepcopy
from quopri import decodestring

""""
Создание пользователей сайта
"""

# абстрактный пользователь
class User:
    pass

# администратор
class Admin(User):
    pass

# клиент
class Client(User):
    pass

class UserFactory:
    types = {
        'admin': Admin,
        'client': Client
    }

# порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


""""
Создание прототипов услуг
"""

# Семейство классов для Hotel
class HotelBooking:  # бронирование отеля
    @staticmethod
    def book():
        print('Hotel book work')


# порождающий паттерн Прототип
class HotelPrototype:
    # прототип гостиницы
    def clone(self):
        return deepcopy(self)


class Hotel(HotelPrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.hotels.append(self)

class HotelСancellater:  # аннуляция отеля
    pass

class HotelСhanger:  # изменение брони
    pass


# Семейство классов для Flight
class FlightBooking:  # бронирование абиабилета
    @staticmethod
    def book():
        print('Flight book work')

class FlightPrototype:
    # прототип авиаперелета
    def clone(self):
        return deepcopy(self)

class Flight(FlightPrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.flights.append(self)

class FlightСancellater:  # аннуляция абиабилета
    pass

class FlightСhanger:  # изменение брони
    pass


# Семейство классов для Carrental
class CarrentalBooking:  # бронирование каршеринга
    @staticmethod
    def book():
        print('Carrental book work')

class CarrentalPrototype:
    # прототип каршеринга
    def clone(self):
        return deepcopy(self)

class Carrental(CarrentalPrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.carrentals.append(self)

class CarrentalСancellater:  # аннуляция каршеринга
    pass

class CarrentalСhanger:  # изменение брони
    pass


class AbstractFactory(ABC):
    @staticmethod
    def create(type_, name, category):
        SERVICES = {
            'Hotel': HotelFactory,
            'Flight': FlightFactory,
            'Carrental': CarrentalFactory
        }
        return SERVICES[type_](name, category)

    @abstractmethod
    def create_booking(self):
        pass

    @abstractmethod
    def create_hotel(self):
        pass

    @abstractmethod
    def create_flight(self):
        pass

    @abstractmethod
    def create_carrental(self):
        pass

    @abstractmethod
    def create_cancellater(self):
        pass

    @abstractmethod
    def create_changer(self):
        pass


class HotelFactory(AbstractFactory):
    def create_booking(self):
        return HotelBooking()

    def create_hotel(self):
        return

    def create_cancellater(self):
        return HotelСancellater()

    def create_changer(self):
        return HotelСhanger()


class FlightFactory(AbstractFactory):
    def create_booking(self):
        return FlightBooking()

    def create_flight(self):
        return

    def create_cancellater(self):
        return FlightСancellater()

    def create_changer(self):
        return FlightСhanger()


class CarrentalFactory(AbstractFactory):
    def create_booking(self):
        return CarrentalBooking()

    def create_carrental(self):
        return

    def create_cancellater(self):
        return CarrentalСancellater()

    def create_changer(self):
        return CarrentalСhanger()


""""
Создание категорий
"""


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.services = []

    def service_count(self):
        result = len(self.services)
        if self.category:
            result += self.category.service_count()
        return result


""""
Основной интерфейс проекта
"""

class Engine:
    def __init__(self):
        self.admins = []
        self.users = []
        self.services = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_service(type_, name, category):
        return AbstractFactory.create(type_, name, category)

    def get_service(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
