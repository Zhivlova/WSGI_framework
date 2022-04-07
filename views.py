from datetime import date
from framework.templator import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


# контроллер - главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


# контроллер "О проекте"
class About:
    def __call__(self, request):
        return '200 OK', render('about 2.html')


# контроллер - Отели
class Hotels:
    def __call__(self, request):
        return '200 OK', render('hotels 2.html', date=date.today())


# контроллер - Авиаперелеты
class Flights:
    def __call__(self, request):
        return '200 OK', render('flights 2.html', date=date.today())


# контроллер - Каршеринг
class Carrental:
    def __call__(self, request):
        return '200 OK', render('carrental 2.html', date=date.today())


# контроллер 404
class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список отелей
class HotelsList:
    def __call__(self, request):
        logger.log('Список отелей')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('hotel_list.html',
                                    objects_list=category.hotels,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No hotels have been added yet'


# контроллер - список авиаперелетов
class FlightsList:
    def __call__(self, request):
        logger.log('Список авиаперелетов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('flight_list.html',
                                    objects_list=category.flights,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No flights have been added yet'


# контроллер - список автомобилей
class CarrentalsList:
    def __call__(self, request):
        logger.log('Список автомобилей')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('carrental_list.html',
                                    objects_list=category.carrentals,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No carrentals have been added yet'


# контроллер - создать отель
class CreateHotel:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                hotel = site.create_hotel('record', name, category)
                site.hotels.append(hotel)

            return '200 OK', render('hotel_list.html',
                                    objects_list=category.hotels,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_hotel.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать авиаперелет
class CreateFlight:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                flight = site.create_flight('record', name, category)
                site.flights.append(flight)

            return '200 OK', render('flight_list.html',
                                    objects_list=category.flights,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_flight.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'



# контроллер - создать автомобиль
class CreateCarrental:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                carrental = site.create_carrental('record', name, category)
                site.carrentals.append(carrental)

            return '200 OK', render('carrental_list.html',
                                    objects_list=category.carrentals,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_carrental.html',
                                    name=category.name,
                                    id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list_hotel.html',
                                objects_list=site.categories)


# контроллер - копировать отель
class CopyHotel:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_hotel = site.get_hotel(name)
            if old_hotel:
                new_name = f'copy_{name}'
                new_hotel = old_hotel.clone()
                new_hotel.name = new_name
                site.hotels.append(new_hotel)

            return '200 OK', render('hotel_list.html',
                                    objects_list=site.hotels,
                                    name=new_hotel.category.name)
        except KeyError:
            return '200 OK', 'No hotels have been added yet'


# контроллер - копировать авиаперелет
class CopyFlight:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_flight = site.get_flight(name)
            if old_flight:
                new_name = f'copy_{name}'
                new_flight = old_flight.clone()
                new_flight.name = new_name
                site.flights.append(new_flight)

            return '200 OK', render('flight_list.html',
                                    objects_list=site.flights,
                                    name=new_flight.category.name)
        except KeyError:
            return '200 OK', 'No flights have been added yet'


# контроллер - копировать автомобиль
class CopyCarrental:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_carrental = site.get_carrental(name)
            if old_carrental:
                new_name = f'copy_{name}'
                new_carrental = old_carrental.clone()
                new_carrental.name = new_name
                site.carrentals.append(new_carrental)

            return '200 OK', render('carrental_list.html',
                                    objects_list=site.carrentals,
                                    name=new_carrental.category.name)
        except KeyError:
            return '200 OK', 'No carrentals have been added yet'
