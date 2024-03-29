from datetime import date
from framework.templator import render
from patterns.сreational_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer
from patterns.architectural_system_pattern import UnitOfWork

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

routes = {}


# контроллер - главная страница
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


# контроллер "О проекте"
@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


# контроллер - Отели
@AppRoute(routes=routes, url='/hotels/')
class Hotels:
    @Debug(name='Hotels')
    def __call__(self, request):
        return '200 OK', render('hotels.html', date=date.today())


# контроллер - Авиаперелеты
@AppRoute(routes=routes, url='/flights/')
class Flights:
    @Debug(name='Flights')
    def __call__(self, request):
        return '200 OK', render('flights.html', date=date.today())


# контроллер - Каршеринг
@AppRoute(routes=routes, url='/carrentals/')
class Carrental:
    @Debug(name='Carrentals')
    def __call__(self, request):
        return '200 OK', render('carrentals.html', date=date.today())


# контроллер 404
class PageNotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список отелей
@AppRoute(routes=routes, url='/hotels-list/')
class HotelsList:
    def __call__(self, request):
        logger.log('Список отелей')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('hotels-list.html',
                                    objects_list=category.hotels,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No hotels have been added yet'


# контроллер - список авиаперелетов
@AppRoute(routes=routes, url='/flights-list/')
class FlightsList:
    def __call__(self, request):
        logger.log('Список авиаперелетов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('flights-list.html',
                                    objects_list=category.flights,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No flights have been added yet'


# контроллер - список автомобилей
@AppRoute(routes=routes, url='/carrental-list/')
class CarrentalsList:
    def __call__(self, request):
        logger.log('Список автомобилей')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('carrental-list.html',
                                    objects_list=category.carrentals,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No carrentals have been added yet'


# контроллер - создать отель
@AppRoute(routes=routes, url='/create-hotel/')
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

                hotel.observers.append(email_notifier)
                hotel.observers.append(sms_notifier)

                site.hotels.append(hotel)

            return '200 OK', render('hotels-list.html',
                                    objects_list=category.hotels,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-hotel.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать авиаперелет
@AppRoute(routes=routes, url='/create-flight/')
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

                flight.observers.append(email_notifier)
                flight.observers.append(sms_notifier)

                site.flights.append(flight)

            return '200 OK', render('flights-list.html',
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
@AppRoute(routes=routes, url='/create-carrental/')
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

                carrental.observers.append(email_notifier)
                carrental.observers.append(sms_notifier)

                site.carrentals.append(carrental)

            return '200 OK', render('carrental-list.html',
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
@AppRoute(routes=routes, url='/create-category/')
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
            return '200 OK', render('create-category.html',
                                    categories=categories)


# контроллер - список категорий отелей
@AppRoute(routes=routes, url='/category_list_hotel/')
class CategoryListHotel:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list_hotel.html',
                                objects_list=site.categories)


# контроллер - список категорий авиабилетов
@AppRoute(routes=routes, url='/category_list_flight/')
class CategoryListFlight:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list_flight',
                                objects_list=site.categories)


# контроллер - список категорий каршеринга
@AppRoute(routes=routes, url='/category_list_ carrental/')
class CategoryListCarrental:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list_ carrental',
                                objects_list=site.categories)


# контроллер - копировать отель
@AppRoute(routes=routes, url='/copy-hotel/')
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

            return '200 OK', render('hotels-list.html',
                                    objects_list=site.hotels,
                                    name=new_hotel.category.name)
        except KeyError:
            return '200 OK', 'No hotels have been added yet'


# контроллер - копировать авиаперелет
@AppRoute(routes=routes, url='/copy-flight/')
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

            return '200 OK', render('flights-list.html',
                                    objects_list=site.flights,
                                    name=new_flight.category.name)
        except KeyError:
            return '200 OK', 'No flights have been added yet'


# контроллер - копировать автомобиль
@AppRoute(routes=routes, url='/copy-carrental/')
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

            return '200 OK', render('carrental-list.html',
                                    objects_list=site.carrentals,
                                    name=new_carrental.category.name)
        except KeyError:
            return '200 OK', 'No carrentals have been added yet'


@AppRoute(routes=routes, url='/client-list/')
class ClientListView(ListView):
    template_name = 'client-list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('client')
        return mapper.all()


@AppRoute(routes=routes, url='/create-client/')
class ClientCreateView(CreateView):
    template_name = 'create_client.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('client', name)
        site.clients.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()

@AppRoute(routes=routes, url='/add-client/')
class AddClientByServiceCreateView(CreateView):
    template_name = 'add_client.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['services'] = site.services
        context['clients'] = site.clients
        return context

    def create_obj(self, data: dict):
        service_name = data['service_name']
        service_name = site.decode_value(service_name)
        service = site.get_service(service_name)
        client_name = data['client_name']
        client_name = site.decode_value(client_name)
        client = site.get_client(client_name)
        service.add_client(client)


@AppRoute(routes=routes, url='/api/')
class ServiceApi:
    @Debug(name='ServiceApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.services).save()
