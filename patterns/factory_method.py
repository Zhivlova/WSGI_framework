from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def available(self):
        pass

    @staticmethod
    def create_service(service_type):
        SERVICES = {
            'hotel': Hotel,
            'flight': Flight,
            'carrental': Carrental
        }
        return SERVICES[service_type]()


class Hotel(Service):

    def available(self):
        print('Hotel service is available')


class Flight(Service):

    def available(self):
        print('Flight service is available')


class Carrental(Service):

    def available(self):
        print('Carrental service is available')


service_type = input("Введите тип услуги")
service = Service.create_service(service_type)
service.available()
